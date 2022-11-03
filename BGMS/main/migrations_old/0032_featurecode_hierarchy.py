# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_auto_20160920_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='featurecode',
            name='hierarchy',
            field=models.IntegerField(default=0),
        ),
    ]
