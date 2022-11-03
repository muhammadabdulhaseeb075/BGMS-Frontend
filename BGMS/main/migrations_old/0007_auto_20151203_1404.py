# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def create_layers(apps, schema_editor):
    FeatureCode = apps.get_model("main", "FeatureCode")
    FeatureGroup = apps.get_model("main", "FeatureGroup")
    if connection.schema_name == 'public':
        if not FeatureCode.objects.filter(feature_type='grid').exists():
            grid = FeatureCode.objects.create(feature_type='grid', display_name='Grid', min_resolution=0, max_resolution=1600, type='vector', show_in_toolbar=True)
            FeatureGroup.objects.get(group_code='administration').feature_codes.add(grid)
        if not FeatureCode.objects.filter(feature_type='tree_trunk').exists():
            tree_trunk = FeatureCode.objects.create(feature_type='tree_trunk', display_name='Tree Trunk', min_resolution=0, max_resolution=25, type='vector', show_in_toolbar=True)
            FeatureGroup.objects.get(group_code='vegetation').feature_codes.add(tree_trunk)
        if not FeatureCode.objects.filter(feature_type='lych_gate').exists():
            lych_gate = FeatureCode.objects.create(feature_type='lych_gate', display_name='Lych Gate', min_resolution=0, max_resolution=100, type='vector', show_in_toolbar=True)
            FeatureGroup.objects.get(group_code='buildings').feature_codes.add(lych_gate)
            FeatureGroup.objects.get(group_code='memorials').feature_codes.add(lych_gate)
        else:
            FeatureGroup.objects.get(group_code='memorials').feature_codes.add(FeatureCode.objects.get(feature_type='lych_gate'))
        
class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150902_1027'),
    ]

    operations = [
        migrations.RunPython(
            code=create_layers,
            reverse_code=None,
            atomic=True,
        ),
    ]
