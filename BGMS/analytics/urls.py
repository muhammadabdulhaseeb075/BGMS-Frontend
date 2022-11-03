from django.conf.urls import url
from analytics.views import AnalyticsView, ModelsFields, ModelEntriesByField, FilterSuggestion, \
    GetAllReports, UpdateOneReport, ReportTemplatesView, ExcelExport

app_name="analytics"

urlpatterns = [
    url(r'^$', AnalyticsView.as_view(), name="index"),
    url(r'^models/$', ModelsFields.as_view(), name="models-endpoint"),
    url(r'^models/(?P<model_name>[a-zA-Z0-9_]+)/$', ModelEntriesByField.as_view(), name="model-entries-endpoint"),
    url(r'^models/(?P<model_name>[a-zA-Z0-9_]+)/filter-suggestion/', FilterSuggestion.as_view(), name="model-filter-suggestion"),

    url(r'^reports/$', GetAllReports.as_view(), name="report-operations"),
    url(r'^reports/(?P<id>[a-zA-Z0-9_]+)/$', UpdateOneReport.as_view(), name="report-update"),
    url(r'^export-reports/(?P<id>[a-zA-Z0-9_]+)/$', ExcelExport.as_view(), name="export-excel"),
    url(r'^report-templates/$', ReportTemplatesView.as_view(), name="report-templates")
]
