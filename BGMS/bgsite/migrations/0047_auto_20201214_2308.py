# Generated by Django 2.1 on 2020-12-15 04:08

from django.db import migrations, models
import django.db.models.deletion
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0046_authorityforinterment'),
    ]

    operations = [
        migrations.AddField(
            model_name='official',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bgsite.Address'),
        ),
        migrations.AddField(
            model_name='official',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[main.validators.email_validator], verbose_name='email'),
        ),
        migrations.AddField(
            model_name='official',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[main.validators.bleach_validator], verbose_name='First phone number'),
        ),
        migrations.AddField(
            model_name='official',
            name='second_phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[main.validators.bleach_validator], verbose_name='Second phone number'),
        ),
    ]
