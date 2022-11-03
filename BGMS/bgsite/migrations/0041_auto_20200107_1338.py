# Generated by Django 2.1 on 2020-01-07 13:38

from django.db import migrations
from bgsite.migrations.custom_functions.migrate_graveref import migrate_graveref, reverse_migrate_graveref


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0040_auto_20200107_1338'),
    ]

    operations = [
        migrations.RunPython(
            code=migrate_graveref,
            reverse_code=reverse_migrate_graveref,
            atomic=True,
        ),
    ]
