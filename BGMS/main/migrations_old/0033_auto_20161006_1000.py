# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def populate_featurecode_hierarchy(apps, schema_editor):
    FeatureCode = apps.get_model("main", "FeatureCode")
    FeatureGroup = apps.get_model("main", "FeatureGroup")

    if connection.schema_name == 'public':
        fgs = FeatureGroup.objects.all().order_by('hierarchy')
        order = 0
        for fg in fgs:
            for fc in fg.feature_codes.all():
                fc.hierarchy = order
                fc.save()
                order += 1
            

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_featurecode_hierarchy'),
    ]

    operations = [
        migrations.RunPython(
            code=populate_featurecode_hierarchy,
            reverse_code=None,
        )
    ]
