from django import template
from django.contrib.auth.models import Group
from django.db import connection
register = template.Library()

#check if the user is authenticated and has the group as a decorator
@register.filter(name='group_required')
def group_required(u, group_names):
    """Requires user membership in at least one of the groups passed in."""
    if u.is_superuser:
        return True
    elif u.is_authenticated:
        site_groups = u.site_groups.filter(burialgroundsite__schema_name__exact=connection.schema_name)
        for site_group in site_groups:
            if bool(site_group.group.name in group_names):
                return True
    return False

#get the user's groups'
@register.filter(name='get_groups')
def get_groups(u):
    if u.is_superuser:
        return ['Superuser']
    elif u.is_authenticated:
        return u.site_groups.all().values_list('group__name', flat=True)
    return False

#check if the user is authenticated and has the group
@register.filter(name='has_group')
def has_group(u, group_name):
        if u.is_authenticated:
            if u.site_groups.filter(burialgroundsite__schema_name__exact=connection.schema_name).filter(group__name=group_name).exists():
                return True
        return False

#implement get function for dictionary
@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

#implement get function for dictionary
@register.filter(name='get_images')
def get_images(dictionary, key):
    return dictionary.get(key).get('images')
