# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0002_inspection'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemorialPersonDetail',
            fields=[
                ('id', models.UUIDField(db_index=True, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('name', models.TextField(null=True, max_length=50)),
                ('age', models.IntegerField(null=True, blank=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('memorial', models.ForeignKey(to='bgsite.Memorial', on_delete=models.CASCADE)),
            ],
        ),
    ]
