# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0005_auto_20160510_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='related_columns',
            field=models.ManyToManyField(related_name='_column_related_columns_+', to='dataentry.Column'),
        ),
        migrations.AddField(
            model_name='column',
            name='is_subcolumn',
            field=models.BooleanField(default=False),
        ),
    ]
