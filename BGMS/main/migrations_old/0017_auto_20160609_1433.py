# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def populate_featurecode_featuregroup(apps, schema_editor):
    FeatureCode = apps.get_model("main", "FeatureCode")
    FeatureGroup = apps.get_model("main", "FeatureGroup")

    if connection.schema_name == 'public':
        feature_names = [{'feature_type':'grave_kerb','display_name':'Grave Kerb','type':'vector','min_resolution':0,'max_resolution':0.5,'show_in_toolbar':True,'feature_group':'divides'},
                        {'feature_type':'grave_slab','display_name':'Grave Slab','type':'vector','min_resolution':0,'max_resolution':0.5,'show_in_toolbar':True,'feature_group':'memorials'},
                        {'feature_type':'obelisk','display_name':'Obelisk','type':'vector','min_resolution':0,'max_resolution':0.5,'show_in_toolbar':True,'feature_group':'memorials'},
                        {'feature_type':'stream','display_name':'Stream','type':'vector','min_resolution':0,'max_resolution':100,'show_in_toolbar':True,'feature_group':'natural_surfaces'},
                        {'feature_type':'other_surface','display_name':'Other Surface','type':'vector','min_resolution':0,'max_resolution':100,'show_in_toolbar':True,'feature_group':'natural_surfaces'},
                        {'feature_type':'woodland','display_name':'Woodland','type':'vector','min_resolution':0,'max_resolution':100,'show_in_toolbar':True,'feature_group':'natural_surfaces'},]

        for name in feature_names:
            fc, created = FeatureCode.objects.get_or_create(feature_type=name['feature_type'], display_name=name['display_name'],type=name['type'],min_resolution=name['min_resolution'], max_resolution=name['max_resolution'], show_in_toolbar=name['show_in_toolbar'])
            if created:
                group = FeatureGroup.objects.get(group_code=name['feature_group'])
                group.feature_codes.add(fc)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_merge'),
    ]

    operations = [
        migrations.RunPython(populate_featurecode_featuregroup),
    ]
