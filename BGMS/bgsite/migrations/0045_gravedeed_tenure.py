# Generated by Django 2.2.9 on 2020-02-14 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0044_auto_20200113_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='gravedeed',
            name='tenure',
            field=models.CharField(blank=True, choices=[('PERPETUAL', 'Perpetual'), ('FIXED', 'Fixed')], max_length=10, null=True),
        ),
    ]
