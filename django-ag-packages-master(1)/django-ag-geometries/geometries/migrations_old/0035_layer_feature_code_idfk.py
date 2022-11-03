# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0034_auto_20170126_1546'),
    ]

    operations = [
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
    ]
