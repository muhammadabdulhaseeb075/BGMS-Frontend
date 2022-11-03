# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0008_auto_20160517_2249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagehistory',
            name='state',
        ),
        migrations.RemoveField(
            model_name='templatehistory',
            name='state',
        ),
    ]
