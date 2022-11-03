from django.core.exceptions import FieldDoesNotExist 
from bgsite.models import Burial, ReservedPlot,\
    Inspection, Death, Person, GravePlot, Memorial, Address

class Register:
    models = {}

    def __init__(self):
        self.subscribe([
            Burial,
            Death,
            Person,
            Address,
            GravePlot,
            ReservedPlot,
            Memorial,
            Inspection
        ])

    def subscribe(self, _models):
        ## Saving each model the registry class, for optimization
        for model in _models:
            self.models[model.__name__] = model
        
    def get_models_with_fields(self):
        values = {}

        for model in self.models.values():
            total_items = model.objects.all().count()
            fields = model._meta.get_fields(include_hidden=False, include_parents=False)
            fields_format = []
            for field in fields:
                field_type = field.get_internal_type()
                field_name = field.name
                if field_name != 'id' and field_type != 'ForeignKey':
                    field_data = {
                        "field": field_name,
                        "type": field_type
                    }

                    ## When the field is related with other model
                    ## Add the model name
                    if field.is_relation:
                        field_data['related_model'] = field.related_model.__name__;
                    
                    fields_format.append(field_data)

                

            values[model.__name__] = {
                "fields": fields_format,
                "records": total_items
            }

        return values
    
    def get_entries_by_field(self, model_name, fields, sort, filters):
        model = self.models[model_name]
        records = None
        ## Testing if the model has an `id` field
        try:
            model._meta.get_field('id')
            fields.append('id')
        except FieldDoesNotExist:
            pass
        
        if filters is not None:
            records = model.objects.filter(**filters).values(*fields)
        else:
            records = model.objects.all().values(*fields)

        if sort is not '':
            records = records.order_by(sort)
        
        records = records.distinct()

        return records
    
    def get_field_suggestion_by_model(self, model_name, field):
        model = self.models[model_name]
        records = model.objects.distinct(field).values_list(field, flat=True)[:10]
        
        return records
