# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0032_auto_20160725_1429'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='attribute',
        #     name='id',
        #     field=models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True),
        # ),
        # migrations.AlterField(
        #     model_name='layer',
        #     name='id',
        #     field=models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True),
        # ),
        # migrations.AlterField(
        #     model_name='raster',
        #     name='id',
        #     field=models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True),
        # ),
        migrations.AlterField(
            model_name='topopoints',
            name='feature_id',
            field=models.CharField(max_length=10),
        ),
        # migrations.AlterField(
        #     model_name='topopoints',
        #     name='id',
        #     field=models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True),
        # ),
        migrations.AlterField(
            model_name='topopolygons',
            name='feature_id',
            field=models.CharField(max_length=10),
        ),
        # migrations.AlterField(
        #     model_name='topopolygons',
        #     name='id',
        #     field=models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True),
        # ),
        migrations.AlterField(
            model_name='topopolylines',
            name='feature_id',
            field=models.CharField(max_length=10),
        ),
        # migrations.AlterField(
        #     model_name='topopolylines',
        #     name='id',
        #     field=models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True),
        # ),
    ]
