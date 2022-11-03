# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datamatching', '0003_auto_20150511_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='gravenames',
            name='revisit',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
