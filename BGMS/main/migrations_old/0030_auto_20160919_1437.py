# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20160823_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='burialgroundsite',
            name='created_on',
            field=models.DateTimeField(help_text='Date the site is added', auto_now_add=True),
        ),
    ]
