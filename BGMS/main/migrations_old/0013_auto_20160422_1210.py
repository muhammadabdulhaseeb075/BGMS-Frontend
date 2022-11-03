# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def create_image_state(apps, schema_editor):
    ImageState = apps.get_model("main", "ImageState")
    if connection.schema_name == 'public':
        ImageState.objects.update_or_create(image_state="unprocessed")
        ImageState.objects.update_or_create(image_state="processing")
        ImageState.objects.update_or_create(image_state="processed")
        

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_merge'),
    ]

    operations = [ 
        migrations.RunPython(
            code=create_image_state,
            reverse_code=None,
            atomic=True,
        ),
    ]
