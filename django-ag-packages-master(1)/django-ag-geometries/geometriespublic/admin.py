from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from geometriespublic.models import FeatureCode, FeatureGroup, PublicAttribute
from django.http import HttpResponseBadRequest
from surveypublic.forms import SurveyTemplateFieldForm
import sys

class PublicAttributesInline(admin.TabularInline):
    model = PublicAttribute.feature_codes.through
    fields = ('publicattribute',)
    extra = 1

# Register your models here.
class FeatureCodeAdmin(admin.ModelAdmin):
    model = FeatureCode
    inlines = [
        PublicAttributesInline,
    ]
    # exclude = ('domain_url','schema_name')
    list_display = ('feature_type', 'display_name', 'hierarchy')
    # list_filter = ('feature_type')
    ordering = ('hierarchy',)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            form_data = form.cleaned_data
            # Re order hirachy level when updating value
            new_h = form_data['hierarchy']
            
            if len(FeatureCode.objects.filter(feature_type=form_data['feature_type'])) > 0:
                old_h = FeatureCode.objects.get(feature_type=form_data['feature_type']).hierarchy
            else:
                old_h = sys.maxsize

            if new_h != old_h:
                FeatureCode.objects.reorder_hierarchy(old_h, new_h)
            # import pdb; pdb.set_trace()
            # if old_h != sys.maxsize:
            obj.save()
        else:
            return HttpResponseBadRequest(form.errors)

class FeatureGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('feature_codes',)
    # fieldsets = (
    #     (None, {'fields': ('layer', 'extent', 'address', 'aerial')}),
    # 
    list_display = ('group_code', 'display_name', 'hierarchy')
    # list_filter = ('feature_type')
    ordering = ('hierarchy',)

class PublicAttributeAdmin(admin.ModelAdmin):
    model = PublicAttribute
    list_display = ('name', 'type')
    ordering = ('name',)
    filter_horizontal = ('feature_codes',)
    form = SurveyTemplateFieldForm

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "feature_codes":
            kwargs["queryset"] = FeatureCode.objects.filter(type='vector').order_by('display_name')
        return super(PublicAttributeAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(FeatureGroup, FeatureGroupAdmin)
admin.site.register(FeatureCode, FeatureCodeAdmin)
admin.site.register(PublicAttribute, PublicAttributeAdmin)
