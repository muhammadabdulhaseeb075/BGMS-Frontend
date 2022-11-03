from django.urls import path
from cemeteryadminpublic import views

app_name = 'cemeteryadminpublic'

urlpatterns = [
    path('funeralEvents/', views.FuneralEventsView.as_view()),
]