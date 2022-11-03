# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def change_displayname_featuregroup(apps, schema_editor):
    FeatureGroup = apps.get_model("main", "FeatureGroup")
    if connection.schema_name == 'public':
        basefc = FeatureGroup.objects.get(group_code="base")
        if basefc:
            basefc.display_name = 'Map'
            basefc.save()
        basefc = FeatureGroup.objects.get(group_code="aerial")
        if basefc:
            basefc.display_name = 'Aerial'
            basefc.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_burialimage'),
    ]

    operations = [
        migrations.RunPython(
            code=change_displayname_featuregroup,
            reverse_code=None,
            atomic=True,
        ),
    ]
