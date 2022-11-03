# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def update_column_remove_burial_officials(apps, schema_editor):
    if connection.schema_name != 'public':
        Column = apps.get_model("dataentry", "Column")
        Column.objects.filter(fieldname='burial_officials').delete()
                   
def add_related_columns(apps, schema_editor):
    column_dict = {
        "Person":{
            "name":[
                "title",
                "first_names",
                "birth_name",
                "other_names",
                "last_name"      
            ],
            "birth_date":[
                "impossible_date_day",
                "impossible_date_month",
                "impossible_date_year"
            ]
        },
        "Death":{
            "age":[
                "age_years",
                "age_months",
                "age_weeks",
                "age_days",
                "age_hours"
            ],
            "death_date":[
                "impossible_date_day",
                "impossible_date_month",
                "impossible_date_year"
            ]
        },
        "Burial":{
            "burial_date":[
                "impossible_date_day",
                "impossible_date_month",
                "impossible_date_year"
            ]
        }
    }
    column_name = {
        'name': 'Name',
        'birth_date': 'Birth Date',
        'age': 'Age',
        'death_date': 'Death Date',
        'burial_date': 'Burial Date'
    }
    if connection.schema_name != 'public':
        Table = apps.get_model("dataentry", "Table")
        Column = apps.get_model("dataentry", "Column")
        if not Column.objects.all().exists():
            for table in Table.objects.all():
                related_columns_dict = column_dict[table.modelname]
                print(related_columns_dict)
                for key in related_columns_dict:
                    values = related_columns_dict[key]
                    displayname = column_name[key]
                    related_column = Column.objects.create(fieldname=key, name=displayname, displayname=displayname, table=table, is_subcolumn=False)
                    for fieldname in values:
                        column = None
                        if not Column.objects.filter(table=table,fieldname=fieldname).exists():
                            DjangoModel = apps.get_model(app_label=table.appname, model_name=table.modelname)
                            column_displayname = DjangoModel._meta.get_field(fieldname).verbose_name
                            column = Column.objects.create(table=table, fieldname=fieldname, name=column_displayname, displayname=column_displayname, is_subcolumn=True)
                        else:
                            column = Column.objects.get(table=table,fieldname=fieldname)
                            column.is_subcolumn = True
                            column.save()
                        related_column.related_columns.add(column)
                        
def update_column_is_compulsary(apps, schema_editor):
    if connection.schema_name != 'public':
        Column = apps.get_model("dataentry", "Column")
        for column in Column.objects.all():
            if column.fieldname=='user_remarks' or column.fieldname=='requires_investigation':
                column.is_compulsary = True
                column.save()
                
def reverse_update_column_is_compulsary(apps, schema_editor):
    if connection.schema_name != 'public':
        Column = apps.get_model("dataentry", "Column")
        for column in Column.objects.all():
            if column.fieldname=='user_remarks' or column.fieldname=='requires_investigation':
                column.is_compulsary = False
                column.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0017_auto_20160629_1651'),
    ]

    operations = [
        migrations.RunPython(
            code=update_column_remove_burial_officials,
            reverse_code=None,
            atomic=True,
        ),
        migrations.RunPython(
            code=add_related_columns,
            reverse_code=None,
            atomic=True,
        ),
        migrations.RunPython(
            code=update_column_is_compulsary,
            reverse_code=reverse_update_column_is_compulsary,
            atomic=True,
        ),
    ]
