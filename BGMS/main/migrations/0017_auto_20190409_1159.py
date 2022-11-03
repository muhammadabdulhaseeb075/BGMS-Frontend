# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import main.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0027_graveowner_data_upload'),
        ('main', '0016_auto_20190408_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicPerson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, editable=False, serialize=False)),
                ('title', models.CharField(max_length=30, null=True, verbose_name='Title', validators=[main.validators.bleach_validator], blank=True)),
                ('first_names', models.CharField(max_length=200, null=True, verbose_name='First names', validators=[main.validators.bleach_validator], blank=True)),
                ('birth_name', models.CharField(max_length=200, null=True, verbose_name='Birth name', validators=[main.validators.bleach_validator], blank=True)),
                ('other_names', models.CharField(max_length=100, null=True, verbose_name='Nicknames', validators=[main.validators.bleach_validator], blank=True)),
                ('last_name', models.CharField(max_length=35, null=True, verbose_name='Last name', validators=[main.validators.bleach_validator], blank=True)),
                ('birth_date', models.DateField(editable=False, null=True)),
                ('impossible_birth_date', models.BooleanField(default=False, editable=False, help_text='If true means the others day/month/year fields have the non real date entered in the registry for the person')),
                ('birth_date_day', models.IntegerField(null=True, verbose_name='Day of Birth', blank=True)),
                ('birth_date_month', models.IntegerField(null=True, verbose_name='Month of Birth', blank=True)),
                ('birth_date_year', models.IntegerField(null=True, verbose_name='Year of Birth', blank=True)),
                ('gender', models.CharField(max_length=10, null=True, verbose_name='Gender', validators=[main.validators.bleach_validator], blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=20, null=True, blank=True)),
                ('phone_number_2', models.CharField(max_length=20, null=True, blank=True)),
                ('remarks', models.CharField(max_length=200, null=True, verbose_name='Remarks about Person', validators=[main.validators.bleach_validator], blank=True)),
                ('from_data_upload', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('addresses', models.ManyToManyField(to='main.Address')),
                ('clients', models.ManyToManyField(to='main.Client')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='person',
            name='addresses',
        ),
        migrations.RemoveField(
            model_name='person',
            name='clients',
        ),
        migrations.RemoveField(
            model_name='person',
            name='created_by',
        ),
        migrations.AlterField(
            model_name='company',
            name='persons',
            field=models.ManyToManyField(to='main.PublicPerson'),
        ),
        migrations.AlterField(
            model_name='company',
            name='remarks',
            field=models.CharField(max_length=200, null=True, verbose_name='Remarks about company', validators=[main.validators.bleach_validator], blank=True),
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
