from django.conf.urls import url

from .views import CreateTemplateView
from django.views.generic.base import TemplateView
from dataentry.views import DataEntryView, AddBurialRecordView, GetTemplateView,\
    DynamicFormView, FinishedImageView, SkipImageView, GetTagView,\
    GetTemplateList, DeleteTemplateView, EditTemplateView,\
    DeleteBurialRecordView, SaveImageCommentsView, ChangeImageView,\
    UpdateBurialRecordView, DeleteBurialOfficialView, GetImageStatus,\
    ChangeToImageById, NextImageView, PrevImageView, GetUserActivity

app_name = 'dataentry'
 
urlpatterns = [
#     url(r'^$', DataMatchingView.as_view(), name='matching'),
    url(r'^$', DataEntryView.as_view(), name="index"),
    url(r'^listTemplates/', GetTemplateList.as_view(), name="listTemplates"),
    url(r'^createTemplate/', CreateTemplateView.as_view(), name="createTemplate"),
    url(r'^addBurialRecord/', AddBurialRecordView.as_view(), name="addBurialRecord"),
    url(r'^getTemplate/', GetTemplateView.as_view(), name="getTemplate"),
    url(r'^editTemplate/', EditTemplateView.as_view(), name="editTemplate"),
    url(r'^deleteTemplate/', DeleteTemplateView.as_view(), name="deleteTemplate"),
    url(r'^getDynamicForm/', DynamicFormView.as_view(), name="getDynamicForm"),
    url(r'^deleteBurialRecord/', DeleteBurialRecordView.as_view(), name="deleteBurialRecord"),
    url(r'^updateBurialRecord/', UpdateBurialRecordView.as_view(), name="updateBurialRecord"),
    url(r'^deleteBurialOfficial/', DeleteBurialOfficialView.as_view(), name="deleteBurialOfficial"),
    url(r'^finishedImage/', FinishedImageView.as_view(), name="finishedImage"),
    url(r'^skipImage/', SkipImageView.as_view(), name="skipImage"),
    url(r'^changeImage/', ChangeImageView.as_view(), name="changeImage"),
    url(r'^saveImageComment/', SaveImageCommentsView.as_view(), name="saveImageComment"),
    url(r'^getTags/', GetTagView.as_view(), name="getTags"),
    url(r'^getImageStatus/', GetImageStatus.as_view(), name="getImageStatus"),
    url(r'^getUserActivity/', GetUserActivity.as_view(), name="getUserActivity"),
    url(r'^changeToImage/', ChangeToImageById.as_view(), name="changeToImage"),
    url(r'^nextImage/', NextImageView.as_view(), name="nextImage"),
    url(r'^prevImage/', PrevImageView.as_view(), name="prevImage"),
]