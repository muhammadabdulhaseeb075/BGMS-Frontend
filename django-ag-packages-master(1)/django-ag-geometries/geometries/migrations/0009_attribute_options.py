# Generated by Django 2.1 on 2019-07-17 11:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0008_auto_20190520_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='options',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None, verbose_name="Options (for 'Select' type only)"),
        ),
    ]
