""" URL dispatcher for cemeteryadmin """

from django.urls import path
from cemeteryadmin import views

app_name = 'cemeteryadmin'
urlpatterns = [
    path('funeralCreators/', views.FuneralCreatorsView.as_view()),
    path('funeralDirector/', views.FuneralDirectorView.as_view()),
    path('funeralDirector/<str:pk>/', views.FuneralDirectorView.as_view()),
    path('funeralDirectorsList/', views.FuneralDirectorsListView.as_view()),
    path('funeralEvent/', views.FuneralEventView.as_view()),
    path('funeralEvent/<str:event_id>/', views.FuneralEventView.as_view()),
    path('funeralEvent/<str:event_id>/cancel/', views.CancelFuneralEventView.as_view()),
    path('calendarEvents/<str:start>/<str:end>/', views.CalendarEventsView.as_view()),
    path('preburialCheck/', views.PreburialCheckView.as_view()),
    #path('preburialCheck/<str:preburial_id>/', views.PreburialCheckView.as_view()),
    path('preburialCheck/<str:preburial_id>/<str:postburial_id>/<str:cancelburial_id>/', views.PreburialCheckView.as_view()),
    path('postburialCheck/', views.PostburialCheckView.as_view()),
    path('postburialCheck/<str:postburial_id>/', views.PostburialCheckView.as_view()),
    path('cancelburial/', views.CancelburialView.as_view()),
    path('cancelburial/<str:cancelburial_id>/', views.CancelburialView.as_view()),
    path('meetingLocation/', views.MeetingLocationView.as_view()),
    path('meetingLocation/<str:pk>/', views.MeetingLocationView.as_view()),
    path('meetingLocationsList/', views.MeetingLocationListView.as_view()),
    path('settings/<str:name>/', views.SettingsView.as_view()),
    #path('settings/<str:pk>/', views.SettingsView.as_view()),
    
]
