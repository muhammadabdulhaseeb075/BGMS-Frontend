# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0008_auto_20180816_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='burial',
            name='depth_position',
            field=models.CharField(null=True, verbose_name='Depth position of grave', blank=True, max_length=15),
        ),
    ]
