# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0016_column_is_through_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='column',
            name='is_through_field',
        ),
        migrations.AddField(
            model_name='column',
            name='through_field',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
