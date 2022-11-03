# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
import uuid


def populate_field_types(apps, schema_editor):
    FieldType = apps.get_model("geometriespublic", "FieldType")
    if connection.schema_name == 'public':
    
        type = FieldType.objects.get(name='char')
        type.label = 'Text'
        type.type_name = 'char'
        type.save()
    
        type = FieldType.objects.get(name='integer')
        type.label = 'Number (whole)'
        type.type_name = 'integer'
        type.save()
    
        type = FieldType.objects.get(name='float')
        type.label = 'Number (decimal)'
        type.type_name = 'float'
        type.save()
    
        type = FieldType.objects.get(name='boolean')
        type.label = 'True or False'
        type.type_name = 'boolean'
        type.save()
    
        type = FieldType.objects.get(name='date')
        type.label = 'Date'
        type.type_name = 'date'
        type.save()
    
        type = FieldType.objects.get(name='textarea')
        type.label = 'Text area'
        type.type_name = 'textarea'
        type.save()
    
        type = FieldType.objects.get(name='image')
        type.label = 'Image'
        type.type_name = 'image'
        type.save()


class Migration(migrations.Migration):

    dependencies = [
        ('geometriespublic', '0007_auto_20190524_1718'),
    ]

    operations = [
        migrations.RunPython(
            code=populate_field_types,
        ),
        migrations.AlterField(
            model_name='fieldtype',
            name='label',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
