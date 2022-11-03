# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('bgsite', '0025_auto_20190225_1243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='address',
        ),
        migrations.RemoveField(
            model_name='owner',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='owner',
            name='data_upload',
        ),
        migrations.RemoveField(
            model_name='gravedeed',
            name='owners',
        ),
        migrations.RemoveField(
            model_name='graveowner',
            name='owner',
        ),
        migrations.AddField(
            model_name='graveowner',
            name='owner_id',
            field=models.UUIDField(null=True),
        ),
        migrations.AddField(
            model_name='graveowner',
            name='owner_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='grave_owners', to='contenttypes.ContentType'),
        ),
        migrations.DeleteModel(
            name='Owner',
        ),
    ]
