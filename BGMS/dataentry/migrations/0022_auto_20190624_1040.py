# Generated by Django 2.1 on 2019-06-24 09:40

from django.db import migrations
from dataentry.utils import add_subcolumns_to_column


def add_related_columns(apps, schema_editor):
    column_dict = {
        "Death":{
            "age":[
                "age_minutes"
            ]
        }
    }
    parent_column_name = {
        'age': 'Age'
    }
    
    add_subcolumns_to_column(apps, parent_column_name, column_dict)

class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0021_auto_20181023'),
    ]

    operations = [
        migrations.RunPython(
                code=add_related_columns,
                reverse_code=None,
                atomic=True,
            ),
    ]