# Generated by Django 2.1 on 2019-10-01 02:35

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20190613_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('table_schema', django.contrib.postgres.fields.jsonb.JSONField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
