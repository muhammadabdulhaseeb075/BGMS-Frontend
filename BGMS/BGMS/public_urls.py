from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetCompleteView
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView

from bgsite.views_admin import ResetAuthView
from main import views

urlpatterns = [
    path('', include('main.urls', namespace="main")),
    path('cemeteryadminpublic/', include('cemeteryadminpublic.urls', namespace="cemeteryadminpublic")),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^sitemanagement/', include((admin.site.urls[0], admin.site.urls[1]), namespace=admin.site.urls[2])),
    url(r'^register/$', views.RegisterView.as_view(), name="register"),
    url(r'^confirm/(?P<activation_key>\w+)', views.ConfirmMailView.as_view()),
    url(r'^analytics/', include('analytics.urls', namespace="analytics")),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='/'), name="logout"),
    # url(r'^redirect/$', views.TenantRedirectView.as_view(), name='tenant_redirect'),
    url(r'^redirect/$', views.TenantRedirectAjaxView.as_view(), name='tenant_redirect'),
    url(r'^403/$', TemplateView.as_view(template_name='403.html')),
    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    url(r'^500/$', TemplateView.as_view(template_name='500.html')),
    path('request_reset/$', views.ResetRequestView.as_view(), name="request_reset"),
    path('reset/<uidb64>/<token>/', views.ConfirmPasswordResetView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='reset_done.html'), name='password_reset_complete'),
]

# from django.conf import settings
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += (url(r'^__debug__/', include(debug_toolbar.urls)),)
