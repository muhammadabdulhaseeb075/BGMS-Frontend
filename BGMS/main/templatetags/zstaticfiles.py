from django import template
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage
from config.storages.staticS3storage import StaticShareS3Storage

register = template.Library()

@register.simple_tag
def static_original(url):
    if settings.DEBUG:
        return settings.STATIC_URL + url
    else:
        return S3BotoStorage().url(url)

@register.simple_tag
def static_sign(url):
    if settings.DEBUG:
        return settings.STATIC_URL + url
    else:
        return StaticShareS3Storage().url(url)

@register.simple_tag
def get_static_prefix_s3():
    return settings.STATIC_URL
