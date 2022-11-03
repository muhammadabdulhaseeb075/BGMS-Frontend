from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from bgsite.views import AuthenticatedView, DataMatchView, AjaxableResponseMixin, ViewOnlyView, group_required, WardenView
from datamatching.forms import BurialOfficialForm, SearchForm, MemorialForm, MatchingForm, DeathPersonForm, BurialForm
from bgsite.models import Memorial, GravePlot, Person, MemorialInscriptionDetail, create_date
from django.db import transaction
from django.core import serializers
from django.forms.formsets import formset_factory
from geometries.models import TopoPolygons
from geometriespublic.models import FeatureCode
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from _datetime import date
from django.views.generic.base import TemplateView
from datamatching.models import DataMatchingUser, DataMatchingMemorial, MemorialHistory, MemorialState
from main.models import ImageState, BurialGroundSite
from datetime import datetime
from django.conf import settings
import bleach
import json
from uuid import UUID
from django.template.loader import render_to_string

from datamatching.serializers import MemorialMatchSerializer, UserActivitySerializer, MemorialStateSerializer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class DataMatchingSearchView(AjaxableResponseMixin, FormView, ViewOnlyView):
    """
    It is call when the post request searchPerson/ is executed.
    This request needs to be from an ajax request.

    When datamatching.forms.SearchForm form is valid, the search is processed and
    returns the template mapmanagement/search-form.html in success.

    When the form is invalid, it returns Form invalid.
    """
    template_name = 'datamatching/search-form.html'
    success_template_name = 'datamatching/search-results.html'
    # success url is not used (due to ajax mixin), but can't be removed because
    # django throws error if it is not there
    success_url = '/datamatching'
    form_class = SearchForm

    class UUIDEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, UUID):
                # if the obj is uuid, we simply return the value of uuid
                return obj.hex
            return json.JSONEncoder.default(self, obj)

    def get_context_data(self, **kwargs):
        context = super(DataMatchingSearchView, self).get_context_data(**kwargs)
        context['action'] = 'person.submitSearchForm("/datamatching/searchPerson/",".search-form",".search-results-div","#searchForm")'
        context['mapSearch'] = False
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        mem_type = form.cleaned_data['memorial_types'] if form.cleaned_data['memorial_types'] != "" else None
        persons = Person.objects.search_persons(first_names=form.cleaned_data['first_names'], last_name=form.cleaned_data['last_name'], age=form.cleaned_data['age'], age_to=form.cleaned_data['age_to'],
            # death_date=form.cleaned_data['death_date'], death_date_to=form.cleaned_data['death_date_to'],
            burial_date=form.cleaned_data['burial_date'], burial_date_to=form.cleaned_data['burial_date_to'], fuzzy_value=form.cleaned_data['fuzzy_value'], memorial_type=mem_type, search_type='data_matching' )
        json_persons = bleach.clean(json.dumps(list(persons), cls=self.UUIDEncoder), strip=True, strip_comments=True, tags=[], attributes=[], styles=[])
        responseData = {'data':  render_to_string(self.success_template_name, context={'deathPerson': json_persons.replace('\'', '\\\'')})}
        return super(DataMatchingSearchView, self).form_valid(form, responseData)

    def form_invalid(self, form):
        print('invalid data')
        # return super(DataMatchingSearchView, self).form_invalid({'data': 'Form invalid.'})

class DataMatchingView(DataMatchView, TemplateView):
    search_form_class = SearchForm
    template_name = 'datamatching/matching.html'

    def get_context_data(self, **kwargs):
        context = super(DataMatchingView, self).get_context_data(**kwargs)
        siteDetails = BurialGroundSite.get_site_details()
        context['formSearch'] = self.search_form_class()
        context['SiteUrls'] = {'dataentry':'/dataentry/',
                              'datamatching':'/datamatching/',
                              'mapmanagement':'/mapmanagement/'
                              }
        context['SiteDetails'] = siteDetails
        return context


class MemorialDetailsView(APIView):
    def get(self,request):
        user = DataMatchingUser.objects.get(id=request.user.id)
        current_memorial = user.get_in_use_memorial()
        if not current_memorial:
            current_memorial = user.set_in_use_memorial()
        if current_memorial:
            serializer = MemorialMatchSerializer(Memorial.objects.prefetch_related('memorial_inscriptions').prefetch_related('memorial_deaths').get(id=current_memorial.memorial.id))
            return JsonResponse(serializer.data, safe=False)

class UnmatchedMemorialsCountView(AuthenticatedView):
    def get(self, request):

        memorials_left = Memorial.objects.filter(memorial_deaths__isnull=True).distinct().count()

        return JsonResponse({'memorials_left': memorials_left,}, status=200, content_type ='application/json')

class MemorialValidated(DataMatchView):
    def post(self, request):
        user = DataMatchingUser.objects.get(id=request.user.id)
        current_memorial_id = user.get_in_use_memorial_id()
        user.set_current_processed()
        dmmemorial = user.set_in_use_memorial(current_memorial_id)

        if dmmemorial:
            serializer = MemorialMatchSerializer(Memorial.objects.prefetch_related('memorial_inscriptions').prefetch_related('memorial_deaths').get(id=dmmemorial.memorial.id))
            return JsonResponse(serializer.data, safe=False)


class MemorialSkipped(DataMatchView):
    def post(self, request):
        user = DataMatchingUser.objects.get(id=request.user.id)
        current_memorial_id = user.get_in_use_memorial_id()
        user.set_skipped_memorial()
        dmmemorial = user.set_in_use_memorial(current_memorial_id)

        if dmmemorial:
            serializer = MemorialMatchSerializer(Memorial.objects.prefetch_related('memorial_inscriptions').prefetch_related('memorial_deaths').get(id=dmmemorial.memorial.id))
            return JsonResponse(serializer.data, safe=False)


class ChangeMemorial(APIView):
    def post(self, request):
        user = DataMatchingUser.objects.get(id=request.user.id)
        current_memorial_id = user.get_in_use_memorial_id()
        user.set_memorial_viewed()
        dmmemorial = user.set_in_use_memorial(current_memorial_id, request.data.get('forwardDirection'))

        if dmmemorial:
            serializer = MemorialMatchSerializer(Memorial.objects.prefetch_related('memorial_inscriptions').prefetch_related('memorial_deaths').get(id=dmmemorial.memorial.id))
            return JsonResponse(serializer.data, safe=False)


class ChangeToMemorialById(APIView):
    def post(self, request):

        dmmemorial = DataMatchingMemorial.objects.get(memorial_id=request.data.get('data_matching_memorial_id'))
        user = DataMatchingUser.objects.get(id=request.user.id)

        # find if memorial is being used by a different user
        memorial_in_use = MemorialHistory.objects.filter(memorial=dmmemorial, state_id=MemorialState.objects.get_in_use()).exclude(user=user)
        
        if not memorial_in_use:
            if dmmemorial:
                user.set_memorial_viewed()
                user.set_in_use_memorial(memorial=dmmemorial)
                return HttpResponse(status=200)
            else:
                raise 400
        else:
            return JsonResponse({'status': 'error', 'message': 'The memorial is currently in use by another user.'}, status=400)


class MemorialByImageSearch(DataMatchView):
    def get(self, request):
        dmuser = DataMatchingUser.objects.get(id=request.user.id)
        # dmuser = request.user.datamatchinguser
        image_name = request.GET.get('image_search').strip()
        if image_name:
            if not image_name.lower().endswith('.jpg'):
                image_name = image_name+'.jpg'
            with transaction.atomic():
                searched_memorials = DataMatchingMemorial.objects.filter(memorial__images__url__icontains=image_name)

                if searched_memorials.count() > 0:
                    searchedmemorial = searched_memorials[0] #TODO: handle multiple results, support for the moment to just unique names
                    # change in_use current MemorialHistory to "viewed" and set in_use for the one just found
                    # change to unprocessed current DataMatchingMemorial from processign, and change to processing the one just found.
                    memorialhistory = MemorialHistory.objects.get(user_id=dmuser.id, state_id=MemorialState.objects.get_in_use())

                    if memorialhistory:
                        memorialhistory.state = MemorialState.objects.get_viewed()
                        memorialhistory.memorial.state = ImageState.objects.get(image_state='unprocessed')
                        memorialhistory.time = datetime.now()
                        memorialhistory.save()
                    # import pdb; pdb.set_trace()
                    searchedmemorialshistory = MemorialHistory.objects.filter(user=dmuser, memorial=searchedmemorial)
                    if searchedmemorialshistory.count() > 0:
                        searchedmemorialhistory = searchedmemorialshistory[0]
                        searchedmemorialhistory.state = MemorialState.objects.get_in_use()
                        searchedmemorialhistory.time = datetime.now()
                        searchedmemorialhistory.save()
                    else:
                        MemorialHistory.objects.update_or_create(user=dmuser, state=MemorialState.objects.get_in_use(), memorial=searchedmemorial)
                    searchedmemorial.memorial.state = ImageState.objects.get(image_state='processing')
                    searchedmemorial.save()

        return HttpResponse(status=200)


class BreakLink(APIView):
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def post(self, request):
        person_id = request.data.get('personId')
        memorial_id = request.data.get('memorialId')
        with transaction.atomic():
            person = Person.objects.get(id=person_id)
            memorial = Memorial.objects.get(id=memorial_id)
            person.death.memorials.remove(memorial)
            if memorial.graveplot_memorials.count() >= 1 and person.death.death_burials.count() >= 1:
                for linkedGravePlot in memorial.graveplot_memorials.all():
                    for burialTobeRemoved in person.death.death_burials.all():
                        if burialTobeRemoved in linkedGravePlot.burials.all():
                            linkedGravePlot.burials.remove(burialTobeRemoved)
        return HttpResponse(status=200)


# class MarkNameAsRevisit(DataMatchView):
#     def post(self, request):
#         user = request.user
#         grave_person_id = request.POST.get('gravePersonId')
#         memorial_id = request.POST.get('memorialId')
#         with transaction.atomic():
#             grave_person = GraveNames.objects.get(id=grave_person_id)
#             grave_person.revisit = True
#             grave_person.save()
#         return HttpResponseRedirect('/datamatching')

class LinkPersonMemorialView(APIView):
    def post(self,request):
        memorial_id = request.data.get('memorialId')
        person_id = request.data.get('personId')
        person = Person.objects.get(id=person_id)
        memorial = Memorial.objects.get(id=memorial_id)
        person.add_memorial(memorial)
        return HttpResponse(status=200)

class AddNewPersonView(DataMatchView):
    def post(self, request):
        first_name = request.POST.get('personFirstName')
        last_name = request.POST.get('personLastName')
        year_of_death = request.POST.get('personYearOfDeath')
        memorial_id = request.POST.get('memorialId')
        person = Person.objects.create(first_names=first_name, last_name=last_name)
        person.add_death_details(death_year=year_of_death)
        person.add_memorial(Memorial.objects.get(id=memorial_id))
        return HttpResponseRedirect('/datamatching')

class AddPersonView(ViewOnlyView):
    """
    GET request: Display datamatching/person_modal.html returning person_form
                 This person_modal is to create a new Person.
    """
    person_form_class = DeathPersonForm

    def get(self, request):
        # context for the template
        person_form = DeathPersonForm()
        return render(request, 'datamatching/person_modal.html', {'DeathPersonForm': person_form})

class GetUserActivityView(APIView): 

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))   
    def get(self, request):

        memorial_history = MemorialHistory.objects.select_related('user').select_related('memorial').all().order_by('-time')
        serializer = UserActivitySerializer(memorial_history, many=True)
        return JsonResponse(serializer.data, safe=False)

class GetMemorialStateView(APIView): 

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))   
    def get(self, request):

        memorial_history = DataMatchingMemorial.objects.select_related('state').select_related('memorial').all()
        #memorials = Memorial.objects.select_related('data_matching').all()
        serializer = MemorialStateSerializer(memorial_history, many=True)
        return JsonResponse(serializer.data, safe=False)

class DeathPersonDetailsView(ViewOnlyView):
    """
    GET request: Display datamatching/deathpersonmodal.html returning multiple forms within the response.
                 The forms returned are person_form, memorial_form, burial_form, memorial_images and burial_image
                 All the forms contain the whole information related to a Death person.

                 In case the request is executed without an ID for the user, It means a new Person will be created,
                 therefore the forms will be return as a new instance empty.

    POST request: Three forms are requested in POST: DeathPersonForm, MemorialForm, BurialForm.
                  If the DeathPersonFomr.id_person is empty, then it would create a new Person and add all its details
                  into database. In case the id_person is not empty, It will modify the current Person selected.
                  In case a form is invalid, it will return 500 bad request.

    """
    person_form_class = DeathPersonForm
    memorial_form_class = MemorialForm
    burial_form_class = BurialForm

    def get(self, request):
        # context for the template
        id = request.GET.get('id')
        memorial_id = request.GET.get('memorialId')
        unknown_grave = request.GET.get('unknown')
        person_form = None
        burial_form = None
        burial_image = None
        BurialOfficialSet = None
        burial_official_formset = None
        MemorialSet = None
        memorial_formset = None

        if id is not None: #edit person
            person = Person.objects.get(id=id)
            person_details = person.get_all_details()
            person_form = DeathPersonForm().createDeathPersonForm(person_details)
            memorials = person.get_memorials()
            memorial_forms = []

            if memorials:
                MemorialSet = formset_factory(MemorialForm, extra = 0)
                for memorial in memorials:
                    # import pdb; pdb.set_trace()
                    memorial_details = memorial.get_all_details()
                    memorial_details['person_id'] = id
                    memorial_forms.append(memorial_details)
                memorial_formset = MemorialSet(initial=memorial_forms,prefix='memorial')
                # import pdb; pdb.set_trace()
            else:
                MemorialSet = formset_factory(MemorialForm, extra = 1)
                memorial_formset = MemorialSet(initial=[],prefix='memorial')

            burials = person.get_burials()
            burial_forms = []
            if burials:
                for burial in burials:  #TODO: Add support for multiple burial officials when multiple burials will be implemented
                    burial_details = burial.get_all_details()
                    burial_official_list = burial.get_burial_officials_setlist()
                    # import pdb; pdb.set_trace()
                    if not burial_official_list:
                        BurialOfficialSet = formset_factory(BurialOfficialForm, extra=1, can_delete=True)
                    else:
                        BurialOfficialSet = formset_factory(BurialOfficialForm, extra=0, can_delete=True)
                    burial_official_formset = BurialOfficialSet(initial=burial_official_list, prefix='burialOfficial')
                    burial_details['person_id'] = id
                    burial_forms.append(BurialForm().createBurialForm(burial_details))
            else:
                BurialOfficialSet = formset_factory(BurialOfficialForm, extra=1, can_delete=True)
                burial_official_formset = BurialOfficialSet(initial=[],prefix='burialOfficial')

            if len(burial_forms) > 0:
                burial_form = burial_forms[0]
                burial_image = burials[0].get_image_url()
            else:
                burial_form = BurialForm({'person_id':id})
        elif memorial_id is not None and memorial_id != '': #Click on memorial
            memorial = Memorial.objects.get_from_uuid(memorial_id)
            #TODO: check this scenario
            MemorialSet = formset_factory(MemorialForm, extra = 0)
            memorial_details = memorial.get_all_details()
            memorial_details['person_id'] = None
            memorial_formset = MemorialSet(initial=[memorial_details],prefix='memorial')

            if unknown_grave is not None and unknown_grave:
                unknown_grave = True

            person_form = DeathPersonForm()
            burial_form = BurialForm()
            burial_image = ''
            BurialOfficialSet = formset_factory(BurialOfficialForm, extra=1, can_delete=True)
            burial_official_formset = BurialOfficialSet(initial=[],prefix='burialOfficial')
        else: #new person
            person_form = DeathPersonForm()
            burial_form = BurialForm()
            burial_image = ''
            MemorialSet = formset_factory(MemorialForm, extra = 1)
            memorial_formset = MemorialSet(initial=[],prefix='memorial')
            BurialOfficialSet = formset_factory(BurialOfficialForm, extra=1, can_delete=True)
            burial_official_formset = BurialOfficialSet(initial=[],prefix='burialOfficial')
        return render(request, 'datamatching/deathpersonmodal.html',
                      {'DeathPersonForm': person_form, 'MemorialForm': memorial_formset, 'BurialForm': burial_form,
                       'burial_official_formset': burial_official_formset, 'burial_image': burial_image, 'unknown_grave': unknown_grave})


class PersonEditView(AjaxableResponseMixin, FormView, WardenView):
    template_name = 'mapmanagement/edit/person-edit.html'
    success_template_name = 'mapmanagement/edit/person-edit.html'
    # success url is not used (due to ajax mixin), but can't be removed because
    # django throws error if it is not there
    success_url = '/mapmanagement'
    form_class = DeathPersonForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        person_data = form.cleaned_data
        flag_new_person = False
        if person_data['id_person']:
            person = Person.objects.get(id=person_data['id_person'])
        else:
            person = Person()
            flag_new_person = True

        person.add_person_data(person_data)

        if person_data['graveplot_polygon_feature'] and person_data['graveplot_polygon_feature'] != '' and flag_new_person:

            feature_json = json.loads(person_data['graveplot_polygon_feature'])
            buried_person = person.bury_person(feature_json)
            memodial_ids = []
            memodial_ids.append(str(buried_person['graveplot'].get_uuid()))

            # get ids of any memorials linked to this plot
            if buried_person['feature_dict']['properties']['layer'] in ['plot', 'available_plot', 'reserved_plot']:
                for memorial in buried_person['graveplot'].memorials.all():
                    memodial_ids.append(str(memorial.get_uuid()))
            # get ids of any graveplots linked to this memorial
            else:
                for graveplot in buried_person['graveplot'].graveplot_memorials.all():
                    memodial_ids.append(str(graveplot.get_uuid()))

            person_feature = {'id':person.id, 'memorial_id':memodial_ids, 'first_names': person.first_names, 'last_name':person.last_name, 'burial_date':None, 'age_years':person.death.age_years, 'age_months': person.death.age_months, 'age_weeks': person.death.age_weeks, 'age_days': person.death.age_days, 'age_hours':person.death.age_hours, 'age_minutes':person.death.age_minutes}

            responseData = {'status': 'ok', 'old_plot_id': str(buried_person['feature_dict']['id']), 'old_layer': buried_person['feature_dict']['properties']['marker_type'], 'person_feature': person_feature}
        else:
            responseData = {"status":"ok", 'person_feature':{'id':person.id, 'first_names': person.first_names, 'last_name':person.last_name, 'age_years':person.death.age_years, 'age_months': person.death.age_months, 'age_weeks': person.death.age_weeks, 'age_days': person.death.age_days, 'age_hours':person.death.age_hours, 'age_minutes':person.death.age_minutes}}
        return super(PersonEditView, self).form_valid(form, responseData)


class BurialRecordEditView(AjaxableResponseMixin, WardenView):
    template_name = 'datamatching/memorial-edit.html'
    success_template_name = 'datamatching/memorial-edit.html'
    # success url is not used (due to ajax mixin), but can't be removed because
    # django throws error if it is not there
    success_url = '/mapmanagement'
    burial_form_class = BurialForm
    burialOfficials_formset_class = formset_factory(BurialOfficialForm)

    def post(self, request):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # person_form = self.person_form_class(request.POST)
        # memorial_form = self.memorial_form_class(request.POST)
        burial_form = self.burial_form_class(request.POST)
        burialOfficials_formset = self.burialOfficials_formset_class(request.POST, prefix='burialOfficial')

        if burial_form.is_valid() and burialOfficials_formset.is_valid():
            burial_data = burial_form.cleaned_data
            burialOfficials_data = burialOfficials_formset.cleaned_data
            # import pdb; pdb.set_trace()
            person = Person.objects.get(id=burial_data['person_id'])
            memorials = person.get_memorials()
            burial = None
            burials = person.get_burials()
            if burials.exists():
                burial = burials[0]
            else:
                burial = person.create_burial(burial_number=burial_data['burial_number'])
            # Handle impossible dates
            if burial.burial_date == None:
                burial.burial_date = create_date(day=burial_data['impossible_date_day'], month=burial_data['impossible_date_month'], year=burial_data['impossible_date_year'])
            #FIN: handle impossible dates
            # TODO: add support to mburial_date_formatted.ultiple burials
            burial.add_burial_details(grave_number=burial_data['grave_number'], burial_number=burial_data['burial_number'],
                                        section=burial_data['section'], subsection=burial_data['subsection'],         
                                        impossible_date_day=burial_data['impossible_date_day'],
                                        impossible_date_month=burial_data['impossible_date_month'], impossible_date_year=burial_data['impossible_date_year'],
                                        cremation_certificate_no=burial_data['cremation_certificate_no'], depth=burial_data['depth'],
                                        user_remarks=burial_data['user_remarks'], burial_remarks=burial_data['burial_remarks'], consecrated=burial_data['consecrated'],
                                        interred=burial_data['interred'], requires_investigation=burial_data['requires_investigation'], burial_officials = burialOfficials_data)
            #Upload burial record Image
            if len(request.FILES) != 0:
                try:
                    for key in request.FILES:
                        burialfilekey = key

                    burial.create_image(request.FILES[burialfilekey])
                except Exception as e:
                    return HttpResponseBadRequest(str(e))

            #get burial image url to attach it to the response data
            burial_image = burial.get_image_url()

            if burial_data['graveplot_polygon_feature']:
                feature_dict = json.loads(json.loads(burial_data['graveplot_polygon_feature']))
                feature_id = feature_dict['id']
                headpoint_string = feature_dict['properties']['headpoint']
                old_layer_name = feature_dict['properties']['layer']
                geometryGeoJSON = json.dumps(feature_dict['geometry'])
                burial_plot = None
                try:
                    burial_plot = TopoPolygons.objects.get(id=feature_id, layer__feature_code=FeatureCode.objects.get(feature_type='plot'))
                    graveplot = GravePlot.objects.get(plot_polygon=burial_plot)
                    burial.graveplot = graveplot
                except:
                    print('No graveplot associated with burial')
            responseData = {'status': 'ok', 'burial_image': burial_image, 'person_feature':{'id':person.id, 'first_names': person.first_names, 'last_name':person.last_name, 'burial_date':burial.burial_date, 'age_years':person.death.age_years, 'age_months': person.death.age_months, 'age_weeks': person.death.age_weeks, 'age_days': person.death.age_days, 'age_hours':person.death.age_hours, 'age_minutes':person.death.age_minutes}}
            return JsonResponse(responseData)
        return HttpResponseBadRequest(burial_form.errors)


class MemorialEditView(AjaxableResponseMixin, WardenView):
    template_name = 'datamatching/memorial-edit.html'
    success_template_name = 'datamatching/memorial-edit.html'
    # success url is not used (due to ajax mixin), but can't be removed because
    # django throws error if it is not there
    success_url = '/mapmanagement'
    formset_class = formset_factory(MemorialForm)

    def post(self, request):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        memorial_formset = self.formset_class(request.POST, prefix='memorial')
        # import pdb; pdb.set_trace()
        if memorial_formset.is_valid(): #TODO: when new memorial there is no memorial_id, but this will be move to another diferent post by clicking the plot
            try:
                memorials_data = memorial_formset.cleaned_data
                for key in request.FILES:
                    memorialpos = key.split('-')[1]
                    memorialfilekey = key
                memorial_data = memorials_data[int(memorialpos)]
                # import pdb; pdb.set_trace()
                memorial = Memorial.objects.get(id=memorial_data['memorial_id'])
                memorial.create_image(request.FILES[memorialfilekey])
                return JsonResponse({})
            except Exception as e:
                return HttpResponseBadRequest(str(e))
        return HttpResponseBadRequest(memorial_formset.errors)