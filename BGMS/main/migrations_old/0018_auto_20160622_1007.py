# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def populate_featurecode_featuregroup(apps, schema_editor):
    FeatureCode = apps.get_model("main", "FeatureCode")
    FeatureGroup = apps.get_model("main", "FeatureGroup")

    if connection.schema_name == 'public':
        feature_names = [{'feature_type':'memorial_tree','display_name':'Memorial Tree','type':'vector','min_resolution':0,'max_resolution':0.5,'show_in_toolbar':True,'feature_group':'memorials'},
        {'feature_type':'memorial_bush_shrub','display_name':'Memorial Bush/Shrub','type':'vector','min_resolution':0,'max_resolution':0.5,'show_in_toolbar':True,'feature_group':'memorials'},]

        for name in feature_names:
            fc, created = FeatureCode.objects.get_or_create(feature_type=name['feature_type'], display_name=name['display_name'],type=name['type'],min_resolution=name['min_resolution'], max_resolution=name['max_resolution'], show_in_toolbar=name['show_in_toolbar'])
            if created:
                group = FeatureGroup.objects.get(group_code=name['feature_group'])
                group.feature_codes.add(fc)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20160609_1433'),
    ]

    operations = [
        migrations.RunPython(populate_featurecode_featuregroup),
    ]
