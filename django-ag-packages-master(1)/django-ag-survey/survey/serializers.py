from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from geometriespublic.models import FeatureCode
from survey.models import Survey, SurveyField, SurveyTemplate, SurveyTemplateField
from surveypublic.models import MasterSurveyTemplate, PublicSurveyTemplateField, MasterSurveyTemplate_Field

class SurveyFieldSerializer(serializers.ModelSerializer):

    survey_field_id = serializers.CharField(source='id')
    survey_template_field_id = serializers.CharField()
    label = serializers.SerializerMethodField()
    field_name = serializers.SerializerMethodField()
    field_type = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = SurveyField
        fields = ('survey_field_id', 'survey_template_field_id', 'label', 'field_name', 'field_type', 'value')
    
    def get_label(self, obj):
        return obj.survey_template_field.field.name
    
    def get_field_name(self, obj):
        return obj.survey_template_field.field.type.name
    
    def get_field_type(self, obj):
        return obj.survey_template_field.field.type.type_name
    
    def get_value(self, obj):
        field_type = self.get_field_type(obj)

        if field_type == 'image':
            if obj.image_value:
                return { 'image_url': obj.image_value.url.url, 'thumbnail_url': obj.image_value.thumbnail.url.url }
            else:
                return None

        return getattr(obj, field_type + '_value')


class SurveySerializer(serializers.ModelSerializer):

    survey_template_name = serializers.SerializerMethodField()
    fields = SurveyFieldSerializer(many=True, read_only=True, source='survey_fields')

    class Meta:
        model = Survey
        fields = ('survey_template_name', 'fields',)

    def get_survey_template_name(self, obj):
        return obj.survey_template.name

class SurveysListSerializer(serializers.ModelSerializer):

    survey_id = serializers.CharField(source='id')
    survey_date = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = ('survey_id', 'survey_date',)

    def get_survey_date(self, obj):
        survey_field = SurveyField.objects.filter(survey=obj, survey_template_field__public_survey_template_fields__name='Survey Date')[0]
        return survey_field.date_value

class SurveyTemplateFieldSerializer(serializers.ModelSerializer):

    survey_template_field_id = serializers.CharField(source='id')
    label = serializers.SerializerMethodField()
    field_name = serializers.SerializerMethodField()
    field_type = serializers.SerializerMethodField()
    select_options = serializers.SerializerMethodField()

    class Meta:
        model = SurveyTemplateField
        fields = ('survey_template_field_id', 'label', 'field_name', 'field_type', 'select_options')
    
    def get_label(self, obj):
        return obj.field.name
    
    def get_field_name(self, obj):
        return obj.field.type.name
    
    def get_field_type(self, obj):
        return obj.field.type.type_name
    
    def get_select_options(self, obj):
        if obj.field.type.name == 'select':
            return obj.field.options
        else:
            return None


class LayerSurveyTemplatesSerializer(serializers.ModelSerializer):

    survey_template_id = serializers.CharField(source='id')
    # for some unknown reason, get_fields doesn't work
    fields = serializers.SerializerMethodField(method_name='get_survey_fields')

    class Meta:
        model = SurveyTemplate
        fields = ('survey_template_id', 'name', 'fields',)

    def get_survey_fields(self, obj):
        fields = obj.fields.all().order_by('survey_template_fields__hierarchy')
        return SurveyTemplateFieldSerializer(fields, many=True).data


class PublicSurveyTemplateFieldSerializer(serializers.ModelSerializer):
    
    id = serializers.SerializerMethodField()

    class Meta:
        model = MasterSurveyTemplate_Field
        fields = ('id', 'hierarchy')
    
    def get_id(self, obj):
        content_type = ContentType.objects.get(app_label='surveypublic', model='publicsurveytemplatefield')
        survey_template_field,created = SurveyTemplateField.objects.get_or_create(content_type=content_type, object_id=obj.publicsurveytemplatefield_id)
        return survey_template_field.id



class FeatureCodesSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureCode
        fields = ('id',)


class MasterTemplateSerializer(serializers.ModelSerializer):

    fields = PublicSurveyTemplateFieldSerializer(many=True, read_only=True, source='master_survey_template_fields')
    feature_codes = FeatureCodesSerializer(many=True, read_only=True)

    class Meta:
        model = MasterSurveyTemplate
        fields = ('name', 'fields', 'feature_codes',)