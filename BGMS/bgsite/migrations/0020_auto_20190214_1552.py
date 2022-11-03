# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0019_auto_20190208_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='created_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='subsection',
            name='created_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
    ]
