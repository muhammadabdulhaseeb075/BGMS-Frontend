# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geometriespublic', '0001_initial'),
        ('geometries', '0037_remove_layer_feature_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='feature_code',
            field=models.ForeignKey(to='geometriespublic.FeatureCode', null=True),
        ),
    ]
