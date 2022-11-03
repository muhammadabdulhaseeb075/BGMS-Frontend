# Generated by Django 2.1 on 2019-10-23 01:22

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('table_schema', django.contrib.postgres.fields.jsonb.JSONField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
