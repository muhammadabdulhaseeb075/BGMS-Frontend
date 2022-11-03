from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models, transaction
from geometriespublic.models import FeatureCode
from survey.models import SurveyTemplateFieldBase
import uuid


class PublicSurveyTemplateField(SurveyTemplateFieldBase):
    """
    Survey template fields that are available to all sites
    """
    optional = models.BooleanField(default=True)
    default = models.BooleanField(default=False) # If true, this field will be automatically added to every new template
    survey_template_field = GenericRelation('survey.SurveyTemplateField', related_query_name='public_survey_template_fields')

    def __str__(self):
        return self.name.title()


class MasterSurveyTemplate(models.Model):
    """
    Survey Templates linked to features.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    feature_codes = models.ManyToManyField(FeatureCode, related_name='master_survey_templates', blank=True)
    fields = models.ManyToManyField(PublicSurveyTemplateField, through="MasterSurveyTemplate_Field")
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class MasterSurveyTemplate_Field(models.Model):
    mastersurveytemplate = models.ForeignKey(MasterSurveyTemplate, on_delete=models.CASCADE, related_name="master_survey_template_fields")
    publicsurveytemplatefield = models.ForeignKey(PublicSurveyTemplateField, on_delete=models.CASCADE)
    hierarchy = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Master Survey Template Fields"