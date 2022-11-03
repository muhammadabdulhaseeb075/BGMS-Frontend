# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.contrib.gis.db.models.fields
import uuid


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# geometries.migrations.0036_auto_20170129_1703
# geometries.migrations.0029_auto_20160704_1253
# geometries.migrations.0030_auto_20160712_0818
# geometries.migrations.0032_auto_20160725_1429
# geometries.migrations.0031_auto_20160714_0945
# geometries.migrations.0028_auto_20160608_1434
# geometries.migrations.0001_squashed_0027_auto_20160218_1400

class Migration(migrations.Migration):

    replaces = [('geometries', '0001_squashed_0027_auto_20160218_1400'), ('geometries', '0028_auto_20160608_1434'), ('geometries', '0029_auto_20160704_1253'), ('geometries', '0030_auto_20160712_0818'), ('geometries', '0031_auto_20160714_0945'), ('geometries', '0032_auto_20160725_1429'), ('geometries', '0033_auto_20160823_1110'), ('geometries', '0034_auto_20170126_1546'), ('geometries', '0035_layer_feature_code_idfk'), ('geometries', '0036_auto_20170129_1703'), ('geometries', '0037_remove_layer_feature_code'), ('geometries', '0038_layer_feature_code')]

    dependencies = [
        ('geometriespublic', '0001_initial'),
        ('filemanager', '0002_auto_20170123_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, verbose_name='ID', default=uuid.uuid4)),
                ('display_name', models.CharField(max_length=20)),
                ('show_in_toolbar', models.BooleanField()),
                ('initial_visibility', models.BooleanField(default=False)),
                ('feature_code', models.ForeignKey(to='main.FeatureCode')),
            ],
        ),
        migrations.CreateModel(
            name='TopoPoints',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, verbose_name='ID', default=uuid.uuid4)),
                ('veg_spread', models.FloatField(null=True)),
                ('date_uploaded', models.DateField(default=django.utils.timezone.now, null=True)),
                ('geom_acc', models.FloatField(null=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=27700)),
                ('layer', models.ForeignKey(to='geometries.Layer', on_delete=models.CASCADE)),
                ('surveyor', models.ForeignKey(to='main.Surveyor', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TopoPolygons',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, verbose_name='ID', default=uuid.uuid4)),
                ('date_uploaded', models.DateField(default=django.utils.timezone.now, null=True)),
                ('geom_acc', models.FloatField(null=True)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=27700)),
                ('layer', models.ForeignKey(to='geometries.Layer', on_delete=models.CASCADE)),
                ('surveyor', models.ForeignKey(to='main.Surveyor', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TopoPolylines',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, verbose_name='ID', default=uuid.uuid4)),
                ('width', models.FloatField(null=True)),
                ('date_uploaded', models.DateField(default=django.utils.timezone.now, null=True)),
                ('geom_acc', models.FloatField(null=True)),
                ('geometry', django.contrib.gis.db.models.fields.MultiLineStringField(srid=27700)),
                ('layer', models.ForeignKey(to='geometries.Layer', on_delete=models.CASCADE)),
                ('surveyor', models.ForeignKey(to='main.Surveyor', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Raster',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, verbose_name='ID', default=uuid.uuid4)),
                ('type', models.CharField(max_length=10)),
                ('url', models.CharField(max_length=200)),
                ('layer', models.ForeignKey(to='geometries.Layer', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, verbose_name='ID', default=uuid.uuid4)),
                ('attribute_name', models.CharField(max_length=100)),
                ('attribute_value', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='topopoints',
            name='attributes',
            field=models.ManyToManyField(to='geometries.Attribute'),
        ),
        migrations.AddField(
            model_name='topopolygons',
            name='attributes',
            field=models.ManyToManyField(to='geometries.Attribute'),
        ),
        migrations.AddField(
            model_name='topopolylines',
            name='attributes',
            field=models.ManyToManyField(to='geometries.Attribute'),
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
        # migrations.RunPython(
        #     code=geometries.migrations.0001_squashed_0027_auto_20160218_1400.create_layers,
        # ),
        # migrations.RunPython(
        #     code=geometries.migrations.0028_auto_20160608_1434.merge_coffin_and_table_tomb_into_chest_tomb,
        # ),
        # migrations.RunPython(
        #     code=geometries.migrations.0029_auto_20160704_1253.migrate_statue_obelisk,
        # ),
        # migrations.RunPython(
        #     code=geometries.migrations.0030_auto_20160712_0818.delete_features_surfaces,
        # ),
        # migrations.RunPython(
        #     code=geometries.migrations.0031_auto_20160714_0945.switch_initial_visibility,
        # ),
        # migrations.RunPython(
        #     code=geometries.migrations.0032_auto_20160725_1429.populate_featurecode_reserved_plot,
        # ),
        migrations.AlterField(
            model_name='topopoints',
            name='feature_id',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='topopolygons',
            name='feature_id',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='topopolylines',
            name='feature_id',
            field=models.CharField(max_length=10),
        ),
        migrations.AddField(
            model_name='topopoints',
            name='file',
            field=models.ForeignKey(to='filemanager.File', null=True),
        ),
        migrations.AddField(
            model_name='topopolygons',
            name='file',
            field=models.ForeignKey(to='filemanager.File', null=True),
        ),
        migrations.AddField(
            model_name='topopolylines',
            name='file',
            field=models.ForeignKey(to='filemanager.File', null=True),
        ),
        migrations.AlterModelOptions(
            name='topopoints',
            options={'verbose_name_plural': 'TopoPoints', 'verbose_name': 'TopoPoint'},
        ),
        migrations.AlterModelOptions(
            name='topopolygons',
            options={'verbose_name_plural': 'TopoPolygons', 'verbose_name': 'TopoPolygon'},
        ),
        migrations.AlterModelOptions(
            name='topopolylines',
            options={'verbose_name_plural': 'TopoPolylines', 'verbose_name': 'TopoPolyline'},
        ),
        migrations.AlterField(
            model_name='attribute',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='layer',
            name='feature_code',
            field=models.ForeignKey(to='geometriespublic.FeatureCode'),
        ),
        migrations.AlterField(
            model_name='layer',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='raster',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='topopoints',
            name='attributes',
            field=models.ManyToManyField(to='geometries.Attribute', blank=True),
        ),
        migrations.AlterField(
            model_name='topopoints',
            name='geom_acc',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='topopoints',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='topopoints',
            name='surveyor',
            field=models.ForeignKey(to='geometriespublic.Surveyor', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='topopolygons',
            name='attributes',
            field=models.ManyToManyField(to='geometries.Attribute', blank=True),
        ),
        migrations.AlterField(
            model_name='topopolygons',
            name='geom_acc',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='topopolygons',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='topopolygons',
            name='surveyor',
            field=models.ForeignKey(to='geometriespublic.Surveyor', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='topopolylines',
            name='attributes',
            field=models.ManyToManyField(to='geometries.Attribute', blank=True),
        ),
        migrations.AlterField(
            model_name='topopolylines',
            name='geom_acc',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='topopolylines',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='topopolylines',
            name='surveyor',
            field=models.ForeignKey(to='geometriespublic.Surveyor', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='layer',
            name='feature_code_idfk',
            field=models.IntegerField(null=True),
        ),
        migrations.RemoveField(
            model_name='topopoints',
            name='file',
        ),
        migrations.RemoveField(
            model_name='topopolygons',
            name='file',
        ),
        migrations.RemoveField(
            model_name='topopolylines',
            name='file',
        ),
        # migrations.RunPython(
        #     code=geometries.migrations.0036_auto_20170129_1703.move_featurecodes_fk,
        # ),
        migrations.RemoveField(
            model_name='layer',
            name='feature_code',
        ),
        migrations.AddField(
            model_name='layer',
            name='feature_code',
            field=models.ForeignKey(to='geometriespublic.FeatureCode', null=True),
        ),
    ]
