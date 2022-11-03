# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20190321_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='phone_number_2',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='phone_number_2',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
