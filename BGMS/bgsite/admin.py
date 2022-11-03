from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.contrib.gis import admin as admingis
from bgsite.models import UserRequest, TenantUser, Official, Person, Image, PersonField
from django.db import connection
from django.contrib.admin.options import ModelAdmin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import get_deleted_objects, model_ngettext, unquote
from django.core.exceptions import PermissionDenied
from django.db import router
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _, ugettext_lazy
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from bgsite.forms_admin import TenantUserForm
from django.conf.urls import url
from django.utils import timezone
from django.utils.translation import ngettext

from config.storages.staticS3storage import StaticS3Storage

from bgsite.models import MeetingLocation
from bgsite.views_admin import UploadPhotosView, uploadBurialRecordPhotosView, addUserPermissions, sendEmailInvitationView, DataUploadView, submit_data_upload, delete_data_upload, link_registers, SectionLinkView, update_graveplot_layers, uploadOwnershipRegisterPhotosView, ResetAuthView
from cemeteryadmin.models import EventType, EventCategory, Settings
from geometries.models import TopoPolygons, TopoPolylines, TopoPoints, Layer, Attribute
from geometriespublic.models import FeatureCode
from main.admin import BGUserAdmin
from survey.models import SiteSurveyTemplateField, SurveyTemplate
from survey.admin import SiteSurveyTemplateFieldAdmin, SurveyTemplateAdmin
from surveypublic.forms import SurveyTemplateFieldForm
from django.contrib.postgres import fields # if django < 3.1
from django_json_widget.widgets import JSONEditorWidget
from django.urls import path
from  django import forms
from main.models import siteReferenceSettings, BurialGroundSite
import pdb

class ClientAdminSite(AdminSite):
    def get_urls(self):
        urls = super(ClientAdminSite, self).get_urls()
        urls += [
            url(r'^uploadPhotos/$', self.admin_view(UploadPhotosView.as_view()), name='uploadPhotos'),
            url(r'^dataUpload/$', self.admin_view(DataUploadView.as_view()), name='dataUpload'),
            url(r'^sectionLink/$', self.admin_view(SectionLinkView.as_view()), name='sectionLink'),
            url(r'linkRegisters/$', self.admin_view(link_registers), name='linkBurialRegisters'),
            url(r'updateGraveplotLayers/$', self.admin_view(update_graveplot_layers), name='updateGraveplotLayers'),
            url(r'^dataUpload/submitDataUpload/$', self.admin_view(submit_data_upload), name='submitDataUpload'),
            url(r'^dataUpload/deleteDataUpload/$', self.admin_view(delete_data_upload), name='deleteDataUpload'),
            url(r'^uploadBurialRecordPhotos/$', self.admin_view(uploadBurialRecordPhotosView.as_view()), name='uploadBurialRecordPhotos'),
            url(r'^uploadOwnershipRegisterPhotos/$', self.admin_view(uploadOwnershipRegisterPhotosView.as_view()), name='uploadOwnershipRegisterPhotos'),
            url(r'^addUserPermissions/$', self.admin_view(addUserPermissions.as_view()), name='addUserPermissions'),
            url(r'^sendEmailInvitation/$', self.admin_view(sendEmailInvitationView.as_view()), name='sendEmailInvitation'),
            path('resetAuth/', self.admin_view(ResetAuthView.as_view()), name='resetAuth'),
        ]
        return urls

tenant_admin_site = ClientAdminSite(name='tenant_admin')
tenant_admin_site.site_header = 'BGMS | Site Content Management System'


class TenantUserAdmin(BGUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email',)}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('site_groups',)}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('email', 'username', 'first_name', 'last_name', 'last_login', 'date_joined',)
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'site_groups__group')
    filter_horizontal = ('site_groups',)
    ordering = ('username',)
    actions = BGUserAdmin.actions + ['custom_delete_selected']
    form = TenantUserForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',),
        }),
    )
    # add_form = None
    add_form_template = "admin/user/add_permissions.html"
    change_password_form = None

    def get_actions(self, request):
        #Disable delete
        actions = super(TenantUserAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    # return False in order to disable add from dajngo admin model
    # def has_add_permission(self, request):
    #     return False

    def custom_delete_selected(self, modeladmin, request, queryset):
        """
        Default action which deletes the selected objects.

        This action first displays a confirmation page whichs shows all the
        deleteable objects, or, if the user has no permission one of the related
        childs (foreignkeys), a "permission denied" message.

        Next, it deletes all selected objects and redirects back to the change list.
        """
        opts = modeladmin.model._meta
        app_label = opts.app_label

        # Check that the user has delete permission for the actual model
        if not modeladmin.has_delete_permission(request):
            raise PermissionDenied

        # Populate deletable_objects, a data structure of all related objects that
        # will also be deleted.
        deletable_objects, model_count, perms_needed, protected = get_deleted_objects(queryset, request, self.admin_site)

        # The user has already confirmed the deletion.
        # Do the deletion and return a None to display the change list view again.
        if request.POST.get('post'):
            if perms_needed:
                raise PermissionDenied
            n = queryset.count()
            if n:
                for obj in queryset:
                    obj_display = force_text(obj)
                    modeladmin.log_deletion(request, obj, obj_display)
                    obj.remove_all_site_groups_for_schema(connection.schema_name)
                modeladmin.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                    "count": n, "items": model_ngettext(modeladmin.opts, n)
                }, messages.SUCCESS)
            # Return None to display the change list page again.
            return None

        if len(queryset) == 1:
            objects_name = force_text(opts.verbose_name)
        else:
            objects_name = force_text(opts.verbose_name_plural)

        if perms_needed or protected:
            title = _("Cannot delete %(name)s") % {"name": objects_name}
        else:
            title = _("Are you sure you want to permanently delete the selected "+ objects_name +"  from the site?")

        context = dict(
            modeladmin.admin_site.each_context(request),
            title=title,
            objects_name=objects_name,
            deletable_objects=[deletable_objects],
            model_count=dict(model_count).items(),
            queryset=queryset,
            perms_lacking=perms_needed,
            protected=protected,
            opts=opts,
            action_checkbox_name=helpers.ACTION_CHECKBOX_NAME,
        )

        request.current_app = modeladmin.admin_site.name

        # Display the confirmation page
        return TemplateResponse(request, modeladmin.delete_selected_confirmation_template or [
            "admin/%s/%s/delete_selected_confirmation_tenant_user.html" % (app_label, opts.model_name),
            "admin/%s/delete_selected_confirmation_tenant_user.html" % app_label,
            "admin/delete_selected_confirmation_tenant_user.html"
        ], context)
    custom_delete_selected.short_description = ugettext_lazy("Delete selected %(verbose_name_plural)s")

    csrf_protect_m = method_decorator(csrf_protect)

    @csrf_protect_m
    @transaction.atomic
    def delete_view(self, request, object_id, extra_context=None):
        "The 'delete' admin view for this model."
        opts = self.model._meta
        app_label = opts.app_label

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        obj = self.get_object(request, unquote(object_id), to_field)

        if not self.has_delete_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(
                _('%(name)s object with primary key %(key)r does not exist.') %
                {'name': force_text(opts.verbose_name), 'key': escape(object_id)}
            )

        # Populate deleted_objects, a data structure of all related objects that
        # will also be deleted.
        deleted_objects, model_count, perms_needed, protected = get_deleted_objects([obj], request, self.admin_site)

        # import pdb; pdb.set_trace()
        if request.POST:  # The user has already confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = force_text(obj)
            attr = str(to_field) if to_field else opts.pk.attname
            obj_id = obj.serializable_value(attr)
            obj.remove_all_site_groups_for_schema(connection.schema_name)
            self.log_deletion(request, obj, obj_display)

            return self.response_delete(request, obj_display, obj_id)

        object_name = force_text(opts.verbose_name)

        if perms_needed or protected:
            title = _("Cannot delete %(name)s") % {"name": object_name}
        else:
            title = _("Are you sure you want to permanently delete the selected "+ object_name +"  from the site?")

        context = dict(
            self.admin_site.each_context(request),
            title=title,
            object_name=object_name,
            object=obj,
            deleted_objects=deleted_objects,
            model_count=dict(model_count).items(),
            perms_lacking=perms_needed,
            protected=protected,
            opts=opts,
            app_label=app_label,
            preserved_filters=self.get_preserved_filters(request),
            is_popup=(IS_POPUP_VAR in request.POST or
                      IS_POPUP_VAR in request.GET),
            to_field=to_field,
        )
        context.update(extra_context or {})

        return self.render_delete_form(request, context)

    def render_delete_form(self, request, context):
        opts = self.model._meta
        app_label = opts.app_label

        request.current_app = self.admin_site.name
        context.update(
            to_field_var=TO_FIELD_VAR,
            is_popup_var=IS_POPUP_VAR,
        )

        return TemplateResponse(request,
            self.delete_confirmation_template or [
                "admin/{}/{}/delete_confirmation_tenant_user.html".format(app_label, opts.model_name),
                "admin/{}/delete_confirmation_tenant_user.html".format(app_label),
                "admin/delete_confirmation_tenant_user.html"
            ], context)

# class TenantUserInline(admin.TabularInline):
#     model = BGUser

class UserRequestAdmin(ModelAdmin):
    readonly_fields = ('user', 'comments')
#     inlines = (TenantUserInline,)

tenant_admin_site.register(TenantUser, TenantUserAdmin)

# tenant_admin_site.register(UserRequest, UserRequestAdmin)



IS_POPUP_VAR = '_popup'
TO_FIELD_VAR = '_to_field'

@admin.register(Official, site=tenant_admin_site)
class OfficialAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_names','company_name')
    actions = ["make_inactive"]
    ordering = ('last_name',)
    exclude = ("email", "phone_number", "second_phone_number", "address", "used_on", "title", "deleted_at")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_queryset(self, request):
        qs = self.model.all_objects.filter(deleted_at=None)
        # The below is copied from the base implementation in BaseModelAdmin to prevent other changes in behavior
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def make_inactive(self, request, queryset):
        updated = queryset.update(deleted_at=timezone.now())
        self.message_user(request, ngettext(
            '%d Official was successfully marked as archived.',
            '%d Officials were successfully marked as archived.',
            updated,
        ) % updated, messages.SUCCESS)

    make_inactive.short_description = ugettext_lazy("Archive selected %(verbose_name_plural)s")

'''
    def get_actions(self, request):
        actions = super(OfficialAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
'''

'''
    def render_delete_form(self, modeladmin, request, context):
        fk_related = False
        if not request.POST:
            #Check if the official has burial related
            # import pdb; pdb.set_trace()
            if len(context['object'].burial_set.all()) > 0:
                fk_related = True
                context['title'] = 'Warning'
        opts = modeladmin.model._meta
        app_label = opts.app_label

        request.current_app = modeladmin.admin_site.name
        context.update(
            to_field_var=TO_FIELD_VAR,
            is_popup_var=IS_POPUP_VAR,
            fk_related=fk_related,
        )
        return TemplateResponse(request,
            modeladmin.delete_confirmation_template or [
                "admin/{}/{}/delete_confirmation.html".format(app_label, opts.model_name),
                "admin/{}/delete_confirmation.html".format(app_label),
                "admin/delete_confirmation.html"
            ], context)
'''
'''
    def custom_delete_selected(self, modeladmin, request, queryset):
        """
        Default action which deletes the selected objects.

        This action first displays a confirmation page whichs shows all the
        deleteable objects, or, if the user has no permission one of the related
        childs (foreignkeys), a "permission denied" message.

        Next, it deletes all selected objects and redirects back to the change list.
        """
        #Check if the official has burial related
        fk_related = False
        for offi in queryset:
            if len(offi.burial_set.all()) > 0:
                fk_related = True

        opts = modeladmin.model._meta
        app_label = opts.app_label

        # Check that the user has delete permission for the actual model
        if not modeladmin.has_delete_permission(request):
            raise PermissionDenied

        # Populate deletable_objects, a data structure of all related objects that
        # will also be deleted.
        
        deletable_objects, model_count, perms_needed, protected = get_deleted_objects(queryset, request, self.admin_site)
        # import pdb; pdb.set_trace()
        # The user has already confirmed the deletion.
        # Do the deletion and return a None to display the change list view again.
        if request.POST.get('post'):
            if perms_needed:
                raise PermissionDenied
            n = queryset.count()
            if n:
                for obj in queryset:
                    obj_display = force_text(obj)
                    modeladmin.log_deletion(request, obj, obj_display)
                queryset.delete()
                modeladmin.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                    "count": n, "items": model_ngettext(modeladmin.opts, n)
                }, messages.SUCCESS)
            # Return None to display the change list page again.
            return None

        if len(queryset) == 1:
            objects_name = force_text(opts.verbose_name)
        else:
            objects_name = force_text(opts.verbose_name_plural)

        if perms_needed or protected:
            title = _("Cannot delete %(name)s") % {"name": objects_name}
        else:
            if fk_related:
                title = _("Warning")
            else:
                title = _("Are you sure?")

        context = dict(
            modeladmin.admin_site.each_context(request),
            title=title,
            objects_name=objects_name,
            deletable_objects=[deletable_objects],
            model_count=dict(model_count).items(),
            queryset=queryset,
            perms_lacking=perms_needed,
            protected=protected,
            opts=opts,
            action_checkbox_name=helpers.ACTION_CHECKBOX_NAME,
            fk_related=fk_related,
        )

        request.current_app = modeladmin.admin_site.name

        # Display the confirmation page
        return TemplateResponse(request, modeladmin.delete_selected_confirmation_template or [
            "admin/%s/%s/delete_selected_confirmation_official.html" % (app_label, opts.model_name),
            "admin/%s/delete_selected_confirmation_official.html" % app_label,
            "admin/delete_selected_confirmation_official.html"
        ], context)

    custom_delete_selected.short_description = ugettext_lazy("Delete selected %(verbose_name_plural)s")
'''


# @admin.register(Person, site=tenant_admin_site)
class PersonAdmin(admin.ModelAdmin):
    # actions = None
    list_display = ('last_name','first_names','get_age_years', 'get_burial_date')
    # search_fields = ['last_name', ]
    # fields = ('title', 'first_names','last_name', 'profession')
    ordering = ('last_name',)
    fieldsets = [(None, {'fields':()}),]

    def __init__(self, *args, **kwargs):
        super(PersonAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = None

    def has_add_permission(self, request):
        return False

    # def has_change_permission(self, request):
    #     return False

tenant_admin_site.register(Person, PersonAdmin)

class ImageAdmin(admin.ModelAdmin):
    # actions = None
    list_display = ('url',)
    search_fields = ['url', ]
    # fields = ('title', 'first_names','last_name', 'profession')
    ordering = ('url',)
    fieldsets = [(None, {'fields':()}),]

    def __init__(self, *args, **kwargs):
        super(ImageAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = None

tenant_admin_site.register(Image, ImageAdmin)


#Geographic admingis

# if settings.DEBUG:
#     openlayers_url = 'libs/OpenLayers-2.13/OpenLayers.js'
# else:
    # openlayers_url = StaticS3Storage().url(str('libs/OpenLayers-2.13/OpenLayers.js'))

class OSMGeoAdminSite(admingis.OSMGeoAdmin):

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if request.user.is_staff:
            self.form.base_fields['user_created'] = forms.BooleanField(required=False, initial=False, disabled=False)
        else:
            self.form.base_fields['user_created'] = forms.BooleanField(required=False, initial=True, disabled=True)
        return super(OSMGeoAdminSite, self).changeform_view(request, object_id, form_url, extra_context)

    def get_changeform_initial_data(self, request):
        if request.user.is_staff:
            return {'user_created': False}
        else:
            return {'user_created': True}

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return request.user.is_staff or obj.user_created
        else:
            return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return request.user.is_staff or obj.user_created
        else:
            return request.user.is_staff

    # map_template = 'gis/admin/osm.html'
    map_template = 'gis/admin/openlayers.html'
    num_zoom = 20
    map_srid = 27700
    max_extent = False
    max_extent = '-3276800, -3276800, 3276800, 3276800'
    max_resolution = '1'
    point_zoom = num_zoom - 6
    units = 'm'

    default_lon = 0
    default_lat = 0
    default_zoom = 10
    display_wkt = False
    display_srid = True
    extra_js = []
    max_zoom = 100
    min_zoom = 100
    modifiable = True
    mouse_position = True
    scale_text = True
    layerswitcher = True
    scrollable = True
    map_width = 800
    map_height = 400
    # openlayers_url = openlayers_url #http://openlayers.org/api/2.13/OpenLayers.js'
    openlayers_url = 'https://openlayers.org/api/2.13/OpenLayers.js'
    wms_url = 'https://t0.ads.astuntechnology.com/open/osopen/service?'
    wms_layer = 'osopen'
    wms_name = 'osopen WMS'
    # wms_options = {'format': 'image/jpeg'}
    wms_options = {'format': 'image/png'}
    # debug = True

    fieldsets = (
        (None, {'fields': ('id', 'layer', 'feature_id', 'date_uploaded', 'geometry', 'user_created', 'surveyor', 'geom_acc')}),
    )
    readonly_fields = ('id', 'date_uploaded')
    list_display = ('id', 'feature_id', 'date_uploaded', 'user_created', 'layer')
    list_filter = ('layer', 'feature_id')
    search_fields = ('id',)
    ordering = ('layer',)



class OSMGeoAdminSitePolylines(OSMGeoAdminSite):
    pass

class OSMGeoAdminSitePoints(OSMGeoAdminSite):
    fieldsets = (
        (None, {'fields': OSMGeoAdminSite.fieldsets[0][1].get("fields") + ('veg_spread',)}),
    )

# import pdb; pdb.set_trace()
# tenant_admin_site.register(TopoPolygons, admin.GeoModelAdmin)
# tenant_admin_site.register(TopoPolygons, admin.OSMGeoAdmin)
tenant_admin_site.register(TopoPolygons, OSMGeoAdminSite)
tenant_admin_site.register(TopoPolylines, OSMGeoAdminSitePolylines)
tenant_admin_site.register(TopoPoints, OSMGeoAdminSitePoints)

#class AttributesInline(admin.TabularInline):
#    model = FeatureCode
#    fields = ('attribute',)

class LayerAdmin(admin.ModelAdmin):
    # actions = None
    #inlines = [
    #    AttributesInline,
    #]
    list_display = ('display_name', 'show_in_toolbar', 'initial_visibility', 'min_resolution', 'max_resolution')
    search_fields = ['display_name',]
    ordering = ('display_name',)
    fields = ('feature_code', 'display_name', 'show_in_toolbar', 'initial_visibility', 'min_resolution', 'max_resolution')
    readonly_fields = ('feature_code',)

    def __init__(self, *args, **kwargs):
        super(LayerAdmin, self).__init__(*args, **kwargs)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

tenant_admin_site.register(Layer, LayerAdmin)

#END Geographic admin

class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    list_display = ('name', 'type')
    ordering = ('name',)
    filter_horizontal = ('feature_codes',)
    form = SurveyTemplateFieldForm

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'feature_codes':
            kwargs["queryset"] = FeatureCode.objects.filter(type='vector')

        return db_field.formfield(**kwargs)

tenant_admin_site.register(Attribute, AttributeAdmin)

class EventCategoryAdmin(admin.ModelAdmin):
    model = EventCategory
    list_display = ('name',)
    ordering = ('name',)

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

tenant_admin_site.register(EventCategory, EventCategoryAdmin)

class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
    list_display = ('name', 'category')
    ordering = ('name',)

    def category(self, obj):
        return obj.event_category.name
    
class SettingsAdmin(admin.ModelAdmin):
    model = Settings
    list_display = ('name',)
    readonly_field = ('id',)
    formfield_overrides = {       
        fields.JSONField: {'widget': JSONEditorWidget}, # if django < 3.1
        #models.JSONField: {'widget': JSONEditorWidget},
    }
tenant_admin_site.register(Settings, SettingsAdmin)

class CustomPersonField(admin.ModelAdmin):
    change_form_template = 'main/custom_person_field.html'
    model = PersonField
    list_display = ('name',)
    readonly_field = ('id',)
    ordering = ('name',)
    extra = 0

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Field Customisation'}
        return super(CustomPersonField, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if object_id is not None:
            data_person = PersonField.objects.get(id=object_id).__dict__
            data_person['_state'] = data_person['_state'].__dict__
            extra_context = {'data': data_person}

        extra_context['title'] = 'Field Customisation'
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_change_permission(self, request, obj=None):
        return request.user.is_active

class MeetingLocationAdmin(admin.ModelAdmin):
    model= MeetingLocation
    list_display = ('location_address',)
    ordering = ('location_address',)

    def category(self, obj):
        return obj.meeting_location.location_address

class siteReferenceSettingsAdmin(admin.ModelAdmin):
    model = siteReferenceSettings
    list_display = ('ref_style','start_number',)
    ordering = ('start_number',)
    fieldsets =((
        None, {
            'fields': ('start_number','ref_style',)
        }),
        )
    def save_model(self, request, obj, form, change):
        if not obj.burialgroundsite_id:
            site = BurialGroundSite.objects.get(schema_name=connection.schema_name)
            obj.burialgroundsite_id = site.id
        obj.save()

    def has_add_permission(self, request):
        site = BurialGroundSite.objects.get(schema_name=connection.schema_name)
        queryset = super(siteReferenceSettingsAdmin, self).get_queryset(request)
        qs = queryset.filter(burialgroundsite_id = site.id)
        if qs.count() >= 1:
            return False
        return super().has_add_permission(request)

    def get_queryset(self, request):
        """
        Filter the objects displayed in the SITE REFERNENCE SETTINGS to only
        display those for the current burial ground site.
        """
        site = BurialGroundSite.objects.get(schema_name=connection.schema_name)
        queryset = super(siteReferenceSettingsAdmin, self).get_queryset(request)

        return queryset.filter(burialgroundsite_id = site.id)

tenant_admin_site.register(EventType, EventTypeAdmin)
tenant_admin_site.register(MeetingLocation, MeetingLocationAdmin)
tenant_admin_site.register(siteReferenceSettings, siteReferenceSettingsAdmin)

tenant_admin_site.register(SiteSurveyTemplateField, SiteSurveyTemplateFieldAdmin)
tenant_admin_site.register(SurveyTemplate, SurveyTemplateAdmin)
tenant_admin_site.register(PersonField, CustomPersonField)
