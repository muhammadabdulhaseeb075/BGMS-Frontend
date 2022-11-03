# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from django.db import migrations, models, connection

def add_type_file(apps, schema_editor):
    ImageType = apps.get_model("main", "ImageType")

    if connection.schema_name == 'public':
        ImageType.objects.create(image_type='file')

class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=add_type_file,
            reverse_code=None,
        )
    ]
