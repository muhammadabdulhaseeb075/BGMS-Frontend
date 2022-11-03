# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_newdatamatchinguser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NewDataMatchingUser',
        ),
        migrations.CreateModel(
            name='DataMatchingUser',
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
