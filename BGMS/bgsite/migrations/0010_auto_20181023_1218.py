# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0010_auto_20181011_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='burial',
            name='impossible_cremation_date',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='burial',
            name='impossible_cremation_date_day',
            field=models.IntegerField(blank=True, verbose_name='Day of Cremation', null=True),
        ),
        migrations.AddField(
            model_name='burial',
            name='impossible_cremation_date_month',
            field=models.IntegerField(blank=True, verbose_name='Month of Cremation', null=True),
        ),
        migrations.AddField(
            model_name='burial',
            name='impossible_cremation_date_year',
            field=models.IntegerField(blank=True, verbose_name='Year of Cremation', null=True),
        ),
        migrations.AlterField(
            model_name='burial',
            name='cremation_date',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='graveplot',
            name='impossible_date_day',
            field=models.IntegerField(blank=True, verbose_name='Day of Purchase', null=True),
        ),
        migrations.AlterField(
            model_name='graveplot',
            name='impossible_date_month',
            field=models.IntegerField(blank=True, verbose_name='Month of Purchase', null=True),
        ),
        migrations.AlterField(
            model_name='graveplot',
            name='impossible_date_year',
            field=models.IntegerField(blank=True, verbose_name='Year of Purchase', null=True),
        ),
    ]
