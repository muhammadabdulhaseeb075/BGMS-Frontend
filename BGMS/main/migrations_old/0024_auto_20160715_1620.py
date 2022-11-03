# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitedetails',
            name='default_srid',
        ),
        migrations.RemoveField(
            model_name='sitedetails',
            name='matrixIds',
        ),
        migrations.RemoveField(
            model_name='sitedetails',
            name='resolutions',
        ),
        migrations.RemoveField(
            model_name='sitedetails',
            name='style',
        ),
    ]
