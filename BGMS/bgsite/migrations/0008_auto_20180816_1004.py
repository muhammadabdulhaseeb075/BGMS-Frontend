# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0007_auto_20180807_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graveplot',
            name='length',
        ),
        migrations.RemoveField(
            model_name='graveplot',
            name='width',
        ),
        migrations.AddField(
            model_name='graveplot',
            name='size',
            field=models.CharField(null=True, blank=True, validators=[main.validators.bleach_validator], max_length=15),
        ),
        migrations.AlterField(
            model_name='graveplot',
            name='size_units',
            field=models.CharField(null=True, blank=True, validators=[main.validators.bleach_validator], max_length=15),
        ),
    ]
