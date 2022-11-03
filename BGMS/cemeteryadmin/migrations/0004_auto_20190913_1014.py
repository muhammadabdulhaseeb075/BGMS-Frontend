# Generated by Django 2.1 on 2019-09-13 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cemeteryadmin', '0003_auto_20190910_0943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funeralevent',
            name='id',
        ),
        migrations.AlterField(
            model_name='funeralevent',
            name='calendar_event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='funeral_event', serialize=False, to='cemeteryadmin.CalendarEvents'),
        ),
    ]
