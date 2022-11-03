from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.gis.geos import Point
from django.core import serializers
from django.core.exceptions import PermissionDenied
#v1.8. from django.core.serializers import serialize
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.db.models import Q

from rest_framework import permissions

from bgsite.models import Memorial, Person, Death, Image
from main.models import ImageState, ImageType, BurialGroundSite
from main.templatetags import perm_filters

import json

def login_required_custom(function):
    """ Check if user is authenticated """

    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_authenticated:
            return function(request, *args, **kw)
        else:
            if BurialGroundSite.site_has_public_access():
                return HttpResponseForbidden()
            else:
                return HttpResponseForbidden(settings.LOGIN_URL)

    return wrapper

def public_access_or_login_required(function):
    """ Check if site has public access or the user is authenticated """

    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_authenticated or BurialGroundSite.site_has_public_access():
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrapper

def has_bereavement_site_access(function):
    """  """

    def check_sites(request, *args, **kw):
      """Check if user is admin with all permissions"""
      user = request.user
      has_permission = user.is_superuser

      """if not, just check if user has bevearement stuff access to some sites"""
      if not has_permission:
        """ Getting for all bevearement stuff sites """    
        burialgroundsite_ids = user.site_groups.filter(Q(group__name='SiteAdmin') | Q(group__name='BereavementStaff')).values_list('burialgroundsite_id', flat=True).distinct()
        sites = BurialGroundSite.objects.filter(id__in=burialgroundsite_ids)
        """ Checking if the user has at least one bereavement staff site permission  """
        has_permission = len(sites) > 0

      if has_permission:
        return function(request, *args, **kw)
      else:
        raise PermissionDenied()
        return HttpResponseForbidden()

    return check_sites

"""Requires user membership in at least one of the groups passed in."""
def in_groups(u, group_names, raise_exception=False):
    if u.is_superuser:
        return True
    elif u.is_authenticated:
        site_groups = u.site_groups.filter(burialgroundsite__schema_name__exact=connection.schema_name)
        for site_group in site_groups:
            if bool(site_group.group.name in group_names):
                return True
        # raise exception when logged in but don't have access to this site
        raise_exception = True
    if raise_exception:
        raise PermissionDenied
    return False

#check if the user is authenticated and has the group as a decorator
def group_required(*group_names, raise_exception=False):

    def is_in_groups(u):
        return in_groups(u, group_names, raise_exception)

    return user_passes_test(is_in_groups)

#check if site has public access or the user is authenticated and has the group as a decorator
def public_access_or_group_required(*group_names, raise_exception=False):

    def is_in_groups(u):
        if not u.is_authenticated and BurialGroundSite.site_has_public_access():
            return True

        return in_groups(u, group_names, raise_exception)

    return user_passes_test(is_in_groups)


@method_decorator(login_required_custom, name='dispatch')
class AuthenticatedView(View):
    """
    Basic authenticated view. Most views (not APIView, they are checked by default) must extend at least this.
    View requires user to be logged in.
    """


@method_decorator([public_access_or_login_required, public_access_or_group_required('SiteUser', 'SiteWarden', 'SiteAdmin')], name='dispatch')
class PublicAccessOrViewOnlyView(View):
    """Requires site to be public or user to have view-only permissions for the site."""


@method_decorator([login_required_custom, group_required('SiteUser', 'SiteWarden', 'SiteAdmin')], name='dispatch')
class ViewOnlyView(View):
    """Requires User to have view-only permissions for the site."""


@method_decorator([login_required_custom, group_required('DataMatcher', 'SiteWarden', 'SiteAdmin')], name='dispatch')
class DataMatchView(View):
    """Requires User to have view-only permissions for the site."""


@method_decorator([login_required_custom, group_required('DataEntry', 'SiteWarden', 'SiteAdmin')], name='dispatch')
class DataEntryView(View):
    """Requires User to have view-only permissions for the site."""


@method_decorator([login_required_custom, group_required('MemorialPhotographer', 'SiteWarden', 'SiteAdmin')], name='dispatch')
class MemorialPhotographyView(View):
    """Requires User to have view-only permissions for the site."""


@method_decorator([login_required_custom, group_required('SiteWarden', 'SiteAdmin', raise_exception=True)], name='dispatch')
class WardenView(View):
    """Warden group authenticated view.
    Requires user to be part of group SiteWarden.
    User can do everything a SiteAdmin can, except 
    login to admin portal"""


@method_decorator([login_required_custom, group_required('SiteAdmin', raise_exception=True)], name='dispatch')
class AdminView(View):
    """Admin group authenticated view.
    Requires user to be part of group SiteAdmin"""


@method_decorator([login_required_custom, group_required('AGAdmin', raise_exception=True)], name='dispatch')
class AGAdminView(View):
    """AGAdmin group authenticated view.
    Requires user to be part of group AGAdmin """

@method_decorator([login_required_custom, has_bereavement_site_access], name='dispatch')
class BStaffView(View):
    """BereavementStaff group authenticated view.
    Requires user to be part of BereavementStaff group """


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form, responseData):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            return JsonResponse(responseData)
        else:
            return response

class GroupRequiredView(View):

    template_name = "main/home.html"
    def get(self,request):
        group_names = json.loads(request.GET.get('group_names'))# json.loads(data)['group_names']
        result = perm_filters.group_required(request.user, group_names)
        return JsonResponse({"status":"ok", "group_required": result})

class UserGroupsView(PublicAccessOrViewOnlyView):

    def get(self, request):
        result = perm_filters.get_groups(request.user)
        groups = list(result) if result else None
        return JsonResponse({"status":"ok", "groups": groups}, safe=False)

class SiteDetailsView(PublicAccessOrViewOnlyView):

    def get(self, request):
        return JsonResponse({**BurialGroundSite.get_site_details(), **BurialGroundSite.get_site_documents()}, safe=False)