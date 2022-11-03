# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0009_auto_20180921_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='burial',
            name='graveplot',
            field=models.ForeignKey(to='bgsite.GravePlot', editable=False, null=True, related_name='burials', help_text='Multiple people buried in same plot eg. family members but only one graveplot per burial record', on_delete=models.CASCADE),
        ),
    ]
