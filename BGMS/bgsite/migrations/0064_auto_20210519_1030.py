# Generated by Django 2.2.9 on 2021-05-19 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0063_auto_20210518_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='next_of_kin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_of_kin_to', to='main.PublicPerson', verbose_name='Next of kin'),
        ),
        migrations.AlterField(
            model_name='person',
            name='other_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='other_address', to='bgsite.Address', verbose_name='Other Address'),
        ),
        migrations.AlterField(
            model_name='person',
            name='residence_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='residence_address', to='bgsite.Address', verbose_name='Residence Address'),
        ),
    ]
