# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150817_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitedetails',
            name='address',
            field=models.ForeignKey(to='main.Address', null=True),
        ),
    ]
