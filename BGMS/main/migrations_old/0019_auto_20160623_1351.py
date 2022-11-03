# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20160622_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(null=True, max_length=35, validators=[main.validators.bleach_validator], blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(null=True, max_length=35, validators=[main.validators.bleach_validator], blank=True),
        ),
        migrations.AlterField(
            model_name='featurecode',
            name='display_name',
            field=models.CharField(max_length=20, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='featurecode',
            name='feature_type',
            field=models.CharField(max_length=20, db_index=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='featurecode',
            name='type',
            field=models.CharField(max_length=20, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='featuregroup',
            name='display_name',
            field=models.CharField(max_length=20, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='featuregroup',
            name='group_code',
            field=models.CharField(max_length=20, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='imagestate',
            name='image_state',
            field=models.CharField(max_length=15, validators=[main.validators.bleach_validator], unique=True),
        ),
        migrations.AlterField(
            model_name='imagetype',
            name='image_type',
            field=models.CharField(max_length=20, validators=[main.validators.bleach_validator], unique=True),
        ),
        migrations.AlterField(
            model_name='nicknames',
            name='actual_name',
            field=models.CharField(max_length=30, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='nicknames',
            name='nickname',
            field=models.CharField(max_length=20, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='parish',
            name='parish',
            field=models.CharField(null=True, max_length=50, validators=[main.validators.bleach_validator], blank=True),
        ),
        migrations.AlterField(
            model_name='religion',
            name='religion',
            field=models.CharField(null=True, max_length=50, validators=[main.validators.bleach_validator], blank=True),
        ),
        migrations.AlterField(
            model_name='surveyor',
            name='surveyor_name',
            field=models.CharField(max_length=100, validators=[main.validators.bleach_validator]),
        ),
    ]
