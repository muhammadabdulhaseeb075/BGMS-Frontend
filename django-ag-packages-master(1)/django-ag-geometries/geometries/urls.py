from django.conf.urls import url

from geometries.views import LayerView, ImportShapeFile,\
    SiteLayerNames, SiteAllLayerNames, FeatureAttributeMaterials

app_name = 'geometries'

urlpatterns = [
    # # ex: /mapmanagement/
    url(r'^getLayerNames/', SiteLayerNames.as_view()),
    url(r'getLayer/', LayerView.as_view()),
    url(r'^importShapeFile/', ImportShapeFile.as_view()),
    url(r'^getAllLayerNames/', SiteAllLayerNames.as_view()),
    url(r'^featureAttributeMaterials/', FeatureAttributeMaterials.as_view()),
]