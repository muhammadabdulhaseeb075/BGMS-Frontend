# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0019_auto_20160704_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='name',
            field=models.CharField(error_messages={'unique': 'A template with this name already exists. Please ensure the template name is unique.'}, max_length=50, unique=True),
        ),
    ]
