from bgsite.models import Image, ImageType, ImageState

from django.db import models
from django.db.models import Q, Prefetch
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField

from geometries.models import TopoPolygons, TopoPolylines, TopoPoints
from geometriespublic.models import FieldType, FeatureCode

import uuid

class SurveyTemplateField(models.Model):
    """
    Table combines SiteSurveyTemplateField and PublicSurveyTemplateField 
    to allow many to many relationship with survey template
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={ Q(app_label='surveypublic', model='PublicSurveyTemplateField') | Q(app_label='survey', model='SiteSurveyTemplateField') })
    object_id = models.UUIDField()
    field = GenericForeignKey('content_type', 'object_id')
    """Field - can link to survey template fields in publicsurvey or survey"""

    def __str__(self):
        return_value = self.field.name + ' (' + self.field.type.label + ')'

        return return_value
    
    class Meta:
        ordering = ['content_type__model', 'site_survey_template_fields__name', 'public_survey_template_fields__name']
        unique_together = ('content_type', 'object_id',)


class SurveyTemplate(models.Model):
    """
    Survey Templates linked to features.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    feature_codes = models.ManyToManyField(FeatureCode, related_name='survey_templates', blank=True)
    fields = models.ManyToManyField(SurveyTemplateField, through="SurveyTemplate_Field")
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class SurveyTemplate_Field(models.Model):
    surveytemplate = models.ForeignKey(SurveyTemplate, on_delete=models.CASCADE, related_name="survey_template_fields")
    surveytemplatefield = models.ForeignKey(SurveyTemplateField, on_delete=models.CASCADE, related_name="survey_template_fields")
    hierarchy = models.IntegerField(default=1)


class SurveyTemplateFieldBase(models.Model):
    """
    Fields belonging to survey templates
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    type = models.ForeignKey(FieldType, on_delete=models.CASCADE, limit_choices_to={'survey': True})
    options = ArrayField(base_field=models.CharField(max_length=50), null=True, blank=True, verbose_name="Options (for 'Select' type only)")
    retired = models.BooleanField(default=False)

    class Meta:
        abstract = True
    
    def save(self, **kwargs):

        # options field should be null unless the type is 'select'
        if self.type.name!='select':
            self.options = None

        super(SurveyTemplateFieldBase, self).save()


class SiteSurveyTemplateField(SurveyTemplateFieldBase):
    """
    Fields belonging to survey templates
    """
    survey_template_field = GenericRelation(SurveyTemplateField, related_query_name='site_survey_template_fields')

    def __str__(self):
        return self.name.title()


class Survey(models.Model):
    """
    An individual feature survey.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    survey_template = models.ForeignKey(SurveyTemplate, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class SurveyField(models.Model):
    """
    Field from a survey. Contains the data.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="survey_fields")
    survey_template_field = models.ForeignKey(SurveyTemplateField, on_delete=models.CASCADE)
    char_value = models.CharField(max_length=255, null=True, blank=True)
    integer_value = models.IntegerField(null=True, blank=True)
    float_value = models.FloatField(null=True, blank=True)
    boolean_value = models.NullBooleanField()
    date_value = models.DateField(null=True)
    textarea_value = models.CharField(max_length=400, null=True, blank=True)
    image_value = models.ForeignKey('bgsite.Image', null=True, blank=True, editable=False, on_delete=models.CASCADE)

    def create_image(self, url):
        """
        Add an image and thumbnail to the survey field
        """
        image = Image(url=url, image_type=ImageType.objects.get(image_type='memorial'), image_state=ImageState.objects.get(image_state='unprocessed'))
        image.save()
        image.create_thumbnail(url)
        self.image_value = image
        self.save()


class TopoPolygonSurvey(models.Model):
    """
    Links a survey to a topopolygon feature. A feature can have any number of surveys
    """
    topopolygon = models.ForeignKey(TopoPolygons, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="topopolygon_surveys")


class TopoPolylineSurvey(models.Model):
    """
    Links a survey to a topopolyline feature. A feature can have any number of surveys
    """
    topopolyline = models.ForeignKey(TopoPolylines, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="topopolyline_surveys")


class TopoPointSurvey(models.Model):
    """
    Links a survey to a topopoint feature. A feature can have any number of surveys
    """
    topopoint = models.ForeignKey(TopoPoints, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="topopoint_surveys")