# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20160718_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservePlotState',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('state', models.CharField(max_length=20, unique=True)),
            ],
        ),
    ]
