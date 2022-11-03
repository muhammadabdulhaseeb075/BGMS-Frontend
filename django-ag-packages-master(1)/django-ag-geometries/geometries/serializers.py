from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField

from geometries.models import TopoPolylines, TopoPoints, TopoPolygons, Feature, Attribute, FeatureAttributes
from geometriespublic.models import PublicAttribute


class FeatureGeoSerializer(GeoFeatureModelSerializer):

    marker_type = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    class Meta:
        model = Feature
        fields = ('id', 'geometry', 'marker_type', 'label')
        geo_field = "geometry"
        abstract = True

    def get_marker_type(self, obj):        
        marker_type = self.context.get("marker_type")
        if marker_type:
            return marker_type
        try:
            return obj['marker_type']
        except:
            return obj.layer.feature_code.feature_type

    def get_label(self, obj):
        try:
            return obj['label']
        except:
            return None

class TopoPolygonGeoSerializer(FeatureGeoSerializer):

    class Meta(FeatureGeoSerializer.Meta):
        model = TopoPolygons

class TopoPolylineGeoSerializer(FeatureGeoSerializer):

    class Meta(FeatureGeoSerializer.Meta):
        model = TopoPolylines

class TopoPointGeoSerializer(FeatureGeoSerializer):

    veg_spread = serializers.SerializerMethodField()

    class Meta(FeatureGeoSerializer.Meta):
        model = TopoPoints
        fields = FeatureGeoSerializer.Meta.fields + ('veg_spread',)

    def get_veg_spread(self, obj):
        try:
            return obj['veg_spread']
        except:
            return None