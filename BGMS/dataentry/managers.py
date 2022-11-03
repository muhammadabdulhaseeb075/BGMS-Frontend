'''
Created on 25 Feb 2016

@author: achickermane
'''
from django.db.models.query import QuerySet
from django.apps import apps
import itertools
from django.db import transaction
from bgsite.models import Image

class TemplateQuerySet(QuerySet):
    def create_template(self, name, description, book_name, user, columns=None, column_displaynames=None):
        template = self.create(name=name, description=description, book_name=book_name)
        template.add_columns(columns)
        template.update_column_displaynames(column_displaynames)
        template.add_history(user, state='created')
        return template
    
    def update_template(self, id, name, description, book_name, user, columns=None, column_displaynames=None):
        self.filter(id=id).update(name=name, description=description, book_name=book_name)
        template = self.get(id=id)
        template.columnposition_set.all().delete()
        template.add_columns(columns)
        template.update_column_displaynames(column_displaynames)
        template.add_history(user, state='updated')
        return template
    
    def all_template_values(self):
        templates = self.all()
        template_values = []
        for template in templates:
            values = template.get_values()
            values['burial_image'] = Image.objects.exclude(url__icontains='_t_').exclude(url__icontains='_u_').filter(url__icontains=values['book_name']).filter(image_type__image_type='burial_record').first().url.url
            template_values.append(values)
        return template_values
    

class TableQuerySet(QuerySet):
    def get_all_columns(self):
        columns = []
        for table in self.all():
            itertools.chain(columns, table.get_all_columns())
        
class ColumnQuerySet(QuerySet):
    def create_column(self, table, field_name):
        DjangoModel = table.get_model()
        name = DjangoModel._meta.get_field(field_name).verbose_name
        return self.create(table=table, fieldname=field_name, name=name)
    
    def get_all_columns(self, modelname, appname):
        apps.get_model(app_label='auth', model_name='User')


class BurialImageQuerySet(QuerySet):
    def all(self):
        # BUG: This function isn't run when using BurialImage.objects.all()
        return self.filter(image_type__image_type='burial_record')
        
    def all_unprocessed(self, book_name=None):
        if book_name:
            return self.all().filter(url__icontains=book_name).filter(image_state__image_state='unprocessed')
        else:
            return self.all().filter(image_state__image_state='unprocessed')
    
    def get_burial_books(self):
        self.exclude(url__icontains='_t_').exclude(url__icontains='_u_').filter(url__regex=r'[A-Za-z0-9]+_[0-9\-]+_[0-9]+\.jpg').filter(image_type__image_type='burial_record')
        
    def all_burial_image_history_values(self):
        """
        Returns burial image history for all images
        """
        history_values = []
        burial_images = self.all().distinct('id')
        for image in burial_images:
            image_value = {
               "id": image.id,
               "url": image.url.url
            }
            history = image.imagehistory_set.all().order_by('-time').first()
            if history:
                time = history.time
                comments = history.comments
            else:
                time = None
                comments = None
            history_values.append({
                "image": image_value,
                "time": time,
                "comments": comments,
                "status": image.image_state.image_state.replace('_', ' ').capitalize()
            })
        return history_values
    
    def get_user_activity(self):
        """
        Returns user activity for all images
        """
        activity_log = []
        burial_images = self.all().exclude(imagehistory=None).distinct('id')
        for image in burial_images:
            image_value = {
               "id": image.id,
               "url": image.url.url
            }
            
            history_set = image.imagehistory_set.all().order_by('-time')
            for history in history_set:
                activity_log.append({
                    "image": image_value,
                    "user": {
                        "id": history.user.id,
                        "name": history.user.username,
                        "first_name": history.user.first_name,
                        "last_name": history.user.last_name
                    },
                    "id": history.id,
                    "time": history.time,
                    "status": history.state.state.replace('_', ' ').capitalize(),
                    "comments": history.comments
                })
        return activity_log
    
    def summary(self):
        summary_values = {}
        summary_values["done"] = self.all().filter(image_state__image_state='processed').count()
        summary_values["remaining"] = self.all().filter(image_state__image_state='unprocessed').count()
        return summary_values