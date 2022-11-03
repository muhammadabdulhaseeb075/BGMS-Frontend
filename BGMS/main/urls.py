from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name="home"),
    path('main/', views.MainView.as_view(), name="main"),
    path('userAccess/', views.UserAccessView.as_view(), name="user_access"),
]