# Generated by Django 2.1 on 2021-05-04 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cemeteryadmin', '0022_auto_20210504_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='funeralevent',
            old_name='Cancelburial',
            new_name='cancelburial',
        ),
    ]