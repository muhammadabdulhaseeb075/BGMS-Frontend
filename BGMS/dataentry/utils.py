from django.db import connection

def add_subcolumns_to_column(apps, parent_column_name, column_dict):
    """
    Used by migrations.
    Creates/gets parent column from Column model and add subcolumns.
    """
    if connection.schema_name != 'public':
        Table = apps.get_model("dataentry", "Table")
        Column = apps.get_model("dataentry", "Column")

        table = Table.objects.all().filter(modelname=next(iter(column_dict)))[0]
        related_columns_dict = column_dict[table.modelname]
        print(related_columns_dict)
        for key in related_columns_dict:
            values = related_columns_dict[key]
            displayname = parent_column_name[key]
            related_column,created = Column.objects.get_or_create(fieldname=key, name=displayname, displayname=displayname, table=table, is_subcolumn=False)
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