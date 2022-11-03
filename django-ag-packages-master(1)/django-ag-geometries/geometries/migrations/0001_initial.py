# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
import uuid
import django.utils.timezone
import django.contrib.gis.db.models.fields


def create_layers(apps, schema_editor):
    """
    Creates layer objects off of the main feature_code objects.
    Also creates the aerial and base raster objects.
    """
    Layer = apps.get_model("geometries", "Layer")
    FeatureCode = apps.get_model("geometriespublic", "FeatureCode")
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
            try:
                aerial = Layer.objects.get(feature_code__feature_type='aerial')
                Raster.objects.create(type='TileWMTS', layer=aerial, url='')
            except:
                print('Aerial layer not included')

            try:
                base = Layer.objects.get(feature_code__feature_type='base')
                Raster.objects.create(type='TileWMS', layer=base, url='')
            except:
                print('Base layer not included')


class Migration(migrations.Migration):

    dependencies = [
        ('geometriespublic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4)),
                ('attribute_name', models.CharField(max_length=100)),
                ('attribute_value', models.CharField(null=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4)),
                ('feature_code_idfk', models.IntegerField(null=True)),
                ('display_name', models.CharField(max_length=20)),
                ('show_in_toolbar', models.BooleanField()),
                ('initial_visibility', models.BooleanField(default=False)),
                ('feature_code', models.ForeignKey(null=True, to='geometriespublic.FeatureCode', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Raster',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4)),
                ('type', models.CharField(max_length=10)),
                ('url', models.CharField(max_length=200)),
                ('layer', models.ForeignKey(to='geometries.Layer', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='TopoPoints',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4)),
                ('feature_id', models.CharField(max_length=10)),
                ('date_uploaded', models.DateField(null=True, default=django.utils.timezone.now)),
                ('geom_acc', models.FloatField(null=True, blank=True)),
                ('user_created', models.BooleanField(default=False)),
                ('veg_spread', models.FloatField(null=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=27700)),
                ('attributes', models.ManyToManyField(blank=True, to='geometries.Attribute')),
                ('layer', models.ForeignKey(to='geometries.Layer', on_delete=models.CASCADE)),
                ('surveyor', models.ForeignKey(null=True, blank=True, to='geometriespublic.Surveyor', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'TopoPoint',
                'verbose_name_plural': 'TopoPoints',
            },
        ),
        migrations.CreateModel(
            name='TopoPolygons',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4)),
                ('feature_id', models.CharField(max_length=10)),
                ('date_uploaded', models.DateField(null=True, default=django.utils.timezone.now)),
                ('geom_acc', models.FloatField(null=True, blank=True)),
                ('user_created', models.BooleanField(default=False)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=27700)),
                ('attributes', models.ManyToManyField(blank=True, to='geometries.Attribute')),
                ('layer', models.ForeignKey(to='geometries.Layer', on_delete=models.CASCADE)),
                ('surveyor', models.ForeignKey(null=True, blank=True, to='geometriespublic.Surveyor', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'TopoPolygon',
                'verbose_name_plural': 'TopoPolygons',
            },
        ),
        migrations.CreateModel(
            name='TopoPolylines',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4)),
                ('feature_id', models.CharField(max_length=10)),
                ('date_uploaded', models.DateField(null=True, default=django.utils.timezone.now)),
                ('geom_acc', models.FloatField(null=True, blank=True)),
                ('user_created', models.BooleanField(default=False)),
                ('width', models.FloatField(null=True)),
                ('geometry', django.contrib.gis.db.models.fields.MultiLineStringField(srid=27700)),
                ('attributes', models.ManyToManyField(blank=True, to='geometries.Attribute')),
                ('layer', models.ForeignKey(to='geometries.Layer', on_delete=models.CASCADE)),
                ('surveyor', models.ForeignKey(null=True, blank=True, to='geometriespublic.Surveyor', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'TopoPolyline',
                'verbose_name_plural': 'TopoPolylines',
            },
        ),
        migrations.RunPython(
            code=create_layers,
        ),
    ]
