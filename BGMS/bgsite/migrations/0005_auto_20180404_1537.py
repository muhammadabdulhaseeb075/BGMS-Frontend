# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0004_auto_20180404_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memorialinscriptiondetail',
            name='name',
        ),
        migrations.AddField(
            model_name='memorialinscriptiondetail',
            name='first_names',
            field=models.CharField(verbose_name='First names', max_length=200, blank=True, validators=[main.validators.bleach_validator], null=True),
        ),
        migrations.AddField(
            model_name='memorialinscriptiondetail',
            name='last_name',
            field=models.CharField(verbose_name='Last name', max_length=35, blank=True, validators=[main.validators.bleach_validator], null=True),
        ),
    ]
