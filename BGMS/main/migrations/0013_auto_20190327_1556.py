# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='burialgroundsite',
            name='client',
            field=models.ForeignKey(help_text='Parent client that this site belongs to', to='main.Client', on_delete=models.CASCADE),
        ),
    ]
