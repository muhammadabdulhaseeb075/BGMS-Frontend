# Generated by Django 2.2.9 on 2022-01-27 14:10

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cemeteryadmin', '0023_auto_20210504_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('preferences', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
