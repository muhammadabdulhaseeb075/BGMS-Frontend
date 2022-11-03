from django.urls import include, path
from django.conf.urls import url
from django.views.generic import TemplateView
from bgsite.admin import tenant_admin_site
from django.views.generic.base import RedirectView
from bgsite.views import GroupRequiredView, UserGroupsView, SiteDetailsView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetCompleteView
from main.views import ResetRequestView, ConfirmPasswordResetView
from main.models import UserPasswordRequests

urlpatterns = [
    url(r'^mapmanagement/', include('mapmanagement.urls', namespace="mapmanagement")),
    path('geometries/', include('geometries.urls', namespace="geometries")),
    #url(r'geometries/', include('geometries.urls', namespace="geometries")),
    path('survey/', include('survey.urls', namespace="survey")),
    path('cemeteryadmin/', include('cemeteryadmin.urls', namespace="cemeteryadmin")),
    path('api/', include('bgsite.common_apis.urls', namespace="bgsite")),
    url(r'^dataentry/', include('dataentry.urls', namespace="dataentry")),
    url(r'^datamatching/', include('datamatching.urls', namespace="datamatching")),
    url(r'^analytics/', include('analytics.urls', namespace="analytics")),
    url(r'^$', RedirectView.as_view(pattern_name='mapmanagement:index', permanent=True)),
    url(r'^siteadminportal/', include((tenant_admin_site.urls[0], tenant_admin_site.urls[1]), namespace="tenant_admin")),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='/'), name="logout"),
    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    url(r'^500/$', TemplateView.as_view(template_name='500.html')),
    url(r'^bgsite/group_required/$', GroupRequiredView.as_view()),
    url(r'^bgsite/user_groups/$', UserGroupsView.as_view()),
    path('bgsite/sitedetails/', SiteDetailsView.as_view()),
    url(r'^sw(.*.js)$', TemplateView.as_view(template_name='sw.js', content_type='text/javascript')),
    path('request_reset/', ResetRequestView.as_view(), name="request_reset"),
    path('reset/<uidb64>/<token>/', ConfirmPasswordResetView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='reset_done.html'), name='password_reset_complete'),

]

#from django.conf import settings
#from django.conf.urls import include, url
##
DEBUG = True
#if DEBUG:
#   import debug_toolbar
#   urlpatterns += [
#       url(r'^__debug__/', include(debug_toolbar.urls)),
#   ]

#cloud based load testing tool?
#if 'loaderio' in settings.INSTALLED_APPS:
#    from loaderio.views import show_token
#    urlpatterns += [url(r'^(?P<token>loaderio-[0-9a-z]+)(?:\.txt|\.html|/)?$', show_token),]

if DEBUG:
    import mimetypes
    mimetypes.add_type("text/javascript", ".js", True)
