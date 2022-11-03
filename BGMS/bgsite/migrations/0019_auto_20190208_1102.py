# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0018_auto_20190204_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='death',
            name='event',
            field=models.ForeignKey(blank=True, verbose_name='War/Event related to Death', help_text='Optional. Death have one related Event', null=True, to='bgsite.Event', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='death',
            name='parish',
            field=models.ForeignKey(blank=True, verbose_name='Parish', null=True, to='bgsite.Parish', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='death',
            name='religion',
            field=models.ForeignKey(blank=True, verbose_name='Religion', null=True, to='bgsite.Religion', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='person',
            name='profession',
            field=models.ForeignKey(blank=True, verbose_name='Profession', null=True, to='bgsite.Profession', on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
