from django.conf.urls import include, url
from bgsite.tests.views import DummyAuthenticatedView, DummyViewOnlyView, DummyAdminView

# urlpatterns = [
    # Examples:
    # url(r'^$', 'BGMS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#     url(r'^', include('BGMS.urls')),
#     url(r'^test_authenticated_view/$', DummyAuthenticatedView.as_view(), name='test_authenticated_view'),
#     url(r'^test_view_only_view/$', DummyViewOnlyView.as_view(), name='test_view_only_view'),
#     url(r'^test_aadmin_view/$', DummyAdminView.as_view(), name='test_aadmin_view'),
# ]