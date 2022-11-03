# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
import uuid

def populate_default_field(apps, schema_editor):
    DefaultSurveyTemplateField = apps.get_model("surveypublic", "DefaultSurveyTemplateField")
    if connection.schema_name == 'public':
    
        field = DefaultSurveyTemplateField.objects.get_or_create(name='Survey Date',optional=False,type_id='date')


class Migration(migrations.Migration):

    dependencies = [
        ('surveypublic', '0002_auto_20190520_1120'),
    ]

    operations = [
        migrations.RunPython(
            code=populate_default_field,
        ),
    ]
