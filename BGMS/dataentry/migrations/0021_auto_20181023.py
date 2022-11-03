# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dataentry.utils import add_subcolumns_to_column

from django.db import migrations
                   
def add_related_columns(apps, schema_editor):
    column_dict = {
        "Burial":{
            "cremation_date":[
                "impossible_cremation_date_day",
                "impossible_cremation_date_month",
                "impossible_cremation_date_year"
            ]
        }
    }
    parent_column_name = {
        'cremation_date': 'Cremation Date'
    }
    
    add_subcolumns_to_column(apps, parent_column_name, column_dict)


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0020_auto_20160719_1435'),
    ]

    operations = [
        migrations.RunPython(
            code=add_related_columns,
            reverse_code=None,
            atomic=True,
        ),
    ]
