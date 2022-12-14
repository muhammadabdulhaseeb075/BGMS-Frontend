# Generated by Django 2.1 on 2020-01-10 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0042_auto_20200107_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graveref',
            name='section',
            field=models.ForeignKey(blank=True, help_text='Section containing the plot.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='bgsite.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='graveref',
            name='subsection',
            field=models.ForeignKey(blank=True, help_text='Subsection containing the plot.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='bgsite.Subsection', verbose_name='Subsection'),
        ),
    ]
