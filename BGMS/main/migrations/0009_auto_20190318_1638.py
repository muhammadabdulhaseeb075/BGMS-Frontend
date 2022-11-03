# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20190315_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='first_line',
            field=models.CharField(null=True, blank=True, max_length=200),
        ),
    ]
