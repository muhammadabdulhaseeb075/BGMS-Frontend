# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150902_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featurecode',
            name='feature_type',
            field=models.CharField(max_length=20, db_index=True),
        ),
    ]
