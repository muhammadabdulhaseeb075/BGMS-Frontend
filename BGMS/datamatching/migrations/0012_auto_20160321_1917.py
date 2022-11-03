# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        ('bgsite', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datamatching', '0011_auto_20160321_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataMatchingMemorial',
            fields=[
                ('memorial', models.OneToOneField(primary_key=True, to='bgsite.Memorial', serialize=False, on_delete=models.CASCADE)),
                ('state', models.ForeignKey(to='main.ImageState', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='MemorialHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('memorial', models.ForeignKey(to='datamatching.DataMatchingMemorial', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='MemorialState',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('state', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='memorialhistory',
            name='state',
            field=models.ForeignKey(to='datamatching.MemorialState', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='memorialhistory',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='memorialhistory',
            unique_together=set([('user', 'memorial', 'state')]),
        ),
    ]
