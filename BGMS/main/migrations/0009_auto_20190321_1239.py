# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
from django.conf import settings
from django.core.management import call_command
import django.db.models.deletion


def populate_featurecode_featuregroup(apps, schema_editor):
    if connection.schema_name == 'public':
        call_command('loaddata', 'burialofficialtype.json')


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20190315_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.EmailField(null=True, blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='company',
            name='phone_number',
            field=models.CharField(null=True, blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(null=True, blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='person',
            name='phone_number',
            field=models.CharField(null=True, blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='burialgroundsite',
            name='client',
            field=models.ForeignKey(to='main.Client', null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='company',
            name='clients',
            field=models.ManyToManyField(to='main.Client'),
        ),
        migrations.AddField(
            model_name='person',
            name='clients',
            field=models.ManyToManyField(to='main.Client'),
        ),
        migrations.RunPython(
            code=populate_featurecode_featuregroup,
        ),
    ]
