# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0010_auto_20181023_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(validators=[main.validators.bleach_validator], blank=True, max_length=35, null=True)),
                ('description', models.CharField(validators=[main.validators.bleach_validator], blank=True, max_length=35, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewParish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('parish', models.CharField(validators=[main.validators.bleach_validator], blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewReligion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('religion', models.CharField(validators=[main.validators.bleach_validator], blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='death',
            name='newevent',
            field=models.ForeignKey(to='bgsite.NewEvent', help_text='Optional. Death have one related Event', blank=True, null=True, verbose_name='War/Event related to Death', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='death',
            name='newparish',
            field=models.ForeignKey(to='bgsite.NewParish', blank=True, null=True, verbose_name='Parish', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='death',
            name='newreligion',
            field=models.ForeignKey(to='bgsite.NewReligion', blank=True, null=True, verbose_name='Religion', on_delete=models.CASCADE),
        ),
    ]
