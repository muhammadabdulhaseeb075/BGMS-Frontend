# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0013_auto_20181026_0942'),
        ('main', '0003_auto_20180906_1025'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='Parish',
        ),
        migrations.DeleteModel(
            name='Religion',
        ),
    ]
