from django.db.models.signals import post_save
from tenant_schemas.utils import schema_context

def create_template_field(sender, instance, created, **kwargs):
    """
    Creates a SurveyTemplateField object 
    """

    from main.models import BurialGroundSite
    from survey.models import SurveyTemplateField
    from surveypublic.models import PublicSurveyTemplateField

    if created:
        sites = BurialGroundSite.objects.all()
        for site in sites:
            if site.schema_name!='public':
                with schema_context(site.schema_name):
                    SurveyTemplateField.objects.create(field=instance)