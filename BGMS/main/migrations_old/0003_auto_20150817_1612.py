# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150826_1450'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='bguser',
            managers=[
                ('objects', main.models.BGUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='bguser',
            name='email',
            field=models.EmailField(verbose_name='email address', help_text='Required.', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='bguser',
            name='groups',
            field=models.ManyToManyField(related_name='user_set', verbose_name='groups', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='bguser',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
        migrations.AlterField(
            model_name='imagetype',
            name='image_type',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
