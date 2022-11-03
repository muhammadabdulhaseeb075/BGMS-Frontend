# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0001_initial'),
        ('bgsite', '0017_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='topopolygon',
            field=models.OneToOneField(editable=False, related_name='section', to='geometries.TopoPolygons', null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='subsection',
            name='topopolygon',
            field=models.OneToOneField(editable=False, related_name='subsection', to='geometries.TopoPolygons', null=True, on_delete=models.CASCADE),
        ),
    ]
