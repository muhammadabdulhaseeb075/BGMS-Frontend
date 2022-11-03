# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0024_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='graveowner',
            old_name='impossible_owner_date',
            new_name='impossible_owner_from_date',
        ),
        migrations.RenameField(
            model_name='graveowner',
            old_name='owner_date',
            new_name='owner_from_date',
        ),
        migrations.RemoveField(
            model_name='graveowner',
            name='owner_date_day',
        ),
        migrations.RemoveField(
            model_name='graveowner',
            name='owner_date_month',
        ),
        migrations.RemoveField(
            model_name='graveowner',
            name='owner_date_year',
        ),
        migrations.AddField(
            model_name='gravedeed',
            name='data_upload',
            field=models.ForeignKey(verbose_name='Data Upload', to='bgsite.DataUpload', help_text='The data upload from which this record was created.', null=True, blank=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='graveowner',
            name='impossible_owner_to_date',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='graveowner',
            name='owner_from_date_day',
            field=models.IntegerField(null=True, verbose_name='Day Ownership Began', blank=True),
        ),
        migrations.AddField(
            model_name='graveowner',
            name='owner_from_date_month',
            field=models.IntegerField(null=True, verbose_name='Month Ownership Began', blank=True),
        ),
        migrations.AddField(
            model_name='graveowner',
            name='owner_from_date_year',
            field=models.IntegerField(null=True, verbose_name='Year Ownership Began', blank=True),
        ),
        migrations.AddField(
            model_name='graveowner',
            name='owner_to_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='graveowner',
            name='owner_to_date_day',
            field=models.IntegerField(null=True, verbose_name='Day Ownership Ended', blank=True),
        ),
        migrations.AddField(
            model_name='graveowner',
            name='owner_to_date_month',
            field=models.IntegerField(null=True, verbose_name='Month Ownership Ended', blank=True),
        ),
        migrations.AddField(
            model_name='graveowner',
            name='owner_to_date_year',
            field=models.IntegerField(null=True, verbose_name='Year Ownership Ended', blank=True),
        ),
        migrations.AlterField(
            model_name='featuresrelationship',
            name='relationship',
            field=models.ForeignKey(to='main.RelationshipType', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.RemoveField(
            model_name='owner',
            name='address',
        ),
        migrations.AddField(
            model_name='owner',
            name='address',
            field=models.ManyToManyField(blank=True, to='bgsite.Address'),
        ),
        migrations.AlterField(
            model_name='section',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='subsection',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
