# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, connection

def migrate_featuregroups_featurecodes(apps, schema_editor):
    FeatureCode = apps.get_model("main", "FeatureCode")
    FeatureGroup = apps.get_model("main", "FeatureGroup")
    gFeatureCode = apps.get_model("geometriespublic", "FeatureCode")
    gFeatureGroup = apps.get_model("geometriespublic", "FeatureGroup")

    if connection.schema_name == 'public':
        for fc in FeatureCode.objects.all():
            gFeatureCode.objects.create(id=fc.id, feature_type=fc.feature_type, type=fc.type, display_name=fc.display_name, min_resolution=fc.min_resolution, max_resolution=fc.max_resolution, show_in_toolbar=fc.show_in_toolbar, hierarchy=fc.hierarchy)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_auto_20161212_1634'),
    ]

    operations = [
        migrations.RunPython(
            code=migrate_featuregroups_featurecodes,
            reverse_code=None,
        )
    ]
