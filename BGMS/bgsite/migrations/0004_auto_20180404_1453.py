# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0003_memorialpersondetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemorialInscriptionDetail',
            fields=[
                ('id', models.UUIDField(serialize=False, db_index=True, primary_key=True, default=uuid.uuid4)),
                ('name', models.TextField(max_length=50, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('memorial', models.ForeignKey(to='bgsite.Memorial', on_delete=models.CASCADE)),
            ],
        ),
        migrations.RemoveField(
            model_name='memorialpersondetail',
            name='memorial',
        ),
        migrations.DeleteModel(
            name='MemorialPersonDetail',
        ),
    ]
