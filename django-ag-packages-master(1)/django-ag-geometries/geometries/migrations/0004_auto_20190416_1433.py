# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0003_move_attribute_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='featureattributes',
            name='date_value',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='featureattributes',
            name='textarea_value',
            field=models.CharField(max_length=400, blank=True, null=True),
        ),
    ]
