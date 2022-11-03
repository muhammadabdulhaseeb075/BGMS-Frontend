# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
from django.db.models import Q

def merge_coffin_and_table_tomb_into_chest_tomb(apps, schema_editor):
    FeatureGroup = apps.get_model("main", "FeatureGroup")
    FeatureCode = apps.get_model("main", "FeatureCode")
    Layer = apps.get_model("geometries", "Layer")
    TopoPolygons = apps.get_model("geometries", "TopoPolygons")
    BurialGroundSite = apps.get_model("main", "BurialGroundSite")


    if connection.schema_name != 'public':
        if not FeatureCode.objects.filter(feature_type='chest_tomb').exists():
            ct = FeatureCode.objects.create(feature_type='chest_tomb', display_name='Chest Tomb', min_resolution=0, max_resolution=0.5, type='vector', show_in_toolbar=True)
            FeatureGroup.objects.get(group_code='memorials').feature_codes.add(ct)

        chest_tomb_layer = None
        # Create layer chest_tomb per site,
        if not Layer.objects.filter(feature_code=FeatureCode.objects.get(feature_type='chest_tomb')).exists():
            featurecode = FeatureCode.objects.get(feature_type='chest_tomb')
            chest_tomb_layer = Layer.objects.create(feature_code=featurecode, display_name=featurecode.display_name,
                                     show_in_toolbar=featurecode.show_in_toolbar,
                                     initial_visibility=featurecode.featuregroup_set.first().initial_visibility)

        # Move coffin tomb and table tomb polygons to new layer
        if chest_tomb_layer != None:
            if FeatureCode.objects.filter(feature_type='coffin_tomb').exists():
                coffin_tomb_layer = Layer.objects.get(feature_code=FeatureCode.objects.get(feature_type='coffin_tomb'))
                TopoPolygons.objects.filter(layer=coffin_tomb_layer).update(layer=chest_tomb_layer)
                Layer.objects.filter(feature_code=FeatureCode.objects.get(feature_type='coffin_tomb')).delete()
            if FeatureCode.objects.filter(feature_type='table_tomb').exists():
                table_tomb_layer = Layer.objects.get(feature_code=FeatureCode.objects.get(feature_type='table_tomb'))
                TopoPolygons.objects.filter(layer=table_tomb_layer).update(layer=chest_tomb_layer)
                Layer.objects.filter(feature_code=FeatureCode.objects.get(feature_type='table_tomb')).delete()

        delete_coffin_tomb = True
        bgs = BurialGroundSite.objects.all()
        current_connection = connection.schema_name
        for bg in bgs:
            if bg.schema_name != 'public':
                # print('SCHEMA NAME:'+bg.schema_name)
                connection.schema_name = bg.schema_name
                if FeatureCode.objects.filter(feature_type='coffin_tomb').exists() and FeatureCode.objects.filter(feature_type='table_tomb').exists():
                    coffin_tomb = FeatureCode.objects.get(feature_type='coffin_tomb')
                    table_tomb = FeatureCode.objects.get(feature_type='table_tomb')
                    # print('IF: '+str(len(coffin_tomb.layer_set.all()))+' or '+str(len(table_tomb.layer_set.all())))
                    if len(coffin_tomb.layer_set.all()) != 0 or len(table_tomb.layer_set.all()) != 0:
                        # print('delete_coffin_tomb = false')
                        delete_coffin_tomb = False
        if delete_coffin_tomb:
            FeatureCode.objects.filter(Q(feature_type='coffin_tomb') | Q(feature_type='table_tomb')).delete()

        connection.schema_name = current_connection

class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0001_squashed_0027_auto_20160218_1400'),
    ]

    operations = [
        migrations.RunPython(merge_coffin_and_table_tomb_into_chest_tomb),
    ]
