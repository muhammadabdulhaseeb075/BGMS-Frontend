# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='burialgroundsite',
            name='client',
            field=models.ForeignKey(to='main.Client', help_text='Parent client that this site belongs to', related_name='sites', on_delete=models.CASCADE),
        ),
    ]
