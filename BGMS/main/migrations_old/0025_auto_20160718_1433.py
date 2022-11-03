# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20160715_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitedetails',
            name='aerial',
            field=models.BooleanField(default=True, verbose_name='Aerial?'),
        ),
        migrations.AlterField(
            model_name='sitedetails',
            name='layer',
            field=models.CharField(null=True, max_length=20, verbose_name='Schema Name', help_text='Only one word in lowercase'),
        ),
    ]
