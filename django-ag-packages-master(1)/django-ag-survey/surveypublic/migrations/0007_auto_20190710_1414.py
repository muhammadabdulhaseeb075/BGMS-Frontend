# Generated by Django 2.1 on 2019-07-10 13:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveypublic', '0006_publicsurveytemplatefield_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicsurveytemplatefield',
            name='options',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None, verbose_name="Options (for 'Select' type only)"),
        ),
    ]
