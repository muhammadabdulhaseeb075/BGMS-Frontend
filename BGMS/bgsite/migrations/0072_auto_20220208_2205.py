# Generated by Django 2.2.9 on 2022-02-08 22:05

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0071_auto_20220208_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='graveref',
            name='bacas_grave_ref_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]