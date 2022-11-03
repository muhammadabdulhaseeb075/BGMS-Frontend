# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_dataentryuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(max_length=35, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=35, blank=True),
        ),
        migrations.AlterField(
            model_name='parish',
            name='parish',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='religion',
            name='religion',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
