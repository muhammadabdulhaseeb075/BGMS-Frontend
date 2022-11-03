from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.serializers import serialize
from django.db import transaction
from django.db.models import Count, Q, F
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
import json

from cemeteryadmin import serializer
json.encoder.FLOAT_REPR = lambda o: format(o, '.2f')
from datetime import date, datetime

from bgsite.common_apis.bacas_api import *

from bgsite.common_apis.serializers import DeathPersonSerializer, BurialDetailsSerializer, BurialListSerializer, \
    MemorialListSerializer, PersonFieldSerializer, BurialNumberSerializer
from bgsite.common_apis.views import PublicPersonView
from bgsite.models import Official, Person, Memorial, Death, Burial, GravePlot, Official, Image, ReservedPlot, \
    GraveplotStatus, GraveplotState, GraveplotType, BurialOfficialType, \
    MemorialGraveplot, GraveDeed, GraveOwner, ReservePlotState, OwnerStatus, GraveRef, PersonField
from bgsite.views import AjaxableResponseMixin, ViewOnlyView, group_required, PublicAccessOrViewOnlyView
from config.security.drf_permissions import IsAuthenticatedOrPublicAccessReadOnly
from geometries.models import FeatureAttributes, TopoPolygons, TopoPolylines, TopoPoints, Attribute, Layer, LayerCache
from geometriespublic.models import PublicAttribute
from main.models import Currency, PublicPerson, Company as PublicCompany, BurialGroundSite
from main.serializers import PersonSerializer, CompanySerializer
from mapmanagement.serializers import GraveDetailsSerializer, MemorialSerializer, BurialInformationSerializer, \
    PersonListSerializer, GraveDeedsListSerializer, DeedSerializer, GraveOwnerSerializer, \
    PersonCompanyOwnershipListSerializer, ReservedPersonListSerializer, PersonNextOfKinToSerializer, \
    NewGraveOwnerSerializer

import traceback
import uuid

from rest_framework.parsers import JSONParser,FileUploadParser,MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tenant_schemas.utils import schema_context

class AvailablePlotGravePlotView(APIView):

    def get(self, request):

        available_plot_id = request.GET.get('available_plot_id')

        if available_plot_id:
            graveplot,created = GravePlot.objects.get_or_create(topopolygon_id=available_plot_id)
            return JsonResponse({ 'graveplot_id': graveplot.uuid }, safe=False)
        else:
            return HttpResponseBadRequest("Available Plot ID does not exist")

class GetGraveplotLayerView(APIView):
    """ Gets a graveplots layer name i.e. 'plot', 'available_plot', 'reserved_plot'
        Also gets topopolygon_id. """

    def get(self, request):

        graveplot_id = request.GET.get('graveplot_id')

        if graveplot_id:
            graveplot = GravePlot.objects.get_from_uuid(graveplot_id)

            if graveplot.topopolygon:
                return JsonResponse({ 'layer': graveplot.topopolygon.layer.feature_code.feature_type, 'topopolygon_id': graveplot.topopolygon.id }, safe=False)
            else:
                return JsonResponse({ 'layer': 'plot' }, safe=False)
        else:
            return HttpResponseBadRequest("Available Plot ID does not exist")

class RelatedBurialsView(APIView): 

    def get(self, request):

        graveplot_uuid = request.GET.get('graveplot_uuid')
        person_id = request.GET.get('person_id')
        burials = None

        if graveplot_uuid:
            obj = GravePlot.objects.prefetch_related('burials').get_from_uuid(graveplot_uuid)                        

            '''BACAS - Commenting out in case it is causing issues            
            schema_name = request._request.tenant.schema_name #This may not work for servers other than Uwsgi, will eventually pull from DB anyway
            if schema_name == 'western': #Western is the BACAS demo schema so perform REST query.
                graveref = obj.graveref;
                bacas_section_number = int(graveref.bacas_section_number)
                bacas_grave_ref_number = int(graveref.bacas_grave_ref_number)
                print('BACAS. Section: ' + str(bacas_section_number) + ' ' + 'Grave: ' + str(bacas_grave_ref_number))
                deceased = bacas_get_deceased(bacas_section_number, bacas_grave_ref_number)                                
                return JsonResponse(deceased, safe=False)
            '''
            
            if obj and obj.burials:
                burials = obj.burials
        elif person_id:
            obj = Death.objects.prefetch_related('death_burials').get(person_id=person_id)
            if obj and obj.death_burials:
                burials = obj.death_burials
        else:
            return HttpResponseBadRequest("Object not specified")

        if obj:
            serializer = BurialListSerializer(instance=burials, many=True, read_only=True)
            
            # sort result by burial_date
            result = sorted(serializer.data, key=lambda k: k['burial_date'] if k['burial_date'] else date(9999, 12, 31), reverse=True)

            return JsonResponse(result, safe=False)
        else:
            return HttpResponseBadRequest("Object does not exist")

class RelatedReservationsView(APIView):

    def get(self, request):

        try:
            graveplot_uuid = request.GET.get('graveplot_uuid')

            if graveplot_uuid:

                state=ReservePlotState.objects.get(state='reserved')
                reserved_persons = Person.objects.filter(reservedplot__grave_plot__uuid=graveplot_uuid, reservedplot__state=state)
            else:
                return HttpResponseBadRequest("Grave not specified")

            serializer = ReservedPersonListSerializer(instance=reserved_persons, many=True, read_only=True)

            return JsonResponse(serializer.data, safe=False)

        except ValidationError as e:
            print(e)
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

class RelatedMemorialsView(APIView):

    permission_classes = [IsAuthenticatedOrPublicAccessReadOnly]

    def get(self, request):

        graveplot_uuid = request.GET.get('graveplot_uuid')
        person_id = request.GET.get('person_id')

        ''' Memorial could be related to graveplot or a person '''
        if graveplot_uuid:
            obj = GravePlot.objects.prefetch_related('memorials').get_from_uuid(graveplot_uuid)
        elif person_id:
            obj = Death.objects.prefetch_related('memorials').get(person_id=person_id)
        else:
            return HttpResponseBadRequest("Object not specified")

        if obj:
            serializer = MemorialListSerializer(instance=obj.memorials, many=True, read_only=True)
            return JsonResponse({ 'linkedMemorials': serializer.data }, safe=False)
        else:
            return HttpResponseBadRequest("Object does not exist")

class GraveDetailsView(APIView):

    def get(self, request):

        graveplot_uuid = request.GET.get('graveplot_uuid')
        grave_number = request.GET.get('graveNumber')

        if not graveplot_uuid and not grave_number:
            return HttpResponseBadRequest("Grave not specified")

        if graveplot_uuid:
            grave = GravePlot.objects.get_from_uuid(graveplot_uuid)

        if grave_number:
            grave_ref = GraveRef.objects.filter(grave_number=grave_number)
            if grave_ref.first():
                grave = GravePlot.objects.get_from_ref_id(grave_ref.first().id)

        if grave:
            serializer = GraveDetailsSerializer(instance=grave)
            return JsonResponse(serializer.data, safe=False)
        else:
            return HttpResponseBadRequest("Grave does not exist")
    
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def patch(self, request):

        data=request.data 
        #Get uuid & grave_number from request
        grave_uuid = data.get('id')
        grave_number = data.get('grave_number')
        #Section & Subsection are not passed in but can get them from uuid
        grave_section = None
        grave_subsection = None

        if not grave_uuid: #If uuid is not specified then we can't do anything
            return HttpResponseBadRequest("Grave not specified")

        #get a graveplot object based on the uuid
        grave = GravePlot.objects.get_from_uuid(grave_uuid)

        if grave: #populate the section & subsection from the grave object
            grave_section = grave.graveref.section_id
            grave_subsection = grave.graveref.subsection_id

        grave_plot_to_copy = None
        if grave_number:
            if grave_section and grave_subsection:                
                grave_ref = GraveRef.objects.get(grave_number=grave_number, section_id=grave_section, subsection_id=grave_subsection)
            else:
                grave_ref = GraveRef.objects.get(grave_number=grave_number) #in case there are schemas with section & subsection not populated

            #For reasons unknown grave plots don't have a section or subsection while burials (graveref) do. 
            #To get the section & subsection it finds and lists all graverefs that match the grave number then gets the plot from the first one returned.
            grave_plots_with_grave_number = GravePlot.objects.filter(graveref_id=grave_ref)
            grave_plot_to_copy = grave_plots_with_grave_number.first()

            #The grave plot to copy is the first (and only?) grave plot assigned to the graveref. However, that is the new grave number so it is referencing a plot that may not exist?
            if grave_plot_to_copy:
                if grave_plot_to_copy.topopolygon is None:
                    if grave:
                        reserved_plots_copy = ReservedPlot.objects.filter(grave_plot_id=grave.id)
                        reserved_last_plots_copy = ReservedPlot.objects.filter(grave_plot_id=grave_plot_to_copy.id)
                        grave_plot_to_copy.topopolygon = grave.topopolygon
                        grave_plot_to_copy.uuid = grave.uuid

                        if reserved_plots_copy:
                            for reserved_plot in reserved_plots_copy:
                                can_copy = True
                                for reserved_last_plot in reserved_last_plots_copy:
                                    if reserved_last_plot.person_id == reserved_plot.person_id:
                                        can_copy = False
                                if can_copy:
                                    reserved_plot.grave_plot = grave_plot_to_copy
                                    reserved_plot.save()
                        else:
                            for reserved_last_plot in reserved_last_plots_copy:
                                reserved_last_plot.grave_plot = grave_plot_to_copy
                                reserved_last_plot.save()
                        grave.delete()
                    grave = grave_plot_to_copy

                else:
                    return HttpResponseBadRequest("The grave number is already used")


        if 'grave_number' in data:
            # if grave number has changed
            grave.modify_grave_number(data.get('grave_number'))

        if grave:
            serializer = GraveDetailsSerializer(grave, data=data, partial=True)
            if serializer.is_valid():
                try:
                    serializer.save()

                    if grave_plot_to_copy:
                        grave.update_plot_layer()
                        LayerCache.objects.all().delete()

                    return Response(serializer.data)
                except ValidationError as e:
                    # most likely cause of failure is that the ref is not unique
                    return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponseBadRequest("Grave does not exist")



class GraveDeedsListView(APIView):

    def get(self, request):

        graveplot_uuid = request.GET.get('graveplot_uuid')

        if not graveplot_uuid:
            return HttpResponseBadRequest("Grave not specified")

        graveplot_deeds = GravePlot.objects.get_from_uuid(graveplot_uuid).graveplot_deeds

        if graveplot_deeds:
            serializer = GraveDeedsListSerializer(instance=graveplot_deeds, many=True)
            
            # sort result by purchase_date
            result = sorted(serializer.data, key=lambda k: k['purchase_date'] if k['purchase_date'] else '9999-12-31', reverse=True)

            return JsonResponse(result, safe=False)
        else:
            return HttpResponseBadRequest("Grave deed/s do not exist")

class GraveDeedView(APIView):

    def update_grave_deed(self, grave_deed, data):

        save_image_1 = False
        save_image_2 = False
        image_1 = {}
        image_2 = {}

        if 'image_1' in data:
            # don't process this field in serializer. Hence remove it from data object.
            image_1 = json.loads(data['image_1'])
            del data['image_1']
            save_image_1 = True

        if 'image_2' in data:
            # don't process this field in serializer. Hence remove it from data object.
            image_2 = json.loads(data['image_2'])
            del data['image_2']
            save_image_2 = True

        serializer = DeedSerializer(grave_deed, data=data, partial=True)
            
        if serializer.is_valid():

            serializer.save()

            if save_image_1 or save_image_2:
                grave_deed = GraveDeed.objects.get(id=serializer.data.get('id'))

                if save_image_1:
                    if 'original_id' in image_1:
                        # delete original image
                        grave_deed.images.remove(Image.objects.get(id=image_1.get('original_id')))
                    
                    if 'thumbnail_url' in image_1:
                        # add/replace image
                        image = image_1['thumbnail_url'].replace("data:image/jpeg;base64,", "")
                        if image is not None:
                            grave_deed.add_image(Image.base64_to_image(image))

                if save_image_2:
                    if 'original_id' in image_2:
                        # delete original image
                        grave_deed.images.remove(Image.objects.get(id=image_2.get('original_id')))
                    
                    if 'thumbnail_url' in image_2:
                        # add/replace image
                        image = image_2['thumbnail_url'].replace("data:image/jpeg;base64,", "")
                        if image is not None:
                            grave_deed.add_image(Image.base64_to_image(image))

            return serializer.data
        else:
            raise ValidationError(serializer.errors)

    def get(self, request):

        if 'deed_id' not in request.GET or not request.GET.get('deed_id'):
            deed = GraveDeed()
        else:
            try:
                deed = GraveDeed.objects.prefetch_related('grave_owners').get(id=request.GET.get('deed_id'))
            except Exception as e:
                print(e)
                return HttpResponseBadRequest("Deed does not exist")

        serializer = DeedSerializer(instance=deed)
        return JsonResponse(serializer.data, safe=False)
    
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def patch(self, request):

        data=request.data.copy()

        if not 'id' in data:
            return HttpResponseBadRequest("Deed not specified")

        try:
            if 'deed_reference' in data and GraveDeed.objects.filter(deed_reference=data.get('deed_reference')).exists():
                return Response(data={ 'deed_reference_taken': True }, status=status.HTTP_400_BAD_REQUEST)
 
            deed = GraveDeed.objects.get(id=data.get('id'))
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Deed does not exist")

        if 'deed_url' in data and (data.get('deed_url') == None or data.get('deed_url') == 'null'):
            del data['deed_url']
            deed.deed_url = None
            deed.save()

        try:
            return Response(self.update_grave_deed(deed, data))

        except Exception as e:
            print(traceback.format_exc())
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def post(self, request):

        try:
            if 'deed_reference' in request.data and GraveDeed.objects.filter(deed_reference=request.data.get('deed_reference')).exists():
                return Response(data={ 'deed_reference_taken': True }, status=status.HTTP_400_BAD_REQUEST)
            
            grave_plot = GravePlot.objects.get(uuid=request.data.get('graveplot_id'))
            grave_deed = GraveDeed.objects.create(graveplot=grave_plot)

            response = self.update_grave_deed(grave_deed, request.data.copy())

            # update layer if needed
            grave_plot.update_plot_layer()

            return Response(response)

        except ValidationError as e:
            print(traceback.format_exc())
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

class GraveOwnerView(APIView):

    def get(self, request):

        if 'id' not in request.GET or not request.GET.get('id'):
            grave_owner = GraveOwner()
            grave_owner.owner_from_date_day = datetime.now().day
            grave_owner.owner_from_date_month = datetime.now().month
            grave_owner.owner_from_date_year = datetime.now().year

            serializer = NewGraveOwnerSerializer(instance=grave_owner)
            data = serializer.data
            data['owner_status'] = []
            return JsonResponse(data, safe=False)
        else:
            try:
                grave_owner = GraveOwner.objects.prefetch_related('owner').get(id=request.GET.get('id'))
            except ValidationError as e:
                print(e)
                return HttpResponseBadRequest("Grave deed does not exist")

            # if active owner field needs updated
            if grave_owner.active_owner==True and grave_owner.owner_to_date and grave_owner.owner_to_date < date(datetime.now().year, datetime.now().month, datetime.now().day):
                grave_owner.active_owner=False
                grave_owner.save()

            serializer = GraveOwnerSerializer(instance=grave_owner)
            return JsonResponse(serializer.data, safe=False)
    
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def patch(self, request):

        data=request.data

        if 'id' not in data or not data.get('id'):
            return HttpResponseBadRequest("Grave owner not specified")

        grave_owner = GraveOwner.objects.get(id=data.get('id'))

        if grave_owner:
            serializer = GraveOwnerSerializer(grave_owner, data=data, partial=True)
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data)
                except ValidationError as e:
                    print(e)
                    return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponseBadRequest("Grave owner does not exist")


class CreateNewOwnerView(APIView):
    
    ''' Create a new owner record with (public) person record '''
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    @transaction.atomic 
    def post(self, request):

        data = request.data

        if 'deed_id' not in data or not data.get('deed_id'):
            return HttpResponseBadRequest("Ownership id not specified")

        grave_owner_data = data.get('grave_owner')
        owner = None

        try:
            if 'person_id' in data:
                owner = PublicPerson.objects.get(id=data.get('person_id'))
            elif 'person_details' in data:
                # create new person
                serializer = PersonSerializer(data=data.get('person_details'))
                if serializer.is_valid():
                    owner = serializer.save(id=data.get('person_details').get('id', None), created_by=request.user, address=data.get('address', None))
                else:
                    print(serializer.errors)
                    raise ValidationError(serializer.errors)
            elif 'company_id' in data:
                owner = PublicCompany.objects.get(id=data.get('company_id'))
            elif 'company_details' in data:
                # create new company
                serializer = CompanySerializer(data=data.get('company_details'))
                if serializer.is_valid():
                    owner = serializer.save(id=data.get('company_details').get('id', None), created_by=request.user, address=data.get('address', None))
                else:
                    print(serializer.errors)
                    raise ValidationError(serializer.errors)
            else:
                return HttpResponseBadRequest("Person/Company data not specified")
            
            if 'transfer' in data and data.get('transfer'):
                # remove active status of any other owners of this deed
                active_owners = GraveOwner.objects.filter(deed_id=data.get('deed_id'), active_owner=True)

                for active_owner in active_owners:
                    active_owner.active_owner = False

                    if active_owner.owner_to_date and active_owner.owner_to_date > datetime.now():
                        active_owner.owner_to_date_day = datetime.now().day
                        active_owner.owner_to_date_month = datetime.now().month
                        active_owner.owner_to_date_year = datetime.now().year
                    
                    active_owner.save()
            
            grave_owner = GraveOwner.objects.create(deed_id=data.get('deed_id'), owner=owner)
            
            del grave_owner_data['owner_id']
            serializer = GraveOwnerSerializer(grave_owner, data=grave_owner_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                raise ValidationError(serializer.errors)

        except ValidationError as e:
            return Response(data={ 'detail': e.message }, status=status.HTTP_400_BAD_REQUEST)
        except:
            print(traceback.format_exc())
            return Response(status=status.HTTP_400_BAD_REQUEST)

''' Get roles of person within this site '''
class PersonRolesView(APIView):

    def get(self, request):

        person_id = request.GET.get('id')

        roles = {}

        if not person_id:
            return HttpResponseBadRequest("Person not specified")

        sites = BurialGroundSite.get_client_sites()

        for site in sites:
            with schema_context(site['schema_name']):
                # Is person an owner?
                if not 'owner' in roles and PublicPerson.objects.filter(id=person_id).exclude(graves_owned__isnull=True).exists():
                    roles['owner'] = True
                # Is person a next of kin?
                if not 'next_of_kin' in roles and PublicPerson.objects.filter(id=person_id).exclude(next_of_kin_to__isnull=True).exists():
                    roles['next_of_kin'] = True
 
                if 'owner' in roles and 'next_of_kin' in roles:
                    break

        return JsonResponse(roles, safe=False)

''' Get roles of company within this site '''
class CompanyRolesView(APIView):

    def get(self, request):

        company_id = request.GET.get('id')

        roles = {}

        if not company_id:
            return HttpResponseBadRequest("Company not specified")

        sites = BurialGroundSite.get_client_sites()

        for site in sites:
            with schema_context(site['schema_name']):
                if PublicCompany.objects.filter(id=company_id).exclude(graves_owned__isnull=True).exists():
                    roles['owner'] = True
                    break

        return JsonResponse(roles, safe=False)

''' Get graves which person owns '''
class PersonOwnershipView(APIView):

    def get(self, request):

        person_id = request.GET.get('id')

        if not person_id:
            return HttpResponseBadRequest("Person not specified")

        sites = BurialGroundSite.get_client_sites()

        owned_graves = []
        previously_owned_graves = []

        # get the graves owned by this person in each site within the current client
        for site in sites:
            with schema_context(site['schema_name']):

                schema_owned_graves = GraveOwner.objects.prefetch_related('deed').filter(person__id=person_id).filter(Q(active_owner=True) & (Q(owner_to_date__isnull=True) | Q(owner_to_date__gte=datetime.now()))).order_by('-owner_from_date')
            
                schema_previously_owned_graves = GraveOwner.objects.prefetch_related('deed').filter(person__id=person_id).exclude(Q(active_owner=True) & (Q(owner_to_date__isnull=True) | Q(owner_to_date__gte=datetime.now()))).order_by('-owner_from_date')

                if schema_owned_graves:
                    owned_graves += PersonCompanyOwnershipListSerializer(instance=schema_owned_graves, many=True, context={'site_name': site['name']}).data
                if schema_previously_owned_graves:
                    previously_owned_graves += PersonCompanyOwnershipListSerializer(instance=schema_previously_owned_graves, many=True, context={'site_name': site['name']}).data

        return JsonResponse({ 'owned_graves': owned_graves, 'previously_owned_graves': previously_owned_graves, 'current_site_name': BurialGroundSite.get_name() }, safe=False)

''' Get graves which person owns '''
class CompanyOwnershipView(APIView):

    def get(self, request):

        company_id = request.GET.get('id')

        if not company_id:
            return HttpResponseBadRequest("Company not specified")
        
        sites = BurialGroundSite.get_client_sites()

        owned_graves = []
        previously_owned_graves = []

        # get the graves owned by this company in each site within the current client
        for site in sites:
            with schema_context(site['schema_name']):

                schema_owned_graves = GraveOwner.objects.prefetch_related('deed').filter(company__id=company_id).filter(Q(active_owner=True) & (Q(owner_to_date__isnull=True) | Q(owner_to_date__gte=datetime.now()))).order_by('-owner_from_date')
            
                schema_previously_owned_graves = GraveOwner.objects.prefetch_related('deed').filter(company__id=company_id).exclude(Q(active_owner=True) & (Q(owner_to_date__isnull=True) | Q(owner_to_date__gte=datetime.now()))).order_by('-owner_from_date')

                if schema_owned_graves:
                    owned_graves += PersonCompanyOwnershipListSerializer(instance=schema_owned_graves, many=True, context={'site_name': site['name']}).data
                if schema_previously_owned_graves:
                    previously_owned_graves += PersonCompanyOwnershipListSerializer(instance=schema_previously_owned_graves, many=True, context={'site_name': site['name']}).data

        return JsonResponse({ 'owned_graves': owned_graves, 'previously_owned_graves': previously_owned_graves, 'current_site_name': BurialGroundSite.get_name() }, safe=False)

''' Get death persons this person is a next of kin to '''
class PersonNextOfKinToView(APIView):

    def get(self, request):

        person_id = request.GET.get('id')

        if not person_id:
            return HttpResponseBadRequest("Person not specified")

        sites = BurialGroundSite.get_client_sites()

        next_of_kin_to = []

        # get the graves owned by this person in each site within the current client
        for site in sites:
            with schema_context(site['schema_name']):

                schema_next_of_kin_to = Person.objects.filter(next_of_kin__id=person_id)

                if schema_next_of_kin_to:
                    next_of_kin_to += PersonNextOfKinToSerializer(instance=schema_next_of_kin_to, many=True, context={'site_name': site['name']}).data

        next_of_kin_to = sorted(next_of_kin_to, key=lambda k: k['display_name'])

        return JsonResponse({ 'next_of_kin_to': list(next_of_kin_to), 'current_site_name': BurialGroundSite.get_name() }, safe=False)

class NewGraveNumberCheckView(APIView):

    def get(self, request):

        can_create_link = False
        grave_number = request.GET.get('graveNumber')
        section_id = request.GET.get('sectionID')
        subsection_id = request.GET.get('subsectionID')
        if not section_id or not subsection_id:
            grave_ref = GraveRef.objects.filter(grave_number=grave_number) #original code, only searches by grave number    
        else: 
            grave_ref = GraveRef.objects.filter(grave_number=grave_number, section_id=section_id, subsection_id=subsection_id)
        

        if grave_ref:
            graveplot = GravePlot.objects.filter(graveref=grave_ref.first())
            if graveplot:
                if graveplot.first().topopolygon is None:
                    return GraveDetailsView.get(self, request)
            else:
                can_create_link = True
        else:
            GraveRef.objects.create(grave_number=grave_number, section_id=section_id, subsection_id=subsection_id)
            can_create_link = True

        return Response(can_create_link)

class AllGravePlotOptionsView(ViewOnlyView):
    def get(self, request):
        return JsonResponse({
            'status': list(GraveplotStatus.objects.all().values('id', 'status').order_by('status')),
            'state': list(GraveplotState.objects.all().values('id', 'state').order_by('state')),
            'type': list(GraveplotType.objects.all().values('id', 'type').order_by('type')),
            'currency': list(Currency.objects.all().values('id', 'name', 'symbol', 'subunit1_symbol', 'subunit2_symbol', 'unit_name', 'subunit1_name', 'subunit2_name').order_by('name'))
            }, safe=False)

class AllOwnershipOptionsView(APIView):
    def get(self, request):

        currency = list(Currency.objects.all().values('id', 'name', 'symbol', 'subunit1_symbol', 'subunit2_symbol', 'unit_name', 'subunit1_name', 'subunit2_name').order_by('name'))

        owner_status = list(OwnerStatus.objects.all().values('id', 'status').order_by('status'))

        return JsonResponse({
            'currency': currency,
            'ownerStatus': owner_status,
            }, safe=False)

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def put(self, request):

        try:

            created_status = OwnerStatus.objects.get_or_create(status=request.data.get('new_status'))[0]
            return JsonResponse({ 'id': created_status.id, 'status': created_status.status }, safe=False)
    
        except Exception as e:
            print(traceback.format_exc())
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

class RelatedPersonsView(APIView):

    permission_classes = [IsAuthenticatedOrPublicAccessReadOnly]

    def get(self, request):

        memorial_uuid = request.GET.get('memorial_uuid')

        if not memorial_uuid:
            return HttpResponseBadRequest("Memorial not specified")

        memorial = Memorial.objects.prefetch_related('memorial_deaths').get_from_uuid(memorial_uuid)

        if memorial:
            serializer = PersonListSerializer(instance=memorial.memorial_deaths.filter(person__deleted_at=None).prefetch_related('death_burials'), many=True, read_only=True)
            # sort result by most_recent_burial_date
            result = sorted(serializer.data, key=lambda k: k['most_recent_burial_date'] if k['most_recent_burial_date'] else date(9999, 12, 31), reverse=True)
            return JsonResponse(result, safe=False)
        else:
            return HttpResponseBadRequest("Memorial does not exist")

class BasicPersonView(APIView):

    def get(self, request):

        person_id = request.GET.get('person_id')

        if not person_id:
            return HttpResponseBadRequest("Person not specified")

        death = Death.objects.prefetch_related('person').get(person_id=person_id)

        if death:
            serializer = PersonListSerializer(instance=death, read_only=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return HttpResponseBadRequest("Person does not exist")

class MemorialDetailsView(APIView):

    def get(self, request):

        memorial_uuid = request.GET.get('memorial_uuid')

        if not memorial_uuid:
            return HttpResponseBadRequest("Memorial not specified")

        memorial = Memorial.objects.get_from_uuid(memorial_uuid)

        if memorial:
            serializer = MemorialSerializer(instance=memorial)
            return JsonResponse(serializer.data, safe=False)
        else:
            return HttpResponseBadRequest("Memorial does not exist")
    
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def patch(self, request,*args,**kwargs):

        data=request.data

        if not data.get('id'):
            return HttpResponseBadRequest("Memorial not specified")

        memorial = Memorial.objects.get_from_uuid(data.get('id'))

        if memorial:
            serializer = MemorialSerializer(memorial, data=data, partial=True)
            if serializer.is_valid():
                try:
                    serializer.save()

                    if 'feature_type' in data:
                        layer = Layer.objects.filter(feature_code__feature_type = data.get('feature_type')).first()
                        memorial.topopolygon.layer = layer
                        memorial.topopolygon.save()

                    return Response(serializer.data)
                except ValidationError as e:
                    return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponseBadRequest("Memorial does not exist")

class CreateNewBurialView(APIView):
    
    ''' Create a new burial record with person and death records '''
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    @transaction.atomic 
    def post(self, request):

        graveplot_id = request.data.get('graveplot_id')
        burial_details = request.data.get('burial_details')
        person_details = request.data.get('person_details')
        selected_memorials = request.data.get('selected_memorials')
        layer = request.data.get('layer')

        if 'id' not in burial_details or not burial_details.get('id'):
            return HttpResponseBadRequest("Burial ID not specified")

        if 'id' not in person_details or not person_details.get('id'):
            return HttpResponseBadRequest("Person ID not specified")

        try:
            # get or create person, death and burial records
            person,created = Person.objects.get_or_create(id=person_details.get('id'))
            death,created = Death.objects.get_or_create(person=person)

            #link to grave
            if graveplot_id:
                graveplot = GravePlot.objects.prefetch_related('memorials').select_related('topopolygon').get_from_uuid(graveplot_id)
                burial = Burial.objects.create(id=burial_details.get('id'), death=death, graveplot=graveplot)

                # convert to regular plot
                if layer and layer in ['available_plot', 'reserved_plot']:
                    graveplot.topopolygon.update_feature_code('plot')
                    graveplot.save()
            #don't link to grave
            else:
                burial = Burial.objects.create(id=burial_details.get('id'), death=death)

            if death:
                #add memorials to death record
                if selected_memorials and len(selected_memorials) > 0:
                    for memorial in selected_memorials:
                        memorial_record = Memorial.objects.get(uuid=memorial)
                        death.add_memorial(memorial_record)
                    death.save()
            else:
                return HttpResponseBadRequest("Error creating death record")
            
            if person:
                DeathPersonDetailView.update_person(self, person, person_details, request.user)
            else:
                return HttpResponseBadRequest("Error creating person record")
            
            if burial:
                BurialDetailsView.update_burial(self, burial, burial_details, request.user)
            else:
                return HttpResponseBadRequest("Error creating burial record")
            
            return JsonResponse({ 'person_id': person.id, 'burial_id': burial.id }, safe=False)

        except ValidationError as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

class DeathPersonDetailView(APIView):

    permission_classes = [IsAuthenticatedOrPublicAccessReadOnly]
    # parser_classes = [FileUploadParser]
    parser_classes = (MultiPartParser,)

    def update_person(self, person, data, user):

        if data.get('next_of_kin'):
            next_of_kin = data.get('next_of_kin')
            new_next_of_kin_id = None
            if 'new_create_details' in next_of_kin:
                # we need to create a new person record
                new_person = PublicPerson.objects.create(id=next_of_kin.get('new_create_details').get('id'))
                new_person.clients.add(BurialGroundSite.get_client())
                PublicPersonView.update_person(self, new_person, next_of_kin.get('new_create_details'), user)
                new_next_of_kin_id = new_person.id
            elif 'new_id' in next_of_kin:
                new_next_of_kin_id = next_of_kin.get('new_id')

            if new_next_of_kin_id:
                person.next_of_kin_id = new_next_of_kin_id

            del data['next_of_kin']

        else:
            person.next_of_kin = None
        
        if 'reservation_reference' in data and data.get('reservation_reference'):
            if ReservedPlot.objects.filter(reservation_reference=data.get('reservation_reference')).exists():
                # this reference is already taken
                raise Exception('{ "reservation_reference_taken": "True" }')
            else:
                person.reservedplot.reservation_reference = data.get('reservation_reference')
                person.reservedplot.save()
        
        person.save()

        serializer = DeathPersonSerializer(person, data=data, partial=True, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise ValidationError(serializer.errors)

    def get(self, request):

        person_id = request.GET.get('person_id')

        if not person_id:
            # create new person
            person = Person()
            death = Death()
            person.death = death
        else:
            person = Person.objects.select_related('residence_address').select_related('next_of_kin').get(id=person_id)

        if person:
            serializer = DeathPersonSerializer(instance=person, context={'user': request.user})
            fields = PersonField.objects.filter(field_form='DeathPersonDetails')
            form_serializer = PersonFieldSerializer(fields, many=True)
            if len(form_serializer.data) == 4:
                for data_value in form_serializer.data:
                    if data_value['name'] and data_value['name'] == 'Profession':
                        profession_field = dict(data_value)
                    if data_value['name'] and data_value['name'] == 'Religion':
                        religion_field = dict(data_value)
                    if data_value['name'] and data_value['name'] == 'Event':
                        event_field = dict(data_value)
                    if data_value['name'] and data_value['name'] == 'Parish':
                        parish_field = dict(data_value)

                return_data = dict(serializer.data, **{'profession_field': profession_field, 'religion_field': religion_field,
                                                   'parish_field': parish_field, 'event_field': event_field, })
            else:
                return_data = serializer.data
            if return_data['death'] is None:
                return_data['death'] = []
            return JsonResponse(return_data, safe=False)
        else:
            return HttpResponseBadRequest("Person does not exist")
    
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def patch(self, request):
        # Review if the request has the values in the data or the body
        if request.data and len(request.data) != 0:
            data = request.data
        elif request.stream and request.stream.body and len(request.stream.body) != 0:
            data = json.loads(request.stream.body)
        else:
            return HttpResponseBadRequest("No data identified")

        if not data.get('id'):
            return HttpResponseBadRequest("Person not specified")

        person = Person.objects.select_related('death').select_related('residence_address').get(id=data.get('id'))
        if data.get('death'):
            try:
                death = Death.objects.get(person_id=data.get('id'))
                for value in data.get('death'):
                    if data.get('death')[value]:
                        setattr(death, value, data.get('death')[value])
                death.save()
            except Exception as e:
                print(traceback.format_exc())
                return HttpResponseBadRequest(str(e))

        if person:
            try:
                return Response(self.update_person(person, data, request.user))

            except Exception as e:
                print(traceback.format_exc())
                return HttpResponseBadRequest(str(e))
        else:
            return HttpResponseBadRequest("Person does not exist")
    
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def post(self, request):

        if request.data and len(request.data) != 0:
            data = request.data
        elif request.stream and request.stream.body and len(request.stream.body) != 0:
            data = json.loads(request.stream.body)
        else:
            return HttpResponseBadRequest("No data identified")

        reservation = False

        try:
            if 'reservation' in data and data.get('reservation'):
                reservation = True

                if not 'graveplot_id' in data:
                    raise ValidationError("Graveplot not specified")

                if 'reservation_reference' in data:
                    if ReservedPlot.objects.filter(reservation_reference=data.get('reservation_reference')).exists():
                        # this reference is already taken
                        return Response(data={ 'reservation_reference_taken': True }, status=status.HTTP_400_BAD_REQUEST)
            
            
            graveplot=GravePlot.objects.get_from_uuid(data.get('graveplot_id'))

            # create blank person record
            person = Person.objects.create()

            if reservation:
                # create reserved plot record
                state=ReservePlotState.objects.get(state='reserved')
                ReservedPlot.objects.create(person=person, grave_plot=graveplot, state=state)

                if 'layer' in data:
                    layer = data.get('layer')
                    # convert to reserved plot if neccessary
                    if layer=='available_plot':
                        graveplot.topopolygon.update_feature_code('reserved_plot')
                        graveplot.save()
            
            # populate blank person record
            self.update_person(person, data, request.user)

            return JsonResponse({ 'person_id': person.id, 'topopolygon_id': graveplot.topopolygon_id}, safe=False)

        except Exception as e:
            print(traceback.format_exc())
            return HttpResponseBadRequest(str(e))
    
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def put(self, request, filename, format=None):
        file_obj = request.data['file']

        if "file" in file_obj and file_obj.get("file") == None or file_obj.get('file') == 'null':
            Person.file.save(file_obj.title, file_obj, save=True)

        return Response(status=status.HTTP_201_CREATED)
    
    ''' used for deleting a person record '''
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def delete(self, request):

        try:
            if not 'person_id' in request.GET:
                raise ValidationError("Person ID not specified")
            
            person = Person.objects.get(id=request.GET.get('person_id'))

            if person.reservedplot:
                # Don't delete record. Change reservedplot state to 'deleted'
                person.reservedplot.state = ReservePlotState.objects.get(state='deleted')

                if 'notes' in request.GET:
                    person.reservedplot.notes = request.GET['notes']

                person.reservedplot.save()
            else:
                # actually delete the person
                person.delete()

            available_plot = False
            topopolygon_id = None

            if 'graveplot_id' in request.GET:

                graveplot = GravePlot.objects.get_from_uuid(request.GET.get('graveplot_id'))
                topopolygon_id = graveplot.topopolygon.id
                available_plot = graveplot.update_plot_layer()=='available_plot'

            return JsonResponse({ 'available_plot': available_plot, 'topopolygon_id': topopolygon_id }, safe=False, status=200)

        except Exception as e:
            print(e)
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

class ConvertReservationToBurialView(APIView):
    
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def post(self, request):

        data=request.data

        try:
            if not 'graveplot_id' in data:
                raise ValidationError("Graveplot not specified")

            if not 'person_id' in data:
                raise ValidationError("Reservation person not specified")

            if not 'burial_day' in data or  not 'burial_month' in data or  not 'burial_year' in data:
                raise ValidationError("Burial date not specified")

            # get person record and make sure it has a linked death record
            person = Person.objects.get(id=data.get('person_id'))

            if not person.get_death():
                Death.objects.create(person=person)
            
            # get graveplot
            graveplot = GravePlot.objects.get_from_uuid(data.get('graveplot_id'))
            
            # create burial
            burial = Burial.objects.create(graveplot=graveplot, death_id=person.id, impossible_date_day=data['burial_day'], impossible_date_month=data['burial_month'], impossible_date_year=data['burial_year'])

            # add burial to any selected memorials
            if 'selected_memorials' in data:
                death = person.death

                for memorial_id in data['selected_memorials']:
                    death.add_memorial(Memorial.objects.get(uuid=memorial_id))
                
                death.save()

            # change reservedplot state to 'buried'
            reserved_plot = ReservedPlot.objects.get(person=person)
            reserved_plot.state = ReservePlotState.objects.get(state='buried')
            reserved_plot.save()

            if 'layer' in data:
                layer = data.get('layer')
                # convert to regular plot if neccessary
                if layer in ['available_plot', 'reserved_plot']:
                    graveplot.topopolygon.update_feature_code('plot')
                    graveplot.save()

            return JsonResponse({ 'person_id': person.id, 'burial_id': burial.id, 'topopolygon_id': graveplot.topopolygon.id }, safe=False)

        except Exception as e:
            print(e)
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        

class BurialInformationView(APIView):

    def get(self, request):

        burial_id = request.GET.get('burial_id')

        if not burial_id:
            burial = Burial()
        else:
            burial = Burial.objects.select_related("graveplot").get(id=burial_id)

        if burial:
            serializer = BurialInformationSerializer(instance=burial)
            return JsonResponse(serializer.data, safe=False)
        else:
            return HttpResponseBadRequest("Burial does not exist")
    
    ''' used for deleting a burial record '''
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def delete(self, request):

        burial_id = request.GET.get('burial_id')

        if not burial_id:
            return HttpResponseBadRequest("Burial ID not specified")
        
        burial = Burial.objects.get(id=burial_id)

        if burial:
            burial.delete()
        else:
            return HttpResponseBadRequest("Burial not found")

        return HttpResponse(status=204)

class BurialDetailsView(APIView):

    permission_classes = [IsAuthenticatedOrPublicAccessReadOnly]

    def update_burial(self, burial, data, user):

        save_image = False
        burial_record_image = {}

        # Extract the register from Image Name
        if 'burial_record_image' in data:
            if data["burial_record_image"] is not None and "image_name" in data["burial_record_image"]:
                image_name = data["burial_record_image"]["image_name"]
                del data["burial_record_image"]["image_name"]
                if len(image_name.split("_")) > 1:
                    try:
                        data["register"] = image_name.split("_")[1]
                    except:
                        raise ValidationError("Image Name is Improperly Configured")
                else:
                    data["register"] = None

        if 'burial_record_image' in data:
            # don't process this field in serializer. Hence remove it from data object.
            burial_record_image = data['burial_record_image']
            del data['burial_record_image']
            save_image = True

        serializer = BurialDetailsSerializer(burial, data=data, partial=True, context={'user': user})
            
        if serializer.is_valid():

            serializer.save()

            burial = Burial.objects.get(id=data.get('id'))

            if save_image:
                if not burial_record_image:
                    # delete image
                    burial.burial_record_image = None
                elif 'thumbnail_url' in burial_record_image:
                    # add/replace image
                    image = burial_record_image['thumbnail_url'].replace("data:image/jpeg;base64,", "")
                    if image is not None:
                        burial.create_image(Image.base64_to_image(image))

                burial.save()

            return serializer.data
        else:
            raise ValidationError(serializer.errors)

    def get(self, request):

        burial_id = request.GET.get('burial_id')

        try:
            if not burial_id or burial_id == 'null':
                # create new burial
                burial = Burial()
            else:
                burial = Burial.objects.prefetch_related("burial_officials").get(id=burial_id)

            if burial:
                fields = PersonField.objects.filter(field_form='BurialDetails')
                form_serializer = PersonFieldSerializer(fields, many=True)
                serializer = BurialDetailsSerializer(instance=burial, context={'user': request.user})
                return_data = dict(serializer.data, **{'form_fields': form_serializer.data})
                return JsonResponse(return_data, safe=False)
        except Exception as e:
            return HttpResponseBadRequest("Burial does not exist: " + str(e))
    
    ''' used for updating a existing burial record '''
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def patch(self, request):

        data=request.data

        if not data.get('id'):
            return HttpResponseBadRequest("Burial not specified")

        burial = Burial.objects.get(id=data.get('id'))

        if burial:
            try:
                return Response(self.update_burial(burial, data, request.user))

            except Exception as e:
                return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponseBadRequest("Burial does not exist")


class AllBurialOptionsView(PublicAccessOrViewOnlyView):

    def get(self, request):

        burial_officials = Official.objects.extra(select={'date_is_null': 'used_on IS NULL'},order_by=['date_is_null','-used_on'])

        grouped_burial_officials = [
            { 'group': 'Recently used', 'list': [] },
            { 'group': 'Other', 'list': [] } ]

        top_three = []

        # remove most recently used
        count = 0
        loop_length = min(3,len(burial_officials))
        while count < loop_length:
            top_three.append(burial_officials[0])
            burial_officials = burial_officials.exclude(id=burial_officials[0].id)
            count += 1
        
        burial_officials = burial_officials.order_by('last_name')

        # add officials into two groups
        for bo in top_three:
            grouped_burial_officials[0]['list'].append({ 'id':str(bo.id), 'label': '{0}, {1} ({2})'.format(bo.last_name,bo.first_names, bo.title), 'title': bo.title, 'first_names': bo.first_names, 'last_name': bo.last_name })

        for bo in burial_officials:
            grouped_burial_officials[1]['list'].append({ 'id':str(bo.id), 'label': '{0}, {1} ({2})'.format(bo.last_name,bo.first_names, bo.title), 'title': bo.title, 'first_names': bo.first_names, 'last_name': bo.last_name })
    
        return JsonResponse({
            'burial_official_list' : list(grouped_burial_officials),
            'burial_official_type': list(BurialOfficialType.objects.all().values('id', 'official_type').order_by('official_type'))
            }, safe=False)
    
class MoveBurialPersonRecordsView(APIView):
    
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    @transaction.atomic
    def post(self, request):
        
        burial = None
        burial_id = request.data.get('burial_id')
        person_id = request.data.get('person_id')
        remove_from_original = request.data.get('removeFromOriginal')
        from_graveplot_uuid = request.data.get('from_graveplot_uuid')
        from_memorial_uuid = request.data.get('from_memorial_uuid')
        to_grave_id = request.data.get('to_grave_id')
        to_available_plot_id = request.data.get('to_available_plot_id')
        to_feature_id = request.data.get('to_feature_id')

        layer = False
        graveplot = None

        if burial_id:
            burial = Burial.objects.get(id=burial_id)

        if person_id:
            death = Death.objects.get(person_id=person_id)
        
        # Burials can be linked to only one graveplot. 
        # Hence, to move graveplots, either the burial is not linked to any grave, 
        # or we have permission to remove burial from current linked grave.
        try:
            if (to_grave_id or to_available_plot_id) and burial and (remove_from_original or not from_graveplot_uuid):
                try:
                    if to_grave_id:
                        graveplot = GravePlot.objects.get(uuid=to_grave_id)
                    else:
                        # this is an available plot
                        graveplot,created = GravePlot.objects.select_related('topopolygon').get_or_create(topopolygon_id=to_available_plot_id)
                        graveplot.topopolygon.update_feature_code('plot')
                        graveplot.save()
                except Exception as e:
                    return HttpResponseBadRequest("Graveplot not found")

                burial.graveplot = graveplot
                burial.save()
                    
                # change to plot if required
                graveplot.update_plot_layer()

                # remove from memorial
                if from_memorial_uuid and death:
                    memorial_old = Memorial.objects.get(uuid=from_memorial_uuid)
                    death.remove_memorial(memorial_old)

                # remove from memorials linked to old graveplot
                if from_graveplot_uuid and death:
                    grave_old = GravePlot.objects.get(uuid=from_graveplot_uuid)
                    memorial_graveplots = MemorialGraveplot.objects.select_related('memorial').filter(graveplot=grave_old)

                    for memorial_graveplot in memorial_graveplots:
                        death.remove_memorial(memorial_graveplot.memorial)
                    
                    # change to available plot if required
                    layer = grave_old.update_plot_layer()

                # add memorials linked to new graveplot
                if death:
                    memorial_graveplots = MemorialGraveplot.objects.select_related('memorial').filter(graveplot=graveplot)

                    for memorial_graveplot in memorial_graveplots:
                        death.add_memorial(memorial_graveplot.memorial)

        except Exception as e:
            print("Error moving burial: " + str(e))
            return HttpResponseBadRequest("Error moving burial: " + str(e))

        # Persons can be linked to multiple memorials.
        try:
            if to_feature_id and death:
                memorial = Memorial.objects.get(feature_id=to_feature_id)
                death.add_memorial(memorial)

                if remove_from_original:
                    if from_memorial_uuid:
                        memorial_old = Memorial.objects.get(uuid=from_memorial_uuid)
                        death.remove_memorial(memorial_old)
                    elif from_graveplot_uuid:
                        grave_old = GravePlot.objects.get(uuid=from_graveplot_uuid)
                        memorial_graveplots = MemorialGraveplot.objects.select_related('memorial').filter(graveplot=grave_old)

                        for memorial_graveplot in memorial_graveplots:
                            death.remove_memorial(memorial_graveplot.memorial)

                    if burial:
                        # Add first grave that is linked to memorial to burial. This could be unwanted!
                        memorial_graveplots = MemorialGraveplot.objects.filter(memorial=memorial)
                        burial.graveplot_id = memorial_graveplots[0].graveplot_id
                        burial.save()
            
            death.save()
        except Exception as e:
            return HttpResponseBadRequest("Error moving memorial: " + str(e))

        if graveplot:
            response = { 'graveplot_uuid': graveplot.uuid }
            if layer and grave_old:
                response['layer'] = layer
                response['topopolygon_id'] = grave_old.topopolygon_id
            return JsonResponse(response, safe=False) 
        else:
            return HttpResponse(status=204)
    
class RemoveBurialPersonRecordsView(APIView):
    
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def post(self, request):

        burial_id = request.data.get('burial_id')
        person_id = request.data.get('person_id')
        memorial_uuid = request.data.get('memorial_uuid')

        layer = None

        try:
            # remove from grave
            if burial_id:
                burial = Burial.objects.get(id=burial_id)
                grave_old = burial.graveplot
                
                burial.graveplot = None
                burial.save()
                
                # change to available plot if required
                layer = grave_old.update_plot_layer()

        except Exception as e:
            print("Error removing from memorial: " + str(e))
            return HttpResponseBadRequest("Error removing from memorial: " + str(e))
        
        try:
            # remove from memorial
            if person_id and memorial_uuid:
                death = Death.objects.get(person_id=person_id)
                memorial_old = Memorial.objects.get(uuid=memorial_uuid)
                death.remove_memorial(memorial_old)
                death.save()
        except Exception as e:
            return HttpResponseBadRequest("Error removing from memorial: " + str(e))

        if layer and grave_old:
            return JsonResponse({ 'layer': layer, 'topopolygon_id': grave_old.topopolygon_id }, safe=False) 
        return HttpResponse(status=204)
    
class DeleteBurialPersonRecordsView(APIView):
    
    @method_decorator(group_required('SiteAdmin', raise_exception=True,))
    @transaction.atomic
    def delete(self, request):

        burial_id = request.GET.get('burial_id')
        person_id = request.GET.get('person_id')

        layer = None
        graveplot_uuid = None
        topopolygon_id = None

        try:
            if burial_id:
                burial = Burial.objects.get(id=burial_id)
                burial.delete()
                
                if burial.graveplot:
                    layer = burial.graveplot.update_plot_layer()
                    graveplot_uuid = burial.graveplot.uuid
                    topopolygon_id = burial.graveplot.topopolygon.id
        except Exception as e:
            print("Error deleting burial: " + str(e))
            return HttpResponseBadRequest("Error deleting burial: " + str(e))
        
        try:
            if person_id:
                Person.objects.get(id=person_id).delete()
        except Exception as e:
            return HttpResponseBadRequest("Error deleting person: " + str(e))

        return JsonResponse({ 'layer': layer, 'graveplot_id': graveplot_uuid, 'topopolygon_id': topopolygon_id }, safe=False, status=200)

class PublicPersonCompanySearchView(APIView):

    def get(self, request):

        data = request.GET
        results = []

        if 'first_names' in data or 'last_name' in data:
            results = PublicPerson.objects.search_persons(first_names=data.get('first_names'), last_name=data.get('last_name'))
        
        if 'name' in data:
            results += PublicCompany.objects.search_companies(name=data.get('name'))
        
        return JsonResponse(list(results), safe=False)


def getFeatureAttributes(requestGet):

    if not 'feature_id' in requestGet and not 'graveplot_id' in requestGet and not 'memorial_id' in requestGet:
        raise ValidationError("Feature ID not specified")
        
    feature = None
    feature_type = None
    attributes = None
    public_attributes = None

    if 'feature_id' in requestGet:
        # the feature could be a TopoPolygons, TopoPolylines or TopoPoints
        try:
            feature = TopoPolygons.objects.get(id=requestGet.get('feature_id', False))
            feature_type = 'topopolygons'
        except:
            try:
                feature = TopoPolylines.objects.get(id=requestGet.get('feature_id', False))
                feature_type = 'topopolylines'
            except:
                try:
                    feature = TopoPoints.objects.get(id=requestGet.get('feature_id', False))
                    feature_type = 'topopoints'
                except:
                    raise ValidationError("Feature does not exist")
        
    elif 'graveplot_id' in requestGet:
        feature = GravePlot.objects.get_from_uuid(requestGet.get('graveplot_id')).topopolygon
        feature_type = 'topopolygons'
        
    elif 'memorial_id' in requestGet:
        feature = Memorial.objects.get_from_uuid(requestGet.get('memorial_id')).topopolygon
        feature_type = 'topopolygons'
    
    # not all graves/memorials have features
    if feature:
        public_attributes = feature.layer.feature_code.public_attributes.all()
        attributes = feature.layer.feature_code.attributes.all()

    return [feature, feature_type, public_attributes, attributes]

class FeatureAttributesView(APIView):

    def getAttributeDetails(self, attribute, feature_type, feature, public):

        attribute_details = { 
            'attribute_id': attribute.id,
            'label': attribute.name,
            'field_name': attribute.type.name,
            'field_type': attribute.type.type_name }

        if attribute.type.name == 'select':
            attribute_details['select_options'] = attribute.options
        
        attribute_model = 'public_attribute' if public else 'schema_attribute'

        # find an existing value for this attribute
        feature_attributes = FeatureAttributes.objects.filter(**{ attribute_model: attribute, feature_type + '__in': [feature] })

        if feature_attributes and len(feature_attributes) > 0:
            attribute_details['feature_attribute_id'] = feature_attributes[0].id
            attribute_details['value'] = getattr(feature_attributes[0], attribute.type.type_name + '_value')

            if attribute.type.type_name=='date':
                ''' split date into seperate parts '''
                attribute_details['day'] = feature_attributes[0].date_value.day if feature_attributes[0].date_value else None
                attribute_details['month'] = feature_attributes[0].date_value.month if feature_attributes[0].date_value else None
                attribute_details['year'] = feature_attributes[0].date_value.year if feature_attributes[0].date_value else None
                
        else:
            attribute_details['feature_attribute_id'] = None
            attribute_details['value'] = None

            if attribute.type.type_name=='date':
                ''' split date into seperate parts '''
                attribute_details['day'] = None
                attribute_details['month'] = None
                attribute_details['year'] = None
        
        if public:
            attribute_details['public'] = True
        else:
            attribute_details['public'] = False
        
        return attribute_details

    def get(self, request):
        """Returns a json object containing all the attributes for a feature:
            -feature_attribute_id: the feature_attributes id
            -attribute_id: the attribute's id
            -label: the attribute's label to be shown in form
            -type: the attribute type - boolean, char, float or integer 
            -value: the value of the attribute """
        
        try:
            feature, feature_type, public_attributes, schema_attributes = getFeatureAttributes(request.GET)

            attribute_list = []

            # add public attributes to list
            for attribute in public_attributes:
                attribute_list.append(self.getAttributeDetails(attribute, feature_type, feature, True))

            # add schema attributes to list
            for attribute in schema_attributes:
                attribute_list.append(self.getAttributeDetails(attribute, feature_type, feature, False))

        except Exception as e:
            print(traceback.format_exc())
            return HttpResponseBadRequest(str(e))

        return JsonResponse({'attributes': list(attribute_list)}, safe=False)

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def patch(self, request):

        data=request.data

        try:
            if not 'feature_id' in data and not 'graveplot_id' in data and not 'memorial_id' in data:
                raise ValidationError("Feature ID not specified")

            if not data.get('attributes'):
                raise ValidationError("Attributes not specified")
            
            attributes = data.get('attributes')

            for attribute in attributes:
                if attribute['feature_attribute_id']:
                    ''' Find existing feature attribute '''
                    feature_attribute = FeatureAttributes.objects.get(id=attribute['feature_attribute_id'])
                else:
                    ''' create a new feature attribute '''
                    if attribute['public']:
                        attribute_object = PublicAttribute.objects.get(id=attribute['attribute_id'])
                    else:
                        attribute_object = Attribute.objects.get(id=attribute['attribute_id'])
    
                    feature_attribute = FeatureAttributes.objects.create(attribute=attribute_object)

                    if 'feature_id' in data:
                        # the feature could be a TopoPolygons, TopoPolylines or TopoPoints
                        try:
                            feature = TopoPolygons.objects.get(id=data.get('feature_id', False))
                        except:
                            try:
                                feature = TopoPolylines.objects.get(id=data.get('feature_id', False))
                            except:
                                try:
                                    feature = TopoPoints.objects.get(id=data.get('feature_id', False))
                                except:
                                    raise ValidationError("Feature does not exist")
                
                    elif 'graveplot_id' in data:
                        feature = GravePlot.objects.get_from_uuid(data.get('graveplot_id')).topopolygon
                        
                    elif 'memorial_id' in data:
                        feature = Memorial.objects.get_from_uuid(data.get('memorial_id')).topopolygon

                    feature.feature_attributes.add(feature_attribute)
                
                # set feature attribute value
                setattr(feature_attribute, attribute['field_type'] + '_value', attribute['value'])
                feature_attribute.save()

            return HttpResponse(status=204)
    
        except Exception as e:
            print(traceback.format_exc())
            return HttpResponseBadRequest(str(e))

class FeatureAttributesExistView(APIView):

    def get(self, request):
        
        feature, feature_type, public_attributes, schema_attributes = getFeatureAttributes(request.GET)

        attributes_found = False

        if (public_attributes and len(public_attributes) > 0) or (schema_attributes and len(schema_attributes) > 0):
            attributes_found = True
        
        return JsonResponse({'attributesFound': attributes_found}, safe=False)

class UnlinkedBurialsWithTranscribedGraveNumberView(APIView):

    @method_decorator(group_required('SiteAdmin', 'SiteWarden', raise_exception=True,))
    def get(self, request, grave_number):
        """
        Gets burials not linked to a graveplot and with given grave number.
        """

        try:
            graveplot_burial_distinct_list = Burial.objects.get_unlinked_burials_with_transcribed_grave_number(grave_number)
            return JsonResponse({ 'graveplot_burial_distinct_list': graveplot_burial_distinct_list }, safe=False)

        except ValidationError as e:
            print(e)
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

class BurialNumberView(APIView):
    """
    filter for only grave numbers
    """
    permission_classes = [IsAuthenticatedOrPublicAccessReadOnly]
    def get(self, request):
        """ Search for graveplots with a graveref and get list of graveplot id and their graveref """
        serializer = BurialNumberSerializer(Burial.objects.all(),many=True)
        my_data = json.loads(json.dumps(serializer.data))
        new_data = {}
        for memorial in my_data:  
            if 'burial_number' in memorial and 'id' in memorial and memorial['id'] is not None: 
                new_data[memorial['id'] + ''] = memorial['burial_number']
            elif 'burial_number' in memorial and 'topopolygon_id' in memorial and memorial['topopolygon_id'] is not  None:
                    new_data[memorial['topopolygon_id'] + ''] = memorial['burial_number']
        return JsonResponse(json.dumps(new_data), safe=False)

       