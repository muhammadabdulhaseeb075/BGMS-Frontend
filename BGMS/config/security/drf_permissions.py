"""
Django Rest Framework authentication and authorisation
"""

from rest_framework import permissions

from bgsite.views import in_groups
from main.models import BurialGroundSite

class IsAuthenticatedCustom(permissions.BasePermission):
    """
    This is the default for drf APIs. Set in default settings.
    User must be authenticated AND be authorised to have basic access.
    """

    def has_permission(self, request, view):
        return in_groups(request.user, [ 'SiteUser', 'SiteAdmin', 'SiteWarden' ], True)

class IsAuthenticatedOrPublicAccessReadOnly(permissions.BasePermission):
    """
    User must be authenticated and authorised, or the site must have public access.
    Read only permission for users who are unauthenticated on a public access site.
    """

    def has_object_permission(self, request, view, obj):
        # Read permission - always allow for GET request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions - only if authenticated
        return request.user and request.user.is_authenticated()

    def has_permission(self, request, view):
        return BurialGroundSite.site_has_public_access() or in_groups(request.user, [ 'SiteUser', 'SiteAdmin', 'SiteWarden' ], True)

class BereavementStaffPermission(permissions.BasePermission):
    """
    Global permission check if user has access to bereavement services.
    Used with DRF.
    """

    def has_permission(self, request, view):
        return in_groups(request.user, [ 'BereavementStaff', 'SiteAdmin' ], True)