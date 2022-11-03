# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def move_featurecodes_fk(apps, schema_editor):
    Layer = apps.get_model("geometries", "Layer")

    if connection.schema_name != 'public':
        for lyr in Layer.objects.all():
            # import pdb; pdb.set_trace()
            lyr.feature_code_idfk = lyr.feature_code.id
            lyr.save()


class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0035_layer_feature_code_idfk'),
    ]

    operations = [
        migrations.RunPython(
            code=move_featurecodes_fk,
            reverse_code=None,
        )
    ]
