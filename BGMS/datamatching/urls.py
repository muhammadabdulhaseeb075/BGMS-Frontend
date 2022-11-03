from django.conf.urls import url

from datamatching.views import DataMatchingView, DataMatchingSearchView, LinkPersonMemorialView, MemorialDetailsView, MemorialValidated, MemorialSkipped, ChangeMemorial, AddNewPersonView, ChangeToMemorialById, AddPersonView,\
    MemorialByImageSearch, BreakLink, UnmatchedMemorialsCountView, GetUserActivityView, GetMemorialStateView, DeathPersonDetailsView, PersonEditView, BurialRecordEditView, MemorialEditView
from django.views.generic.base import TemplateView

app_name = 'datamatching'

urlpatterns = [
    url(r'^$', DataMatchingView.as_view(), name='matching'),
    url(r'^searchPerson/', DataMatchingSearchView.as_view(), name="searchPerson"),
    url(r'^searchImages/', MemorialByImageSearch.as_view(), name="searchPerson"),
    url(r'^breakLink/', BreakLink.as_view(), name="breakLink"),
    url(r'^addPerson/', AddPersonView.as_view(), name="add_person"),
    url(r'^personSuccess/', TemplateView.as_view(template_name="datamatching/person-edit-success.html"), name="addPerson"),
    url(r'^unmatchedMemorials/', MemorialDetailsView.as_view(), name="unmatchedMemorials"),
    url(r'^unmatchedMemorialsCount/', UnmatchedMemorialsCountView.as_view(), name="unmatchedMemorialsCount"),
    url(r'^memorialValidated/', MemorialValidated.as_view(), name="memorialValidated"),
#     url(r'^markNameAsRevisit/', MarkNameAsRevisit.as_view(), name="markNameAsRevisit"),
    url(r'^memorialSkipped/', MemorialSkipped.as_view(), name="memorialSkipped"),
    url(r'^changeMemorial/', ChangeMemorial.as_view(), name="changeMemorial"),
    url(r'^changeToMemorialById/', ChangeToMemorialById.as_view(), name="changeToMemorialById"),
    url(r'^linkMemorial/', LinkPersonMemorialView.as_view(), name="linkMemorial"),
    url(r'^getUserActivity/', GetUserActivityView.as_view(), name="getUserActivity"),
    url(r'^getMemorialState/', GetMemorialStateView.as_view(), name="getMemorialState"),
    url(r'^personDetails/', DeathPersonDetailsView.as_view(), name="person_details"),
    url(r'^personEdit/', PersonEditView.as_view(), name="person_edit"),
    url(r'^burialEdit/', BurialRecordEditView.as_view(), name="burial_edit"),
    url(r'^memorialEdit/', MemorialEditView.as_view(), name="memorial_edit"),
]
