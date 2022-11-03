from django import forms
from main.validators import bleach_validator
from django.forms.forms import Form
from dataentry import helpers
from dataentry import models
from django.forms.models import ModelForm, inlineformset_factory
from bgsite.models import Person, Death, Burial, Address,\
    Official, GraveRef
from django.contrib.gis.forms.fields import PointField, MultiPointField
from _datetime import date
from dataentry.models import Template

class CreateTemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = ['name', 'description', 'columns']
        
    name = forms.CharField(label='', validators=[bleach_validator], required=True, widget=forms.TextInput(attrs={'tabindex':'1','class':'form-control', 'maxlength':'50'}))
    burial_image = forms.ChoiceField(choices=helpers.get_burial_images, required=True, widget=forms.Select(attrs={'tabindex':'2'}))
    base_template = forms.ChoiceField(choices=helpers.get_base_templates, required=False, widget=forms.Select(attrs={'tabindex':'2'}))
    description = forms.CharField(label='', validators=[bleach_validator], required=False, widget=forms.Textarea(attrs={'tabindex':'3','class':'form-control', 'rows': '2', 'maxlength':'200'}))
    columns = forms.MultipleChoiceField(choices=helpers.get_column_names, required=True, widget=forms.CheckboxSelectMultiple(attrs={'tabindex':'4'}))
    column_displaynames = forms.CharField(label='', validators=[bleach_validator], required=False, widget=forms.HiddenInput())

class EditTemplateForm(CreateTemplateForm):
    id = forms.CharField(label='', validators=[bleach_validator], required=True, widget=forms.TextInput(attrs={'tabindex':'5','class':'form-control', 'maxlength':'50'}))
    
class AddBurialRecordForm(Form):
    templates = forms.ChoiceField(choices=helpers.get_templates, required=False, widget=forms.Select(attrs={'tabindex':'1'}))
    books = forms.ChoiceField(choices=helpers.get_burial_books, required=False, widget=forms.Select(attrs={'tabindex':'2'}))
    comments = forms.CharField(label='', validators=[bleach_validator], required=False, widget=forms.Textarea(attrs={'tabindex':'3','class':'form-control', 'rows': '2', 'maxlength':'200'}))
    
class TagsForm(Form):
    top_left_bottom_right = MultiPointField(label='', srid=0, required=False, widget=forms.HiddenInput())
    
class PersonModelForm(ModelForm):   
    class Meta:
        model=Person
        exclude=['id']
        labels = {
            'impossible_date_day': 'Day',
            'impossible_date_month': 'Month',
            'impossible_date_year': 'Year',
        }        
    
    impossible_date_day = forms.ChoiceField(choices=[(0,'-')]+[(x,x) for x in range(1,32)], required=False, widget=forms.Select(attrs={'tabindex':'13','DISABLED':'DISABLED'}))
    impossible_date_month = forms.ChoiceField(choices=[(0,'-'),(1,'Jan'),(2,'Feb'),(3,'Mar'),(4,'Apr'),(5,'May'),(6,'June'),(7,'July'),(8,'Aug'),(9,'Sept'),(10,'Oct'),(11,'Nov'),(12,'Dec')], required=False, widget=forms.Select(attrs={'tabindex':'14','DISABLED':'DISABLED'}))
    impossible_date_year = forms.ChoiceField(choices=[(0,'-')]+[(x,x) for x in reversed(range(1000,date.today().year + 1))], required=False, widget=forms.Select(attrs={'tabindex':'15','DISABLED':'DISABLED'}))
    #additional field to include id sent from user
    person_id = forms.UUIDField(required=False, widget=forms.HiddenInput())
            
class DeathModelForm(ModelForm):    
    class Meta:
        model=Death
        exclude=['person', 'memorials']
        labels = {
            'impossible_date_day': 'dd',
            'impossible_date_month': 'mm',
            'impossible_date_year': 'yyyy',
        }
    
    impossible_date_day = forms.ChoiceField(choices=[(0,'-')]+[(x,x) for x in range(1,32)], required=False, widget=forms.Select(attrs={'tabindex':'13','DISABLED':'DISABLED'}))
    impossible_date_month = forms.ChoiceField(choices=[(0,'-'),(1,'Jan'),(2,'Feb'),(3,'Mar'),(4,'Apr'),(5,'May'),(6,'June'),(7,'July'),(8,'Aug'),(9,'Sept'),(10,'Oct'),(11,'Nov'),(12,'Dec')], required=False, widget=forms.Select(attrs={'tabindex':'14','DISABLED':'DISABLED'}))
    impossible_date_year = forms.ChoiceField(choices=[(0,'-')]+[(x,x) for x in reversed(range(1000,date.today().year + 1))], required=False, widget=forms.Select(attrs={'tabindex':'15','DISABLED':'DISABLED'}))

        
class BurialModelForm(ModelForm):
    class Meta:
        model=Burial
        exclude=['death', 'id', 'graveplot']
        labels = {
            'impossible_date_day': 'dd',
            'impossible_date_month': 'mm',
            'impossible_date_year': 'yyyy',
            'impossible_cremation_date_day': 'dd',
            'impossible_cremation_date_month': 'mm',
            'impossible_cremation_date_year': 'yyyy',
        }
        widgets = {
            'consecrated': forms.CheckboxInput,
            'cremated': forms.CheckboxInput,
            'interred':forms.CheckboxInput
        }
    
    impossible_date_day = forms.ChoiceField(choices=[(0,'-')]+[(x,x) for x in range(1,32)], required=False, widget=forms.Select(attrs={'tabindex':'13','DISABLED':'DISABLED'}))
    impossible_date_month = forms.ChoiceField(choices=[(0,'-'),(1,'Jan'),(2,'Feb'),(3,'Mar'),(4,'Apr'),(5,'May'),(6,'June'),(7,'July'),(8,'Aug'),(9,'Sept'),(10,'Oct'),(11,'Nov'),(12,'Dec')], required=False, widget=forms.Select(attrs={'tabindex':'14','DISABLED':'DISABLED'}))
    impossible_date_year = forms.ChoiceField(choices=[(0,'-')]+[(x,x) for x in reversed(range(1000,date.today().year + 1))], required=False, widget=forms.Select(attrs={'tabindex':'15','DISABLED':'DISABLED'}))

    impossible_cremation_date_day = forms.ChoiceField(choices=[(0,'-')]+[(x,x) for x in range(1,32)], required=False, widget=forms.Select(attrs={'tabindex':'16','DISABLED':'DISABLED'}))
    impossible_cremation_date_month = forms.ChoiceField(choices=[(0,'-'),(1,'Jan'),(2,'Feb'),(3,'Mar'),(4,'Apr'),(5,'May'),(6,'June'),(7,'July'),(8,'Aug'),(9,'Sept'),(10,'Oct'),(11,'Nov'),(12,'Dec')], required=False, widget=forms.Select(attrs={'tabindex':'17','DISABLED':'DISABLED'}))
    impossible_cremation_date_year = forms.ChoiceField(choices=[(0,'-')]+[(x,x) for x in reversed(range(1000,date.today().year + 1))], required=False, widget=forms.Select(attrs={'tabindex':'18','DISABLED':'DISABLED'}))


#foreign keys represented by forms
        
class AddressModelForm(ModelForm):
    class Meta:
        model=Address
        exclude=['id']
        labels = {
            'first_line': 'Name/Number, Street',
            'second_line': 'Village/Locality',
        }
        
class GraveRefModelForm(ModelForm):
    class Meta:
        model=GraveRef
        exclude=['id']
        labels = {
            'grave_number': 'Grave Number',
            'section': 'Section',
            'subsection': 'Subsection',
        }

    def clean(self):
        cd = self.cleaned_data

        return cd

#m2m keys represented by normal form, due to through in m2m
#TODO: change to Formset after further investigation

class BurialOfficialForm(Form):
    burial_official_type = forms.CharField(label='Official Type Id', required=True, validators=[bleach_validator], widget=forms.HiddenInput(attrs={'class':'form-control non-editable burial-official-type', 'readonly':'readonly', 'maxlength':'200'}))
    official_type = forms.CharField(label='Type of Official', required=False, validators=[bleach_validator], widget=forms.HiddenInput(attrs={'class':'form-control non-editable burial-official-type', 'readonly':'readonly', 'maxlength':'200'}))
    title = forms.CharField(label='Title', required=False, validators=[bleach_validator], widget=forms.TextInput(attrs={'class':'form-control non-editable', 'readonly':'readonly', 'maxlength':'200'}))
    first_names = forms.CharField(label='First Names', required=False, validators=[bleach_validator], widget=forms.TextInput(attrs={'class':'form-control non-editable', 'readonly':'readonly', 'maxlength':'200'}))
    last_name = forms.CharField(label='Last Name', required=False, validators=[bleach_validator], widget=forms.TextInput(attrs={'class':'form-control non-editable', 'readonly':'readonly', 'maxlength':'200'}))

# class BurialOfficialForm(Form):
#     class Meta:
#         model=Official
#         exclude=['id', 'used_on']
#   
#     official_type = forms.CharField(label='Type of Official', required=False, validators=[bleach_validator], widget=forms.TextInput(attrs={'class':'form-control non-editable burial-official-type field-to-hide', 'readonly':'readonly', 'maxlength':'200'}))

# BurialOfficialFormSet = inlineformset_factory(Official, Burial, exclude=['id'], extra=1, can_delete=False)
