from django.apps import AppConfig
from django.db.models.signals import post_save

class SurveyConfig(AppConfig):
    name = 'survey'
    verbose_name = "Survey"

    def ready(self):
        from survey.models import SiteSurveyTemplateField
        from survey.signals import create_template_field

        post_save.connect(create_template_field, sender=SiteSurveyTemplateField)
