# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def update_column_rename_non_unique(apps, schema_editor):
    if connection.schema_name != 'public':
        Template = apps.get_model("dataentry", "Template")
        for template in Template.objects.all():
            count = Template.objects.filter(name=template.name).count()
            if count>1:
                template.name = template.name + ' ' + str(count)
                template.save()

class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0018_auto_20160704_1637'),
    ]

    operations = [
        migrations.RunPython(
            code=update_column_rename_non_unique,
            reverse_code=None,
            atomic=True,
        ),
        migrations.AlterField(
            model_name='template',
            name='name',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
