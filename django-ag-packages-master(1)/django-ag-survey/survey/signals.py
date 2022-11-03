def create_template_field(sender, instance, created, **kwargs):
    from survey.models import SiteSurveyTemplateField, SurveyTemplateField
    
    if created:
        SurveyTemplateField.objects.create(field=instance)