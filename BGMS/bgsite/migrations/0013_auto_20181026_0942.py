# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0012_move_event_religion_parish_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='death',
            name='event',
        ),
        migrations.RemoveField(
            model_name='death',
            name='parish',
        ),
        migrations.RemoveField(
            model_name='death',
            name='religion',
        ),
    ]
