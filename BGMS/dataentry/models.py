from django.db import models, transaction
from django.utils import timezone
from django.conf import settings
from bgsite.models import Image
from main.models import ImageState, BGUser, BurialOfficialType
import uuid
from django.db.models.fields.related import ManyToManyField
from dataentry.managers import TemplateQuerySet, TableQuerySet, ColumnQuerySet,\
    BurialImageQuerySet
from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned
from main.templatetags.bgms_field_filters import max_length
import itertools

# Create your models here.


class DataEntryUser(BGUser):
 
    class Meta:
        proxy = True
        app_label = 'main'

    def set_current_image(self, image=None, book_name=None):
        """Sets the given image as the current image for the user. If no image is given,
        it gets a random image and sets that as the current image."""
        with transaction.atomic():
            if image is None:
                image = BurialImage.objects.all_unprocessed(book_name=book_name).exclude(id__in=ImageHistory.objects.filter(state=UserState.objects.get(state='in_use')).values('image__id')).exclude(id__in=ImageHistory.objects.filter(user=self).filter(state=UserState.objects.get(state='skipped')).values('image__id')).order_by('url').first()
            if image:
                image.image_state = ImageState.objects.get(image_state='processing')
                image.save()
                ImageHistory.objects.update_or_create(image=image, user=self, defaults={'time':timezone.now(), 'state':UserState.objects.get(state='in_use')})
                return image
    
    def set_image_processed(self, image=None, comments=None):
        """Sets the given image as the current image for the user. If no image is given,
        it gets the current image and sets that as processed."""
        with transaction.atomic():
            if image is None:
                image = self.get_current_image()
            if image:
                image.image_state = ImageState.objects.get_or_create(image_state='processed')[0]
                image.save()
                ImageHistory.objects.update_or_create(image=image, user=self, defaults={'time':timezone.now(), 'state':UserState.objects.get(state='done'), 'comments':comments })
                return image
        
    def set_image_skipped(self, image=None, comments=None):
        """Sets the given image as the current image for the user. If no image is given,
        it gets the current image and sets that as processed."""
        with transaction.atomic():
            if image is None:
                image = self.get_current_image()
            if image:
                image.image_state = ImageState.objects.get_or_create(image_state='unprocessed')[0]
                image.save()
                ImageHistory.objects.update_or_create(image=image, user=self, defaults={'time':timezone.now(), 'state':UserState.objects.get(state='skipped'), 'comments':comments })
                return image
        
    def set_image_viewed(self, image=None, comments=None):
        """Sets the given image as the current image for the user. If no image is given,
        it gets the current image and sets that as unprocessed."""
        with transaction.atomic():
            if image is None:
                image = self.get_current_image()
            if image:
                #checking if the immediate preceeding state was done i.e. if we view after it is done, it stays as processed
                history = ImageHistory.objects.filter(image=image).exclude(state=UserState.objects.get(state='in_use')).exclude(state=UserState.objects.get(state='viewed')).order_by('-time')
                if history.exists() and (history[0].state == UserState.objects.get(state='done')):
                    image.image_state = ImageState.objects.get_or_create(image_state='processed')[0]
                else:
                    image.image_state = ImageState.objects.get_or_create(image_state='unprocessed')[0]
                image.save()
                ImageHistory.objects.update_or_create(image=image, user=self, defaults={'time':timezone.now(), 'state':UserState.objects.get(state='viewed'), 'comments':comments })
                return image
             
    def save_image_comments(self, image=None, comments=None):
        """Sets the given image as the current image for the user. If no image is given,
        it gets the current image and sets that as processed."""
        with transaction.atomic():
            if image is None:
                image = self.get_current_image()
            if image:
                ImageHistory.objects.update_or_create(image=image, user=self, defaults={'time':timezone.now(), 'state':UserState.objects.get(state='in_use'), 'comments':comments })
                return image
        
    def get_current_image(self):
        """Gets the current image the user is transcribing"""
        current_image = ImageHistory.objects.filter(user=self, state=UserState.objects.get(state='in_use'))
        if current_image.exists() and (current_image.count() == 1):
            return current_image.first().image
        elif current_image.count() > 1:
            raise MultipleObjectsReturned('Multiple Objects returned')
        else:
            return None
        
        
class BurialImage(Image):
    objects = BurialImageQuerySet.as_manager()
 
    class Meta:
        proxy = True
        app_label = 'bgsite'
        

class UserState(models.Model):
    state = models.CharField(max_length=10)
    
    
class Table(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    appname = models.CharField(max_length=50)
    modelname = models.CharField(max_length=50)
    
    def update_columns(self):
        #all columns except combined columns
        DjangoModel = self.get_model()
        columns_names = Column.objects.filter(table=self).exclude(related_columns__isnull=False).values('fieldname')
        columns_names = [column['fieldname'] for column in columns_names]
        fields = DjangoModel._meta.get_fields()
        #create new columns if they don't exist
        for field in fields:
            if hasattr(field, 'verbose_name') and field.editable and not (field.name in columns_names) and not field.many_to_many:
                #excluding many-to-many to remove burial official
                newColumn = Column.objects.create(table=self, fieldname=field.name, name=field.verbose_name)
            elif hasattr(field, 'verbose_name') and field.editable and field.many_to_many:
                #creating through relation in burial official as columns, calculated dynamically each time
                if field.m2m_db_table() == 'bgsite_burial_official':
                    types = list(BurialOfficialType.objects.all().exclude(official_type=''))
#                     types = [type.official_type for type in types]
                    # removing 
                    m2m_fields = Column.objects.filter(table=self).exclude(through_field__isnull=True)
                    for m2m_field in m2m_fields:
                        through_type = BurialOfficialType.objects.filter(id=m2m_field.through_field).first()
                        if through_type not in types: 
                            m2m_field.delete()
                        else:
                            types.remove(through_type)
                    for type in types:
                        newColumn = Column.objects.create(table=self, fieldname=field.name, name=type.official_type, displayname=type.official_type, through_field=type.id)
                
        #TODO: if a column has been removed, delete it
    
    def get_all_columns(self):
        self.update_columns()
        related_columns = Column.objects.filter(table=self).exclude(is_subcolumn=True).exclude(related_columns__isnull=False)
        columns = Column.objects.filter(table=self).exclude(is_subcolumn=True).exclude(related_columns__isnull=True)
        columns = itertools.chain(columns,related_columns)
        return columns
    
    def get_model(self):
        return apps.get_model(app_label=self.appname, model_name=self.modelname)


#TODO: Move to main?
class Column(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50)
    fieldname = models.CharField(max_length=50)
    displayname = models.CharField(max_length=100, blank=True)
    is_subcolumn = models.BooleanField(default=False)
    through_field = models.CharField(max_length=50, blank=True, null=True)
    is_compulsary = models.BooleanField(default=False)
    related_columns = models.ManyToManyField("self")
    #TODO: solve this when running migrations creating a new site: django.db.utils.OperationalError: cannot DROP TABLE "dataentry_column_related_columns" because it has pending trigger events
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    objects = ColumnQuerySet.as_manager()
    
    @property
    def type(self):
        if self.related_columns.exists():
            return 'CombinedColumn'
        if self.through_field:
            return 'ManyToManyKey'
        else:
            DjangoModel = self.table.get_model()
            field = DjangoModel._meta.get_field(self.fieldname)        
            if (field.__class__.__name__ is 'ForeignKey'):
                return 'ForeignKey'
#             elif (field.__class__.__name__ is 'ManyToManyField'):
#                 return 'ManyToManyKey'
            elif self.is_subcolumn:
                return 'SubColumn'
            else:
                return 'SimpleColumn'
    
    def get_field(self):
        DjangoModel = self.table.get_model()
        return DjangoModel._meta.get_field(self.fieldname)
    
    def get_or_create_displayname(self):
        if not self.displayname:
            self.displayname = self.get_field().verbose_name
            self.save()
        return self.displayname
    
    def column_values(self):
        subcolumns = None
        if self.related_columns.all().exists():
            subcolumns = []
            subcolumn_position = 0
            for subcolumn in self.related_columns.all():
                subcolumns.append({
                    'id': str(subcolumn.id),
                    'name': subcolumn.name,
                    'fieldname': subcolumn.fieldname,
                    'displayname': subcolumn.displayname,
                    'modelname': subcolumn.table.modelname.lower(),
                    'type': subcolumn.type,
                    'table': str(subcolumn.table.id),
                    'position': subcolumn_position                        
                })
                subcolumn_position+=1
        column_values = {
                'id': str(self.id),
                'name': self.name,
                'fieldname': self.fieldname,
                'displayname': self.get_or_create_displayname(),
                'modelname': self.table.modelname.lower(),
                'through': self.through_field,
                'type': self.type,
                'table': str(self.table.id),
                'is_compulsary': self.is_compulsary,
                'subcolumns': subcolumns
            }
        return column_values
    
    
class Template(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50, unique=True, error_messages={'unique': 'A template with this name already exists. Please ensure the template name is unique.'})
    description = models.CharField(max_length=200)
    book_name = models.CharField(max_length=50, blank=True)
    columns = models.ManyToManyField(Column, through='ColumnPosition')
    objects = TemplateQuerySet.as_manager()

    def get_values(self):
        values = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'book_name': self.book_name
        }
        columns=[]
        position = 0
        for columnposition in ColumnPosition.objects.filter(template=self).order_by('position'):
            column = columnposition.column
            column_values = column.column_values()
            column_values['position'] = position
            column_values['displayname'] = columnposition.displayname
            columns.append(column_values)
            position+=1
        # adding compulsary columns if they don't exist
        currentColumns = ColumnPosition.objects.filter(template=self).order_by('position')
        currentColumns = [column.column for column in currentColumns]
        for column in Column.objects.filter(is_compulsary=True):
            if column not in currentColumns:
                column_values = column.column_values()
                column_values['position'] = position
                columns.append(column_values)
                position+=1
        values['columns'] = columns
        return values
    
    def get_tables(self):
        return self.columns.all().distinct('table').values('table__modelname')
        
    def get_columns(self, model_name=None):
        columns=[]
        column_positions = ColumnPosition.objects.filter(template=self)
        if model_name:
            column_positions = ColumnPosition.objects.filter(template=self).filter(column__table__modelname=model_name)
        for columnposition in column_positions:
            columns.append(columnposition)
        return columns
        
    def add_history(self, user, state):
        template_history = TemplateHistory.objects.create(template=self, state=UserState.objects.get(state=state), user=user)
        
    def add_columns(self, columns):
        for index, column_id in enumerate(columns, start=0):
            column = Column.objects.get(id=column_id)
            ColumnPosition.objects.update_or_create(template=self, column=column, defaults={'position':index})
        
    def update_column_displaynames(self, column_displaynames):
        """
        Updates displayname for the particular column and template.
        column_displaynames structure: {'column_id':displayname}
        """
        if column_displaynames:
            for columnposition in ColumnPosition.objects.filter(template=self):
                if str(columnposition.column.id) in column_displaynames:
                    columnposition.displayname = column_displaynames[str(columnposition.column.id)]
                    columnposition.save()
        
class ColumnPosition(models.Model):    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    displayname = models.CharField(max_length=100, blank=True)
    position = models.IntegerField() 
    
    def get_displayname(self):
        """
        returns the customised display name for the template if
        it exists, otherwise returns the default display name.
        """
        if self.displayname:
            return self.displayname
        else:
            return self.column.get_or_create_displayname()
    
    
class AbstractHistoryModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    state = models.ForeignKey(UserState, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=timezone.now)

    class Meta:
        abstract = True
        

class ImageHistory(AbstractHistoryModel):
    image = models.ForeignKey(BurialImage, on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, blank=True, null=True)
    

class TemplateHistory(AbstractHistoryModel):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)