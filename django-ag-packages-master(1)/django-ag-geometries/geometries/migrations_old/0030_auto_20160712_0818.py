# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def delete_features_surfaces(apps, schema_editor):
    FeatureCode = apps.get_model("main", "FeatureCode")
    FeatureGroup = apps.get_model("main", "FeatureGroup")
    Layer = apps.get_model("geometries", "Layer")
    TopoPolygons = apps.get_model("geometries", "TopoPolygons")
    TopoPoints = apps.get_model("geometries", "TopoPoints")
    TopoPolylines = apps.get_model("geometries", "TopoPolylines")

    # Delete the following features (groups) for the schemas below in the if condition:
    # -	Administration
    # -	Building (s)
    # -	Thoroughfare (s)
    # -	Divides
    # -	Natural Surface (s)
    # -	Grid : group administration
    # -	Vegetation
    # -	Vegetation Points : group vegetation
    # -	Furniture
    # -	Utilities
    if connection.schema_name == 'caldbeck' or connection.schema_name == 'finsthwaite' or connection.schema_name == 'barton' or connection.schema_name == 'watermillock' or connection.schema_name == 'martindale' or connection.schema_name == 'dalston' or connection.schema_name == 'dalton' or connection.schema_name == 'pershore' or connection.schema_name == 'daffodil' or connection.schema_name == 'dalstondemo' or connection.schema_name == 'caldbeckdemo':
        # for each group loop features
            allgroups = FeatureGroup.objects.all()
            for group in allgroups:
                if group.group_code == 'administration' or group.group_code == 'buildings' or group.group_code == 'thoroughfares' or group.group_code == 'divides' or group.group_code == 'natural_surfaces' or group.group_code == 'vegetation' or group.group_code == 'furniture' or group.group_code == 'utilities':
                    features = group.feature_codes.all()
                    for feature in features:
                        # get layer for feature
                        if Layer.objects.filter(feature_code=feature).exists() and feature.feature_type != 'bench':
                            lyr = Layer.objects.get(feature_code=feature)
                            # delete TopoPolygons with this feature and attributes related
                            if TopoPolygons.objects.filter(layer=lyr).exists():
                                TopoPolygons.objects.filter(layer=lyr).delete()
                            # delete TopoPoints with this feature and attributes related
                            if TopoPoints.objects.filter(layer=lyr).exists():
                                TopoPoints.objects.filter(layer=lyr).delete()
                            # delete TopoPolylines with this feature and attributes related
                            if TopoPolylines.objects.filter(layer=lyr).exists():
                                TopoPolylines.objects.filter(layer=lyr).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0029_auto_20160704_1253'),
    ]

    operations = [
        migrations.RunPython(
            code=delete_features_surfaces,
            reverse_code=None,
        )
    ]
