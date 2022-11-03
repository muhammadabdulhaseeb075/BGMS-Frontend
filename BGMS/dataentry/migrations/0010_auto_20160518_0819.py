# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0009_auto_20160517_2253'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagehistory',
            old_name='user_state',
            new_name='state',
        ),
        migrations.RenameField(
            model_name='templatehistory',
            old_name='user_state',
            new_name='state',
        ),
    ]
