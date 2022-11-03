# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0003_imagehistory_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedColumns',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4)),
                ('displayname', models.CharField(max_length=100, blank=True)),
                ('name', models.CharField(max_length=50)),
                ('columns', models.ManyToManyField(to='dataentry.Column')),
                ('table', models.ForeignKey(to='dataentry.Table', on_delete=models.CASCADE)),
            ],
        ),
    ]
