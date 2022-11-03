# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
import geometriespublic.validators
from django.core.management import call_command

def pupulate_featurecode_featuregroup(apps, schema_editor):
    if connection.schema_name == 'public':
        call_command('loaddata', 'featuregroup.json')
        call_command('loaddata', 'featurecode.json')
    # call_command('loaddata', 'geometriespublic_featuregroup_feature_codes.json')


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('feature_type', models.CharField(db_index=True, validators=[geometriespublic.validators.bleach_validator], max_length=20)),
                ('type', models.CharField(validators=[geometriespublic.validators.bleach_validator], max_length=20)),
                ('display_name', models.CharField(validators=[geometriespublic.validators.bleach_validator], max_length=20)),
                ('min_resolution', models.FloatField()),
                ('max_resolution', models.FloatField()),
                ('show_in_toolbar', models.BooleanField()),
                ('hierarchy', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('group_code', models.CharField(validators=[geometriespublic.validators.bleach_validator], max_length=20)),
                ('display_name', models.CharField(validators=[geometriespublic.validators.bleach_validator], max_length=20)),
                ('switch_on_off', models.BooleanField(default=True)),
                ('initial_visibility', models.BooleanField(default=False)),
                ('hierarchy', models.IntegerField()),
                ('feature_codes', models.ManyToManyField(to='geometriespublic.FeatureCode')),
            ],
        ),
        migrations.CreateModel(
            name='Surveyor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('surveyor_name', models.CharField(validators=[geometriespublic.validators.bleach_validator], max_length=100)),
            ],
        ),
        migrations.RunPython(
            code=pupulate_featurecode_featuregroup,
        ),
    ]
