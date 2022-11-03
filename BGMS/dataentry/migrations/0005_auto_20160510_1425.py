# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0004_relatedcolumns'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relatedcolumns',
            name='columns',
        ),
        migrations.RemoveField(
            model_name='relatedcolumns',
            name='table',
        ),
        migrations.DeleteModel(
            name='RelatedColumns',
        ),
    ]
