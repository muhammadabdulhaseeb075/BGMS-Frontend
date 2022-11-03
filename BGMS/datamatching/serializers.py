from django.conf import settings

from bgsite.models import Memorial, Person, MemorialInscriptionDetail, Death
from bgsite.common_apis.serializers import ImageSerializer
from datamatching.models import MemorialHistory, DataMatchingMemorial

from rest_framework import serializers

class MemorialInscriptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MemorialInscriptionDetail
        fields = ('id', 'first_names', 'last_name', 'age', 'date')

class MemorialDeathSerializer(serializers.ModelSerializer):
    
    person_id = serializers.CharField(source='person.id', read_only=True)
    first_names = serializers.CharField(source='person.first_names', allow_null=True, read_only=True)
    last_name = serializers.CharField(source='person.last_name', allow_null=True, read_only=True)

    class Meta:
        model = Death
        fields = ('person_id', 'first_names', 'last_name', 'age_years', 'age_months', 'age_weeks', 'age_days', 'age_hours', 'age_minutes')

class MemorialMatchSerializer(serializers.ModelSerializer):
    
    memorial_persons = MemorialDeathSerializer(many=True, read_only=True, source='memorial_deaths')
    memorial_inscriptions = MemorialInscriptionSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True,)
    
    class Meta:
        model = Memorial
        fields = ('id', 'feature_id', 'memorial_persons', 'images', 'memorial_inscriptions',)

def format_feature_id(feature_id):
    # if feature is a number, add leading zeros
    if feature_id.isdigit():
        feature_id = feature_id.zfill(10)
    
    return feature_id

class UserActivitySerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    feature_id = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    data_matching_memorial_id = serializers.CharField(source='memorial.memorial.id')

    class Meta:
        model = MemorialHistory
        fields = ('id', 'feature_id', 'name', 'date', 'state', 'data_matching_memorial_id')
    
    def get_name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name) 
    
    def get_state(self, obj):
        return obj.state.state.replace('_', ' ').capitalize()

    def get_date(self, obj):
        return obj.time.strftime("%d/%m/%Y, %I:%M %p")
    
    def get_feature_id(self, obj):
        return format_feature_id(obj.memorial.memorial.feature_id)


class MemorialStateSerializer(serializers.ModelSerializer):

    feature_id = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    data_matching_memorial_id = serializers.CharField(source='memorial.id')

    class Meta:
        model = DataMatchingMemorial
        fields = ('feature_id', 'state', 'data_matching_memorial_id')
    
    def get_state(self, obj):
        return obj.state.image_state.replace('_', ' ').capitalize()
    
    def get_feature_id(self, obj):
        return format_feature_id(obj.memorial.feature_id)

#class MemorialStateSerializer(serializers.ModelSerializer):

#    state = serializers.SerializerMethodField()

#    class Meta:
#        model = Memorial
#        fields = ('feature_id', 'state')
    
#    def get_state(self, obj):
        # if memorial has a record in DataMatchingMemorial
#        if hasattr(obj, 'data_matching'):
#            return obj.data_matching.state.image_state.replace('_', ' ').capitalize()
#        else:
#            return 'Unprocessed'