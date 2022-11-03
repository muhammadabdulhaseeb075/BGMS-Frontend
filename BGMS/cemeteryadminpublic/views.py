from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.timezone import make_naive, is_naive
from enum import Enum

from rest_framework.views import APIView

from tenant_schemas.utils import schema_context

import json
import pytz

from bgsite.views import group_required
from cemeteryadmin.models import CalendarEvents, FuneralEvent
from cemeteryadmin.utils import python_time_to_display_string, python_date_to_display_string
from config.security.drf_permissions import BereavementStaffPermission
from main.models import BurialGroundSite
from bgsite.models import GravePlot, GraveRef, MemorialGraveplot

class FuneralEventsView(APIView):

    class SortHeaders(Enum):
        """
        Enum containing table columns that are sortable
        """
        START = 'start'
        SITE_NAME = 'site_name'
        FIRST_NAMES = 'first_names'
        LAST_NAME = 'last_name'
        FUNERAL_DIRECTOR = 'funeral_director'
        STATUS = 'status'

    def getOrderCriteria(self, query_params):
        """
        Returns order criteria for request (order_by and order_desc)
        """

        order_by = query_params.get('order_by', self.SortHeaders.START.value)

        if order_by == 'start_date':
            order_by = self.SortHeaders.START.value

        elif order_by == 'site_id':
            order_by = self.SortHeaders.SITE_NAME.value

        elif order_by == 'funeral_director_id':
            order_by = self.SortHeaders.FUNERAL_DIRECTOR.value

        # Make sure order is valid. This is the only way I can think of to avoid injection attack vulnerability.
        if order_by not in self.SortHeaders._value2member_map_:
            order_by = self.SortHeaders.START.value

        order_desc = query_params.get('order_desc', False)

        return order_by, order_desc

    def get(self, request):
        """
        Get paginated, sorted and filtered list of funeral bookings
        """

        site_ids = json.loads(self.request.query_params.get('site_ids', "[]"))
        no_sites_selected = not len(site_ids)
        if not request.user.is_superuser:
            # check user has permission to access these sites
            burialgroundsite_ids = list(request.user.site_groups.filter(Q(group__name='SiteAdmin') | Q(group__name='SiteWarden') | Q(group__name='SiteUser') | Q(group__name='BereavementStaff')).values_list('burialgroundsite_id', flat=True).distinct())
            if not set(site_ids).issubset(burialgroundsite_ids):
                # they're trying to access a site they don't have permission for
                return JsonResponse({'detail': "Permission denied"}, safe=False, status=401)

            if no_sites_selected:
                site_ids = burialgroundsite_ids
        elif no_sites_selected:
            site_ids = list(BurialGroundSite.objects.exclude(schema_name='public').values_list('id', flat=True).distinct())

        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))

        filters = request.query_params.get('filters', None)

        if filters:
            # filters string needs parsed to json
            filters = json.loads(filters)

        order_by, order_desc = self.getOrderCriteria(request.query_params)

        sites = BurialGroundSite.objects.filter(id__in=site_ids).exclude(schema_name='public')
        events = []

        if not sites:
            return JsonResponse({'total_rows': 0, 'events': events}, safe=False)

        sql = ''
        params = []

        for site in sites:

            site.name = site.name.replace("'", "''")

            if not sql:
                # wrap selects in a common table expression (see below for further explaination)
                sql = 'WITH Data_CTE AS ('
            else:
                # selects for different sites are unioned
                sql += ' UNION ALL '

            sql += (
                "SELECT {} AS site_id, ".format(str(site.id)) +
                "'{}' AS site_name, ".format(str(site.name)) +
                "ce.event_type_id,"
                "ce.id, "
                "ce.reference_number, "
                "ce.start, "
                "ce.created_by_id, "
                "ce.created_date, "
                "p.first_names, "
                "p.last_name, "
                "fe.funeral_director_id, "
                "fd.first_names as funeral_director_name, "
                "fd.last_name as funeral_director_last_names, "
                "fd.title as funeral_director_title, "
                "fd.company_name as funeral_director_company_name, "
                "fe.status,"
                "bu.cremated,"
                "bu.burial_number,"
                "bu.new_burial_grave"
            )

            # need additional fields if sorting by funeral director
            if order_by == self.SortHeaders.FUNERAL_DIRECTOR.value:
                sql += (
                    ", " +
                    "fd_p.last_name AS funeral_director"
                )

            sql += (
                " " +
                "FROM {}.cemeteryadmin_funeralevent AS fe ".format(site.schema_name) +
                "INNER JOIN {}.cemeteryadmin_calendarevents AS ce ON fe.calendar_event_id = ce.id ".format(site.schema_name) +
                "INNER JOIN {}.bgsite_person AS p ON fe.person_id = p.id ".format(site.schema_name) +
                "INNER JOIN {}.bgsite_death AS d ON p.id = d.person_id ".format(site.schema_name) +
                "INNER JOIN {}.bgsite_burial AS bu ON bu.death_id = d.person_id ".format(site.schema_name) +
                "LEFT JOIN {}.bgsite_official AS fd ON fd.id = fe.funeral_director_id ".format(site.schema_name)
            )

            # need additional fields if sorting by funeral director
            if order_by == self.SortHeaders.FUNERAL_DIRECTOR.value:
                sql += (
                    "LEFT JOIN public.main_publicperson AS fd_p ON fd.person_id = fd_p.id "
                )

            if filters:
                # if first filter to be processed
                first = True

                for key, value in filters.items():
                    if value is None or value is '' or len(value) == 0:
                        continue

                    if first:
                        sql += "WHERE "
                        first = False
                    else:
                        sql += " AND "

                    if key == 'name':
                        name_filter_formatted = '%%' + value.upper() + '%%'
                        sql += "(UPPER(first_names) LIKE %s OR UPPER(last_name) LIKE %s)"
                        params.extend([name_filter_formatted, name_filter_formatted])
                    else:
                        if key == 'year':
                            sql += "EXTRACT(YEAR FROM start) = %s"
                        elif key == 'month':
                            sql += "EXTRACT(MONTH FROM start) = %s"
                        elif key == 'day':
                            sql += "EXTRACT(DAY FROM start) = %s"
                        elif key == 'date':
                            sql += "(ce.start >= %s AND ce.start <= %s::date + interval '23 hours')"
                        elif key == 'created_year':
                            sql += "EXTRACT(YEAR FROM created_date) = %s"
                        elif key == 'created_month':
                            sql += "EXTRACT(MONTH FROM created_date) = %s"
                        elif key == 'created_day':
                            sql += "EXTRACT(DAY FROM created_date) = %s"
                        elif key == 'status':
                            # status is an array
                            i = 1
                            sql += " " + key + " IN ( "
                            status_values = value.split(", ")

                            for status in status_values:
                                sql += "%s"
                                if i != len(status_values) and len(status_values) != 1:
                                    sql += " , "
                                i += 1
                            sql += " )"
                        else:
                            sql += key + " = %s"

                        if type(value) is dict or key == 'status':
                            # this is an array
                            if key == 'status':
                                param_value = value.split(", ")
                            else:
                                param_value = value
                            for objectKey in param_value:
                                if key == 'status':
                                    params.append(objectKey)
                                else:
                                    params.append(param_value[objectKey])

                        else:
                            params.append(value)

        sql += "), "

        # create a second CTE which counts the total rows from the first CTE
        sql += "Count_CTE AS (SELECT COUNT(*) AS total_rows FROM Data_CTE) "

        # join data from first CTE and count from second
        sql += "SELECT * FROM Data_CTE CROSS JOIN Count_CTE"

        # offset and limit are what make pagination possible!
        order_by += " " + ("DESC" if order_desc else "ASC")
        sql += " ORDER BY {} OFFSET %s LIMIT %s".format(order_by)
        params.extend([int(offset), int(limit)])

        # Assuming here that sites will be in the same timezone. This might need changed in the future.
        timezone = pytz.timezone(sites.first().site_details.site_preferences.site_timezone)

        events_raw_queryset = CalendarEvents.objects.raw(sql, params)
        # import pdb; pdb.set_trace()
        total_rows = 0

        # serialize the data
        for e in events_raw_queryset:

            obj = {'site_id': e.site_id, 'id': e.id, 'reference': e.reference_number, 'first_names': e.first_names, 'last_name': e.last_name,
                   'event_type_id': e.event_type_id,
                   'funeral_director_id': e.funeral_director_id, 'status': e.status, 'cremated': e.cremated,
                   'funeral_director_name': e.funeral_director_name,
                   'funeral_director_last_names': e.funeral_director_last_names,
                   'funeral_director_title': e.funeral_director_title,
                   'funeral_director_company_name': e.funeral_director_company_name}

            burial_number = e.burial_number
            new_burial_grave = e.new_burial_grave

            obj['map_management'] = {
                'has_grave': False
            }

            if burial_number and burial_number != '':
                    obj['map_management'] = {
                        'has_grave': True,
                        'burial_number': burial_number,
                        'new_burial_grave': new_burial_grave
                    }
            if is_naive(e.start):
                start = e.start
            else:
                start = make_naive(e.start, timezone)

            # This formating removes leading zero from hour and makes am/pm lowercase
            obj['start_date'] = python_date_to_display_string(start)
            obj['start_time'] = python_time_to_display_string(start.time())
            obj['created_date'] = python_date_to_display_string(e.created_date)

            events.append(obj)

            if not total_rows:
                # Every row will contain this field. We only need to retrieve it once.
                total_rows = e.total_rows

        for event in events:

            site_id = event.get('site_id')
            if site_id:
                schema = BurialGroundSite.objects.filter(id=site_id).exclude(schema_name='public').first()
                if schema:
                    with schema_context(schema.schema_name):
                        if 'map_management' in event:
                            map_management = event['map_management']
                            if 'new_burial_grave' in map_management:
                                new_burial_grave = map_management['new_burial_grave']

                                if new_burial_grave:
                                    burial_number = map_management['burial_number']
                                    burial_number_splited = burial_number.split(' ')
                                    if len(burial_number_splited) is 3:
                                        graveref = GraveRef.objects.filter(grave_number=burial_number_splited[2]).first()
                                    else:
                                        graveref = GraveRef.objects.filter(grave_number=burial_number).first()

                                    if graveref:
                                        grave_plot = GravePlot.objects.filter(graveref=graveref).first()
                                        if grave_plot:
                                            event['map_management'] = {
                                                'grave_plot_uuid': grave_plot.uuid,
                                                'topopolygon_id': grave_plot.topopolygon_id,
                                                'has_grave': True
                                            }

                                if new_burial_grave is False:
                                    burial_number = map_management['burial_number']
                                    graveref = GraveRef.objects.filter(grave_number=burial_number).first()
                                    memorial = None

                                    if graveref:
                                        grave_plot = GravePlot.objects.filter(graveref=graveref).first()
                                        if grave_plot:
                                            memorial_graveplot = MemorialGraveplot.objects.filter(graveplot=grave_plot).first()
                                            event['map_management'] = {
                                                'grave_plot_uuid': grave_plot.uuid,
                                                'has_grave': True
                                            }
                                            if memorial_graveplot:
                                                memorial = memorial_graveplot.memorial

                                    if memorial:
                                        event['map_management'] = {
                                            'memorial_uuid': memorial.uuid,
                                            'layer_type': memorial.marker_type,
                                            'has_grave': True,
                                        }

        return JsonResponse({'total_rows': total_rows, 'events': events}, safe=False) #Return GET request

    def post(self, request):
        """
        Get paginated, sorted and filtered list of funeral bookings
        """
        site_request = self.request.data.get('site_ids', "[]")
        site_ids = site_request
        #site_ids = json.load(self.request.data.get('site_ids'))
        no_sites_selected = not len(site_ids)
        if not request.user.is_superuser:
            # check user has permission to access these sites
            burialgroundsite_ids = list(request.user.site_groups.filter(Q(group__name='SiteAdmin') | Q(group__name='SiteWarden') | Q(group__name='SiteUser') | Q(group__name='BereavementStaff')).values_list('burialgroundsite_id', flat=True).distinct())
            if not set(site_ids).issubset(burialgroundsite_ids):
                # they're trying to access a site they don't have permission for
                return JsonResponse({'detail': "Permission denied"}, safe=False, status=401)

            if no_sites_selected:
                site_ids = burialgroundsite_ids
        elif no_sites_selected:
            site_ids = list(BurialGroundSite.objects.exclude(schema_name='public').values_list('id', flat=True).distinct())

        limit = int(request.data.get('limit', 10))
        offset = int(request.data.get('offset', 0))

        filters = request.data.get('filters', None)

        if filters:
            # filters string needs parsed to json
            filters = json.loads(filters)

        order_by, order_desc = self.getOrderCriteria(request.data)

        sites = BurialGroundSite.objects.filter(id__in=site_ids).exclude(schema_name='public')
        events = []

        if not sites:
            return JsonResponse({'total_rows': 0, 'events': events}, safe=False)

        sql = ''
        params = []

        for site in sites:

            site.name = site.name.replace("'", "''")

            if not sql:
                # wrap selects in a common table expression (see below for further explaination)
                sql = 'WITH Data_CTE AS ('
            else:
                # selects for different sites are unioned
                sql += ' UNION ALL '

            sql += (
                "SELECT {} AS site_id, ".format(str(site.id)) +
                "'{}' AS site_name, ".format(str(site.name)) +
                "ce.event_type_id,"
                "ce.id, "
                "ce.reference_number, "
                "ce.start, "
                "ce.created_by_id, "
                "ce.created_date, "
                "p.first_names, "
                "p.last_name, "
                "fe.funeral_director_id, "
                "fd.first_names as funeral_director_name, "
                "fd.last_name as funeral_director_last_names, "
                "fd.title as funeral_director_title, "
                "fd.company_name as funeral_director_company_name, "
                "fe.status,"
                "bu.cremated,"
                "bu.burial_number,"
                "bu.new_burial_grave"
            )

            # need additional fields if sorting by funeral director
            if order_by == self.SortHeaders.FUNERAL_DIRECTOR.value:
                sql += (
                    ", " +
                    "fd_p.last_name AS funeral_director"
                )

            sql += (
                " " +
                "FROM {}.cemeteryadmin_funeralevent AS fe ".format(site.schema_name) +
                "INNER JOIN {}.cemeteryadmin_calendarevents AS ce ON fe.calendar_event_id = ce.id ".format(site.schema_name) +
                "INNER JOIN {}.bgsite_person AS p ON fe.person_id = p.id ".format(site.schema_name) +
                "INNER JOIN {}.bgsite_death AS d ON p.id = d.person_id ".format(site.schema_name) +
                "INNER JOIN {}.bgsite_burial AS bu ON bu.death_id = d.person_id ".format(site.schema_name) +
                "LEFT JOIN {}.bgsite_official AS fd ON fd.id = fe.funeral_director_id ".format(site.schema_name)
            )

            # need additional fields if sorting by funeral director
            if order_by == self.SortHeaders.FUNERAL_DIRECTOR.value:
                sql += (
                    "LEFT JOIN public.main_publicperson AS fd_p ON fd.person_id = fd_p.id "
                )

            if filters:
                # if first filter to be processed
                first = True

                for key, value in filters.items():
                    if value is None or value is '' or len(value) == 0:
                        continue

                    if first:
                        sql_pre = "WHERE "
                        first = False
                    else:
                        sql_pre = " AND "

                    if key == 'name':
                        name_filter_formatted = '%%' + value.upper() + '%%'
                        sql += sql_pre + "(UPPER(p.first_names) LIKE %s OR UPPER(p.last_name) LIKE %s)"
                        params.extend([name_filter_formatted, name_filter_formatted])
                    elif key == 'date':
                        if ('from' in value.keys() and value['from']) and ((not ('to' in value.keys())) or not value['to']):
                            sql += sql_pre + "(ce.start >= '" + value['from'] + "')"
                        elif ('to' in value.keys() and value['to']) and ((not ('from' in value.keys())) or not value['from']):
                            sql += sql_pre + "(ce.end <= '" + value['to'] + "')"
                        elif ('to' in value.keys() and value['to']) and ('from' in value.keys() and value['from']):
                            sql += sql_pre + "(ce.start >= '" + value['from'] + "' AND ce.end <= '" + value['to'] + "')"
                        # {'from': '2022-05-28', 'to': ''}
                        # sql += "(ce.start >= %s AND ce.start <= %s::date + interval '23 hours')"
                    elif key == 'funeral_director_id':
                        id_list = value.split(',')  # Creates a list of one or more id values. Works for single director & multiple.
                        sql += sql_pre + " " + 'funeral_director_id' + " IN ( "
                        sql_comma = "" # for first value no comma, add comma in front of subsequent values
                        for i in id_list:
                            sql += sql_comma + "'" + i.strip() + "'"
                            sql_comma = " , "
                        sql += " )"
                    elif key == 'cremated':
                        # if ashes & burial are both specified do nothing so all records will be returned
                        if ('ashes' in value) and ('burial' not in value):
                            # only looking for ashes so get records where cremated is true
                            sql += sql_pre + " bu.cremated"
                        elif ('ashes' not in value) and ('burial' in value):
                            # only looking for burial so get records where cremated is false
                            sql += sql_pre + " NOT bu.cremated"

                    else:
                        if key == 'last_name':
                            sql += sql_pre + "p.last_name = %s"
                        elif key == 'year':
                            sql += sql_pre + "EXTRACT(YEAR FROM start) = %s"
                        elif key == 'month':
                            sql += sql_pre + "EXTRACT(MONTH FROM start) = %s"
                        elif key == 'day':
                            sql += sql_pre + "EXTRACT(DAY FROM start) = %s"
                        elif key == 'created_year':
                            sql += sql_pre + "EXTRACT(YEAR FROM created_date) = %s"
                        elif key == 'created_month':
                            sql += sql_pre + "EXTRACT(MONTH FROM created_date) = %s"
                        elif key == 'created_day':
                            sql += sql_pre + "EXTRACT(DAY FROM created_date) = %s"
                        elif key == 'status':
                            # status is an array
                            i = 1
                            sql += sql_pre + " " + key + " IN ( "
                            status_values = value.split(", ")

                            for status in status_values:
                                sql += "%s"
                                if i != len(status_values) and len(status_values) != 1:
                                    sql += " , "
                                i += 1
                            sql += " )"
                        else:
                            sql += sql_pre + key + " = %s"

                        if type(value) is dict or key == 'status':
                            # this is an array
                            if key == 'status':
                                param_value = value.split(", ")
                            else:
                                param_value = value
                            for objectKey in param_value:
                                if key == 'status':
                                    params.append(objectKey)
                                else:
                                    params.append(param_value[objectKey])

                        else:
                            params.append(value)

        sql += "), "

        # create a second CTE which counts the total rows from the first CTE
        sql += "Count_CTE AS (SELECT COUNT(*) AS total_rows FROM Data_CTE) "

        # join data from first CTE and count from second
        sql += "SELECT * FROM Data_CTE CROSS JOIN Count_CTE"

        # offset and limit are what make pagination possible!
        order_by += " " + ("DESC" if order_desc else "ASC")
        sql += " ORDER BY {} OFFSET %s LIMIT %s".format(order_by)
        params.extend([int(offset), int(limit)])

        # Assuming here that sites will be in the same timezone. This might need changed in the future.
        timezone = pytz.timezone(sites.first().site_details.site_preferences.site_timezone)

        events_raw_queryset = CalendarEvents.objects.raw(sql, params)
        # import pdb; pdb.set_trace()
        total_rows = 0

        # serialize the data
        for e in events_raw_queryset:
            obj = {'site_id': e.site_id, 'id': e.id, 'reference': e.reference_number, 'first_names': e.first_names, 'last_name': e.last_name,
                   'event_type_id': e.event_type_id,
                   'funeral_director_id': e.funeral_director_id, 'status': e.status, 'cremated': e.cremated,
                   'funeral_director_name': e.funeral_director_name,
                   'funeral_director_last_names': e.funeral_director_last_names,
                   'funeral_director_title': e.funeral_director_title,
                   'funeral_director_company_name': e.funeral_director_company_name}

            burial_number = e.burial_number
            new_burial_grave = e.new_burial_grave

            obj['map_management'] = {
                'has_grave': False
            }

            if burial_number and burial_number != '':
                    obj['map_management'] = {
                        'has_grave': True,
                        'burial_number': burial_number,
                        'new_burial_grave': new_burial_grave
                    }
            if is_naive(e.start):
                start = e.start
            else:
                start = make_naive(e.start, timezone)

            # This formating removes leading zero from hour and makes am/pm lowercase
            obj['start_date'] = python_date_to_display_string(start)
            obj['start_time'] = python_time_to_display_string(start.time())
            obj['created_date'] = python_date_to_display_string(e.created_date)

            events.append(obj)

            if not total_rows:
                # Every row will contain this field. We only need to retrieve it once.
                total_rows = e.total_rows

        for event in events:

            site_id = event.get('site_id')
            if site_id:
                schema = BurialGroundSite.objects.filter(id=site_id).exclude(schema_name='public').first()
                if schema:
                    with schema_context(schema.schema_name):
                        if 'map_management' in event:
                            map_management = event['map_management']
                            if 'new_burial_grave' in map_management:
                                new_burial_grave = map_management['new_burial_grave']

                                if new_burial_grave:
                                    burial_number = map_management['burial_number']
                                    burial_number_splited = burial_number.split(' ')
                                    if len(burial_number_splited) is 3:
                                        graveref = GraveRef.objects.filter(grave_number=burial_number_splited[2]).first()
                                    else:
                                        graveref = GraveRef.objects.filter(grave_number=burial_number).first()

                                    if graveref:
                                        grave_plot = GravePlot.objects.filter(graveref=graveref).first()
                                        if grave_plot:
                                            event['map_management'] = {
                                                'grave_plot_uuid': grave_plot.uuid,
                                                'topopolygon_id': grave_plot.topopolygon_id,
                                                'has_grave': True
                                            }

                                if new_burial_grave is False:
                                    burial_number = map_management['burial_number']
                                    graveref = GraveRef.objects.filter(grave_number=burial_number).first()
                                    memorial = None

                                    if graveref:
                                        grave_plot = GravePlot.objects.filter(graveref=graveref).first()
                                        if grave_plot:
                                            memorial_graveplot = MemorialGraveplot.objects.filter(graveplot=grave_plot).first()
                                            event['map_management'] = {
                                                'grave_plot_uuid': grave_plot.uuid,
                                                'has_grave': True
                                            }
                                            if memorial_graveplot:
                                                memorial = memorial_graveplot.memorial

                                    if memorial:
                                        event['map_management'] = {
                                            'memorial_uuid': memorial.uuid,
                                            'layer_type': memorial.marker_type,
                                            'has_grave': True,
                                        }

        return JsonResponse({'total_rows': total_rows, 'events': events}, safe=False) #Return POST request
