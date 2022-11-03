# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20181026_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featuregroup',
            name='feature_codes',
        ),
        migrations.DeleteModel(
            name='FeatureCode',
        ),
        migrations.DeleteModel(
            name='FeatureGroup',
        ),
    ]
