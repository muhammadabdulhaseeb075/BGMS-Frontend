# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, connection

def update_wall_hedge_resolutions(apps, schema_editor):
    FeatureCode = apps.get_model("main", "FeatureCode")

    if connection.schema_name == 'public':
        FeatureCode.objects.filter(feature_type='wall').update(max_resolution=100)
        FeatureCode.objects.filter(feature_type='hedge').update(max_resolution=0.25)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20160919_1437'),
    ]

    operations = [
        migrations.RunPython(
            code=update_wall_hedge_resolutions,
            reverse_code=None,
        )
    ]
