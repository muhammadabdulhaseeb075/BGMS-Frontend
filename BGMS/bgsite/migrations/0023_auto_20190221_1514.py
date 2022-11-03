# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0022_migrate_to_deed_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graveplot',
            name='cost_currency',
        ),
        migrations.RemoveField(
            model_name='graveplot',
            name='cost_subunit',
        ),
        migrations.RemoveField(
            model_name='graveplot',
            name='cost_subunit2',
        ),
        migrations.RemoveField(
            model_name='graveplot',
            name='cost_unit',
        ),
        migrations.RemoveField(
            model_name='graveplot',
            name='impossible_date',
        ),
        migrations.RemoveField(
            model_name='graveplot',
            name='impossible_date_day',
        ),
        migrations.RemoveField(
            model_name='graveplot',
            name='impossible_date_month',
        ),
        migrations.RemoveField(
            model_name='graveplot',
            name='impossible_date_year',
        ),
        migrations.RemoveField(
            model_name='graveplot',
            name='purchase_date',
        ),
        migrations.RemoveField(
            model_name='graveplot',
            name='tenure_years',
        ),
    ]
