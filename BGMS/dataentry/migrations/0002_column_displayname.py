# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='displayname',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
