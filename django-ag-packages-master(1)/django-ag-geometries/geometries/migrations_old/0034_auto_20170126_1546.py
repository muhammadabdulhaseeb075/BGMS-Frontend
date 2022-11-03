# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        # ('filemanager', '0002_auto_20170123_1225'),
        ('geometries', '0033_auto_20160823_1110'),
    ]

    operations = [
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
            options={'verbose_name': 'TopoPoint', 'verbose_name_plural': 'TopoPoints'},
        ),
        migrations.AlterModelOptions(
            name='topopolygons',
            options={'verbose_name': 'TopoPolygon', 'verbose_name_plural': 'TopoPolygons'},
        ),
        migrations.AlterModelOptions(
            name='topopolylines',
            options={'verbose_name': 'TopoPolyline', 'verbose_name_plural': 'TopoPolylines'},
        ),
        migrations.AlterField(
            model_name='attribute',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='layer',
            name='feature_code',
            field=models.ForeignKey(to='geometriespublic.FeatureCode'),
        ),
        migrations.AlterField(
            model_name='layer',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='raster',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='topopoints',
            name='attributes',
            field=models.ManyToManyField(blank=True, to='geometries.Attribute'),
        ),
        migrations.AlterField(
            model_name='topopoints',
            name='geom_acc',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='topopoints',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='topopoints',
            name='surveyor',
            field=models.ForeignKey(blank=True, to='geometriespublic.Surveyor', null=True),
        ),
        migrations.AlterField(
            model_name='topopolygons',
            name='attributes',
            field=models.ManyToManyField(blank=True, to='geometries.Attribute'),
        ),
        migrations.AlterField(
            model_name='topopolygons',
            name='geom_acc',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='topopolygons',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='topopolygons',
            name='surveyor',
            field=models.ForeignKey(blank=True, to='geometriespublic.Surveyor', null=True),
        ),
        migrations.AlterField(
            model_name='topopolylines',
            name='attributes',
            field=models.ManyToManyField(blank=True, to='geometries.Attribute'),
        ),
        migrations.AlterField(
            model_name='topopolylines',
            name='geom_acc',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='topopolylines',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='topopolylines',
            name='surveyor',
            field=models.ForeignKey(blank=True, to='geometriespublic.Surveyor', null=True),
        ),
    ]
