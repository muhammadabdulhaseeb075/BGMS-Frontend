# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
import uuid


def populate_field_types(apps, schema_editor):
    AttributeType = apps.get_model("geometriespublic", "FieldType")
    if connection.schema_name == 'public':
        AttributeType.objects.create(name='image', attributes=False)


class Migration(migrations.Migration):

    dependencies = [
        ('geometriespublic', '0004_auto_20190517_1427'),
    ]

    operations = [
        migrations.RunPython(
            code=populate_field_types,
        ),
    ]
