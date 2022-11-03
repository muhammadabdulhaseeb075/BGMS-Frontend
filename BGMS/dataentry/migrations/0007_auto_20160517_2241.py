# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def add_state(apps, schema_editor):
    if connection.schema_name != 'public':
        UserState = apps.get_model("dataentry", "UserState")
        UserState.objects.create(state="in_use")
        UserState.objects.create(state="skipped")
        UserState.objects.create(state="done")
        UserState.objects.create(state="viewed")
        UserState.objects.create(state="created")
        UserState.objects.create(state="updated")

class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0006_auto_20160510_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserState',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='imagehistory',
            name='user_state',
            field=models.ForeignKey(to='dataentry.UserState', default=1, on_delete=models.CASCADE),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='templatehistory',
            name='user_state',
            field=models.ForeignKey(to='dataentry.UserState', default=1, on_delete=models.CASCADE),
            preserve_default=False,
        ),
        migrations.RunPython(
            code=add_state,
            reverse_code=None,
            atomic=True,
        ),             
    ]
