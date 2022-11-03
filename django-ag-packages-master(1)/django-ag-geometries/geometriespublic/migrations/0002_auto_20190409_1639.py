# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
import uuid


def populate_attribute_types(apps, schema_editor):
    AttributeType = apps.get_model("geometriespublic", "AttributeType")
    if connection.schema_name == 'public':
        AttributeType.objects.create(name='char')
        AttributeType.objects.create(name='integer')
        AttributeType.objects.create(name='float')
        AttributeType.objects.create(name='boolean')
        AttributeType.objects.create(name='date')
        AttributeType.objects.create(name='textarea')


class Migration(migrations.Migration):

    dependencies = [
        ('geometriespublic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeType',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, max_length=20)),
            ],
        ),
        migrations.RunPython(
            code=populate_attribute_types,
        ),
        migrations.CreateModel(
            name='PublicAttribute',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, default=uuid.uuid4)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('feature_codes', models.ManyToManyField(related_name='public_attributes', to='geometriespublic.FeatureCode')),
                ('type', models.ForeignKey(to='geometriespublic.AttributeType', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterField(
            model_name='featuregroup',
            name='feature_codes',
            field=models.ManyToManyField(related_name='feature_groups', to='geometriespublic.FeatureCode'),
        ),
    ]
