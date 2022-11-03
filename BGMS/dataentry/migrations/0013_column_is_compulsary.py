# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0012_auto_20160608_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='is_compulsary',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='columnposition',
            name='displayname',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
