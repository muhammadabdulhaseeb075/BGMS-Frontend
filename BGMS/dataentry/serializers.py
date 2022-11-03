from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField

from bgsite.models import Tag


class TagGeoSerializer(GeoFeatureModelSerializer):

    envelope = GeometrySerializerMethodField()
    image__id = serializers.SerializerMethodField()
    person__id = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'envelope', 'image__id', 'person__id')
        extra_kwargs = {'envelope': {'required':True}}
        geo_field = "envelope"

    def get_envelope(self, obj):
        person_data = obj['person__deleted_at']
        if person_data is None:
            return obj['envelope']

    def get_image__id(self, obj):
        return obj['image__id']

    def get_person__id(self, obj):
        return obj['person__id']