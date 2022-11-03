# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamatching', '0010_remove_datamatchingmemorial_memorial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datamatchinguser',
            name='memorials',
        ),
        migrations.RemoveField(
            model_name='datamatchinguser',
            name='user',
        ),
        migrations.RemoveField(
            model_name='memorialuserlink',
            name='datamatching_memorial',
        ),
        migrations.RemoveField(
            model_name='memorialuserlink',
            name='datamatching_user',
        ),
        migrations.DeleteModel(
            name='DataMatchingMemorial',
        ),
        migrations.DeleteModel(
            name='DatamatchingUser',
        ),
        migrations.DeleteModel(
            name='MemorialUserLink',
        ),
    ]
