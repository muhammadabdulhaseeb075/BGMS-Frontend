# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def switch_initial_visibility(apps, schema_editor):
    #migration for existing sites: opposite to geometries_layer.initial_visibility not daffodil, not dalton
    Layer = apps.get_model("geometries", "Layer")

    if connection.schema_name != 'public' and connection.schema_name != 'daffodil' and connection.schema_name != 'dalton':
        lyrs = Layer.objects.all()
        for lyr in lyrs:
            lyr.initial_visibility = not lyr.initial_visibility
            lyr.save()


class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0030_auto_20160712_0818'),
    ]

    operations = [
        migrations.RunPython(
            code=switch_initial_visibility,
            reverse_code=None,
        )
    ]
