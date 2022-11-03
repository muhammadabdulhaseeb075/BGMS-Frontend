# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import main.validators
import uuid
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False, db_index=True)),
                ('name', models.CharField(validators=[main.validators.bleach_validator], blank=True, null=True, max_length=200, verbose_name='Company names')),
                ('remarks', models.CharField(validators=[main.validators.bleach_validator], blank=True, null=True, max_length=200, verbose_name='Remarks about Person')),
                ('from_data_upload', models.BooleanField(default=False)),
                ('date', models.DateTimeField(null=True, auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False, db_index=True)),
                ('title', models.CharField(validators=[main.validators.bleach_validator], blank=True, null=True, max_length=30, verbose_name='Title')),
                ('first_names', models.CharField(validators=[main.validators.bleach_validator], blank=True, null=True, max_length=200, verbose_name='First names')),
                ('birth_name', models.CharField(validators=[main.validators.bleach_validator], blank=True, null=True, max_length=200, verbose_name='Birth name')),
                ('other_names', models.CharField(validators=[main.validators.bleach_validator], blank=True, null=True, max_length=100, verbose_name='Nicknames')),
                ('last_name', models.CharField(validators=[main.validators.bleach_validator], blank=True, null=True, max_length=35, verbose_name='Last name')),
                ('birth_date', models.DateField(null=True, editable=False)),
                ('impossible_birth_date', models.BooleanField(help_text='If true means the others day/month/year fields have the non real date entered in the registry for the person', default=False, editable=False)),
                ('birth_date_day', models.IntegerField(blank=True, null=True, verbose_name='Day of Birth')),
                ('birth_date_month', models.IntegerField(blank=True, null=True, verbose_name='Month of Birth')),
                ('birth_date_year', models.IntegerField(blank=True, null=True, verbose_name='Year of Birth')),
                ('gender', models.CharField(validators=[main.validators.bleach_validator], blank=True, null=True, max_length=10, verbose_name='Gender')),
                ('remarks', models.CharField(validators=[main.validators.bleach_validator], blank=True, null=True, max_length=200, verbose_name='Remarks about Person')),
                ('from_data_upload', models.BooleanField(default=False)),
                ('date', models.DateTimeField(null=True, auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.CharField(blank=True, null=True, max_length=50),
        ),
        migrations.AddField(
            model_name='address',
            name='second_line',
            field=models.CharField(blank=True, null=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='county',
            field=models.CharField(blank=True, null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='address',
            name='first_line',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='postcode',
            field=models.CharField(blank=True, null=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='address',
            name='town',
            field=models.CharField(blank=True, null=True, max_length=50),
        ),
        migrations.AddField(
            model_name='person',
            name='addresses',
            field=models.ManyToManyField(to='main.Address'),
        ),
        migrations.AddField(
            model_name='person',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='addresses',
            field=models.ManyToManyField(to='main.Address'),
        ),
        migrations.AddField(
            model_name='company',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='persons',
            field=models.ManyToManyField(to='main.Person'),
        ),
    ]
