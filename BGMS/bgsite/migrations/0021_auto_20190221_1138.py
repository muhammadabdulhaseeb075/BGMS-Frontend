# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0020_auto_20190221_1059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gravedeed',
            old_name='impossible_date',
            new_name='impossible_purchase_date',
        ),
        migrations.RenameField(
            model_name='gravedeed',
            old_name='impossible_date_day',
            new_name='purchase_date_day',
        ),
        migrations.RenameField(
            model_name='gravedeed',
            old_name='impossible_date_month',
            new_name='purchase_date_month',
        ),
        migrations.RenameField(
            model_name='gravedeed',
            old_name='impossible_date_year',
            new_name='purchase_date_year',
        ),
    ]
