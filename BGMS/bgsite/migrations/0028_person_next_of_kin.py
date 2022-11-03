# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20190409_1159'),
        ('bgsite', '0027_graveowner_data_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='next_of_kin',
            field=models.ForeignKey(verbose_name='Next of kin', related_name='next_of_kin', to='main.PublicPerson', null=True, blank=True, on_delete=models.CASCADE),
        ),
    ]
