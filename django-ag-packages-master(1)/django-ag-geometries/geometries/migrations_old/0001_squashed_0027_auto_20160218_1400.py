# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
import django.utils.timezone
import django.contrib.gis.db.models.fields
import uuid

def create_layers(apps, schema_editor):
    """
    Creates layer objects off of the main feature_code objects.
    Also creates the aerial and base raster objects.
    """
    Layer = apps.get_model("geometries", "Layer")
    FeatureCode = apps.get_model("main", "FeatureCode")
    TopoPolygons = apps.get_model("geometries", "TopoPolygons")
    TopoPolylines = apps.get_model("geometries", "TopoPolylines")
    TopoPoints = apps.get_model("geometries", "TopoPoints")
    Raster = apps.get_model("geometries", "Raster")
    if connection.schema_name != 'public':
        #creating layer objects based on the ones in the main feature_code table
        if not Layer.objects.all().exists():
            for featurecode in FeatureCode.objects.all():
                Layer.objects.create(feature_code=featurecode, display_name=featurecode.display_name, 
                                     show_in_toolbar=featurecode.show_in_toolbar,
                                     initial_visibility=featurecode.featuregroup_set.first().initial_visibility)
            for raster in Raster.objects.all():
                raster.layer = Layer.objects.get(feature_code=raster.feature_code)
                raster.save()
            for point in TopoPoints.objects.all():
                point.layer = Layer.objects.get(feature_code=point.feature_code)
                point.save()
            for polygon in TopoPolygons.objects.all():
                polygon.layer = Layer.objects.get(feature_code=polygon.feature_code)
                polygon.save()
            for line in TopoPolylines.objects.all():
                line.layer = Layer.objects.get(feature_code=line.feature_code)
                line.save()
            
        #creating 'aerial' and 'base' raster objects
        if not Raster.objects.all().exists():
            aerial = Layer.objects.get(feature_code__feature_type='aerial')
            Raster.objects.create(type='TileWMTS', layer=aerial, url='')
            base = Layer.objects.get(feature_code__feature_type='base')
            Raster.objects.create(type='TileWMS', layer=base, url='')

# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# geometries.migrations.0023_auto_20160218_1309
# geometries.migrations.0016_auto_20151209_1607
# geometries.migrations.0007_auto_20150826_1450
# geometries.migrations.0015_auto_20151203_1257
# geometries.migrations.0026_auto_20160218_1352
# geometries.migrations.0022_auto_20160216_1903
# geometries.migrations.0021_auto_20160216_1706
# geometries.migrations.0013_auto_20151009_1536
# geometries.migrations.0020_auto_20160216_1633
# geometries.migrations.0025_auto_20160218_1334
# geometries.migrations.0017_auto_20160212_1200

class Migration(migrations.Migration):

#     replaces = [('geometries', '0001_initial'), ('geometries', '0002_auto_20150312_1616'), ('geometries', '0003_auto_20150313_1628'), ('geometries', '0004_auto_20150313_1629'), ('geometries', '0005_auto_20150501_1123'), ('geometries', '0006_auto_20150619_0927'), ('geometries', '0007_auto_20150826_1450'), ('geometries', '0008_auto_20150827_1605'), ('geometries', '0009_auto_20150828_0938'), ('geometries', '0010_auto_20150813_0959'), ('geometries', '0011_raster'), ('geometries', '0012_auto_20151009_1414'), ('geometries', '0013_auto_20151009_1536'), ('geometries', '0014_auto_20151009_1539'), ('geometries', '0015_auto_20151203_1257'), ('geometries', '0016_auto_20151209_1607'), ('geometries', '0017_auto_20160212_1200'), ('geometries', '0018_auto_20160216_1104'), ('geometries', '0019_auto_20160216_1623'), ('geometries', '0020_auto_20160216_1633'), ('geometries', '0021_auto_20160216_1706'), ('geometries', '0022_auto_20160216_1903'), ('geometries', '0023_auto_20160218_1309'), ('geometries', '0024_auto_20160218_1323'), ('geometries', '0025_auto_20160218_1334'), ('geometries', '0026_auto_20160218_1352'), ('geometries', '0027_auto_20160218_1400')]

    dependencies = [
            # ('main', '0016_merge'),
#         ('bgsite', '0004_auto_20160216_1052'),
#         ('main', '0006_auto_20150902_1027'),
#         ('bgsite', '0003_auto_20160215_1713'),
#         ('main', '0007_auto_20151203_1404'),
#         ('main', '0002_auto_20150826_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, verbose_name='ID', serialize=False, primary_key=True)),
                ('display_name', models.CharField(max_length=20)),
                ('show_in_toolbar', models.BooleanField()),
                ('initial_visibility', models.BooleanField(default=False)),
                ('feature_code', models.ForeignKey(to='main.FeatureCode')),
            ],
        ),
        migrations.CreateModel(
            name='TopoPoints',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, verbose_name='ID', serialize=False, primary_key=True)),
                ('veg_spread', models.FloatField(null=True)),
                ('date_uploaded', models.DateField(null=True, default=django.utils.timezone.now)),
                ('geom_acc', models.FloatField(null=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=27700)),
                ('layer', models.ForeignKey(to='geometries.Layer', on_delete=models.CASCADE)),
                ('surveyor', models.ForeignKey(null=True, to='main.Surveyor')),
            ],
        ),
        migrations.CreateModel(
            name='TopoPolygons',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, verbose_name='ID', serialize=False, primary_key=True)),
                ('date_uploaded', models.DateField(null=True, default=django.utils.timezone.now)),
                ('geom_acc', models.FloatField(null=True)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=27700)),
                ('layer', models.ForeignKey(to='geometries.Layer', on_delete=models.CASCADE)),
                ('surveyor', models.ForeignKey(null=True, to='main.Surveyor')),
            ],
        ),
        migrations.CreateModel(
            name='TopoPolylines',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, verbose_name='ID', serialize=False, primary_key=True)),
                ('width', models.FloatField(null=True)),
                ('date_uploaded', models.DateField(null=True, default=django.utils.timezone.now)),
                ('geom_acc', models.FloatField(null=True)),
                ('geometry', django.contrib.gis.db.models.fields.MultiLineStringField(srid=27700)),
                ('layer', models.ForeignKey(to='geometries.Layer', on_delete=models.CASCADE)),
                ('surveyor', models.ForeignKey(null=True, to='main.Surveyor')),
            ],
        ),
        migrations.CreateModel(
            name='Raster',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, verbose_name='ID', serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=10)),
                ('url', models.CharField(max_length=200)),
                ('layer', models.ForeignKey(to='geometries.Layer', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, verbose_name='ID', serialize=False, primary_key=True)),
                ('attribute_name', models.CharField(max_length=100)),
                ('attribute_value', models.CharField(null=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='topopoints',
            name='attributes',
            field=models.ManyToManyField(null=True, to='geometries.Attribute'),
        ),
        migrations.AddField(
            model_name='topopolygons',
            name='attributes',
            field=models.ManyToManyField(null=True, to='geometries.Attribute'),
        ),
        migrations.AddField(
            model_name='topopolylines',
            name='attributes',
            field=models.ManyToManyField(null=True, to='geometries.Attribute'),
        ),
        migrations.AddField(
            model_name='topopoints',
            name='user_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='topopolygons',
            name='user_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='topopolylines',
            name='user_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='topopoints',
            name='feature_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topopolygons',
            name='feature_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topopolylines',
            name='feature_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topopoints',
            name='attributes',
            field=models.ManyToManyField(to='geometries.Attribute'),
        ),
        migrations.AlterField(
            model_name='topopolygons',
            name='attributes',
            field=models.ManyToManyField(to='geometries.Attribute'),
        ),
        migrations.AlterField(
            model_name='topopolylines',
            name='attributes',
            field=models.ManyToManyField(to='geometries.Attribute'),
        ),
        migrations.RunPython(
            code=create_layers,
        ),
#         migrations.RunPython(
#             code=geometries.migrations.0015_auto_20151203_1257.create_layers,
#         ),
#         migrations.RunPython(
#             code=geometries.migrations.0016_auto_20151209_1607.reset_bench_initial_visibility,
#         ),
    ]
