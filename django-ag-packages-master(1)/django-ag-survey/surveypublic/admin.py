from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.utils.functional import curry
from geometriespublic.models import FeatureCode
from surveypublic.forms import NonOptionalFieldFormSet, SurveyTemplateFieldForm
from surveypublic.models import PublicSurveyTemplateField, MasterSurveyTemplate

class PublicSurveyTemplateFieldAdmin(admin.ModelAdmin):
    model = PublicSurveyTemplateField
    list_display = ('name', 'type', 'optional')
    ordering = ('name',)
    exclude = ('id',)
    form = SurveyTemplateFieldForm

admin.site.register(PublicSurveyTemplateField, PublicSurveyTemplateFieldAdmin)

class NonOptionalFieldInline(admin.TabularInline):
    """
    Readonly inline for displaying compulsory fields
    """
    model = MasterSurveyTemplate.fields.through
    formset = NonOptionalFieldFormSet
    classes = ['hide-add-row',]
    verbose_name = 'Compulsory Survey Template Field'
    verbose_name_plural = 'Compulsory Survey Template Fields'
    ordering = ('hierarchy',)

    def get_extra(self, request, obj=None, **kwargs):
        return PublicSurveyTemplateField.objects.filter(optional=False).count()

    def get_queryset(self, request):
        qs = super(NonOptionalFieldInline, self).get_queryset(request)
        return qs.filter(publicsurveytemplatefield__optional=False)

    def has_delete_permission(self, request, obj=None):
        return False
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(NonOptionalFieldInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'publicsurveytemplatefield':
            field.queryset = field.queryset.filter(optional=False)

        return field

class PublicSurveyTemplateFieldInline(admin.TabularInline):
    """
    Editable inline for selecting fields
    """
    model = MasterSurveyTemplate.fields.through
    extra = 0
    verbose_name = 'Optional Survey Template Field'
    verbose_name_plural = 'Optional Survey Template Fields'
    ordering = ('hierarchy',)
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(PublicSurveyTemplateFieldInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'publicsurveytemplatefield':
            field.queryset = field.queryset.filter(optional=True)

        return field

class MasterSurveyTemplateAdmin(admin.ModelAdmin):

    model = MasterSurveyTemplate
    filter_horizontal = ('feature_codes',)
    inlines = [
        NonOptionalFieldInline,
        PublicSurveyTemplateFieldInline,
    ]
    list_display = ('name', 'date')
    ordering = ('name',)
    exclude = ('id','created_by', 'fields')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "feature_codes":
            kwargs["queryset"] = FeatureCode.objects.filter(type='vector').order_by('display_name')
        return super(MasterSurveyTemplateAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(MasterSurveyTemplate, MasterSurveyTemplateAdmin)