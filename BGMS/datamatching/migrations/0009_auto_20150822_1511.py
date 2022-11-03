# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datamatching', '0008_auto_20150821_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatamatchingUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemorialUserLink',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('skipped', models.BooleanField(default=False)),
                ('datamatching_memorial', models.ForeignKey(to='datamatching.DataMatchingMemorial', on_delete=models.CASCADE)),
                ('datamatching_user', models.ForeignKey(to='datamatching.DatamatchingUser', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='gravenames',
            name='memorial',
        ),
        migrations.DeleteModel(
            name='GraveNames',
        ),
        migrations.RemoveField(
            model_name='memorialuser',
            name='memorials',
        ),
        migrations.RemoveField(
            model_name='memorialuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='MemorialUser',
        ),
        migrations.AddField(
            model_name='datamatchinguser',
            name='memorials',
            field=models.ManyToManyField(through='datamatching.MemorialUserLink', to='datamatching.DataMatchingMemorial'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datamatchinguser',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='datamatchingmemorial',
            name='skipped',
        ),
    ]
