# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0036_auto_20170129_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='layer',
            name='feature_code',
        ),
    ]
