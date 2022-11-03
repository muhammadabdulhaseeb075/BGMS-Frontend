# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0013_auto_20181026_0942'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewEvent',
            new_name='Event',
        ),
        migrations.RenameModel(
            old_name='NewParish',
            new_name='Parish',
        ),
        migrations.RenameModel(
            old_name='NewReligion',
            new_name='Religion',
        ),
        migrations.RenameField(
            model_name='death',
            old_name='newevent',
            new_name='event',
        ),
        migrations.RenameField(
            model_name='death',
            old_name='newparish',
            new_name='parish',
        ),
        migrations.RenameField(
            model_name='death',
            old_name='newreligion',
            new_name='religion',
        ),
    ]
