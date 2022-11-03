# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20160623_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='BurialOfficialType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, serialize=False, db_index=True, primary_key=True)),
                ('official_type', models.CharField(validators=[main.validators.bleach_validator], max_length=50)),
            ],
        ),
    ]
