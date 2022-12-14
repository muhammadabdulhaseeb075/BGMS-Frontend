# Generated by Django 2.1 on 2021-03-31 19:22

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0055_auto_20210331_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='death',
            name='event',
        ),
        migrations.RemoveField(
            model_name='death',
            name='parish',
        ),
        migrations.RemoveField(
            model_name='death',
            name='religion',
        ),
        migrations.RemoveField(
            model_name='person',
            name='profession',
        ),
        migrations.RenameField(
            model_name='death',
            old_name='event_value',
            new_name='event',
        ),
        migrations.RenameField(
            model_name='death',
            old_name='parish_value',
            new_name='parish',
        ),
        migrations.RenameField(
            model_name='death',
            old_name='religion_value',
            new_name='religion',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='profession_value',
            new_name='profession',
        ),
    ]
