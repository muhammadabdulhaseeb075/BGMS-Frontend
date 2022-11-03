from django import forms
from django.contrib.postgres.fields import ArrayField
from django.forms import Textarea
from django.forms.models import BaseInlineFormSet
from survey.models import SurveyTemplateField
from surveypublic.models import PublicSurveyTemplateField

class NonOptionalFieldFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        nonoptional_fields = PublicSurveyTemplateField.objects.filter(optional=False)
        kwargs['initial'] = []

        # add compulsory fields
        for field in nonoptional_fields:
            kwargs['initial'].append({ 'publicsurveytemplatefield': field, 'publicsurveytemplatefield_id': field.id, 'hierarchy': 0 })

        # disable fields
        self.form.base_fields['publicsurveytemplatefield'].disabled = True
        widget = self.form.base_fields['publicsurveytemplatefield'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        self.form.base_fields['hierarchy'].disabled = True
        super(NonOptionalFieldFormSet, self).__init__(*args, **kwargs)

class NonOptionalSurveyTemplateFieldFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):

        # if a new instance
        if not kwargs['instance'].date:
            nonoptional_fields = SurveyTemplateField.objects.filter(public_survey_template_fields__optional=False)
            kwargs['initial'] = []

            # add compulsory fields
            for field in nonoptional_fields:
                kwargs['initial'].append({ 'surveytemplatefield': field, 'surveytemplatefield_id': field.id, 'hierarchy': 0 })

        # disable fields
        self.form.base_fields['surveytemplatefield'].disabled = True
        widget = self.form.base_fields['surveytemplatefield'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        self.form.base_fields['hierarchy'].disabled = True
        super(NonOptionalSurveyTemplateFieldFormSet, self).__init__(*args, **kwargs)

class ArrayWidget(Textarea):
    def format_value(self, value):
        if value is None or len(value) == 0:
            return None
        else:
            return '\n'.join(value.split(','))

    def value_from_datadict(self, data, files, name):
        return data.get(name).splitlines()

class SurveyTemplateFieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyTemplateFieldForm, self).__init__(*args, **kwargs)
        self.fields['options'].widget = ArrayWidget()
        self.fields['options'].help_text = 'Add each option on a seperate line'