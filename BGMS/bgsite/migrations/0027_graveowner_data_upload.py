# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0026_auto_20190228_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='graveowner',
            name='data_upload',
            field=models.ForeignKey(help_text='The data upload from which this record was created.', blank=True, null=True, verbose_name='Data Upload', to='bgsite.DataUpload', on_delete=models.CASCADE),
        ),
    ]
