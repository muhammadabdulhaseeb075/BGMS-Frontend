# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0002_auto_20170123_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.FileField(blank=True, upload_to='', null=True, max_length=200),
        ),
    ]
