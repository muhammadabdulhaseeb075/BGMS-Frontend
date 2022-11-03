# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # ('geometries', '0034_auto_20170126_1546'),
        ('filemanager', '0003_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='topopolygon',
            field=models.ForeignKey(null=True, to='geometries.TopoPolygons', on_delete=models.CASCADE),
        ),
    ]
