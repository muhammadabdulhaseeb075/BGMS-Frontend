from django.apps import AppConfig
from django.db.models.signals import post_save

class SurveyPublicConfig(AppConfig):
    name = 'surveypublic'
    verbose_name = "Survey Public"

    def ready(self):
        from surveypublic.models import PublicSurveyTemplateField
        from surveypublic.signals import create_template_field

        post_save.connect(create_template_field, sender=PublicSurveyTemplateField)
