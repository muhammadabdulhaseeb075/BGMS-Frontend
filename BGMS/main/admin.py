from django.contrib import admin
from main.models import BurialGroundSite, SiteGroup, SiteGroupSite, BGUser,\
    SiteDetails, Address, BurialOfficialType, Currency, Client, SitePreferences
from django import forms
from django.db import connection, transaction
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from django.conf import settings
from main.forms import SiteDetailsAdminForm
from django.core.exceptions import PermissionDenied
from django.contrib.admin.options import csrf_protect_m
from bgsite.models import Burial_Official
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

class BGUserAdmin(UserAdmin):
    model = get_user_model()
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', '_is_staff', 'is_superuser',
                                       'site_groups',)}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_superuser', '_is_staff', 'is_active', 'site_groups__group', 'site_groups__burialgroundsite__name')
    # possibly broken?
    filter_horizontal = ('site_groups',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # import pdb; pdb.set_trace()
        if db_field.name == "site_groups" and connection.schema_name != 'public':
            kwargs["queryset"] = SiteGroupSite.objects.exclude(group__name='SiteAdmin')
        return super(BGUserAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class SiteGroupsInline(NestedStackedInline):
    model = SiteGroup
    extra = 0

class BurialGroundSiteInline(admin.TabularInline):
    model = BurialGroundSite
    exclude = ('domain_url', 'schema_name')
    inlines = []

class BurialGroundSiteChangeInline(NestedStackedInline):
    model = BurialGroundSite
    exclude = ('domain_url', 'schema_name')
    inlines = [SiteGroupsInline]

class SitePreferencesInline(admin.TabularInline):
    form = SiteDetailsAdminForm
    model = SitePreferences
    inlines = []

class SiteDetailsAdmin(NestedModelAdmin):
    fieldsets = (
        (None, {'fields': ('layer', 'extent', 'address', 'aerial', 'plans',)}),
    )
    autocomplete_fields = ['address']

    # SiteGroupsInline inline is only shown when editing existing
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [BurialGroundSiteChangeInline, SitePreferencesInline]
        return super(SiteDetailsAdmin, self).change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = [BurialGroundSiteInline, SitePreferencesInline]
        return super(SiteDetailsAdmin, self).add_view(request, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['layer'] = form_data['layer'].lower()
            # Create BurialGroundSite obj
            if settings.DEBUG:
                domain_url = '{0}.bgms.com'.format(form_data['layer'])
            else:
                domain_url = '{0}.burialgrounds.co.uk'.format(form_data['layer'])
            schema_name = form_data['layer']
            if obj.layer:
                obj.layer = obj.layer.lower()
            obj.burialgroundsite.domain_url = domain_url
            obj.burialgroundsite.schema_name = schema_name
            obj.save()

        else:
            return HttpResponseBadRequest(form.errors)


class ClientAdmin(admin.ModelAdmin):

    model = Client
    exclude = ('created_by',)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class AddressAdmin(admin.ModelAdmin):

    search_fields = ['first_line', 'town', 'postcode']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

@admin.register(BurialOfficialType)
class BurialOfficialTypeAdmin(admin.ModelAdmin):
    delete_confirmation_template = "admin/delete_confirmation_burial_official_type.html"
    delete_selected_confirmation_template = "admin/delete_confirmation_burial_official_type.html"

    @csrf_protect_m
    @transaction.atomic
    def delete_view(self, request, object_id, extra_context=None):
        # checking if any burial_officials are linked to this type
        old_schema = connection.schema_name
        can_delete = True
        sites = BurialGroundSite.objects.all()
        obj = BurialOfficialType.objects.get(id=object_id)
        for site in sites:
            if site.schema_name!='public':
                connection.schema_name = site.schema_name
                print(connection.schema_name)
                if Burial_Official.objects.filter(burial_official_type=obj).exists():
                    can_delete = False
                    break
        connection.schema_name = old_schema
        if can_delete:
            return admin.ModelAdmin.delete_view(self, request, object_id, extra_context=extra_context)
        else:
            return admin.ModelAdmin.delete_view(self, request, object_id, extra_context={'fk_related': True, 'title': "Cannot delete %(name)s"% {"name": obj.official_type}})

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(get_user_model(), BGUserAdmin)
admin.site.register(SiteDetails, SiteDetailsAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(SiteGroupSite)
admin.site.register(Currency, CurrencyAdmin)
