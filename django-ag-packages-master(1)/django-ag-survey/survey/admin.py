from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.forms import CheckboxSelectMultiple
from geometriespublic.models import FeatureCode
from survey.models import SiteSurveyTemplateField, SurveyTemplate, SurveyTemplateField, SurveyTemplate_Field
from surveypublic.forms import NonOptionalSurveyTemplateFieldFormSet, SurveyTemplateFieldForm
from surveypublic.models import PublicSurveyTemplateField, MasterSurveyTemplate

class SiteSurveyTemplateFieldAdmin(admin.ModelAdmin):
    model = SiteSurveyTemplateField
    list_display = ('name', 'type')
    ordering = ('name',)
    exclude = ('id',)
    form = SurveyTemplateFieldForm

    def has_delete_permission(self, request, obj=None):
        return False

class NonOptionalFieldInline(admin.TabularInline):
    """
    Readonly inline for displaying compulsory fields
    """
    model = SurveyTemplate.fields.through
    formset = NonOptionalSurveyTemplateFieldFormSet
    classes = ['hide-add-row',]
    verbose_name = 'Compulsory Survey Template Field'
    verbose_name_plural = 'Compulsory Survey Template Fields'
    ordering = ('hierarchy',)

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            # this is a new object
            return SurveyTemplateField.objects.filter(public_survey_template_fields__optional=False).count()

    def get_queryset(self, request):
        qs = super(NonOptionalFieldInline, self).get_queryset(request)
        return qs.filter(surveytemplatefield__public_survey_template_fields__optional=False)

    def has_delete_permission(self, request, obj=None):
        return False
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(NonOptionalFieldInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'surveytemplatefield':
            field.queryset = field.queryset.filter(public_survey_template_fields__optional=False)

        return field
    
    def get_fields(self, request, obj=None):
        gf = super(NonOptionalFieldInline, self).get_fields(request, obj)
        if 'master_templates' in gf:
            gf.remove('master_templates')   # I'm not sure why this included in the first place...
        return gf

class OptionalFieldInline(admin.TabularInline):
    """
    Editable inline for selecting fields
    """
    publicsurveytemplatefield_content_type,created = ContentType.objects.get_or_create(app_label='surveypublic', model='publicsurveytemplatefield')
    
    model = SurveyTemplate.fields.through
    extra = 0
    verbose_name = 'Optional Survey Template Field'
    verbose_name_plural = 'Optional Survey Template Fields'
    ordering = ('hierarchy',)

    class Media:
        js = [#'libs/bower_components/jquery/dist-js/jquery.min.js',
              "/static/survey/js/admin.js"]
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(OptionalFieldInline, self).formfield_for_fbeeoreignkey(db_field, request, **kwargs)

        if db_field.name == 'surveytemplatefield':
            field.queryset = field.queryset.filter(
                Q(Q(content_type=self.publicsurveytemplatefield_content_type) & Q(public_survey_template_fields__optional=True) & Q(public_survey_template_fields__retired=False))
                | Q(~Q(content_type=self.publicsurveytemplatefield_content_type) & Q(site_survey_template_fields__retired=False)))

        return field
    
    def get_fields(self, request, obj=None):
        gf = super(OptionalFieldInline, self).get_fields(request, obj)
        if 'master_templates' in gf:
            gf.remove('master_templates')   # I'm not sure why this included in the first place...
        return gf

    def get_queryset(self, request):
        qs = super(OptionalFieldInline, self).get_queryset(request)
        return qs.filter(~Q(surveytemplatefield__content_type=self.publicsurveytemplatefield_content_type) | Q(surveytemplatefield__public_survey_template_fields__optional=True))

class SurveyTemplateAdmin(admin.ModelAdmin):
         
    non_optional_fields = PublicSurveyTemplateField.objects.filter(optional=False)

    model = SurveyTemplate
    filter_horizontal = ('feature_codes',)
    inlines = [
        NonOptionalFieldInline,
        OptionalFieldInline,
    ]
    list_display = ('name', 'date')
    ordering = ('name',)
    exclude = ('id', 'created_by', 'fields')

    def has_delete_permission(self, request, obj=None):
        return False

    def get_fields(self, request, obj=None):
        gf = super(SurveyTemplateAdmin, self).get_fields(request, obj)

        # if a new template
        if not obj:
            master_surveys_qs = MasterSurveyTemplate.objects.all()

            # add custom select field populated with list of master templates
            if master_surveys_qs.exists():
                choices = [('', '-')]

                for survey in master_surveys_qs:
                    choices.append((survey.id, survey.name))

                self.form.declared_fields.update(
                    {'master_templates': forms.ChoiceField(
                        widget=forms.Select(),
                        required=False,
                        choices=choices,
                        label="Master Templates")})

                gf = super(SurveyTemplateAdmin, self).get_fields(request, obj)
                gf.insert(0, gf.pop())  # moves custom field to start of form

        return gf

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):    
        if db_field.name == 'feature_codes':
            kwargs["queryset"] = FeatureCode.objects.filter(type='vector').order_by('display_name')

        return super(SurveyTemplateAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):

        # make sure all default fields exist for this schema
        default_fields = PublicSurveyTemplateField.objects.all()
        content_type = ContentType.objects.get(app_label='surveypublic', model='publicsurveytemplatefield')

        for field in default_fields:
            SurveyTemplateField.objects.get_or_create(content_type=content_type, object_id=field.id)

        return {'fields': SurveyTemplateField.objects.filter(content_type__model='publicsurveytemplatefield')}
    
    def save_related(self, request, form, formsets, change):
        super(SurveyTemplateAdmin, self).save_related(request, form, formsets, change)
        
        # add compulsory fields
        obj = form.instance

        compulsory_fields = SurveyTemplateField.objects.filter(object_id__in=self.non_optional_fields.values('id')).all()
        #obj.fields.add(*compulsory_fields)

        for field in compulsory_fields:
            SurveyTemplate_Field.objects.get_or_create(surveytemplate_id=obj.id, surveytemplatefield_id=field.id, hierarchy=0)