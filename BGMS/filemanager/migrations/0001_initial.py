# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filemanager.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, db_index=True, default=uuid.uuid4)),
                ('url', models.FileField(max_length=200, upload_to=filemanager.models.user_uploaded_file_path)),
                ('file_type', models.ForeignKey(to='main.ImageType', on_delete=models.CASCADE)),
            ],
        ),
    ]
