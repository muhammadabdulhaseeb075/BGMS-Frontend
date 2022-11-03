# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_dataentryuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewDataMatchingUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('main.bguser',),
            managers=[
                ('objects', main.models.BGUserManager()),
            ],
        ),
    ]
