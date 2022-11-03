# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0015_auto_20160629_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='is_through_field',
            field=models.BooleanField(default=False),
        ),
    ]
