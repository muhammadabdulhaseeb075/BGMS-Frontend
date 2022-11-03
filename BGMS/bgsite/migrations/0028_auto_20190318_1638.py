# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0027_graveowner_data_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graveowner',
            name='owner_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to='contenttypes.ContentType'),
        ),
    ]
