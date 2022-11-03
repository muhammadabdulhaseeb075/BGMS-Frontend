# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datamatching', '0004_gravenames_revisit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memorialuser',
            name='memorial',
        ),
        migrations.RemoveField(
            model_name='memorialuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='MemorialUser',
        ),
    ]
