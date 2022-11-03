# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(validators=[main.validators.bleach_validator], max_length=20, unique=True)),
                ('symbol', models.CharField(null=True, validators=[main.validators.bleach_validator], blank=True, max_length=1)),
                ('unit_name', models.CharField(null=True, validators=[main.validators.bleach_validator], blank=True, max_length=20)),
                ('subunit1_name', models.CharField(null=True, validators=[main.validators.bleach_validator], blank=True, max_length=20)),
                ('subunit2_name', models.CharField(null=True, validators=[main.validators.bleach_validator], blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RelationshipType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('type', models.CharField(unique=True, max_length=40)),
            ],
        ),
    ]
