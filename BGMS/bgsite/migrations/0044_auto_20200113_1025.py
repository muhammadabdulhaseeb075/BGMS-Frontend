# Generated by Django 2.1 on 2020-01-13 10:25

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0043_auto_20200110_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='burial',
            name='coffin_size',
        ),
        migrations.AddField(
            model_name='burial',
            name='coffin_height',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='burial',
            name='coffin_units',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[main.validators.bleach_validator], verbose_name='Coffin Units(ft/m/cm)'),
        ),
        migrations.AddField(
            model_name='burial',
            name='coffin_width',
            field=models.FloatField(blank=True, null=True),
        ),
    ]