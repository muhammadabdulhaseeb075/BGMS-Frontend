from django.shortcuts import render
from bgsite.views import AjaxableResponseMixin, DataEntryView as DataEntryPermission,\
    AdminView
from django.views.generic.edit import FormView
from main.models import BurialGroundSite
from dataentry.forms import CreateTemplateForm, AddBurialRecordForm,\
    BurialModelForm, PersonModelForm, DeathModelForm, AddressModelForm,\
    BurialOfficialForm, TagsForm, EditTemplateForm, GraveRefModelForm
from dataentry.serializers import TagGeoSerializer
from django.views.generic.base import TemplateView
from dataentry.models import Template, DataEntryUser, ImageHistory, Column,\
    BurialImage, UserState
from django.http.response import JsonResponse, HttpResponse
from django.core import serializers
from bgsite.models import Person, Burial, Tag, Burial_Official
import json
from django.middleware import csrf
from django.forms.formsets import formset_factory
from django.conf import settings
from django.db.models import Func
from geometries.utils import CRS

# Create your views here.


class DataEntryView(DataEntryPermission, TemplateView):
    template_name = 'dataentry/index.html'
    success_template_name = 'mapmanagement/edit/person-edit.html'
    success_url = '/mapmanagement'
    form_class = CreateTemplateForm    
    
    def get_context_data(self, **kwargs):
        kwargs = TemplateView.get_context_data(self, **kwargs)
        kwargs['SiteUrls'] = {'dataentry':'/dataentry/',
                              'datamatching':'/datamatching/',
                              'mapmanagement':'/mapmanagement/'                              
                              }
        kwargs['SiteDetails'] = BurialGroundSite.get_site_details()
        kwargs['GOOGLE_ANALYTICS_KEY'] = settings.GOOGLE_ANALYTICS_KEY
        return kwargs
    

class FinishedImageView(DataEntryPermission, TemplateView):
    template_name = 'dataentry/index.html'
    success_url = '/dataentry/#/addRecord'
    form_class = AddBurialRecordForm
    
    def post(self, request):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = DataEntryUser.objects.get(id=request.user.id)
        comments = request.POST.get('comments')
        book_name = request.POST.get('book_name')
        user.set_image_processed(comments=comments)
        image = user.set_current_image(book_name=book_name)
        if not image:
            user.set_current_image()
        return self.render_to_response({})
    

class SkipImageView(AjaxableResponseMixin, FormView, DataEntryPermission):
    template_name = 'dataentry/index.html'
    success_url = '/dataentry/#/addRecord'
    form_class = AddBurialRecordForm
    
    def post(self, request):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = DataEntryUser.objects.get(id=request.user.id)
        comments = request.POST.get('comments')
        book_name = request.POST.get('book_name')
        user.set_image_skipped(comments=comments)
        image = user.set_current_image(book_name=book_name)
        if not image:
            user.set_current_image()
        return self.render_to_response({})
    

class ChangeImageView(AjaxableResponseMixin, FormView, DataEntryPermission):
    template_name = 'dataentry/index.html'
    success_url = '/dataentry/#/addRecord'
    form_class = AddBurialRecordForm
    
    def post(self, request):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = DataEntryUser.objects.get(id=request.user.id)
        book_name = request.POST.get('book_name')
        user.set_image_viewed()
        user.set_current_image(book_name=book_name)
        return self.render_to_response({})


class NextImageView(AjaxableResponseMixin, FormView, DataEntryPermission):
    template_name = 'dataentry/index.html'
    success_url = '/dataentry/#/addRecord'
    form_class = AddBurialRecordForm
    
    def post(self, request):
        user = DataEntryUser.objects.get(id=request.user.id)
        book_name = request.POST.get('book_name')
        
        # Get the current image instance
        current = user.get_current_image()
        
        if current:
            instance = BurialImage.objects.all().filter(pk=current.pk)
            
            # Get all the unprocessed images
            images_in_book = BurialImage.objects.all_unprocessed(book_name=book_name)
            
            # Insert the current image in the unprocessed images
            join = (instance | images_in_book).order_by('-url')
            
            # Find the previous image
            nextImage = join.first()
            for index, item in enumerate(join):
                if item == current:
                    break
                else:
                    nextImage = item
            
            # Set the new image
            if nextImage != current:
                user.set_image_viewed()
                user.set_current_image(image=nextImage, book_name=book_name)
        else:
            # User doesn't have a current image
            image = user.set_current_image(book_name=book_name)
            if not image:
                user.set_current_image()
        
        return self.render_to_response({})


class PrevImageView(AjaxableResponseMixin, FormView, DataEntryPermission):
    template_name = 'dataentry/index.html'
    success_url = '/dataentry/#/addRecord'
    form_class = AddBurialRecordForm
        
    def post(self, request):
        user = DataEntryUser.objects.get(id=request.user.id)
        book_name = request.POST.get('book_name')
        
        # Get the current image instance
        current = user.get_current_image()
        instance = BurialImage.objects.all().filter(pk=current.pk)
        
        # Get all the unprocessed images
        images_in_book = BurialImage.objects.all_unprocessed(book_name=book_name)
        
        # Insert the current image in the unprocessed images
        join = (instance | images_in_book).order_by('url')
        
        # Find the previous image
        prevImage = join.first()
        for index, item in enumerate(join):
            if item == current:
                break
            else:
                prevImage = item
        
        # Set the new image
        if prevImage != current:
            user.set_image_viewed()
            user.set_current_image(image=prevImage, book_name=book_name)
        
        return self.render_to_response({})


class SaveImageCommentsView(AjaxableResponseMixin, FormView, DataEntryPermission):
    template_name = 'dataentry/index.html'
    success_url = '/dataentry/#/addRecord'
    form_class = AddBurialRecordForm
    
    def post(self, request):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = DataEntryUser.objects.get(id=request.user.id)
        comments = request.POST.get('comments')
        user.save_image_comments(comments=comments)
        return JsonResponse({'status': 'ok'})
    
class GetTemplateView(DataEntryPermission):    
    def get(self, request):
        # book_name of the received data
        template_id = request.GET.get('template_id')
        template = Template.objects.get(pk=template_id)
        book_name = template.book_name

        # book_name requested has template
        has_template = Template.objects.filter(book_name=book_name).exists()

        if has_template:
            return JsonResponse({"status": "ok", 'template': template.get_values()}, safe=False)
        else:
            return self.render_to_response({'message': 'Template not found'}, status=404)

class GetTemplateList(AdminView):    
    def get(self, request):
        templates = Template.objects.all_template_values()
        return JsonResponse({'templates': list(templates), 'csrfmiddlewaretoken':csrf.get_token(request)}, safe=False)
    
    
class DeleteTemplateView(AdminView):    
    def post(self, request):
        template_id = request.POST.get('template_id')
        Template.objects.filter(id=template_id).delete()
        return JsonResponse({"status": "success"})  


class CreateTemplateView(AjaxableResponseMixin, FormView, AdminView ):
    template_name = 'dataentry/json/base-form.json'
    success_url = '/mapmanagement'
    form_class = CreateTemplateForm
    content_type = 'application/json'
    
    def get(self, request):
        templates = Template.objects.all_template_values()
        return self.render_to_response({'templates': templates, 'form':self.get_form()})
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form_data = form.cleaned_data
        column_displaynames_dict = json.loads(form.data['column_displaynames'])
        template = Template.objects.create_template(name=form_data['name'], description=form_data['description'],
                    book_name=form_data['burial_image'], user=self.request.user, columns=form_data['columns'], column_displaynames=column_displaynames_dict)
        return JsonResponse({"status": "ok", "template_id":template.id})
    
    def form_invalid(self, form):
        print('invalid data')
        return JsonResponse(form.errors, status=400)
    

class EditTemplateView(AjaxableResponseMixin, FormView, AdminView ):
    template_name = 'dataentry/json/base-form.json'
    success_url = '/mapmanagement'
    form_class = EditTemplateForm
    content_type = 'application/json'
    
    def get(self, request, *args, **kwargs):
        template_id = request.GET.get('template_id')
        if template_id:
            template = Template.objects.filter(pk=template_id)
            if template.exists():
                template = template.first().get_values()
                columns=[]
                template['columns'] = sorted(template['columns'], key=lambda column: column['position'])
                for c in template['columns']:
                    columns.append(str(c['table'])+'___'+c['fieldname'])
                self.initial = {
                    "id": template['id'],
                    "name": template['name'],
                    "description": template['description'],
                    "burial_image": template['book_name'],
                    "columns": columns,
                    "base_template": template['id']
                } 
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        template_id = request.POST.get('id')
        form_kwargs = self.get_form_kwargs()
        form_kwargs['instance'] = Template.objects.filter(pk=template_id).first()
        
        form = self.form_class(**form_kwargs)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form_data = form.cleaned_data
        column_displaynames_dict = json.loads(form.data['column_displaynames'])
        print(column_displaynames_dict)
        template = Template.objects.update_template(id=form_data['id'], name=form_data['name'], description=form_data['description'],
                    book_name=form_data['burial_image'], user=self.request.user, columns=form_data['columns'], column_displaynames=column_displaynames_dict)
        return super(EditTemplateView, self).form_valid(form, {"status": "ok"})
    
    def form_invalid(self, form):
        print('invalid data')
        return JsonResponse(form.errors, status=400)
    
    
class AddBurialRecordView(AjaxableResponseMixin, FormView, DataEntryPermission ):
    template_name = 'dataentry/json/add-burial-record.json'
    success_url = '/mapmanagement'
    form_class = AddBurialRecordForm
    content_type = 'application/json'
    
    def get(self, request):
        user = DataEntryUser.objects.get(id=request.user.id)
        image = user.get_current_image()
        if not image:
            image = user.set_current_image()
        book_name = str.split(image.url.name, '_')[len(str.split(image.url.name, '_'))-2]
        template = Template.objects.filter(book_name=book_name).first()
        if not template:
            template = Template.objects.first()
        if template:
            self.initial = {
                "templates": str(template.id),
                "comments":ImageHistory.objects.filter(image=image, user=user).first().comments
            }
        records = Burial.objects.get_person_death_burial_values(burial_record_image=image)
        columns = Column.objects.filter(is_subcolumn=False)
        # print(records)
        return self.render_to_response({'status': 'ok', 'image': image.url.url, 'image_id': image.id, "image_extent": [0, 0, image.url.width, image.url.height], 'records': records, 'columns': columns, 'form':self.get_form()})


class IsNull(Func):
    template = '%(expressions)s IS NULL'

'''
Gets options needed for data entry. Also cleans data to remove unused.
'''

class DynamicFormView(TemplateView, DataEntryPermission):
    template_name = 'dataentry/json/create-multiple-forms.json'
    success_url = '/mapmanagement'
    content_type = 'application/json'
        
    def get(self, request):
        BurialOfficialFormSet = formset_factory(BurialOfficialForm)
        return self.render_to_response({'status': 'ok',
                                        'formset':[TagsForm(prefix='tags'),
                                            PersonModelForm(prefix="person"), 
                                            DeathModelForm(prefix="death"), 
                                            BurialModelForm(prefix="burial")],
                                        'foreign_keys':[
                                            AddressModelForm(prefix="person-residence_address"),
                                            AddressModelForm(prefix="death-address"),
                                            GraveRefModelForm(prefix="burial-graveref")
                                            ],
                                        'many_to_many_keys': [
                                             #m2m key here temporarily
                                            BurialOfficialFormSet(prefix="burial-burial_officials"),
                                            # BurialOfficialForm(prefix="burial-burial_officials")
                                            ]
                                        })
    
    def post(self, request):
        person_form = PersonModelForm(request.POST, prefix="person")
        death_form = DeathModelForm(request.POST, prefix="death")
        burial_form = BurialModelForm(request.POST, prefix="burial")
        tags_form = TagsForm(request.POST, prefix="tags")
        person_address_form = AddressModelForm(request.POST, prefix="person-residence_address")
        death_address_form = AddressModelForm(request.POST, prefix="death-address")
        BurialOfficialFormSet = formset_factory(BurialOfficialForm)
        burial_official_formset = BurialOfficialFormSet(request.POST, prefix="burial-burial_officials")

        # custom processing of graveref data
        grave_number_or_section_removed = False

        if 'burial-graveref-grave_number' in request.POST:
            grave_number = request.POST['burial-graveref-grave_number']

            if not grave_number:
                grave_number_or_section_removed = True
                grave_number = None
        else:
            grave_number = None
        if 'burial-graveref-section' in request.POST:
            section = request.POST['burial-graveref-section']

            if not section:
                grave_number_or_section_removed = True
                section = None
        else:
            section = None
        if 'burial-graveref-subsection' in request.POST and request.POST['burial-graveref-subsection']:
            subsection = request.POST['burial-graveref-subsection']
        else:
            subsection = None

        # person_form.is_valid() break the form and makes impossible date mandatory
        try:
            person_data_form = person_form.cleaned_data
        except:
            person_data_form = {'deleted_at': person_form.data.get('deleted_at', None),
                                'title': person_form.data.get('person-title', ''),
                                'first_names': person_form.data.get('person-first_names', ''),
                                'birth_name': person_form.data.get('person-birth_name', ''),
                                'other_names': person_form.data.get('person-other_names', ''),
                                'last_name': person_form.data.get('person-last_name', ''),
                                'impossible_date_day': person_form.data.get('person-impossible_date_day', ''),
                                'impossible_date_month': person_form.data.get('person-impossible_date_month', ''),
                                'impossible_date_year': person_form.data.get('person-impossible_date_year', ''),
                                'gender': person_form.data.get('person-gender', None),
                                'description': person_form.data.get('person-description', ''),
                                'profession': person_form.data.get('person-profession', None),
                                'residence_address': person_form.data.get('person-residence_address-first_line', ''),
                                'next_of_kin': person_form.data.get('person-next_of_kin', None),
                                'next_of_kin_relationship': person_form.data.get('person-next_of_kin_relationship', None),
                                'data_upload': person_form.data.get('data_upload', None),
                                'person_id': person_form.data.get('person-id', None)}

        if death_form.is_valid() and burial_form.is_valid() \
            and person_address_form.is_valid() and tags_form.is_valid() \
            and death_address_form.is_valid() and burial_official_formset.is_valid():
                person = Person()
                person.add_person_details(person_data_form)
                person.add_residence_address(first_line=person_address_form.cleaned_data['first_line'], \
                                             second_line=person_address_form.cleaned_data['second_line'], \
                                             town=person_address_form.cleaned_data['town'], \
                                             county=person_address_form.cleaned_data['county'], \
                                             postcode=person_address_form.cleaned_data['postcode'], \
                                             country=person_address_form.cleaned_data['country'])
                if 'person-profession' in request.POST:
                    person.add_profession(request.POST['person-profession'])
                person.add_death_details(death_form.cleaned_data)
                if 'death-event' in request.POST:
                    person.death.add_event(request.POST['death-event'])
                person.death.add_address(first_line=death_address_form.cleaned_data['first_line'], \
                                         second_line=death_address_form.cleaned_data['second_line'], \
                                         town=death_address_form.cleaned_data['town'], \
                                         county=death_address_form.cleaned_data['county'], \
                                         postcode=death_address_form.cleaned_data['postcode'], \
                                         country=death_address_form.cleaned_data['country'])
                if 'death-parish' in request.POST:
                    person.death.add_parish(parish=request.POST['death-event'])
                if 'death-religion' in request.POST:
                    person.death.add_religion(religion=request.POST['death-religion'])
                # conditional to prevent day, month or year "out of range" by add_burial_details restriction
                if burial_form.cleaned_data['impossible_date_day'] <= '0' or burial_form.cleaned_data['impossible_date_month'] <= '0' or burial_form.cleaned_data['impossible_date_year'] <= '0':
                    burial_form.cleaned_data['impossible_date_day'] = '0'
                    burial_form.cleaned_data['impossible_date_month'] = '0'
                    burial_form.cleaned_data['impossible_date_year'] = '0'
                burial_officials = burial_form.cleaned_data.pop('burial_officials')
                burial = person.create_burial(burial_form.cleaned_data)
                burial.add_burial_details(grave_number=grave_number, \
                                            section=section, \
                                            subsection=subsection, \
                                            grave_number_or_section_removed=grave_number_or_section_removed)
                for official_form in burial_official_formset:
                    official_data = official_form.cleaned_data
                    if 'burial_official_type' in official_data and (official_data['title']!='' or official_data['first_names']!='' or official_data['last_name']!=''):
                        burial.create_burial_official(official_data['official_type'], \
                                                      official_data['title'], \
                                                      official_data['first_names'], \
                                                      official_data['last_name'],\
                                                      official_data['burial_official_type'])
                user = DataEntryUser.objects.get(id=request.user.id)
                image = user.get_current_image()
                burial.add_image(image)
                burial.save()
                tag = Tag(image=image, person=person, top_left_bottom_right=tags_form.cleaned_data['top_left_bottom_right'])
                tag.save()
                return JsonResponse({'status': 'ok', 'person___id': str(person.id), 'person___tag_id':str(tag.id)}, status=200)
        else:
            errors = {}
            errors.update(tags_form.errors)
            for field, error in person_form.errors.items():
                errors['person-'+field] = error
            for field, error in death_form.errors.items():
                errors['death-'+field] = error
            for field, error in burial_form.errors.items():
                errors['burial-'+field] = error
            for field, error in person_address_form.errors.items():
                errors['person-residence_address-'+field] = error
            for field, error in death_address_form.errors.items():
                errors['death-address-'+field] = error
            # for field, error in burial_graveref_form.errors.items():
            #     errors['burial-graveref-'+field] = error
            for singledict in burial_official_formset.errors:
                for field, error in singledict.items():
                    errors['burial-burial_officials-'+field] = error
            return JsonResponse(errors, status=400)
    
    
class GetTagView(DataEntryPermission):    
    def get(self, request):
        image_id = request.GET.get('image_id')
        tags = Tag.objects.tag_values_from_image(image=image_id)

        serializer = TagGeoSerializer(tags, many=True)

        geoj = serializer.data
        geoj.update(CRS)

        return JsonResponse(geoj, safe=False)


class DeleteBurialRecordView(DataEntryPermission):    
    def post(self, request):
        person_id = request.POST.get('person_id')
        Person.objects.filter(id=person_id).delete()
        Burial.objects.filter(death_id=person_id).delete()
        return JsonResponse({"status": "ok"})


class UpdateBurialRecordView(DataEntryPermission):    
    def post(self, request):
        person_form = PersonModelForm(request.POST, prefix="person")
        death_form = DeathModelForm(request.POST, prefix="death")
        burial_form = BurialModelForm(request.POST, prefix="burial")
        tags_form = TagsForm(request.POST, prefix="tags")
        person_address_form = AddressModelForm(request.POST, prefix="person-residence_address")
        death_address_form = AddressModelForm(request.POST, prefix="death-address")
        BurialOfficialFormSet = formset_factory(BurialOfficialForm)
        burial_official_formset = BurialOfficialFormSet(request.POST, prefix="burial-burial_officials")

        # custom processing of graveref data
        grave_number_or_section_removed = False

        if 'burial-graveref-grave_number' in request.POST:
            grave_number = request.POST['burial-graveref-grave_number']

            if not grave_number:
                grave_number_or_section_removed = True
                grave_number = None
        else:
            grave_number = None
        if 'burial-graveref-section' in request.POST:
            section = request.POST['burial-graveref-section']

            if not section:
                grave_number_or_section_removed = True
                section = None
        else:
            section = None
        if 'burial-graveref-subsection' in request.POST and request.POST['burial-graveref-subsection']:
            subsection = request.POST['burial-graveref-subsection']
        else:
            subsection = None

        if person_form.is_valid() and death_form.is_valid() and burial_form.is_valid() \
            and person_address_form.is_valid() and tags_form.is_valid() \
            and death_address_form.is_valid() and burial_official_formset.is_valid():
                person = Person.objects.get(id=person_form.cleaned_data['person_id'])
                person.add_person_details(person_form.cleaned_data)
                person.add_residence_address(first_line=person_address_form.cleaned_data['first_line'], \
                                             second_line=person_address_form.cleaned_data['second_line'], \
                                             town=person_address_form.cleaned_data['town'], \
                                             county=person_address_form.cleaned_data['county'], \
                                             postcode=person_address_form.cleaned_data['postcode'], \
                                             country=person_address_form.cleaned_data['country'])
                if 'person-profession' in request.POST:
                    person.add_profession(request.POST['person-profession'])
                person.add_death_details(death_form.cleaned_data)
                if 'death-event' in request.POST:
                    person.death.add_event(request.POST['death-event'])
                person.death.add_address(first_line=death_address_form.cleaned_data['first_line'], \
                                         second_line=death_address_form.cleaned_data['second_line'], \
                                         town=death_address_form.cleaned_data['town'], \
                                         county=death_address_form.cleaned_data['county'], \
                                         postcode=death_address_form.cleaned_data['postcode'],\
                                         country=death_address_form.cleaned_data['country'])
                if 'death-parish' in request.POST:
                    person.death.add_parish(parish=request.POST['death-event'])
                if 'death-religion' in request.POST:
                    person.death.add_religion(religion=request.POST['death-religion'])
                user = DataEntryUser.objects.get(id=request.user.id)
                image = user.get_current_image()
                tag = Tag.objects.filter(image=image, person=person).first()
                if tag:
                    tag.top_left_bottom_right=tags_form.cleaned_data['top_left_bottom_right']
                    tag.save()
                burial_officials = burial_form.cleaned_data.pop('burial_officials')
                burial = person.get_burials().first()
                burial.add_burial_details(grave_number=grave_number, \
                                            section=section, \
                                            subsection=subsection, \
                                            grave_number_or_section_removed=grave_number_or_section_removed, \
                                            burial_number=burial_form.cleaned_data['burial_number'], \
                                            impossible_date_day=burial_form.cleaned_data['impossible_date_day'],
                                            impossible_date_month=burial_form.cleaned_data['impossible_date_month'],\
                                            impossible_date_year=burial_form.cleaned_data['impossible_date_year'],\
                                            cremation_certificate_no=burial_form.cleaned_data['cremation_certificate_no'],\
                                            depth=burial_form.cleaned_data['depth'],\
                                            depth_units=burial_form.cleaned_data['depth_units'],\
                                            user_remarks=burial_form.cleaned_data['user_remarks'],\
                                            burial_remarks=burial_form.cleaned_data['burial_remarks'],\
                                            consecrated=burial_form.cleaned_data['consecrated'],
                                            cremated=burial_form.cleaned_data['cremated'],
                                            impossible_cremation_date_day=burial_form.cleaned_data['impossible_cremation_date_day'],
                                            impossible_cremation_date_month=burial_form.cleaned_data['impossible_cremation_date_month'],\
                                            impossible_cremation_date_year=burial_form.cleaned_data['impossible_cremation_date_year'],\
                                            interred=burial_form.cleaned_data['interred'],\
                                            requires_investigation=burial_form.cleaned_data['requires_investigation'],\
                                            situation=burial_form.cleaned_data['situation'],\
                                            place_from_which_brought=burial_form.cleaned_data['place_from_which_brought'],)
                burial.remove_burial_officials()
                for burial_official_form in burial_official_formset:
                    official_data = burial_official_form.cleaned_data
                    if 'burial_official_type' in official_data and (official_data['title']!='' or official_data['first_names']!='' or official_data['last_name']!=''):
                        burial.create_burial_official(official_data['official_type'], \
                                                      official_data['title'], \
                                                      official_data['first_names'], \
                                                      official_data['last_name'],\
                                                      official_data['burial_official_type'])
                user = DataEntryUser.objects.get(id=request.user.id)
                image = user.get_current_image()
                burial.add_image(image)
                burial.save()
                return JsonResponse({'status': 'ok', 'person___id': str(person.id), 'person___tag_id': str(tag.id)}, status=200)
        else:
            errors = {}
            for field, error in person_form.errors.items():
                errors['person-'+field] = error
            for field, error in death_form.errors.items():
                errors['death-'+field] = error
            for field, error in burial_form.errors.items():
                errors['burial-'+field] = error
            for field, error in person_address_form.errors.items():
                errors['person-residence_address-'+field] = error
            for field, error in death_address_form.errors.items():
                errors['death-address-'+field] = error
            # for field, error in burial_graveref_form.errors.items():
            #     errors['burial-graveref-'+field] = error
            for singledict in burial_official_formset.errors:
                for field, error in singledict.items():
                    errors['burial-burial_officials-'+field] = error
            return JsonResponse(errors, status=400)
    

class DeleteBurialOfficialView(DataEntryPermission):    
    def post(self, request):
        person_id = request.POST.get('person_id')
        burial_id = Person.objects.get(id=person_id).get_burials().first().id
        official_id = request.POST.get('official_id')
        Burial_Official.objects.filter(official_id=official_id, burial_id=burial_id).delete()
        return JsonResponse({"status": "ok"})  
    

class GetImageStatus(DataEntryPermission):    
    def get(self, request):
        imageHistory = BurialImage.objects.all_burial_image_history_values()
        summary = BurialImage.objects.summary()
        return JsonResponse({'imageHistory': list(imageHistory), 'summary': summary, 'csrfmiddlewaretoken':csrf.get_token(request)}, safe=False)


class GetUserActivity(DataEntryPermission):    
    def get(self, request):
        userActivity = BurialImage.objects.get_user_activity()
        return JsonResponse({
            'userActivity': list(userActivity),
            'csrfmiddlewaretoken': csrf.get_token(request),
        }, safe=False)
    
    
class ChangeToImageById(DataEntryPermission):    
    def post(self, request):
        image_id = request.POST.get('image_id')
        image = BurialImage.objects.get(id=image_id)
        user = DataEntryUser.objects.get(id=request.user.id)
        if not ImageHistory.objects.filter(image=image).filter(state=UserState.objects.get(state='in_use')).exists():
            user.set_image_viewed()
            user.set_current_image(image=image)
            return JsonResponse({"status": "ok"})
        else:
            return JsonResponse({'status': 'error', 'message': 'The image is currently in use.'}, status=400)
