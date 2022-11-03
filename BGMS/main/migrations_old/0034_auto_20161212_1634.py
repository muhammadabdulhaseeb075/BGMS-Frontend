# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_auto_20161006_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteGroupSite',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('main.sitegroup',),
        ),
        migrations.AddField(
            model_name='bguser',
            name='_is_staff',
            field=models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.'),
        ),
    ]
