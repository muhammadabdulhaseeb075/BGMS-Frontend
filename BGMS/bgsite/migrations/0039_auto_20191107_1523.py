# Generated by Django 2.1 on 2019-11-07 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0038_auto_20191004_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='burial',
            name='coffin_size',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Coffin or casket size'),
        ),
        migrations.AddField(
            model_name='person',
            name='next_of_kin_relationship',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Next of kin relationship'),
        ),
    ]
