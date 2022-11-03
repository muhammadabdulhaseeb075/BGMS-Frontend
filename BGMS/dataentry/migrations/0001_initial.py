# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
from django.conf import settings
import uuid


def create_tables(apps, schema_editor):
    #creates Grid & Tree_trunk layers and Base and Aerial rasters
    Table = apps.get_model("dataentry", "Table")
    if connection.schema_name != 'public':
        if not Table.objects.all().exists():
            Table.objects.create(appname='bgsite', modelname='Person')
            Table.objects.create(appname='bgsite', modelname='Death')
            Table.objects.create(appname='bgsite', modelname='Burial')


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bgsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('fieldname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ColumnPosition',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False)),
                ('position', models.IntegerField()),
                ('column', models.ForeignKey(to='dataentry.Column', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='ImageHistory',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False)),
                ('state', models.CharField(max_length=10)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('image', models.ForeignKey(to='bgsite.Image', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False)),
                ('appname', models.CharField(max_length=50)),
                ('modelname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('book_name', models.CharField(max_length=50, blank=True)),
                ('columns', models.ManyToManyField(through='dataentry.ColumnPosition', to='dataentry.Column')),
            ],
        ),
        migrations.CreateModel(
            name='TemplateHistory',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False)),
                ('state', models.CharField(max_length=10)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('template', models.ForeignKey(to='dataentry.Template', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='columnposition',
            name='template',
            field=models.ForeignKey(to='dataentry.Template', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='column',
            name='table',
            field=models.ForeignKey(to='dataentry.Table', on_delete=models.CASCADE),
        ),
        migrations.RunPython(
            code=create_tables,
            reverse_code=None,
            atomic=True,
        ),
    ]
