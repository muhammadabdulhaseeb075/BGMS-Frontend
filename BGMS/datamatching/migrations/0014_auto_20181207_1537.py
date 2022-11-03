# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamatching', '0013_auto_20160504_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datamatchingmemorial',
            name='memorial',
            field=models.OneToOneField(primary_key=True, related_name='data_matching', serialize=False, to='bgsite.Memorial', on_delete=models.CASCADE),
        ),
    ]
