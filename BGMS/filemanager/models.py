from django.db import models
from main.models import ImageType
from django.db import connection
from geometries.models import TopoPolygons
import uuid

def user_uploaded_file_path(file_instance, filename):
    file_type = file_instance.file_type.image_type
    return  os.path.join(connection.schema_name,'images',file_type,filename)

class File(models.Model):
    """
    Contains all details for the files. The url references a location in the S3 storage bucket server under files/ folder.
    It required the url, an file_type from main.ImageType.
    TODO: Change table FileImage to FileType and unify both in django-ag-media package
    """
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    url = models.FileField(upload_to=user_uploaded_file_path, max_length=200)
    """Url for the image"""
    file_type = models.ForeignKey(ImageType, on_delete=models.CASCADE)
    """:model:`main.ImageType` of the image"""
    name = models.FileField(null=True, blank=True, max_length=200)
    """Name file"""
    topopolygon = models.ForeignKey(TopoPolygons, null=True, on_delete=models.CASCADE)