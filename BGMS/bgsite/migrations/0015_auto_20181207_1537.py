# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0014_auto_20181026_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='death',
            name='memorials',
            field=models.ManyToManyField(editable=False, help_text='Many-to-Many relationship', to='bgsite.Memorial', related_name='memorial_deaths'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(max_length=35, null=True, blank=True, validators=[main.validators.bleach_validator], verbose_name='Description of event'),
        ),
        migrations.AlterField(
            model_name='memorialinscriptiondetail',
            name='memorial',
            field=models.ForeignKey(to='bgsite.Memorial', related_name='memorial_inscriptions', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='subsection',
            name='subsection_name',
            field=models.TextField(max_length=20, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterUniqueTogether(
            name='subsection',
            unique_together=set([('subsection_name', 'section')]),
        ),
    ]
