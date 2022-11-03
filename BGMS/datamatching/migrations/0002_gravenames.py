# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0001_initial'),
        ('datamatching', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraveNames',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('year_of_death', models.CharField(max_length=4, null=True)),
                ('memorial', models.ForeignKey(to='bgsite.Memorial', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
