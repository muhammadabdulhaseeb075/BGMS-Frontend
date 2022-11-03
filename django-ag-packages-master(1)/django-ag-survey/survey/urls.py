from django.urls import path
from survey import views

app_name = 'survey'

urlpatterns = [
    path('', views.SurveyView.as_view(), name='survey'),
    path('featureSurveysList/', views.FeatureSurveysListView.as_view(), name='feature_surveys_list'),
    path('layerSurveyTemplates/', views.LayerSurveyTemplatesView.as_view(), name='layer_survey_templates'),
    path('layerSurveyTemplatesExist/', views.LayerSurveyTemplatesExistView.as_view(), name='layer_survey_templates_exist'),
    path('masterTemplate/', views.MasterTemplateView.as_view(), name='master_template'),
]