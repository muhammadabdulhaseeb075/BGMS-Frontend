# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datamatching', '0002_gravenames'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gravenames',
            name='year_of_death',
            field=models.CharField(null=True, max_length=6),
            preserve_default=True,
        ),
    ]
