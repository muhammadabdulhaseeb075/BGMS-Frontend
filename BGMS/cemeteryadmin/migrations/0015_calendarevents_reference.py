# Generated by Django 2.1 on 2021-01-14 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cemeteryadmin', '0014_fill_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarevents',
            name='reference',
            field=models.IntegerField(default=1, unique=True),
        ),
    ]
