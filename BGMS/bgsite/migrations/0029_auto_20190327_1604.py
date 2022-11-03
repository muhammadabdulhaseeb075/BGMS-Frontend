# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0028_auto_20190318_1638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='graveowner',
            old_name='owner_type',
            new_name='content_type',
        ),
        migrations.RenameField(
            model_name='graveowner',
            old_name='owner_id',
            new_name='object_id',
        ),
    ]
