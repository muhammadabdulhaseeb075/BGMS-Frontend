# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, connection

def populate_reserve_plot_states(apps, schema_editor):
    ReservePlotState = apps.get_model("main", "ReservePlotState")

    if connection.schema_name == 'public':
        ReservePlotState.objects.create(state='reserved')
        ReservePlotState.objects.create(state='deleted')
        ReservePlotState.objects.create(state='buried')


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_reserveplotstate'),
    ]

    operations = [
        migrations.RunPython(
            code=populate_reserve_plot_states,
            reverse_code=None,
        )
    ]
