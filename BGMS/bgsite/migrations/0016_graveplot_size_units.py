# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0015_auto_20181122_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='graveplot',
            name='size_units',
            field=models.CharField(null=True, max_length=15, validators=[main.validators.bleach_validator], blank=True),
        ),
    ]
