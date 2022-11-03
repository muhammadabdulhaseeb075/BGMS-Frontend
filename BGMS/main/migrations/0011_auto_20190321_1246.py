# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '00010_create_clients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='burialgroundsite',
            name='client',
            field=models.ForeignKey(to='main.Client', on_delete=models.CASCADE),
        ),
    ]
