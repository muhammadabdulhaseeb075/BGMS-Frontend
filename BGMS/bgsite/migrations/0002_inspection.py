# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, serialize=False)),
                ('condition', models.IntegerField(choices=[(1, 'Good'), (2, 'Reasonable'), (3, 'Poor')], default=1)),
                ('remarks', models.TextField(null=True, blank=True, max_length=200, validators=[main.validators.bleach_validator])),
                ('date', models.DateTimeField(auto_now=True)),
                ('action_required', models.BooleanField(default=False)),
                ('image', models.ForeignKey(to='bgsite.Image', null=True, blank=True, editable=False, on_delete=models.CASCADE)),
                ('memorial', models.ForeignKey(to='bgsite.Memorial', on_delete=models.CASCADE)),
            ],
        ),
    ]
