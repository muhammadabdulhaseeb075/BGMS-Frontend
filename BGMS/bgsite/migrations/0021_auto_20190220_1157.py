# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0020_auto_20190214_1552'),
        ('bgsite', '0020_auto_20190221_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='burial',
            name='consecrated',
            field=models.NullBooleanField(verbose_name='In consecrated ground'),
        ),
    ]
