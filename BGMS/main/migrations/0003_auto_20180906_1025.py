# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_currency_relationshiptype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitedetails',
            name='matrixSet',
        ),
        migrations.RemoveField(
            model_name='sitedetails',
            name='url',
        ),
        migrations.AddField(
            model_name='sitedetails',
            name='plans',
            field=models.BooleanField(verbose_name='Plans?', default=False),
        ),
    ]
