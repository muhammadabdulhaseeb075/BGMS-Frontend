# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0001_initial'),
        ('datamatching', '0006_memorialuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataMatchingMemorial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('is_matched', models.BooleanField(default=False)),
                ('in_use', models.BooleanField(default=False)),
                ('revalidation_required', models.BooleanField(default=False)),
                ('skipped', models.BooleanField(default=False)),
                ('memorial', models.OneToOneField(to='bgsite.Memorial', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='memorialuser',
            name='memorial',
        ),
        migrations.AddField(
            model_name='memorialuser',
            name='memorials',
            field=models.ManyToManyField(to='datamatching.DataMatchingMemorial'),
            preserve_default=True,
        ),
    ]
