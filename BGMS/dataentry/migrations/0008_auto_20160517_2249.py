# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

   
def update_history(apps, schema_editor):
    if connection.schema_name != 'public':
        UserState = apps.get_model("dataentry", "UserState")
        ImageHistory = apps.get_model("dataentry", "ImageHistory")
        TemplateHistory = apps.get_model("dataentry", "TemplateHistory")
        for history in ImageHistory.objects.all():
            history.user_state = UserState.objects.get(state=history.state)
            history.save()
        for history in TemplateHistory.objects.all():
            history.user_state = UserState.objects.get(state=history.state)
            history.save()

class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0007_auto_20160517_2241'),
    ]

    operations = [
        migrations.RunPython(
            code=update_history,
            reverse_code=None,
            atomic=True,
        ),
    ]
