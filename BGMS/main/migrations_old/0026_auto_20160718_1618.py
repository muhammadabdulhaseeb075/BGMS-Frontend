# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20160718_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitedetails',
            name='layer',
            field=models.CharField(help_text='WMTS Layer name / Schema name', verbose_name='Schema name', null=True, max_length=20),
        ),
    ]
