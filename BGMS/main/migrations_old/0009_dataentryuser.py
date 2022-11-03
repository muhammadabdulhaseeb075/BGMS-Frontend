# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataEntryUser',
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
