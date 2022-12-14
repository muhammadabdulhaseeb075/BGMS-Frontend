# Generated by Django 2.2.9 on 2022-02-08 19:11

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0070_meetinglocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='graveref',
            name='bacas_grave_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='graveref',
            name='bacas_section_name',
            field=models.CharField(max_length=20, null=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AddField(
            model_name='graveref',
            name='bacas_section_number',
            field=models.IntegerField(null=True),
        ),
    ]
