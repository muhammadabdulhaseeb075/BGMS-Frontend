# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20181026_0942'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name_plural': 'Currencies'},
        ),
        migrations.AddField(
            model_name='currency',
            name='subunit1_symbol',
            field=models.CharField(null=True, max_length=1, blank=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AddField(
            model_name='currency',
            name='subunit2_symbol',
            field=models.CharField(null=True, max_length=1, blank=True, validators=[main.validators.bleach_validator]),
        ),
    ]
