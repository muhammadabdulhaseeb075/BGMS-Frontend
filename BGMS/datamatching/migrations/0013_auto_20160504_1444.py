# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def chnage_to_processed_callbeck_memorials(apps, schema_editor):
    DataMatchingMemorial = apps.get_model("datamatching", "DataMatchingMemorial")
    ImageState = apps.get_model("main", "ImageState")

    if connection.schema_name == 'caldbeck':
        image_processed = ImageState.objects.get(image_state='processed')
        dmemorials = DataMatchingMemorial.objects.all()
        for dmem in dmemorials:
            dmem.state = image_processed
            dmem.save()

class Migration(migrations.Migration):

    dependencies = [
        ('datamatching', '0012_auto_20160321_1917'),
    ]

    operations = [
        migrations.RunPython(chnage_to_processed_callbeck_memorials),
    ]
