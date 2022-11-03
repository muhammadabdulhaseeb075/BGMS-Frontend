# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0014_auto_20181026_0944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='graveplot',
            old_name='size_units',
            new_name='depth_units',
        ),
        migrations.AlterField(
            model_name='burial',
            name='death',
            field=models.ForeignKey(related_name='death_burials', help_text='Same Death person can be buried multiple times', to='bgsite.Death', editable=False, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='death',
            name='memorials',
            field=models.ManyToManyField(to='bgsite.Memorial', related_name='deaths', help_text='Many-to-Many relationship', editable=False),
        ),
        migrations.AlterField(
            model_name='death',
            name='person',
            field=models.OneToOneField(help_text='One-to-One relationship', serialize=False, primary_key=True, related_name='death', to='bgsite.Person', editable=False, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(null=True, max_length=35, verbose_name='Description of event', blank=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='graveplot',
            name='description',
            field=models.CharField(null=True, max_length=300, blank=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='memorial',
            name='description',
            field=models.CharField(null=True, max_length=300, blank=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='memorial',
            name='graveplot_memorials',
            field=models.ManyToManyField(through='bgsite.MemorialGraveplot', related_name='memorials', to='bgsite.GravePlot'),
        ),
        migrations.AlterField(
            model_name='memorial',
            name='inscription',
            field=models.CharField(null=True, max_length=400, blank=True, validators=[main.validators.bleach_validator]),
        ),
    ]
