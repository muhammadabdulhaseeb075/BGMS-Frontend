# Generated by Django 2.1 on 2021-05-08 23:55

from django.db import migrations, models
import django.db.models.deletion
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0059_auto_20210430_2203'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='Parish',
        ),
        migrations.DeleteModel(
            name='Profession',
        ),
        migrations.DeleteModel(
            name='Religion',
        ),
    ]
