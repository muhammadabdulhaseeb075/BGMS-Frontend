""" URL dispatcher for bgsite endpoints """

from django.urls import path
from bgsite.common_apis import views

app_name = 'bgsite'

urlpatterns = [
    path('address/', views.PublicAddressView.as_view()),
    path('company/', views.PublicCompanyView.as_view()),
    path('graveOwnersList/person/current/<str:graveplot_id>', views.CurrentPersonGraveOwnersListView.as_view()),
    path('graveplotType/all/', views.GraveplotTypesListView.as_view()),
    path('memorialInscriptions/', views.MemorialInscriptionsView.as_view()),
    path('person/', views.PublicPersonView.as_view()),
]