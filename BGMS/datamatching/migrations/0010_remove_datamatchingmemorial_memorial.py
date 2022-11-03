# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamatching', '0009_auto_20150822_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datamatchingmemorial',
            name='memorial',
        ),
        migrations.AddField(
            model_name='datamatchingmemorial',
            name='memorial',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
