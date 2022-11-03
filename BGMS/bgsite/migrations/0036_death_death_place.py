# Generated by Django 2.1 on 2019-09-16 09:09

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0035_auto_20190722_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='death',
            name='death_place',
            field=models.CharField(blank=True, max_length=50, null=True, validators=[main.validators.bleach_validator], verbose_name='Place of death'),
        ),
    ]