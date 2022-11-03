from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.serializers import serialize
from django.db import connection
from django.db.models import Count
from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.generic import FormView, TemplateView
from django.utils.decorators import method_decorator

from BGMS.utils import email_ag_admin
from bgsite.models import Official, Person, Memorial, Death, Burial, GravePlot, GraveRef, Official, Image, ReservedPlot, \
    MemorialGraveplot, MemorialInscriptionDetail, Inspection, Section, Subsection
from bgsite.common_apis.serializers import MemorialInscriptionSerializer, BurialDetailsSerializer
from bgsite.views import AjaxableResponseMixin, WardenView,\
    ViewOnlyView, group_required, MemorialPhotographyView, PublicAccessOrViewOnlyView
from config.security.drf_permissions import IsAuthenticatedOrPublicAccessReadOnly
from filemanager.models import File
from geometries.models import TopoPolygons, Layer, LayerCache
from geometries.views import getALLSiteLayerNamesMinimal, getLayer, CRS
from geometriespublic.models import FeatureGroup
from main.models import BurialGroundSite, Currency, PublicPerson, Company as PublicCompany
from mapmanagement.serializers import InspectionSerializer, MemorialGraveplotSerializer,  \
    SectionSerializer, SubsectionSerializer, GraveNumberSerializer, FeatureIDSerializer, \
    MemorialHeadpointGeoSerializer, GraveplotHeadpointGeoSerializer, GraveplotGeoSerializer, \
    MemorialGeoSerializer, MemorialGraveNumbersSerializer, ReservePlotState,PlotNumberSerializer

import json
json.encoder.FLOAT_REPR = lambda o: format(o, '.2f')
from datetime import date
import datetime
import bleach
import itertools
import uuid
import traceback

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from proxy.views import proxy_view
from rest_framework.response import Response
from rest_framework import status



# Create your views here.

""" search_type argument can be 'burial', 'reservation' or 'owner'. Default is 'burial' """
class MapSearchView(APIView):

    permission_classes = [IsAuthenticatedOrPublicAccessReadOnly]

    def burial_has_impossible_month(self, persons):
        for person in persons:
            burial_id = person['first_burial_id']
            if burial_id:
                try:
                    burial = Burial.objects.prefetch_related("burial_officials").get(id=burial_id)
                    if burial:
                        burial_month = burial.serializable_value('impossible_date_month')
                        if burial_month:
                            person['has_impossible_month'] = True
                        else:
                            person['has_impossible_month'] = False
                
                except Burial.DoesNotExist:
                    person['has_impossible_month'] = False
            else:
                person['has_impossible_month'] = False
        return persons

    def get(self, request):

        search_type = 'burial'
        call_purpouse = request.GET.get('purpouse')

        if 'search_type' in request.GET:
            search_type = request.GET.get('search_type')
        
        if search_type != 'burial' and not (request.user and request.user.is_authenticated):
            # only burial searches are allowed for public access
            if call_purpouse and call_purpouse != 'download_shapefile':
                return HttpResponseForbidden()
        
        if search_type == 'grave':

            result = list(GravePlot.objects.search_graveplots(request.GET.get('graveplot_grave_number'), request.GET.get('section_id'), request.GET.get('subsection_id'), request.GET.get('graveplot_layer'), int(request.GET.get('fuzzy_value')), call_purpouse))

        else:
            person_fields = 'id', 'first_names', 'last_name'
            kwargs = { 'fuzzy_value':int(request.GET.get('fuzzy_value')), 'search_type':search_type }
            
            if search_type == 'owner':
                kwargs = dict(list(kwargs.items()) + list({ 'email':request.GET.get('email') }.items()))

                persons = []
                try:
                    persons = PublicPerson.objects.search_persons(first_names=request.GET.get('first_names'), last_name=request.GET.get('last_name'), **kwargs)
                except:
                    pass
                try:
                    persons += PublicCompany.objects.search_companies(name=request.GET.get('company_name'), **kwargs)
                except:
                    pass

                person_fields += 'name', 'type', 'addresses__first_line', 'addresses__town', 'addresses__postcode'

            else: # burial or reservation
                kwargs = dict(list(kwargs.items()) + list({ 'first_names':request.GET.get('first_names'), 'last_name':request.GET.get('last_name'), 'graveplot_grave_number':request.GET.get('graveplot_grave_number'), 'section_id':request.GET.get('section_id'), 'subsection_id':request.GET.get('subsection_id') }.items()))

                if search_type=='reservation':
                    persons = Person.objects.search_persons(**kwargs)

                    person_fields += 'topopolygon_id',
                
                else: # burial type
                    memorial_types = request.GET.get('memorial_types')
                    mem_type = memorial_types if memorial_types != "" else None

                    kwargs = dict(list(kwargs.items()) + list({ 'age':request.GET.get('age'), 'age_to':request.GET.get('age_to'), 'burial_date':request.GET.get('burial_date'), 'burial_date_to':request.GET.get('burial_date_to'), 
                    'memorial_type':mem_type }.items()))

                    persons = Person.objects.search_persons(**kwargs)

                    person_fields += 'age_years', 'age_months', 'age_weeks', 'age_days', 'age_hours', 'age_minutes', 'first_burial_id', 'burial_date'
                    
            persons_grouped = []

            # Each person should only have one record. Multiple memorials and/or graves are put into arrays within person record.
            for person in persons:
                if len(persons_grouped)==0 or person['id']!=persons_grouped[-1]['id']:
                    #person_object = { field: person[field] for field in person_fields }
                    person_object = {}

                    for field in person_fields:
                        if field in person:
                            person_object[field] = person[field]

                    person_object['memorials'] = []
                    person_object['graveplots'] = []
                    persons_grouped.append(person_object)

                #add memorial info
                if 'memorial_uuid' in person and person['memorial_uuid']:
                    # check if memorial is already included
                    add_memorial = True
                    for memorial in persons_grouped[-1]['memorials']:
                        if person['memorial_uuid']==memorial['memorial_uuid']:
                            add_memorial = False
                            break
                    
                    if add_memorial:
                        persons_grouped[-1]['memorials'].append({ 'memorial_uuid': person['memorial_uuid'], 'memorial_layer': person['memorial_layer'] })
                
                #add grave info
                if 'graveplot_uuid' in person and person['graveplot_uuid']:
                    # check if graveplot is already included
                    add_graveplot = True
                    for graveplot in persons_grouped[-1]['graveplots']:
                        if person['graveplot_uuid']==graveplot['graveplot_uuid']:
                            add_graveplot = False
                            break
                    
                    if add_graveplot:
                        graveplot_layer = person['graveplot_layer'] if 'graveplot_layer' in person else 'plot'
                        new_graveplot = { 'graveplot_uuid': person['graveplot_uuid'], 'graveplot_layer': graveplot_layer }

                        if 'topopolygon_id' in person:
                            new_graveplot['topopolygon_id'] = person['topopolygon_id']

                        persons_grouped[-1]['graveplots'].append(new_graveplot)

            result = persons_grouped
            # add a flagg if has impossible month just if is for burials
            if search_type == 'burial':
                result = self.burial_has_impossible_month(result)

        return JsonResponse(result, safe=False)


class IncludeGravesInSearchView(ViewOnlyView):
    def get(self, request):
        """
        Returns true if we should include graves in the seach function.
        """
        
        return JsonResponse({'include': GravePlot.objects.graveplots_with_ref_exist()}, safe=False)


class MapManagementView(PublicAccessOrViewOnlyView, TemplateView):
    template_name = 'mapmanagement/index.html'


class RenderedMapManagementIndexView(PublicAccessOrViewOnlyView):
    def get(self, request):
        """
        Return rendered template-for-vue.html
        """
        template = loader.get_template("mapmanagement/template-for-vue.html")

        return HttpResponse(template.render({'user': request.user}))


def getClusterLayer(**kwargs):

    layer_obj = kwargs.get('layer_obj', Layer.objects.get(feature_code__feature_type='cluster'))
    create_if_not_exists = kwargs.get('create_if_not_exists', False)

    if create_if_not_exists or LayerCache.objects.filter(layer=layer_obj).exists():
        query_set = Memorial.objects.filter(topopolygon__geometry__isnull=False).prefetch_related('topopolygon')
            
        if query_set.exists():
            serializer = MemorialHeadpointGeoSerializer(query_set, many=True)
        else:
            query_set = GravePlot.objects.filter(topopolygon__geometry__isnull=False, topopolygon__layer__feature_code__feature_type='plot').prefetch_related('topopolygon')
            serializer = GraveplotHeadpointGeoSerializer(query_set, many=True)

        geoj = serializer.data
        geoj.update(CRS)

        layer_obj.update_layer_geojson_cache(geoj, False)

        return geoj
    
    else:
        return None


def getMemorials(layer):
    if layer.startswith('memorials_'):
        layer = layer[len('memorials_'):]
    geoj = None
    
    layer_obj = Layer.objects.get(feature_code__feature_type=layer)
    layer_cache = layer_obj.get_layer_geojson_cache(False)

    if layer_cache:
        return layer_cache
    else:
        if layer == 'cluster':
            geoj = getClusterLayer(layer_obj=layer_obj, create_if_not_exists=True)
        else:
            query_set = Memorial.objects.filter(topopolygon__layer=layer_obj).prefetch_related('topopolygon').annotate(images_count=Count('images',distinct=True)).annotate(linked_graves_count=Count('graveplot_memorials',distinct=True))
            serializer = MemorialGeoSerializer(query_set, many=True, context={ 'marker_type': layer })

            geoj = serializer.data
            geoj.update(CRS)

            layer_obj.update_layer_geojson_cache(geoj, False)

        return geoj


class AllFeaturesView(ViewOnlyView):
    ''' Get all features that are needed for the site '''
    def get(self, request):
        siteGroupsAndLayers = getALLSiteLayerNamesMinimal()
        returnGroups = []

        for group in siteGroupsAndLayers:
            returnGroup = []
            for layer in group.get("layers"):
                _layer_type = ""
                if group.get("group_code") == "memorials":
                    returnGroup.append({ 'layer': getMemorials(layer.get("layer_code")), 'layer_type': "memorials_" + layer.get("layer_code") })
                elif layer.get("layer_code") == "plot":
                    returnGroup.append({ 'layer': getGraveplot(), 'layer_type': "memorials_graveplot" })
                elif layer.get("layer_code") == "reserved_plot":
                    returnGroup.append({ 'layer': getGraveplot('reserved_plot'), 'layer_type': "memorials_reserved_graveplot" })
                elif layer.get("layer_type") == "cluster":
                    returnGroup.append({ 'layer': getMemorials('cluster'), 'layer_type': "memorials_cluster" })
                elif layer.get("layer_type") == "raster":
                    continue # These layers don't make a request to the server
                else:
                    returnGroup.append({ 'layer': getLayer(layer.get("layer_code"), True), 'layer_type': "geometries_" + layer.get("layer_code") })

            if len(returnGroup)>0:
                returnGroups.append({ "group_code": group.get("group_code"), "layers": returnGroup })

        return JsonResponse(returnGroups, safe=False)

class MemorialView(PublicAccessOrViewOnlyView):
    def get(self, request):
        geoj = getMemorials(request.GET.get('layer'))
        return JsonResponse(geoj, safe=False)

class MemorialJsonView(PublicAccessOrViewOnlyView):
    def get(self, request):
#         get cluster layer
        cluster = GravePlot.objects.get_headpoint_json_values(True)
        if len(cluster) == 0:
            cluster = Memorial.objects.get_headpoint_json_values()
        plots = GravePlot.objects.get_centrepoint_json_values()
        memorials = Memorial.objects.get_centrepoint_json_values()
        memorials = list(itertools.chain(cluster,plots,memorials))

        ## @TODO: Find the actual reason of this error in burnsall data
        ## There is an error parsing the json because of the centerpoint is not an array
        ## ref: BGMS-1273
        memorials_response = None
        try:
            memorials_response = JsonResponse({'memorials': memorials}, safe=False)
        except:
            memorials_response = JsonResponse({'memorials': []}, safe=False)
        
        return memorials_response

def getGraveplot(feature_type='plot'):
    layer_obj = Layer.objects.get(feature_code__feature_type=feature_type)
    layer_cache = layer_obj.get_layer_geojson_cache(False)

    if layer_cache:
        return layer_cache
    else:
        query_set = GravePlot.objects.select_related("topopolygon").filter(topopolygon__layer=layer_obj)
        serializer = GraveplotGeoSerializer(query_set, many=True)
        geoj = serializer.data
        geoj.update(CRS)

        layer_obj.update_layer_geojson_cache(geoj, False)

        return geoj

class GraveplotView(ViewOnlyView):
    def get(self, request):
        geoj = getGraveplot()
        return JsonResponse(geoj, safe=False)

class PersonView(ViewOnlyView):
    def get(self, request):
        """
        Returns all persons. But only if there are less than 10,000 total. More that slows everything down too much.
        """
        persons_count = Person.objects.all().count()

        if persons_count < 10000:
            return JsonResponse({'persons': list(Person.objects.all_persons_values())}, safe=False)
        else:
            return JsonResponse({'persons': None}, safe=False)


class PersonByMemorialIDView(PublicAccessOrViewOnlyView):
    def get(self, request):
        memorial_id_array = json.loads(request.GET.get('memorialId'))
        return JsonResponse({'persons': list(Person.objects.persons_by_memorial_id_values(memorial_id_array))}, safe=False)


class FindGraveplotByGraveNumberView(ViewOnlyView):
    def get(self, request):

        graveplot = GravePlot.objects.get_graveplots_from_grave_ref(request.GET.get('graveNumber'), request.GET.get('sectionID'), request.GET.get('subsectionID'), True)

        if graveplot:
            # more than one result
            if len(graveplot) > 1:
                graves = []
                for grave in graveplot:
                    graveData = {'grave_number': grave.graveref.grave_number}

                    if grave.graveref.section:
                        graveData['section'] = grave.graveref.section.section_name
                    if grave.graveref.subsection:
                        graveData['subsection'] = grave.graveref.subsection.subsection_name

                    graves.append(graveData)

                return JsonResponse({'results': len(graveplot), 'graves': graves}, safe=False)
            # valid result
            else:
                persons = Person.objects.filter(death__death_burials__graveplot=graveplot[0]).values('id', 'first_names', 'last_name')
                graveData = {'results': 1, 'grave_id': graveplot[0].uuid, 'grave_number': graveplot[0].graveref.grave_number, 'persons': list(persons)}

                if graveplot[0].graveref.section:
                    graveData['section'] = graveplot[0].graveref.section.section_name
                if graveplot[0].graveref.subsection:
                    graveData['subsection'] = graveplot[0].graveref.subsection.subsection_name

                return JsonResponse(graveData, safe=False)
        # not found
        else:
            return JsonResponse({'results': 0}, safe=False)


class PersonsByIDsView(ViewOnlyView):
    def get(self, request):
        person_id_array = json.loads(request.GET.get('personIds'))
        personResults = Person.objects.persons_by_id_values(person_id_array)
        groupedPersonResults = {}

        # group array so multiple records for the same person are kept together
        for person in personResults:
            if person["id"] in groupedPersonResults:
                groupedPersonResults[person["id"]].append(person)
            else:
                groupedPersonResults[person["id"]] = [person]

        return JsonResponse({'persons': groupedPersonResults}, safe=False)

class AllMemorialInscriptionsView(ViewOnlyView):
    def get(self, request):
        serializer = MemorialInscriptionSerializer(MemorialInscriptionDetail.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False)


class MapInitialisationView(PublicAccessOrViewOnlyView):
    """
    Get Initial details for map creation, base map and aerial
    """
    def get(self, request):
        site = BurialGroundSite.objects.get(schema_name__exact=connection.schema_name)
        # import pdb; pdb.set_trace()
        return JsonResponse(site.get_map_initialization_details())


class AddHeadstoneView(WardenView):
    def post(self, request):
        response = request.body.decode()
        geojson_feature = json.loads(response)['geojsonFeature']
        geojson_polygon = json.dumps(json.loads(geojson_feature)['geometry'])
        geojson_id = json.loads(geojson_feature)['id']
        print(geojson_polygon)
        # QUESTION: Does the TopoPolygon and Memorial having the same UUID break anything?
        memorial_polygon = TopoPolygons.objects.get_or_create_from_geojson(geojson_feature)[0]
        memorial = Memorial.objects.create(uuid=geojson_id, user_generated=True, topopolygon=memorial_polygon)
        
        geoj = memorial.get_geojson()

        return JsonResponse(geoj, safe=False)

class LinkHeadstonePlotView(WardenView):
    def post(self, request):
        response = json.loads(request.body.decode())
        memorial_uuid = response.get('memorial_id')
        graveplot_uuid = response.get('plot_id')
        memorial = Memorial.objects.get_from_uuid(memorial_uuid)
        graveplot = GravePlot.objects.get_from_uuid(graveplot_uuid)
        MemorialGraveplot.objects.get_or_create(memorial=memorial,graveplot=graveplot)
        persons = Person.objects.filter(death__death_burials__graveplot=graveplot)
        for person in persons:
            person.add_memorial(memorial)

        geoj = memorial.get_geojson()

        return JsonResponse(geoj, safe=False)

class DeleteHeadstoneView(WardenView):
    def post(self, request):
        response = json.loads(request.body.decode())
        memorial_uuid = response.get('memorial_id')
        # import pdb; pdb.set_trace()
        marker_type = response.get('marker_type')
        response = None
        try:
            Memorial.objects.delete_memorial_with_no_person(memorial_uuid, marker_type)
            response = JsonResponse({'status': 'OK'})
        except ObjectDoesNotExist as e:
            response = HttpResponseBadRequest(str(e))
        return response

class BurialOfficialsView(ViewOnlyView):
    def get(self, request):
        boall = Official.objects.get_all()
        return HttpResponse(json.dumps(boall))

class ReservedPersonsView(ViewOnlyView):
    def get(self, request):
        return JsonResponse({'reserved_persons': list(ReservedPlot.objects.all_reserved_persons_values())}, safe=False)

class ReservedGraveplotsView(ViewOnlyView):
    def get(self, request):
        geoj = getGraveplot('reserved_plot')
        return JsonResponse(geoj, safe=False)


class LayerGroupsView(ViewOnlyView):
    def get(self, request):
        groups_list = request.GET.getlist('groups_to_load[]')
        dict_groups_layers = FeatureGroup.objects.get_layer_groups(groups_list)
        # import pdb; pdb.set_trace()
        # return JsonResponse({'layer_groups': dict_groups_layers}, safe=False)
        return JsonResponse(dict_groups_layers, safe=False)


class SiteFilesView(AjaxableResponseMixin, FormView):
    """
    GET request: display mapmanagement/site_files_modal.html
    """
    success_url = '/mapmanagement'

    def get(self, request):
        files_encoded = File.objects.all()
        files = []
        for fe in files_encoded:
            files.append({'url':fe.url.url, 'name': fe.name})
        return render(request, 'mapmanagement/site_files_modal.html', {'files': files})


class TakePhotoView(MemorialPhotographyView):
    def post(self, request):
        data = json.loads(request.body.decode())
        memorial = Memorial.objects.get(uuid=data['memorial_id'])

        try:
            memorial_image = memorial.create_image(Image.base64_to_image(data['image']))

            return JsonResponse({ 'uuid': memorial_image.id }, status=201)
        except Exception as e:
            print(e)
            return HttpResponseBadRequest('invalid data.')


class MemorialInspectionView(APIView):

    def post(self, request):

        serializer = InspectionSerializer(data=request.data, 
            context={ 'imageBase64':request.data['imageBase64'], 'user': request.user })

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def get(self, request):

        memorial_uuid = request.GET.get('memorial_uuid')

        if not memorial_uuid:
            return HttpResponseBadRequest("Memorial not specified")

        memorial = Memorial.objects.get_from_uuid(memorial_uuid)

        if memorial:
            memorialInspections = Inspection.objects.filter(memorial=memorial).order_by('date')
            serializer = InspectionSerializer(memorialInspections, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return HttpResponseBadRequest("Memorial does not exist")


class GetMemorialImages(PublicAccessOrViewOnlyView):
    def get(self, request):
        id = request.GET.get('id')
        if id is not None and id != '':
            memorial = Memorial.objects.get_from_uuid(id)

            if memorial:
                memorial_images = memorial.list_image_urls()
                return JsonResponse(memorial_images, safe=False)
            return HttpResponseBadRequest("Memorial does not exist")
        return HttpResponseBadRequest("Memorial ID not specified")


class DeleteMemorialImage(MemorialPhotographyView):
    def post(self, request):
        request = json.loads(request.body.decode())
        image_uuid = request['image_uuid']
        memorial_uuid = request['memorial_uuid']

        if not image_uuid or not memorial_uuid:
            return HttpResponseBadRequest("Memorial and/or image not specified")

        memorial = Memorial.objects.get_from_uuid(memorial_uuid)

        if memorial:
            memorial.delete_image(image_uuid)
            return HttpResponse(status=204)
        else:
            return HttpResponseBadRequest("Memorial does not exist")


class SendReport(WardenView):
    def post(self, request):
        data = json.loads(request.body.decode())
        email_ag_admin('BGMS Error Report', 'mail_templated/error_report.tpl', {
            'user': request.user,
            'site': connection.schema_name,
            'datetime': datetime.datetime.now().strftime('%X %x'),
            'json': data['error_message'],
        })
        return HttpResponse(status=200)


class GraveLinkView(APIView):

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def post(self, request):
        try:
            data=request.data

            if not data.get('memorial_id'):
                return HttpResponseBadRequest("Memorial not specified")

            memorial = Memorial.objects.get_from_uuid(data.get('memorial_id'))

            try:
                graveplot_id = data.get('graveplot_id')
                graveplot = GravePlot.objects.get(uuid=graveplot_id)
            except:
                # this must be an available plot
                graveplot,created = GravePlot.objects.get_or_create(topopolygon_id=graveplot_id)

            MemorialGraveplot.objects.get_or_create(memorial=memorial, graveplot=graveplot)

            # add graveplot burial persons to newly linked memorial
            graveplot_persons = Person.objects.filter(death__death_burials__graveplot=graveplot)
            graveplot_burials_distinct = Burial.objects.filter(graveplot=graveplot)
            graveplot_burial_distinct_list = []
            
            memorial_persons = memorial.memorial_deaths.filter(person__deleted_at=None)
            memorial_persons_distinct = memorial.memorial_deaths.filter(person__deleted_at=None)
            memorial_persons_distinct_list = []
            transcribed_burials_distinct_list = []
            
            # get burials that are not linked to any grave and have the same grave number as grave
            if graveplot.graveref and graveplot.graveref.grave_number:
                transcribed_burials_distinct_list = Burial.objects.get_unlinked_burials_with_transcribed_grave_number(graveplot.graveref.grave_number)

            # get persons that are linked to memorial but not grave
            if memorial_persons:
                for person in graveplot_persons:
                    memorial_persons_distinct = memorial_persons_distinct.exclude(person_id=person.id)

                for transcribed_burial in transcribed_burials_distinct_list:
                    memorial_persons_distinct = memorial_persons_distinct.exclude(person_id=transcribed_burial['person_id'])

            # get burials that are linked to grave but not memorial
            if graveplot_persons:
                for death in memorial_persons.all():
                    graveplot_burials_distinct = graveplot_burials_distinct.exclude(death__person_id=death.person_id).filter(death__person__deleted_at=None)
            
            if graveplot_burials_distinct:
                for burial in graveplot_burials_distinct:
                    graveplot_burial_distinct_list.append({ 'person_id': burial.death.person_id, 'burial_id': burial.id, 'display_name': burial.death.person.get_display_name(), 'selected': True })
            
            if memorial_persons_distinct:
                for person in memorial_persons_distinct.all():
                    memorial_persons_distinct_list.append({ 'person_id': person.person_id, 'burial_id': person.get_most_recent_burial_id(), 'display_name': person.person.get_display_name(), 'selected': True })

            # reload data to show new link
            serializer = MemorialGraveplotSerializer(instance=memorial)
            return JsonResponse({ 'memorials':serializer.data, 'memorial_persons_distinct_list': memorial_persons_distinct_list, 'graveplot_burial_distinct_list': graveplot_burial_distinct_list, 'transcribed_burials_distinct_list': transcribed_burials_distinct_list }, safe=False)
        except:
            print(traceback.format_exc())
            return HttpResponseBadRequest()

    def get(self, request):

        memorial_uuid = request.GET.get('memorial_uuid')

        if not memorial_uuid:
            return HttpResponseBadRequest("Memorial not specified")

        memorial = Memorial.objects.prefetch_related('graveplot_memorials').get_from_uuid(memorial_uuid)

        if memorial:
            serializer = MemorialGraveplotSerializer(instance=memorial)
            return JsonResponse(serializer.data, safe=False)
        else:
            return HttpResponseBadRequest("Memorial does not exist")

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def delete(self, request):

        data=request.query_params

        if not data.get('memorial_id'):
            return HttpResponseBadRequest("Memorial not specified")

        memorial = Memorial.objects.get_from_uuid(data.get('memorial_id'))
        graveplot = GravePlot.objects.get(uuid=data.get('graveplot_id'))

        graveplot_burials = Burial.objects.filter(graveplot=graveplot) 
        memorial_persons = memorial.memorial_deaths.filter(person__deleted_at=None).values_list('person_id', flat=True).distinct()

        shared_burials_list = []

        # get burials that are in both grave and memorial
        if graveplot_burials and memorial_persons:
            shared_burials = graveplot_burials.filter(death__person_id__in=memorial_persons)

            if shared_burials:
                for burial in shared_burials:
                    shared_burials_list.append({ 'burial_id': burial.id, 'person_id': burial.death.person_id, 'display_name': burial.death.person.get_display_name(), 'includeInGrave': True, 'includeInMemorial': True })

        MemorialGraveplot.objects.get(memorial=memorial,graveplot=graveplot).delete()

        return JsonResponse({'shared_burials': shared_burials_list, 'memorial_id': data.get('memorial_id') }, safe=False)

class ModifyBurialsLinkedFeaturesView(APIView):

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def post(self, request):
        
        burial_list = request.data.get('burial_list')
        graveplot_uuid = request.data.get('graveplot_uuid')
        memorial_uuid = request.data.get('memorial_uuid')
        grave_number = request.data.get('grave_number')

        graveplot = None
        memorial = None

        added_to_grave = []
        added_to_memorial = []
        removed_from_grave = []
        removed_from_memorial = []

        original_graveplot_layer = None
        new_graveplot_layer = None
        graveplot_topopolygon_id = None

        if graveplot_uuid:
            try:
                graveplot = GravePlot.objects.get(uuid=graveplot_uuid)
            except:
                try:
                    topopolygon = TopoPolygons.objects.get(pk=graveplot_uuid)
                    graveplot,created = GravePlot.objects.get_or_create(topopolygon=topopolygon)
                    graveplot_uuid = graveplot.uuid
                except:
                    return HttpResponseBadRequest("Invalid grave id.")

            if graveplot.topopolygon:
                graveplot_topopolygon_id  = graveplot.topopolygon_id
                original_graveplot_layer = graveplot.topopolygon.layer.feature_code.feature_type

        if grave_number:
            graveRef = GraveRef.objects.get(grave_number=grave_number)
            graveplot, created = GravePlot.objects.get_or_create(graveref=graveRef)
            graveplot_uuid = graveplot.uuid

        if memorial_uuid:
            memorial = Memorial.objects.get(uuid=memorial_uuid)
            MemorialGraveplot.objects.get_or_create(memorial=memorial, graveplot=graveplot)

        for burial_detail in burial_list:

            burial = None
            
            if burial_detail['burial_id']:
                burial = Burial.objects.get(id=burial_detail['burial_id'])

            if 'add_to_grave' in burial_detail:

                if graveplot:

                    # create burial record if one does not already exists
                    # or one exists but is linked to another grave
                    if not burial or (burial_detail['add_to_grave'] and burial.graveplot and burial.graveplot.uuid != graveplot_uuid):
                        burial = Burial.objects.create(death_id=burial_detail['person_id'])
                    
                    if burial_detail['add_to_grave']:
                        burial.graveplot = graveplot
                        added_to_grave.append(burial_detail['person_id'])
                    
                        # option to add burial to memorials linked to grave
                        if 'add_to_memorials_linked_to_grave' in burial_detail and burial_detail['add_to_memorials_linked_to_grave']:
                            for memorial in graveplot.memorials.all():
                                burial.death.add_memorial(memorial)
                                added_to_memorial.append(burial_detail['person_id'])
                    else:
                        burial.graveplot = None
                        removed_from_grave.append(burial_detail['person_id'])
                    
                    burial.save()

                    # graveplot layer might have changed
                    new_graveplot_layer = graveplot.update_plot_layer()
                        
                else:
                    print('ModifyBurialListLinkedFeatures: valid graveplot_uuid missing')

            if 'add_to_memorial' in burial_detail:

                if memorial:
                    if burial_detail['add_to_memorial']:
                        burial.death.add_memorial(memorial)
                        added_to_memorial.append(burial_detail['person_id'])
                    else:
                        burial.death.remove_memorial(memorial)
                        removed_from_memorial.append(burial_detail['person_id'])
                        
                else:
                    print('ModifyBurialListLinkedFeatures: valid memorial_uuid missing')

        serializer = MemorialGraveplotSerializer(instance=memorial)
        # response is needed to update indexeddb in sw
        return JsonResponse({'memorials': serializer.data, 'added_to_grave': added_to_grave, 'removed_from_grave': removed_from_grave, 'added_to_memorial': added_to_memorial, 'removed_from_memorial': removed_from_memorial, 'memorial_id': memorial_uuid, 'graveplot_id': graveplot_uuid, 'original_graveplot_layer': original_graveplot_layer, 'new_graveplot_layer': new_graveplot_layer, 'graveplot_topopolygon_id': graveplot_topopolygon_id }, safe=False, content_type ='application/json')

#from rest_framework import generics
# class GraveNumbersView(generics.ListAPIView):
#     lookup_field = 'id'
#     serializer_class = MemorialGraveNumbersSerializer

#     def get_queryset(self):
#         return Memorial.objects.all()

#     def list(self, request, *args, **kwargs):
#         res = super(GraveNumbersView, self).list(request, *args, **kwargs)
#         # res.data = {"STATUS": "SUCCESS", "DATA": res.data}
#         return JsonResponse(res.data, safe=False)
class GraveNumbersView(APIView):

    def get(self, request):
        """ Search for graveplots with a graveref and get list of graveplot id and their graveref """
        # fetch graveplot and section/subsection in same query which is much faster
        # memorialplot_qs = Memorial.objects.exclude(graveplot_memorials=None)
        # graveplot_qs = GraveNumberSerializer.setup_eager_loading(GravePlot.objects.all().exclude(graveref__isnull=True).exclude(graveref__grave_number__isnull=True).exclude(graveref__grave_number__exact='').order_by('graveref__grave_number'))
        # serializer = GraveNumberSerializer(graveplot_qs, many=True)
        plot_State= ReservePlotState.objects.all()
        try:
            if plot_State :
                serializer = MemorialGraveNumbersSerializer(Memorial.objects.exclude(graveplot_memorials=None), many=True)
                my_data = json.loads(json.dumps(serializer.data))
                new_data = {}
                for memorial in my_data:
                        for grave in memorial['graveplot_memorials']:
                            if 'grave_number' in grave and 'topopolygon_id' in memorial and memorial['topopolygon_id'] is not None:
                                new_data[memorial['topopolygon_id'] + ''] = grave['grave_number']
                            elif 'grave_number' in grave and 'feature_id' in grave and grave['feature_id'] is not None:
                                new_data[grave['feature_id'] + ''] = grave['grave_number']
                return JsonResponse(json.dumps(new_data), safe=False)

        except ValidationError as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        
class SectionView(APIView):

    def get(self, request):

        serializer = SectionSerializer(Section.objects.all().order_by('section_name'), many=True)
        return JsonResponse(serializer.data, safe=False)
        #sections = Section.objects.all().order_by('section_name').values('id','section_name','topopolygon'); #create queryset with limited fields           
        #sections = Section.objects.all().order_by('section_name');
        # Convert the QuerySet to a List
        #list_of_sections = list(sections)   
        #another attempt to get the associated topopolygon object when fetching section
        #serializer = SectionSerializer(data=sections, many=True) 
        
        #return JsonResponse(list_of_sections, safe=False) #works for both empty sets and returned list of sections
        #if serializer.is_valid():
        #    return JsonResponse(serializer.data, safe=False)
        #if sections:  #Original code in case there are issues with the map
        #serializer = SectionSerializer(data=sections, many=True)
        #if serializer.data and serializer.data.list:
        #if serializer.is_valid():
        #    return JsonResponse(serializer.data, safe=False)
        #else:
        #    return JsonResponse([], status=204)        
        #else:
        #    return JsonResponse({}, status=204)

    def get_queryset(self):
        return Section.objects.all().order_by('section_name')

class SectionViewById(APIView):

    def get(self, request):
        id = int(request.query_params['section_id'])
        section = Section.objects.get(id=id)
        serializer = SectionSerializer(section, many=False)
        return JsonResponse(serializer.data, safe=False)


#def get_section_by_sectionid(request, section_id):
#    section = Section.objects.get(id = section_id)
#    return section


def get_featureid_from_sectionid(request, sectionID):
    section = Section.objects.get(id = sectionID)
    topoid = section.topopolygon_id
    topopolygon = TopoPolygons.objects.get(id = topoid)
    featureID = topopolygon.feature_id
    return featureID

class SubsectionView(APIView):

    def get(self, request):

        serializer = SubsectionSerializer(Subsection.objects.all().order_by('subsection_name'), many=True)
        return JsonResponse(serializer.data, safe=False)

class FeatureIDView(APIView):

    def get(self, request):

        serializer = FeatureIDSerializer(
            GravePlot.objects.all().exclude(feature_id__isnull=True).exclude(feature_id__exact='').order_by('feature_id'), many=True)
        return JsonResponse(serializer.data, safe=False)

def proxy(request, url):
	remote_url = request.scheme+ "://" + request.get_host() + '/' + url
	return proxy_view(request, remote_url)
