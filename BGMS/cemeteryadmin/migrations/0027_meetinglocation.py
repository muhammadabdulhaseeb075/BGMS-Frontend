# Generated by Django 2.2.9 on 2022-01-25 14:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cemeteryadmin', '0026_merge_20220127_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingLocation',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location_address', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
