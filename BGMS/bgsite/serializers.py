from django.db.models import Q

from bgsite.models import Memorial, Burial, Person, Address

from rest_framework import serializers

from datetime import datetime, date
import uuid

class MemorialListShortSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='uuid')
    layer_name = serializers.SerializerMethodField()

    class Meta:
        model = Memorial
        fields = ('id', 'layer_name')

    def get_layer_name(self, obj):
        return obj.topopolygon.layer.feature_code.feature_type

class BurialListShortSerializer(serializers.ModelSerializer):

    graveplot_id = serializers.CharField(source='graveplot.uuid')

    class Meta:
        model = Burial
        fields = ('id', 'burial_date', 'graveplot_id')

class BurialSearchSerializer(serializers.ModelSerializer):

    death_date = serializers.DateField(source='death.death_date', allow_null=True, read_only=True)
    age_years = serializers.IntegerField(source='death.age_years', allow_null=True, read_only=True)
    age_months = serializers.IntegerField(source='death.age_months', allow_null=True, read_only=True)
    age_weeks = serializers.IntegerField(source='death.age_weeks', allow_null=True, read_only=True)
    age_days = serializers.IntegerField(source='death.age_days', allow_null=True, read_only=True)
    age_hours = serializers.IntegerField(source='death.age_hours', allow_null=True, read_only=True)
    age_minutes = serializers.IntegerField(source='death.age_minutes', allow_null=True, read_only=True)
    memorials = MemorialListShortSerializer(many=True, read_only=True, source="death.memorials")
    burials = BurialListShortSerializer(many=True, read_only=True, source="death.death_burials")

    class Meta:
        model = Person
        fields = ('id', 'first_names', 'other_names', 'last_name', 'death_date', 'age_years', 'age_months', 'age_weeks', 'age_days', 'age_hours', 'age_minutes', 'memorials', 'burials')


class FuneralDirectorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'first_line', 'second_line', 'town', 'county', 'postcode', 'country')
