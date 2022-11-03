from django import template
from config.storages.media_storages import TenantMediaStorage

register = template.Library()

@register.simple_tag
def mediafiles(url):
    return TenantMediaStorage().url(url)
