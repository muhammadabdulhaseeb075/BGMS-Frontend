# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('geometries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureAttributes',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, default=uuid.uuid4)),
                ('object_id', models.UUIDField()),
                ('char_value', models.CharField(null=True, max_length=255, blank=True)),
                ('integer_value', models.IntegerField(null=True, blank=True)),
                ('float_value', models.FloatField(null=True, blank=True)),
                ('boolean_value', models.NullBooleanField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterModelOptions(
            name='layer',
            options={'ordering': ['display_name']},
        ),
        migrations.AddField(
            model_name='topopoints',
            name='created_by',
            field=models.CharField(null=True, max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='topopoints',
            name='created_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='topopoints',
            name='last_edit_by',
            field=models.CharField(null=True, max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='topopoints',
            name='last_edit_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='topopoints',
            name='map_accura',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='topopoints',
            name='source_id',
            field=models.CharField(null=True, max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='topopolygons',
            name='created_by',
            field=models.CharField(null=True, max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='topopolygons',
            name='created_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='topopolygons',
            name='last_edit_by',
            field=models.CharField(null=True, max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='topopolygons',
            name='last_edit_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='topopolygons',
            name='map_accura',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='topopolygons',
            name='source_id',
            field=models.CharField(null=True, max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='topopolylines',
            name='created_by',
            field=models.CharField(null=True, max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='topopolylines',
            name='created_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='topopolylines',
            name='last_edit_by',
            field=models.CharField(null=True, max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='topopolylines',
            name='last_edit_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='topopolylines',
            name='map_accura',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='topopolylines',
            name='source_id',
            field=models.CharField(null=True, max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='topopoints',
            name='feature_attributes',
            field=models.ManyToManyField(to='geometries.FeatureAttributes', blank=True),
        ),
        migrations.AddField(
            model_name='topopolygons',
            name='feature_attributes',
            field=models.ManyToManyField(to='geometries.FeatureAttributes', blank=True),
        ),
        migrations.AddField(
            model_name='topopolylines',
            name='feature_attributes',
            field=models.ManyToManyField(to='geometries.FeatureAttributes', blank=True),
        ),
    ]
