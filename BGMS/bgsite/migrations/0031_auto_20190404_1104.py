# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0030_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gravedeed',
            name='deed_number',
        ),
        migrations.AddField(
            model_name='gravedeed',
            name='deed_reference',
            field=models.CharField(null=True, unique=True, max_length=35),
        ),
        migrations.AddField(
            model_name='reservedplot',
            name='reservation_reference',
            field=models.CharField(null=True, unique=True, max_length=35),
        ),
        migrations.AlterField(
            model_name='person',
            name='next_of_kin',
            field=models.ForeignKey(blank=True, to='main.PublicPerson', related_name='next_of_kin_to', verbose_name='Next of kin', null=True, on_delete=models.CASCADE),
        ),
    ]
