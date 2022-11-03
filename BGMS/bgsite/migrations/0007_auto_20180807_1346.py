# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0006_auto_20180801_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='owner_date',
        ),
        migrations.AddField(
            model_name='burial',
            name='register_page',
            field=models.IntegerField(null=True, verbose_name='Page number in register', blank=True),
        ),
        migrations.AddField(
            model_name='featuresrelationship',
            name='data_upload',
            field=models.ForeignKey(null=True, blank=True, verbose_name='Data Upload', help_text='The data upload from which this record was created.', to='bgsite.DataUpload', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='owner',
            name='data_upload',
            field=models.ForeignKey(null=True, blank=True, verbose_name='Data Upload', help_text='The data upload from which this record was created.', to='bgsite.DataUpload', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='address',
            name='first_line',
            field=models.CharField(max_length=200, blank=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='address',
            name='second_line',
            field=models.CharField(null=True, max_length=200, blank=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='burial',
            name='cremation_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='burial',
            name='register',
            field=models.CharField(null=True, max_length=30, verbose_name='Register recording burial name/code', blank=True, validators=[main.validators.bleach_validator]),
        ),
    ]
