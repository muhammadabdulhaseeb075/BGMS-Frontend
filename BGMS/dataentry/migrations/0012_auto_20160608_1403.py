# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0011_auto_20160523_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagehistory',
            name='image',
            field=models.ForeignKey(to='bgsite.BurialImage', on_delete=models.CASCADE),
        ),
    ]
