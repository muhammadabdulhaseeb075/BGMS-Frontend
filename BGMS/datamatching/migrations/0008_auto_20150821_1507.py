# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, connection

def create_datamatching_memorials(apps, schema_editor):
    Memorial = apps.get_model("bgsite", "Memorial")
    DataMatchingMemorial = apps.get_model("datamatching", "DataMatchingMemorial")
    if connection.schema_name != 'public':
        memorials = Memorial.objects.all()
        for memorial in memorials:
            DataMatchingMemorial.objects.create(memorial=memorial)

def delete_datamatching_memorials(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('datamatching', '0007_auto_20150821_1457'),
    ]

    operations = [
        migrations.RunPython(
            code=create_datamatching_memorials,
            reverse_code=delete_datamatching_memorials,
            atomic=True,
        ),
    ]
