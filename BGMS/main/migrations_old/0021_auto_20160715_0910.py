# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def switch_initial_visibility_for_new_sites(apps, schema_editor):
    FeatureCode = apps.get_model("main", "FeatureCode")
    FeatureGroup = apps.get_model("main", "FeatureGroup")

    if connection.schema_name == 'public':
        fgs = FeatureGroup.objects.all()
        for fg in fgs:
            if fg.group_code != 'base' and fg.group_code != 'memorial_cluster' and fg.group_code != 'memorials' and fg.group_code != 'plots':
                fg.initial_visibility = not fg.initial_visibility
                fg.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_burialofficialtype'),
    ]

    operations = [
        migrations.RunPython(
            code=switch_initial_visibility_for_new_sites,
            reverse_code=None,
        )
    ]
