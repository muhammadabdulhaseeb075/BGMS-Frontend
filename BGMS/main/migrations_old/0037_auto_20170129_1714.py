# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def move_featurecodes_fk(apps, schema_editor):
    Layer = apps.get_model("geometries", "Layer")
    FeatureCode = apps.get_model("geometriespublic", "FeatureCode")

    if connection.schema_name != 'public':
        for lyr in Layer.objects.all():
            # import pdb; pdb.set_trace()
            lyr.feature_code = FeatureCode.objects.get(id=lyr.feature_code_idfk)
            lyr.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_auto_20170129_1334'),
    ]

    operations = [
        migrations.RunPython(
            code=move_featurecodes_fk,
            reverse_code=None,
        )
    ]
