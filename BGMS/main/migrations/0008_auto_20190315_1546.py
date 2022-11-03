# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20190228_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='current',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='address',
            name='from_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='from_date_day',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='from_date_month',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='from_date_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='impossible_from_date',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='address',
            name='impossible_to_date',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='address',
            name='to_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='to_date_day',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='to_date_month',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='to_date_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
