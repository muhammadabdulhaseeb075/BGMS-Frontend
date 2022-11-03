# Generated by Django 2.1 on 2019-07-22 13:16

from django.db import migrations, models

import main

class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0034_inspection_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnerStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='graveowner',
            name='owner_status',
            field=models.ManyToManyField(to='bgsite.OwnerStatus'),
        ),
        migrations.AddField(
            model_name='graveowner',
            name='remarks',
            field=models.CharField(blank=True, max_length=400, null=True, validators=[main.validators.bleach_validator]),
        ),
    ]
