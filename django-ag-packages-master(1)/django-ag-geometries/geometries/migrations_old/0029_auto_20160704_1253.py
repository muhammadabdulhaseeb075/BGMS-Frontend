# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def migrate_statue_obelisk(apps, schema_editor):
    # FeatureCode = apps.get_model("main", "FeatureCode")
    # FeatureGroup = apps.get_model("main", "FeatureGroup")
    # Layer = apps.get_model("geometries", "Layer")
    # TopoPolygons = apps.get_model("geometries", "TopoPolygons")
    #
    # if connection.schema_name != 'public':
    #     # obj = Layer.create_layer_from_feature_type('obelisk') TODO: find how to call custom querysets from migrations
    #     fc = FeatureCode.objects.get(feature_type='obelisk')
    #     obelisk_layer = Layer.objects.get_or_create(feature_code=fc, display_name=fc.display_name,
    #                      show_in_toolbar=fc.show_in_toolbar,
    #                      initial_visibility=fc.featuregroup_set.first().initial_visibility)
    #     statue_layer = Layer.objects.get(display_name='Statue')
    #     statues = TopoPolygons.objects.filter(layer=statue_layer)
    #     # import pdb; pdb.set_trace()
    #     for sta in statues:
    #         sta.layer = obelisk_layer
    #         sta.save()
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0028_auto_20160608_1434'),
    ]

    operations = [
        migrations.RunPython(
            code=migrate_statue_obelisk,
            reverse_code=None,
        )
    ]
