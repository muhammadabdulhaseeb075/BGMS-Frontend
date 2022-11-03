# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0002_column_displayname'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagehistory',
            name='comments',
            field=models.CharField(blank=True, null=True, max_length=200),
        ),
    ]
