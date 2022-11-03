from django.contrib.gis.db import models
from main.models import ImageType, ImageState, \
    BGUser, BurialOfficialType, ReservePlotState, Currency, RelationshipType, PublicPerson
from main.models_abstract import SoftDeletionModel, SoftDeletionManager
from geometriespublic.models import FeatureCode
from geometries.models import TopoPolygons, Layer
from bgsite.managers import PersonManager, MemorialQuerySet, \
    TenantSiteManager, GraveplotQuerySet, BurialOfficialQuerySet, \
    TagQuerySet, merge_values, ReservedPlotQuerySet, ProfessionManager, EventManager, ParishManager, ReligionManager, \
    GraveRefManager
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import connection
from django.conf import settings
import uuid
import PIL
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.storage import DefaultStorage
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import calendar
import datetime
from datetime import date
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.gdal.geometries import MultiPoint
from main.validators import bleach_validator, email_validator
from django.db.models import Count
from django.db.models.query import QuerySet
from BGMS.utils import get_and_clean_temp_dir, verify_contents, date_elements_to_full_date, \
    get_display_name_from_firstnames_lastname
import re
import shutil
import json
import base64
import io
from main.validators import validate_file_extension
from django.contrib.gis.db.models.functions import Centroid

REGISTER_IMAGE_GRAVENUMBER_PATTERN = ".*\d{4,7}_(\w+)_(\d+)(_\w+)?"
REGISTER_IMAGE_PAGENUMBER_PATTERN = ".*\d{4,7}_(\d{4}-\d{4})_(\d+)(_t)?"

DEFUALT_THUMBNAIL_URL = "https://bgms36.s3.amazonaws.com/images/icons/no_image.jpg"


# models

def user_uploaded_image_path(image_instance, filename):
    image_type = image_instance.image_type.image_type
    return os.path.join(connection.schema_name, 'images', 'user_uploads', image_type, filename)


def user_uploaded_thumbnail_path(thumbnail_instance, filename):
    thumbnail_type = thumbnail_instance.image.image_type.image_type
    return os.path.join(connection.schema_name, 'thumbnails', 'user_uploads', thumbnail_type, filename)


def user_uploaded_deed_path(file_instance, filename):
    return os.path.join(connection.schema_name, 'files', 'deeds', filename)


def death_uploaded_person_pdf_path(file_instance, filename):
    return os.path.join(connection.schema_name, 'files', 'death', filename)


def to_int(num):
    try:
        num = int(num)
    except Exception:
        num = 0
    return num


def create_date(year=None, month=1, day=1):
    year = to_int(year)
    month = to_int(month)
    day = to_int(day)
    if not ((datetime.MINYEAR <= year) and (year <= datetime.MAXYEAR)):
        # invalid year means no date
        return None
    if not ((month >= 1) and (month <= 12)):
        # invalid month, make it jan
        month = 1
    if not ((day >= 1) and (day <= calendar.monthrange(year, month)[1])):
        # invalid day, make it 1st
        day = 1
    return date(year, month, day)


# models for the tenant-specific admin app

class UserRequest(models.Model):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    comments = models.CharField(max_length=200, validators=[bleach_validator])


class TenantUser(BGUser):
    objects = TenantSiteManager()

    class Meta:
        proxy = True
        app_label = 'main'
        verbose_name = "Site User"
        verbose_name_plural = "Site Users"


class Address(models.Model):
    """
    Represents an address, the only field rquired is first_line.
    """
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    first_line = models.CharField(max_length=200, validators=[bleach_validator], blank=True)
    """First line"""
    second_line = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True)
    """Second line"""
    town = models.CharField(max_length=50, validators=[bleach_validator], null=True, blank=True)  # get from webservice
    """Town/Village"""
    county = models.CharField(max_length=50, validators=[bleach_validator], null=True,
                              blank=True)  # get from webservice
    """County"""
    postcode = models.CharField(max_length=10, validators=[bleach_validator], null=True, blank=True)
    """Postcode"""
    country = models.CharField(max_length=50, validators=[bleach_validator], null=True,
                               blank=True)  # get from webservice
    """County"""


class Image(models.Model):
    """
    Contains all details for the images. The url references a location in the S3 storage bucket server under images/ folder.
    It required the url, an image_type from main.ImageType and an image_state from main.ImageState.
    """
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    url = models.ImageField(upload_to=user_uploaded_image_path, max_length=200)
    """Url for the image"""
    metadata = models.CharField(max_length=100, validators=[bleach_validator], null=True)
    """Any metadata related to the image"""
    image_type = models.ForeignKey(ImageType, on_delete=models.CASCADE)
    """:model:`main.ImageType` of the image"""
    image_state = models.ForeignKey(ImageState, on_delete=models.CASCADE)
    """:model:`main.ImageState` of the image"""

    def has_thumbnail(self):
        """
        Returns true if image has a thumbnail, else returns false
        """
        # if hasattr(self, 'thumbnail_id'):
        try:
            if self.thumbnail is not None:
                return True
        except Exception:
            return False

    def get_thumbnail(self):
        """
        Returns thumbnail object if it exist, else raise and Object does not exist execption.
        """
        if self.has_thumbnail() is False:
            return DEFUALT_THUMBNAIL_URL
            # raise ObjectDoesNotExist('The image has no thumbnail')
        return self.thumbnail

    def get_thumbnail_url(self):
        """
        Returns thumbnail url if it exist, else raise and Object does not exist execption.
        """
        if self.has_thumbnail() is False:
            return DEFUALT_THUMBNAIL_URL
            # raise ObjectDoesNotExist('The image has no thumbnail')
        return self.thumbnail.url.url

    def get_image_url(self):
        if self.url is not None:
            return self.url.url
        else:
            return ''

    def create_thumbnail(self, image_file):
        # If there is no image associated with this.
        # do not create thumbnail
        if not image_file:
            return

        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (60, 60)

        DJANGO_TYPE = image_file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        # import pdb; pdb.set_trace()
        # Open original photo which we want to thumbnail using PIL's Image
        fullsize_image = PILImage.open(image_file.file)
        new_image = fullsize_image.copy()
        width, height = new_image.size
        if height >= width:
            amount_to_crop_on_top = int((height - width) / 2)
            new_image = new_image.crop((0, amount_to_crop_on_top, width, width + amount_to_crop_on_top))
        else:
            amount_to_crop_on_top = int((width - height) / 2)
            new_image = new_image.crop((amount_to_crop_on_top, 0, height + amount_to_crop_on_top, height))

        # new_image.show()
        # import pdb; pdb.set_trace()

        new_image.thumbnail(THUMBNAIL_SIZE, PILImage.ANTIALIAS)

        # Save the thumbnail
        temp_handle = BytesIO()
        new_image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)
        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(image_file.name)[-1],
                                 temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        thumb_temp = Thumbnail(image=self)
        thumb_temp.url.save('{}_thumbnail.{}'.format(os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)
        thumb_temp.save()

    # Add to a form containing a FileField and change the field names accordingly.
    from django.template.defaultfilters import filesizeformat
    from django.utils.translation import ugettext_lazy as _

    @staticmethod
    def base64_to_image(image):
        image = base64.b64decode(image)  # Decode the image

        image_output = io.BytesIO()
        image_output.write(image)  # Write decoded image to buffer
        image_output.seek(0)  # seek beginning of the image string

        filename = uuid.uuid4().hex + '.jpg'  # Generate a random file name

        suf = SimpleUploadedFile(filename, image_output.read(), content_type='image/jpeg')
        verify_contents(suf)

        return suf

    @classmethod
    def compressImage(cls, filei, subdir):
        """
        Compress image to approximately 1MB starting in 70% reduction for the resolution,
        Then loop with increments of 10% until the image is above 1MB
        Creates a subdirectory /burial_records_photos/[uuid] to store temp photos and clean uuid folder afterwards
        filei: TemporaryUploadedFile (django)
        """

        # Create folder structure /burial_records_photos/[uuid]
        temp_dir = getattr(settings, 'TEMP_FILES_UPLOAD_PATH')
        session_uuid = str(uuid.uuid4())
        temp_dirs = temp_dir + subdir + '/' + session_uuid
        os.makedirs(temp_dirs)

        pct_comp = 1  # Percentage of compression during steps
        compression_size = 1048576  # 1MB
        DJANGO_TYPE = filei.content_type
        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'

        # temp_path = get_and_clean_temp_dir()
        temp_path = temp_dirs

        # save original file in tmp directory
        path = temp_path + '/' + filei.name
        print(path)
        with open(path, 'wb') as f:
            filecontent = f.write(filei.read())

        # get original width and length
        original_img = PILImage.open(filei)
        original_width, original_length = original_img.size
        img = original_img  # images under 1mb

        # compress image
        increment = 0
        while os.path.getsize(path) >= compression_size:
            new_width = int(original_width * (pct_comp - increment))
            new_length = int(original_length * (pct_comp - increment))
            img = original_img.resize((new_width, new_length), PIL.Image.LANCZOS)
            img.save(path)
            increment = increment + 0.05

        # Save the compressed img
        temp_handle = BytesIO()
        img.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(filei.name)[-1],
                                 temp_handle.read(), content_type=DJANGO_TYPE)

        # delete folder structure and empty files
        shutil.rmtree(temp_dirs)

        return suf


class Thumbnail(models.Model):
    """
    Contains the url of the thumbnail associated to an bgsite.Image in a One-to-One relationship.
    The url references a location in the S3 storage bucket server under thumbnails/ folder. The url is required.
    """
    image = models.OneToOneField(Image, primary_key=True, on_delete=models.CASCADE)
    """One-to-One relationship to the :model:`bgsite.Image`"""
    url = models.ImageField(upload_to=user_uploaded_thumbnail_path)
    """Url in the S3 storage bucket server"""


# model using a geometric field
class Marker(models.Model):
    """
    Represent the abstract information of a point with a relation Many-to-Many bgsite.Image
    """
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=300, validators=[bleach_validator], null=True, blank=True)
    """Description"""
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    """unique id, This Id is attached to the olFeature"""
    topopolygon = models.OneToOneField(TopoPolygons, null=True, editable=False, on_delete=models.CASCADE)
    """One-to-One relationship with a geometries.TopoPolygons - represents a memorial/plot geometry"""
    feature_id = models.CharField(max_length=10, null=True)
    """attribute of topopolygon
       Used for linking purposes between memorial and plot when importing shapefile
       Memorial.feature_id = Memorials.ID from the shapefile
       Graveplot.feature_id = 0

       Also used in Export map
    """

    class Meta:
        abstract = True

    @property
    def head_point(self):
        """Geo Point under EPSG:27700 projection to identify the location of the headstone."""
        if self.topopolygon:
            return self.topopolygon.get_centre()
        else:
            return None

    @property
    def marker_type(self):
        if self.topopolygon:
            return self.topopolygon.layer.feature_code.feature_type

    def get_uuid(self):
        #         if hasattr(self, 'memorialgraveplot'):
        #             return self.memorialgraveplot.uuid
        #         else:
        return self.uuid

    def get_reserved_persons_per_plot(self):
        """
        get reserved persons currently reserved in this plot
        """
        return ReservedPlot.objects.filter(grave_plot=self)


class DataUpload(models.Model):
    """
    Record of all data uploads including their status
    """
    file_name = models.TextField(max_length=200, validators=[bleach_validator], null=False)
    date = models.DateTimeField(auto_now_add=True)
    record_count = models.IntegerField(null=True, blank=True)
    status = models.TextField(max_length=20, validators=[bleach_validator], null=False)
    report = models.TextField(validators=[bleach_validator], null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class FeaturesRelationship(models.Model):
    """
    Creates relationship between two features. Can be memorials or graveplots, hence GenericForeignKey
    """
    feature_1_content_type = models.ForeignKey(ContentType, related_name='feature_1_relationship',
                                               on_delete=models.CASCADE)
    feature_1_object_id = models.UUIDField()
    feature_1_content_object = GenericForeignKey('feature_1_content_type', 'feature_1_object_id')
    feature_2_content_type = models.ForeignKey(ContentType, related_name='feature_2_relationship',
                                               on_delete=models.CASCADE)
    feature_2_object_id = models.UUIDField()
    feature_2_content_object = GenericForeignKey('feature_2_content_type', 'feature_2_object_id')
    relationship = models.ForeignKey(RelationshipType, null=True, on_delete=models.SET_NULL)
    data_upload = models.ForeignKey(DataUpload, null=True, blank=True, verbose_name='Data Upload',
                                    help_text="The data upload from which this record was created.",
                                    on_delete=models.CASCADE)


class SectionQuerySet(QuerySet):
    def get_centrepoint_json__values(self):
        section_queryset = self.filter().annotate(centrepoint=Centroid('topopolygon__geometry')).values('centrepoint')
        for value in section_queryset:
            if value['centrepoint']:
                value['centrepoint'] = value['centrepoint'].coords
            else:
                value['centrepoint'] = None
        return section_queryset


class Section(models.Model):
    """
    List of sections
    """
    section_name = models.TextField(max_length=20, validators=[bleach_validator], unique=True)
    topopolygon = models.OneToOneField(TopoPolygons, null=True, blank=True, editable=False, related_name="section",
                                       on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    objects = SectionQuerySet.as_manager()


class Subsection(models.Model):
    """
    List of subsections
    """
    subsection_name = models.TextField(max_length=20, validators=[bleach_validator])
    section = models.ForeignKey(Section, null=True, on_delete=models.CASCADE)
    topopolygon = models.OneToOneField(TopoPolygons, null=True, editable=False, related_name="subsection",
                                       on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('subsection_name', 'section')


class GraveplotStatus(models.Model):
    """
    List of graveplot statuses
    """
    status = models.TextField(max_length=20, validators=[bleach_validator], unique=True)
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class GraveplotState(models.Model):
    """
    List of graveplot states
    """
    state = models.TextField(max_length=20, validators=[bleach_validator], unique=True)
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class GraveplotType(models.Model):
    """
    List of graveplot types
    """
    type = models.TextField(max_length=20, validators=[bleach_validator], unique=True)
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class GraveRef(models.Model):
    """
    The reference for a grave consisting of:
    - Grave number (required) (not neccessarily a number!!)
    - Section (optional)
    - Subsection (only if section)

    Combination must be unique
    """

    grave_number = models.CharField(max_length=20, validators=[bleach_validator], null=True)
    section = models.ForeignKey(Section, null=True, blank=True, verbose_name='Section',
                                help_text="Section containing the plot.", on_delete=models.SET_NULL)
    subsection = models.ForeignKey(Subsection, null=True, blank=True, verbose_name='Subsection',
                                   help_text="Subsection containing the plot.", on_delete=models.SET_NULL)
    bacas_grave_number = models.IntegerField(null=True)
    bacas_grave_ref_number = models.CharField(max_length=20, null=True)
    bacas_section_number = models.IntegerField(null=True)
    bacas_section_name = models.CharField(max_length=20, validators=[bleach_validator], null=True)
    objects = GraveRefManager()

    class Meta:
        unique_together = ('grave_number', 'section', 'subsection')

    def validate_unique(self, exclude=None):
        # Combination of grave number, section and subsection must be unique
        # In sql null != null, so django's unique_together is inadequate.
        if (self.grave_number != None and self.grave_number != '' and
                ((self.section is None and GraveRef.objects.exclude(id=self.id).filter(
                    grave_number__iexact=self.grave_number, section__isnull=True).exists())
                 or (self.subsection is None and
                     GraveRef.objects.exclude(id=self.id).filter(
                         grave_number__iexact=self.grave_number, section=self.section,
                         subsection__isnull=True).exists())
                 or GraveRef.objects.exclude(id=self.id).filter(
                            grave_number__iexact=self.grave_number, section=self.section,
                            subsection=self.subsection).exists()
                )):
            raise ValidationError("Duplicate Grave Reference")
        super(GraveRef, self).validate_unique(exclude)

    def save(self, *args, **kwargs):
        """ Validate uniqueness before saving """

        self.validate_unique()

        super().save(*args, **kwargs)


# model using a geometric field
class GravePlot(Marker):
    """
    Represent the plot where the person was buried using a polygon in a relation One-to-One between geometries.TopoPolygons
    and plot_polygon field. Also another geometries.TopoPolygons representing the headstone of the Grave.
    """

    graveref = models.OneToOneField(GraveRef, null=True, blank=True, verbose_name="Grave Reference",
                                    on_delete=models.SET_NULL, related_name='graveref_graveplot')

    status = models.ForeignKey(GraveplotStatus, null=True, blank=True, verbose_name='Graveplot Status',
                               help_text="E.g. private, common, invalid.", on_delete=models.SET_NULL)
    """Status of grave"""
    state = models.ForeignKey(GraveplotState, null=True, blank=True, verbose_name='Graveplot State',
                              help_text="E.g. occupied, empty, full.", on_delete=models.SET_NULL)
    """State of grave"""
    type = models.ForeignKey(GraveplotType, null=True, blank=True, verbose_name='Graveplot Type',
                             help_text="E.g. earthen grave, brick grave.", on_delete=models.SET_NULL)
    """Type of grave"""
    size = models.CharField(max_length=15, validators=[bleach_validator], null=True, blank=True)
    """ Size of grave
        Note: this can be anything related to size, i.e. small, 2'6" x 6'6", 0.8x2
    """
    size_units = models.CharField(max_length=15, validators=[bleach_validator], null=True, blank=True)
    """Size Units(ft/m/cm)"""
    depth = models.FloatField(null=True, blank=True)
    """Depth of grave"""
    depth_units = models.CharField(max_length=15, validators=[bleach_validator], null=True, blank=True)
    """Depth Units(ft/m/cm)"""
    perpetual = models.NullBooleanField(null=True, blank=True)
    """Perpetual"""
    consecrated = models.NullBooleanField(verbose_name='Consecrated ground')
    """True or False, default = False"""
    memorial_comment = models.CharField(max_length=400, validators=[bleach_validator], null=True, blank=True)
    """Remarks on the grave"""
    remarks = models.CharField(max_length=400, validators=[bleach_validator], null=True, blank=True)
    """Remarks on the grave"""
    memorial_feature_id = models.CharField(max_length=10, null=True)
    '''Only used for linking purposes between memorial and plot when importing shapefile
       memorial_feature_id = Memorials.ID from the shapefile
    '''
    #     headstone_polygon = models.OneToOneField(TopoPolygons, related_name='headstonepolygons', null=True)
    #     """geometries.TopoPolygons in One-to-One relationship represents the headstone of the Grave"""
    objects = GraveplotQuerySet.as_manager()
    data_upload = models.ForeignKey(DataUpload, null=True, blank=True, verbose_name='Data Upload',
                                    help_text="The data upload from which this record was created.",
                                    on_delete=models.CASCADE)

    def modify_grave_number(self, grave_number):
        """
        Add or change a graveplot's grave_number
        """

        if self.graveref:
            # if graveref already exists

            if grave_number == self.graveref.grave_number:
                return

            if not self.graveref.graveref_burials.exists():
                # if graveref isn't being used by burials
                existing_grave_ref = GraveRef.objects.filter(grave_number=grave_number, section=self.graveref.section,
                                                             subsection=self.graveref.subsection)

                if existing_grave_ref.exists():
                    # if a grave ref already exists, use this and delete original
                    self.graveref.delete()
                    self.graveref = existing_grave_ref[0]
                else:
                    # modify the existing record
                    self.graveref.grave_number = grave_number
                    self.graveref.save()
                    return
            else:
                # If graveref is being used by burials then create new grave ref.
                self.graveref = GraveRef.objects.get_or_create_custom(grave_number, self.graveref.section,
                                                                      self.graveref.subsection)
        else:
            # create new grave ref (if noe previous graveref then it's not in section)
            self.graveref = GraveRef.objects.get_or_create_custom(grave_number, None, None)

        self.save()

    def delete_reserved_plot(self):
        """
        Change status to deleted for reserved plots and remove relation GravePLot to ReservedPlot
        """
        rps = self.reservedplot_set.all()
        for rp in rps:
            rp.delete()

    def update_plot_layer(self):
        """
        Check if graveplot layer needs changed
        i.e. burials, deeds or reservations changed
        Returns plot's layer
        """

        if self.topopolygon:

            original_layer = self.topopolygon.layer.feature_code.feature_type

            # ignore pet graves for now
            if original_layer == 'pet_grave':
                return 'pet_grave'

            layer = None

            if Burial.objects.filter(graveplot=self).exists():
                layer = 'plot'
            elif GraveDeed.objects.filter(graveplot=self).exists() or ReservedPlot.objects.filter(grave_plot=self,
                                                                                                  state=ReservePlotState.objects.get(
                                                                                                          state='reserved')).exists():
                layer = 'reserved_plot'
            else:
                layer = 'available_plot'

            # if layer does need changed
            if layer != original_layer:
                # change the layer
                self.topopolygon.update_feature_code(layer)

            return layer
        return None

    def update_layer_cache(self, created):
        """
        Use after updating graveplot to update cache. Called from signal.
        """
        feature_type = self.topopolygon.layer.feature_code.feature_type

        if not created:
            """ If this is a plot, there is a chance the layer type has changed 
                (I don't know how to find this out for sure).
                If the old layer or new layer is an available plot, this needs removed from the cache.
                Other layer changes get automatically taken care of in update_feature_in_layer_geojson_cache.
                Available plots are different because, sadly, they use topopolygon_id rather than a graveplot_id
            """
            if feature_type == 'available_plot':
                layer_obj = Layer.objects.get(feature_code__feature_type='plot')
                layer_obj.update_feature_in_layer_geojson_cache(self.uuid, None, False, deleted=True)

            elif feature_type == 'reserved_plot' or feature_type == 'plot':
                layer_obj = Layer.objects.get(feature_code__feature_type='available_plot')
                layer_obj.update_feature_in_layer_geojson_cache(self.topopolygon_id, None, True, deleted=True)

        if feature_type == 'available_plot':
            self.topopolygon.update_layer_cache(created=created)
        else:
            layer_obj = Layer.objects.get(feature_code__feature_type=feature_type)
            geoj = self.get_geojson()
            layer_obj.update_feature_in_layer_geojson_cache(self.uuid, geoj, False, created=created)

    def delete_layer_cache(self):
        if self.topopolygon and self.topopolygon.layer:
            feature_type = self.topopolygon.layer.feature_code.feature_type
            if feature_type == 'available_plot':
                layer_obj = Layer.objects.get(feature_code__feature_type='plot')
                layer_obj.update_feature_in_layer_geojson_cache(self.uuid, None, False, deleted=True)

            elif feature_type == 'reserved_plot' or feature_type == 'plot':
                layer_obj = Layer.objects.get(feature_code__feature_type='available_plot')
                layer_obj.update_feature_in_layer_geojson_cache(self.topopolygon_id, None, True, deleted=True)

    def get_geojson(self):
        """
        Returns graveplot geojson
        """
        feature_type = self.topopolygon.layer.feature_code.feature_type
        serializer = GraveplotGeoSerializer(self, context={'marker_type': feature_type})
        return serializer.data


class GraveDeedQuerySet(QuerySet):

    def upload_photos(self, photos_files):
        """
        Upload register scan photos, will upload image per image as long as none
        of the following errors occur, the image with error wont be uploaded, but the others will:
            - Not a valid image contents
            - Match input mask for the filename
        """
        temp_dir = get_and_clean_temp_dir(connection.schema_name)
        result = {'error': []}

        image_type = ImageType.objects.get(image_type='ownership_register')
        image_state = ImageState.objects.get(image_state='unprocessed')

        # sample accepted pattern: 3244_A_00168.jpg
        pattern = re.compile(REGISTER_IMAGE_GRAVENUMBER_PATTERN + '.(jpg|jpeg)$', re.IGNORECASE)

        for pos, photo_file in enumerate(photos_files):
            if pattern.match(photo_file.name):
                # if True: # Remove restriction

                # if image already exists with matching filename
                if Image.objects.filter(url__endswith=photo_file.name, image_type=image_type,
                                        image_state=image_state).exists():
                    result['error'].append("Filename '" + photo_file.name + "' already exists.")
                    continue

                result_val = verify_contents(photo_file)
                if result_val == '':  # image is valid?
                    compressed_image = Image.compressImage(photo_file, 'burial_records_photos')
                    # upload photos to bucket, create record in database, url=photo_file to upload original
                    image = Image(url=compressed_image, image_type=image_type, image_state=image_state)
                    image.save()
                    image.create_thumbnail(photo_file)
                else:
                    result['error'].append(result_val)
            else:
                result['error'].append(
                    'Please make sure the filename "' + photo_file.name + '" meets the correct input format.')

        shutil.rmtree(temp_dir)
        return result


class GraveDeed(models.Model):
    PERPETUAL = 'PERPETUAL'
    FIXED = 'FIXED'
    TENURE_CHOICES = [
        (PERPETUAL, 'Perpetual'),
        (FIXED, 'Fixed'),
    ]

    graveplot = models.ForeignKey(GravePlot, related_name='graveplot_deeds', on_delete=models.CASCADE)
    """Graveplot that this is a deed for"""
    deed_url = models.FileField(upload_to=user_uploaded_deed_path, max_length=200)
    """Deed document"""
    images = models.ManyToManyField(Image)
    """Many-to-Many relationship with :model:`bgsite.Image`"""
    ownership_register = models.CharField(null=True, unique=True, max_length=200)
    """Ownership register"""
    deed_reference = models.CharField(null=True, unique=True, max_length=35)
    """Deed reference"""
    cost_currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.CASCADE)
    """Currency of the grave cost"""
    cost_unit = models.IntegerField(null=True, blank=True)
    """Cost of the grave - units e.g. pounds"""
    cost_subunit = models.IntegerField(null=True, blank=True)
    """Cost of the grave - subunits e.g. shillings"""
    cost_subunit2 = models.FloatField(null=True, blank=True)
    """Cost of the grave - 2nd subunits e.g. pence"""
    purchase_date = models.DateField(null=True, blank=True)
    """Date of purchase. Incorrect if impossible_date is True. Populated in save override."""
    impossible_purchase_date = models.BooleanField(default=False, editable=False)
    """True if purchase date is an impossible date, default = False"""
    purchase_date_day = models.IntegerField(null=True, blank=True, verbose_name='Day of Purchase')
    """Day of Purchase"""
    purchase_date_month = models.IntegerField(null=True, blank=True, verbose_name='Month of Purchase')
    """Month of Purchase"""
    purchase_date_year = models.IntegerField(null=True, blank=True, verbose_name='Year of Purchase')
    """Year of Purchase"""
    tenure = models.CharField(max_length=10, null=True, blank=True, choices=TENURE_CHOICES)
    """Tenure: can be perpetual or fixed number of years"""
    tenure_years = models.IntegerField(null=True, blank=True, verbose_name='Tenure in years')
    """Tenure in years (use if tenure = FIXED)"""
    remarks = models.CharField(max_length=400, validators=[bleach_validator], null=True, blank=True)
    """Remarks on the deed"""
    data_upload = models.ForeignKey(DataUpload, null=True, blank=True, verbose_name='Data Upload',
                                    help_text="The data upload from which this record was created.",
                                    on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    objects = GraveDeedQuerySet.as_manager()

    def save(self, **kwargs):
        full_date, impossible_date = date_elements_to_full_date(self.purchase_date_day, self.purchase_date_month,
                                                                self.purchase_date_year)
        self.purchase_date = full_date
        self.impossible_purchase_date = impossible_date

        super(GraveDeed, self).save()

    def add_image(self, url):
        """
        Add an image related to the burial record assigning the same image_type and create the thumbnail associated to the image
        """
        image = Image(url=url, image_type=ImageType.objects.get(image_type='ownership_register'),
                      image_state=ImageState.objects.get(image_state='unprocessed'))
        image.save()
        image.create_thumbnail(url)
        self.images.add(image)


class OwnerStatus(models.Model):
    """
    Options for the graveowner status
    """
    status = models.CharField(max_length=25)


class GraveOwner(models.Model):
    """
    Links Graveplot to it's owner. A grave can have multiple owners (not at the same time) and an owner can own multiple graves.
    """
    deed = models.ForeignKey(GraveDeed, related_name='grave_owners', on_delete=models.CASCADE)
    """Grave deed"""
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.UUIDField(null=True)
    owner = GenericForeignKey('content_type', 'object_id')
    """Owner - can link to Person or Company models in main"""
    ownership_order = models.IntegerField(default=1)
    """1st owner, 2nd owner, etc. Only used for migrating data (e.g. Highgate).
        Run script to convert this to BGMS system."""
    owner_status = models.ManyToManyField(OwnerStatus)
    active_owner = models.BooleanField(default=True)
    """True if currently owns this grave"""
    owner_from_date = models.DateField(null=True, blank=True)
    """Date became an owner. Incorrect if impossible_date is True. Populated in save override."""
    impossible_owner_from_date = models.BooleanField(default=False, editable=False)
    """True if owner from date is an impossible date, default = False"""
    owner_from_date_day = models.IntegerField(null=True, blank=True, verbose_name='Day Ownership Began')
    """Day ownership began"""
    owner_from_date_month = models.IntegerField(null=True, blank=True, verbose_name='Month Ownership Began')
    """Month ownership began"""
    owner_from_date_year = models.IntegerField(null=True, blank=True, verbose_name='Year Ownership Began')
    """Year ownership began"""
    owner_to_date = models.DateField(null=True, blank=True)
    """Date ending being an owner. Incorrect if impossible_date is True. Populated in save override."""
    impossible_owner_to_date = models.BooleanField(default=False, editable=False)
    """True if owner to date is an impossible date, default = False"""
    owner_to_date_day = models.IntegerField(null=True, blank=True, verbose_name='Day Ownership Ended')
    """Day ownership ended"""
    owner_to_date_month = models.IntegerField(null=True, blank=True, verbose_name='Month Ownership Ended')
    """Month ownership ended"""
    owner_to_date_year = models.IntegerField(null=True, blank=True, verbose_name='Year Ownership Ended')
    """Year ownership ended"""
    remarks = models.CharField(max_length=400, validators=[bleach_validator], null=True, blank=True)
    data_upload = models.ForeignKey(DataUpload, null=True, blank=True, verbose_name='Data Upload',
                                    help_text="The data upload from which this record was created.",
                                    on_delete=models.CASCADE)

    def save(self, **kwargs):
        full_date, impossible_date = date_elements_to_full_date(self.owner_from_date_day, self.owner_from_date_month,
                                                                self.owner_from_date_year)
        self.owner_from_date = full_date
        self.impossible_owner_from_date = impossible_date

        full_date_to, impossible_date_to = date_elements_to_full_date(self.owner_to_date_day, self.owner_to_date_month,
                                                                      self.owner_to_date_year)
        self.owner_to_date = full_date_to
        self.impossible_owner_to_date = impossible_date_to

        super(GraveOwner, self).save()


# model using a geometric field
class Memorial(Marker):
    """
    Represents the Memorial information and extends from the bgsite.Marker, it has also a One-to-One relationship
    with geometries.TopoPolygons to relate the headstone point. There is a head_point of type PointField that represent
    the center of the Memorial in the headstone.
    """
    """Many-to-Many relationship with :model:`bgsite.GravePlot` due to a memorial may contains several graveplots."""
    graveplot_memorials = models.ManyToManyField(GravePlot, through='MemorialGraveplot', related_name='memorials')
    user_generated = models.BooleanField(default=False)
    """True or False, default = false"""
    # datamatching fields
    inscription = models.CharField(max_length=400, validators=[bleach_validator], null=True, blank=True)
    """Inscription on the memorial"""
    images = models.ManyToManyField(Image)
    """Many-to-Many relationship with :model:`bgsite.Image`"""
    # overriding the Manager with a CachingQuerySet to implement caching
    objects = MemorialQuerySet.as_manager()
    data_upload = models.ForeignKey(DataUpload, null=True, blank=True, verbose_name='Data Upload',
                                    help_text="The data upload from which this record was created.",
                                    on_delete=models.CASCADE)

    @property
    def marker_name(self):
        if self.topopolygon:
            return self.topopolygon.layer.feature_code.display_name

    @property
    def marker_type(self):
        if self.topopolygon:
            return self.topopolygon.layer.feature_code.feature_type

    @classmethod
    def get_next_feature_id(cls):
        """
        Returns next feature id available to be assigned
        """
        mem = Memorial.objects.filter(
            feature_id__iregex='^\d+$'
        ).extra(
            {'feature_id_int': "CAST(feature_id AS INT)"}
        ).order_by(
            '-feature_id_int'
        ).first()

        if mem is not None:
            return int(mem.feature_id) + 1
        else:
            return 1

    def save(self, *args, **kwargs):
        """
        Assign next feature_id on save if the memorial doesnt have one
        """
        if self.feature_id is None:
            next_feature_id = Memorial.get_next_feature_id()
            self.feature_id = next_feature_id

            if self.topopolygon:
                self.topopolygon.feature_id = next_feature_id
                self.topopolygon.save()
        super(Memorial, self).save(*args, **kwargs)

    def create_image(self, url):
        """
        Add an image related to the memorial assigning the same image_type and create the thumbnail associated to the image
        """
        # compress image to less than 1mb
        # compressed_image = Image.compressImage(url, 'memorial_photos')
        # image = Image(url=compressed_image, image_type=ImageType.objects.get(image_type='memorial'), image_state=ImageState.objects.get(image_state='unprocessed'))
        image = Image(url=url, image_type=ImageType.objects.get(image_type='memorial'),
                      image_state=ImageState.objects.get(image_state='unprocessed'))
        image.save()
        image.create_thumbnail(url)
        self.images.add(image)
        return image

    def link_graveplot(self, graveplot_id):
        """
        Makes a link between Memorial.graveplot and the Memorial using the graveplot_id
        """
        if graveplot_id:
            graveplot = GravePlot.objects.get(plot_polygon_id=graveplot_id)
            if graveplot not in self.graveplots.all():
                self.graveplots.add(graveplot)
            self.save()

    def link_headstone(self, headstone_id, graveplot_id=None):
        if headstone_id:
            self.headstone = TopoPolygons.objects.get(id=headstone_id)
            # graveplot = None
            # if self.graveplots.exists():
            # graveplot = self.graveplots.all().first()
            #             elif graveplot_id :
            #                 graveplot = GravePlot.objects.get(plot_polygon_id=graveplot_id)
            #             if graveplot:
            #                 graveplot.headstone_polygon = self.headstone
            #                 graveplot.save()
            self.save()

    def get_all_details(self):
        """
        Returns a dictionary (key: field name, value: field value) that contains all the fields related to a Memorial except Memorial.revisit field.
        """
        return {'memorial_id': self.id, 'marker_type': self.marker_name, 'images': self.list_image_urls(),
                'head_point': self.head_point, 'description': self.description, 'inscription': self.inscription,
                'user_generated': self.user_generated, 'feature_id': self.feature_id}

    def list_image_urls(self):
        """
        Returns a vector with the :model:`main.Image` urls related to the Memorial.
        """
        # TODO: test with memorials with no images
        image_list = []
        storage_object = DefaultStorage()
        for image in self.images.all().distinct('url'):
            if storage_object.exists(image.url.name):
                image_dict = {}
                image_dict['image_url'] = image.url.url
                image_dict['id'] = image.id
                if image.has_thumbnail():
                    image_dict['thumbnail_url'] = image.thumbnail.url.url
                else:
                    image_dict['thumbnail_url'] = image_dict['image_url']
                image_list.append(image_dict)
        return image_list

    # class Meta:
    #     unique_together=(('head_point',))

    def list_thumbnails_urls(self):
        """
        Returns a vector with the :model:`bgsite.Thumbnail` urls related to the Memorial.
        """
        return [image.thumbnail.url.url for image in self.images.all().distinct('url')]

    def delete_image(self, uuid_image):
        """
        Delete Image object and thumnail from memorial
        """
        # import pdb; pdb.set_trace()
        img = Image.objects.get(id=uuid_image)
        # thumb = Thumbnail.objects.get(id=uuid_image)
        self.images.remove(img)
        Thumbnail.objects.filter(image=uuid_image).delete()
        Image.objects.filter(id=uuid_image).delete()

    def update_layer_cache(self, created):
        """
        Use after updating memorial to update cache. Called from signal.
        """
        geoj = self.get_geojson()

        feature_type = self.topopolygon.layer.feature_code.feature_type
        layer_obj = Layer.objects.get(feature_code__feature_type=feature_type)
        layer_obj.update_feature_in_layer_geojson_cache(self.uuid, geoj, False, created=created)

    def get_geojson(self):
        """
        Returns memorial geojson
        """
        query_set = Memorial.objects.filter(id=self.id).prefetch_related('topopolygon').annotate(
            images_count=Count('images', distinct=True)).annotate(
            linked_graves_count=Count('graveplot_memorials', distinct=True))
        feature_type = self.topopolygon.layer.feature_code.feature_type
        serializer = MemorialGeoSerializer(query_set[0], context={'marker_type': feature_type})
        return serializer.data


class MemorialGraveplot(models.Model):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    memorial = models.ForeignKey(Memorial, on_delete=models.CASCADE)
    graveplot = models.ForeignKey(GravePlot, on_delete=models.CASCADE)


class Person(SoftDeletionModel):
    """
    Person objects abstract all details of a person. A Person is related to bgsite.Death in a one to one relationship.

    Add person and death details transparently, create memorial, burial and graveplot objects and add them to person via the appropriate method

    Note: this is similar, but different, to the PublicPerson table in main.
    The difference is that the persons in bgsite are occupants or reserved occupants of that site.
    """
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30, validators=[bleach_validator], null=True, blank=True, verbose_name='Title')
    """Title"""
    first_names = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True,
                                   verbose_name='First names')
    """First and Second names in the same field"""
    birth_name = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True,
                                  verbose_name='Birth name')
    """Birth name"""
    other_names = models.CharField(max_length=100, validators=[bleach_validator], null=True, blank=True,
                                   verbose_name='Nicknames')
    last_name = models.CharField(max_length=35, validators=[bleach_validator], null=True, blank=True,
                                 verbose_name='Last name')
    """Last name"""
    birth_date = models.DateField(null=True, editable=False)
    """Birth date, format = dd/mm/yyyy. Incorrect if impossible_date is True. Populated in save override."""
    impossible_date = models.BooleanField(default=False, editable=False,
                                          help_text="If true means the others impossible_date fields have the non real date entered in the registry for the person")
    """If true means the others impossible_date fields have the non real date entered in the registry for the person"""
    impossible_date_day = models.IntegerField(null=True, blank=True, verbose_name="Day of Birth")
    """Day of Birth: 'impossible' is legacy and has no meaning"""
    impossible_date_month = models.IntegerField(null=True, blank=True, verbose_name="Month of Birth")
    """Month of Birth: 'impossible' is legacy and has no meaning"""
    impossible_date_year = models.IntegerField(null=True, blank=True, verbose_name="Year of Birth")
    """Year of Birth: 'impossible' is legacy and has no meaning"""
    age = models.IntegerField(null=True, blank=True, verbose_name="Person age")
    """Age"""
    age_type = models.CharField(max_length=50, validators=[bleach_validator], null=True, blank=True,
                                verbose_name='Age Type')
    """ Age measure unit (years, weeks, minutes, months)"""
    gender = models.CharField(max_length=10, validators=[bleach_validator], null=True, blank=True,
                              verbose_name='Gender')
    """Gender"""
    description = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True,
                                   verbose_name='Description of Person')
    """Description, max length = 200 characteres"""
    profession = models.CharField(max_length=100, null=True, blank=True, verbose_name='Profession')
    "NEVER CREATE A DROP CASCADE RELATION OVER MODELS THAT WILL BE MUTATING CONSTANTLY"
    """:model:`main.Profession` associated, """
    residence_address = models.ForeignKey(Address, related_name='residence_address', null=True, blank=True,
                                          verbose_name='Residence Address', on_delete=models.SET_NULL)
    """:model:`main.Address` other address"""
    other_address = models.ForeignKey(Address, related_name='other_address', null=True, blank=True,
                                      verbose_name='Other Address', on_delete=models.SET_NULL)
    '''Place of death: is the same that residence address'''
    place_of_death = models.BooleanField(default=False)
    next_of_kin = models.ForeignKey(PublicPerson, null=True, blank=True, verbose_name='Next of kin',
                                    related_name='next_of_kin_to', on_delete=models.SET_NULL)
    next_of_kin_relationship = models.CharField(max_length=50, null=True, blank=True,
                                                verbose_name='Next of kin relationship')
    objects = PersonManager()
    data_upload = models.ForeignKey(DataUpload, null=True, blank=True, verbose_name='Data Upload',
                                    help_text="The data upload from which this record was created.",
                                    on_delete=models.CASCADE)
    '''Place of file pdf file upload'''
    file = models.FileField(upload_to=death_uploaded_person_pdf_path, validators=[validate_file_extension], null=True,
                            blank=True)

    def clean(self):
        super(Person, self).clean()
        if self.first_names is None and self.last_name is None:
            raise ValidationError('Person must have a first name and/or last name')

    def save(self, **kwargs):
        if self.last_name:
            self.last_name = self.last_name.upper()

        full_date, impossible_date = date_elements_to_full_date(self.impossible_date_day, self.impossible_date_month,
                                                                self.impossible_date_year)
        self.birth_date = full_date
        self.impossible_date = impossible_date

        if not self.next_of_kin:
            # If next of kin is empty, ensure relationship is also empty.
            self.next_if_kin_relationship = None

        super(Person, self).save()

    # internal functions
    def __str__(self):
        return 'first_names={0}, other_names={1}, last_name={2}, birth_date={3}, gender={4}, description={5}, is_dead={6}'.format(
            self.first_names, self.other_names, self.last_name, self.birth_date, self.gender, self.description,
            self.is_dead())

    # getter functions
    def get_display_name(self):

        return get_display_name_from_firstnames_lastname(self.first_names, self.last_name)

    def get_burial_date(self):
        burial_date = None
        if self.death is not None:
            burials = self.death.get_burials()
            if burials:
                burial_date = burials[0].burial_date
        return burial_date

    get_burial_date.short_description = 'Burial date'

    # TODO: reestructure query, time consuming
    def is_dead(self):
        """Returns True if person is dead, False otherwise"""
        # make this ugly code better. currently using get_death becaause using hasattr(self, 'death') queries the database
        if hasattr(self, 'death'):
            return True
        return False

    def get_death(self):
        """Try to return the object :model:`bgsite.Death` from cache, if it does not exist retrive the object from database"""
        death = None
        try:
            death = Death.objects.get(person_id=self.id)
            # death = Death.objects.get(person_id=self.id)
        except ObjectDoesNotExist:
            death = None
        return death

    def get_burials(self):
        """Returns all BurialRecord objects associated with the person"""
        if self.is_dead():
            return self.get_death().get_burials()
        else:
            return Burial.objects.none()

    # TODO: reestructure query, time consuming
    def get_memorials(self):
        """Returns all Memorial Objects associated with the person"""
        if self.is_dead():
            return self.get_death().get_memorials()
        else:
            return Memorial.objects.none()

    def get_graveplots(self):
        """Returns all GravePlot objects associated with the person"""
        return self.get_death().get_graveplots()

    def get_profession(self):
        """Returns Profession associated, if it does not have returns None."""
        if self.profession is None:
            return None
        return self.profession.profession

    def get_residence_details(self):
        """
        Returns a dictionary with the residence_address :model:`main.Address` details
        (key: field name, value: field value) associated to the person if exist, otherwise returns
        same dictionary but empty::

        - residence_address: residence_address.first_line
        - second_line: residence_address.second_line
        - town: residence_address.town
        - county: residence_address.county
        - country: residence_address.country
        - postcode: residence_address.county
        """
        if self.residence_address is None:
            return {'residence_address': None, 'second_line': None, 'town': None, 'county': None, 'country': None,
                    'postcode': None}
        else:
            return {'residence_address': self.residence_address.first_line,
                    'second_line': self.residence_address.second_line, 'town': self.residence_address.town,
                    'county': self.residence_address.county, 'country': self.residence_address.country,
                    'postcode': self.residence_address.postcode}

    def get_all_details(self):
        """
        Returns all the fields of the person and associated death.
        It also returns lists of all the burial and memorial objects associated with the person.
        """
        # return {key:value for (key, value) in kwargs.iter() if(hasattr(self,key))}
        person_details = {'title': self.title, 'nickname': self.other_names, 'first_names': self.first_names,
                          'last_name': self.last_name, 'birth_date': self.birth_date, 'gender': self.gender,
                          'description': self.description, 'profession': self.get_profession(), 'id_person': self.id,
                          'impossible_date_day_person': self.impossible_date_day,
                          'impossible_date_month_person': self.impossible_date_month,
                          'impossible_date_year_person': self.impossible_date_year}
        residence_details = self.get_residence_details()
        person_details.update(residence_details)
        if self.is_dead():
            death_details = self.death.get_all_details()
            person_details.update(death_details)
        return person_details

    def get_age_years(self):
        """Returns age_years if person is dead, None otherwise"""
        if self.death:
            return self.death.age_years
        return None

    get_age_years.short_description = 'Age (years)'

    # setter functions

    def add_person_details(self, *args, **kwargs):
        """
        Save their details base on the parameter list kwargs, the parameter names have to match Person's field names.
        """
        if args:
            kwargs = args[0]
        if 'first_names' in kwargs:
            self.first_names = kwargs['first_names']
        if 'birth_name' in kwargs:
            self.birth_name = kwargs['birth_name']
        if 'other_names' in kwargs:
            self.other_names = kwargs['other_names']
        if 'last_name' in kwargs:
            self.last_name = kwargs['last_name']
        if 'title' in kwargs:
            self.title = kwargs['title']
        if 'nickname' in kwargs:
            self.other_names = kwargs['nickname']
        if 'gender' in kwargs:
            self.gender = kwargs['gender']
        if 'description' in kwargs:
            self.description = kwargs['description']
        if 'impossible_date_day' in kwargs and kwargs['impossible_date_day'] and kwargs['impossible_date_day'] != 0:
            self.impossible_date_day = kwargs['impossible_date_day']
        if 'impossible_date_month' in kwargs and kwargs['impossible_date_month'] and kwargs[
            'impossible_date_month'] != 0:
            self.impossible_date_month = kwargs['impossible_date_month']
        if 'impossible_date_year' in kwargs and kwargs['impossible_date_year'] and kwargs['impossible_date_year'] != 0:
            self.impossible_date_year = kwargs['impossible_date_year']
        if 'birth_date' in kwargs:
            self.birth_date = kwargs['birth_date']
        else:
            self.birth_date = create_date(year=self.impossible_date_year, month=self.impossible_date_month,
                                          day=self.impossible_date_day)
        self.save()

    def add_death_details(self, *args, **kwargs):
        """
        Will create death object if it doesn't exist, or will update the fields if it does.
        The parameter list have to match bgsite.Death's field names.
        """
        # import pdb; pdb.set_trace()
        if args:
            kwargs = args[0]
        if kwargs['age_years']:  # and isinstance(kwargs['age_years'],float):
            if not kwargs['age_months']:
                kwargs['age_months'] = (kwargs['age_years'] % 1) * 12 if (kwargs['age_years'] % 1) * 12 != 0 else None
            else:
                kwargs['age_months'] = int(kwargs['age_months']) + (kwargs['age_years'] % 1) * 12
            kwargs['age_years'] = int(kwargs['age_years'])

        if kwargs['age_months']:
            if kwargs['age_months'] >= 12:
                if not kwargs['age_years']:
                    kwargs['age_years'] = int(int(kwargs['age_months']) / 12)
                else:
                    kwargs['age_years'] = int(kwargs['age_years']) + int(int(kwargs['age_months']) / 12)
                if not kwargs['age_days']:
                    kwargs['age_days'] = (kwargs['age_months'] % 1) * 30 if (kwargs[
                                                                                 'age_months'] % 1) * 30 != 0 else None
                else:
                    kwargs['age_days'] = int(kwargs['age_days']) + (kwargs['age_months'] % 1) * 30
                kwargs['age_months'] = int(kwargs['age_months']) % 12
            else:
                if not kwargs['age_days']:
                    kwargs['age_days'] = (kwargs['age_months'] % 1) * 30 if (kwargs[
                                                                                 'age_months'] % 1) * 30 != 0 else None
                else:
                    kwargs['age_days'] = int(kwargs['age_days']) + (kwargs['age_months'] % 1) * 30
                kwargs['age_years'] = 0 if kwargs['age_years'] is None else kwargs['age_years']

        if kwargs['age_days']:
            if kwargs['age_days'] >= 365:
                if not kwargs['age_years']:
                    kwargs['age_years'] = int(int(kwargs['age_days']) / 365)
                else:
                    kwargs['age_years'] = int(kwargs['age_years']) + int(int(kwargs['age_days']) / 365)
                kwargs['age_days'] = int(kwargs['age_days']) % 365
            else:
                kwargs['age_years'] = 0 if kwargs['age_years'] is None else kwargs['age_years']

        if kwargs['age_hours']:
            kwargs['age_years'] = 0 if kwargs['age_years'] is None else kwargs['age_years']

        if kwargs['age_minutes']:
            kwargs['age_years'] = 0 if kwargs['age_years'] is None else kwargs['age_years']

        if ('impossible_date_day' in kwargs and not kwargs['impossible_date_day']):
            kwargs['impossible_date_day'] = None
        if ('impossible_date_month' in kwargs and not kwargs['impossible_date_month']):
            kwargs['impossible_date_month'] = None
        if ('impossible_date_year' in kwargs and not kwargs['impossible_date_year']):
            kwargs['impossible_date_year'] = None
        if 'death_date' not in kwargs:
            kwargs['death_date'] = create_date(year=kwargs['impossible_date_year'],
                                               month=kwargs['impossible_date_month'], day=kwargs['impossible_date_day'])

        # TODO:overwrite warning when not null
        death = Death.objects.update_or_create(person=self, defaults=kwargs)
        return death

    def add_residence_address(self, first_line=None, second_line=None, town=None, county=None, postcode=None,
                              country=None):
        """
        Creates a new :model:`main.Address` with the parameters first_line, second_line, city, county, country and postcode.
        If the person already has an address its overwrited.
        """
        # selecting appropriate address if it exists
        if not second_line:
            second_line = None
        if not town:
            town = None
        if not county:
            county = None
        if not country:
            country = None
        if not postcode:
            postcode = None
        addresses = Address.objects.filter(first_line=first_line, second_line=second_line, town=town, county=county,
                                           postcode=postcode, country=country)
        if addresses.exists():
            # QUESTION: Should the old address be deleted from the DB (assuming nobody else has the same address)?
            self.residence_address = addresses.first()
        else:
            self.residence_address = Address.objects.create(first_line=first_line, second_line=second_line, town=town,
                                                            county=county, postcode=postcode, country=country)
        self.save()
        return self.residence_address

    def add_profession(self, profession):
        """
        Associates the :model:`main.Profession` parameter to the Person.profession.
        If this profession value already exists, it will just make the relation,
        if this profession does not exist, it will create the profession value and make the relation.
        """
        self.profession = profession
        self.save()
        return self.profession

    def add_memorial(self, memorial, link_burial_to_graveplot=True):
        """
        Will add an existing Memorial object to person
        """
        if self.is_dead() is False:
            self.add_death_details()
        if memorial not in self.get_memorials():
            self.death.add_memorial(memorial)
        else:
            print('memorial already exists')
        # relate graveplot photo/memorial to person
        if link_burial_to_graveplot and memorial.graveplot_memorials.count() >= 1 and self.death.death_burials.count() >= 1:
            plot_photo = memorial.graveplot_memorials.all().first()
            burial_to_be_added = self.death.death_burials.all().first()
            plot_photo.burials.add(burial_to_be_added)
            plot_photo.save()

    def remove_memorial(self, memorial):
        """
        Will remove an existing Memorial object from person
        """
        if memorial in self.get_memorials():
            self.death.remove_memorial(memorial)
        else:
            print("memorial doesn't exist")

    def add_burial(self, burial):
        """
        Will add an existing Burial object to person
        """
        if self.is_dead() is False:
            self.add_death_details()
        if burial not in self.get_burials():
            self.death.add_burial(burial)
        else:
            print('burial already exists')

    def create_burial(self, *args, **kwargs):
        if self.is_dead() is False:
            self.add_death_details()
        if args:
            kwargs = args[0]
        # if('burial_number' not in kwargs):
        #     raise ObjectDoesNotExist('burial_number is a required argument')
        new_burial = Burial.objects.create(death=self.death)
        new_burial.add_burial_details(*args, **kwargs)
        self.death.add_burial(new_burial)
        return new_burial

    def add_graveplot_to_burial(self, graveplot, burial):
        burials = self.get_burials()
        """Will add a Graveplot object to a specified Burial object"""
        if burial not in self.get_burials():
            raise ObjectDoesNotExist("The burial linked doesn't belong to this person")
        burial.add_graveplot(graveplot)

    def add_person_data(self, person_data):
        """
        Add or Update person details
        """
        # Handle impossible dates
        # Date of birth
        if self.birth_date == None:
            self.birth_date = create_date(year=person_data['impossible_date_year_person'],
                                          month=person_data['impossible_date_month_person'],
                                          day=person_data['impossible_date_day_person'])
        # Date of death
        person_death_date = create_date(year=person_data['impossible_date_year_death'],
                                        month=person_data['impossible_date_month_death'],
                                        day=person_data['impossible_date_day_death'])
        # FIN: handle impossible dates

        self.add_person_details(first_names=person_data['first_names'], last_name=person_data['last_name'],
                                gender=person_data['gender'], title=person_data['title'],
                                nickname=person_data['nickname'],
                                description=person_data['description'],
                                impossible_date_day=person_data['impossible_date_day_person'],
                                impossible_date_month=person_data['impossible_date_month_person'],
                                impossible_date_year=person_data['impossible_date_year_person'])
        if person_data['profession']:
            self.add_profession(person_data['profession'])
        if (person_data['residence_address'] or person_data['second_line'] or person_data['town'] or person_data[
            'county'] or person_data['country'] or person_data['postcode']):
            self.add_residence_address(first_line=person_data['residence_address'],
                                       second_line=person_data['second_line'], town=person_data['town'],
                                       county=person_data['county'], country=person_data['country'],
                                       postcode=person_data['postcode'])

        self.add_death_details(death_date=person_death_date, age_years=person_data['age_years'],
                               age_months=person_data['age_months'], age_weeks=person_data['age_weeks'],
                               age_hours=person_data['age_hours'], age_minutes=person_data['age_minutes'],
                               age_days=person_data['age_days'],
                               impossible_date_day=person_data['impossible_date_day_death'],
                               impossible_date_month=person_data['impossible_date_month_death'],
                               impossible_date_year=person_data['impossible_date_year_death'], )

    def bury_person(self, feature_json):
        """
        Creates memorial, attach memorial to person,
        update graveplot with graveplot_polygon_feature parameter
        Returns dictionary
        """
        # print(graveplot_polygon_feature)
        # import pdb; pdb.set_trace()
        # feature_json = json.loads(graveplot_polygon_feature)
        feature_dict = json.loads(feature_json)
        burial_record = self.get_burials().first()
        if not burial_record:
            burial_record = self.create_burial()

        if feature_dict['properties']['layer'] in ['plot', 'available_plot', 'reserved_plot']:
            # feature_dict['id'] either references a GravePlot or a TopoPolygon
            # If it references a TopoPolygon ('available_plot'), create a GravePlot using said TopoPolygon
            # If it references a GravePlot ('plot', 'reserved_plot'), get it and its TopoPolygon
            feature = GravePlot.objects.get_from_uuid(feature_dict['id'])
            if not feature:
                feature_polygon = TopoPolygons.objects.get(id=feature_dict['id'])
                feature = GravePlot.objects.create(topopolygon=feature_polygon)
            else:
                feature_polygon = feature.topopolygon
            feature_polygon.update_feature_code('plot')

            # add burial to any memorials linked to this graveplot
            for memorial in feature.memorials.all():
                self.add_memorial(memorial)

            burial_record.add_graveplot(feature)
        # i.e. a memorial
        else:
            feature = Memorial.objects.get(uuid=feature_dict['id'])
            self.add_memorial(feature)
            feature_polygon = feature.topopolygon
            feature_polygon.update_feature_code(feature_dict['properties']['layer'])

            # add burial to any graveplots linked to this graveplot
            for graveplot in feature.graveplot_memorials.all():
                self.add_graveplot_to_burial(graveplot, burial_record)

        burial_record.save()
        graveplot_dict = {'id': str(feature.get_uuid()), 'marker_type': feature.marker_type,
                          'geometry': feature_polygon.geometry}

        return {'feature_dict': feature_dict, 'graveplot': feature, 'graveplot_dict': graveplot_dict}


class AuthorityForInterment(SoftDeletionModel):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    first_names = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True,
                                   verbose_name='First names')
    last_name = models.CharField(max_length=50, validators=[bleach_validator], null=True, blank=True,
                                 verbose_name='Last name')
    title = models.CharField(max_length=50, validators=[bleach_validator], null=True, blank=True, verbose_name='Title')


class Tag(models.Model):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    top_left_bottom_right = models.MultiPointField()
    objects = TagQuerySet.as_manager()

    def get_polygon(self):
        envelope = self.top_left_bottom_right.envelope()


class Death(models.Model):
    """
    Death contains details of the bgsite.Person's day of death. They have always one or many bgsite.Memorial related,
    and at the same time the bgsite.Memorial could be related to other Death person.
    """
    person = models.OneToOneField(Person, primary_key=True, help_text="One-to-One relationship", editable=False,
                                  related_name="death", on_delete=models.CASCADE)
    """One-to-One relationship with :model:`bgsite.Person`"""
    memorials = models.ManyToManyField(Memorial, help_text="Many-to-Many relationship", editable=False,
                                       related_name='memorial_deaths')
    """Many-to-Many relationship with :model:`bgsite.Memorial`"""
    event = models.CharField(max_length=100, null=True, blank=True, verbose_name='War/Event related to Death',
                             help_text="Optional. Death have one related Event")
    """Optional. Death have one related Event"""
    address = models.ForeignKey(Address, null=True, verbose_name='Place of Death',
                                help_text="Optional. Death have one related Address", blank=True,
                                on_delete=models.CASCADE)
    """Optional. Death have one related Address"""
    age_years = models.PositiveIntegerField(db_index=True, verbose_name='Age(years)', null=True, blank=True)
    """Age years"""
    age_months = models.PositiveIntegerField(null=True, verbose_name='Age(months)', blank=True)
    """Age months"""
    age_weeks = models.PositiveIntegerField(null=True, verbose_name='Age(weeks)', blank=True)
    """Age weeks"""
    age_days = models.PositiveIntegerField(null=True, verbose_name='Age(days)', blank=True)
    """Age days"""
    age_hours = models.PositiveIntegerField(null=True, verbose_name='Age(hours)', blank=True)
    """Age hours"""
    age_minutes = models.PositiveIntegerField(null=True, verbose_name='Age(minutes)', blank=True)
    """Age minutes"""
    parish = models.CharField(max_length=100, null=True, blank=True, verbose_name='Parish')
    """:model:`main.Parish` related to where the person was buried"""
    religion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Religion')
    """:model:`main.Religion`"""
    death_date = models.DateField(db_index=True, null=True, editable=False)
    """Date of death: format = dd/mm/yyyy. Incorrect if impossible_date is True. Populated in save override."""
    impossible_date = models.BooleanField(default=False, editable=False)
    """True or False, default = False"""
    impossible_date_day = models.IntegerField(null=True, blank=True, verbose_name='Day of Death')
    """Day of Death: 'impossible' is legacy and has no meaning"""
    impossible_date_month = models.IntegerField(null=True, blank=True, verbose_name='Month of Death')
    """Month of Death: 'impossible' is legacy and has no meaning"""
    impossible_date_year = models.IntegerField(null=True, blank=True, verbose_name='Year of death')
    """Year of death: 'impossible' is legacy and has no meaning"""
    death_place = models.CharField(max_length=50, validators=[bleach_validator], null=True, blank=True,
                                   verbose_name='Place of death')
    """Place of death"""
    death_year = models.CharField(max_length=6, validators=[bleach_validator], null=True, blank=True, editable=False,
                                  help_text="Optional. Temp daeth_year as char to record death date off headstone")
    """Optional. Temp death_year as char to record death date off headstone"""
    death_cause = models.CharField(max_length=250, validators=[bleach_validator], null=True, blank=True,
                                   verbose_name='Cause of death')
    """Death cause, max length =  250 characteres"""

    def __str__(self):
        return 'Date of death {0}'.format(self.death_date)

    def save(self, **kwargs):

        full_date, impossible_date = date_elements_to_full_date(self.impossible_date_day, self.impossible_date_month,
                                                                self.impossible_date_year)
        self.death_date = full_date
        self.impossible_date = impossible_date

        super(Death, self).save()

    def get_all_details(self):
        """
        Returns a dictionary (key: Field Name, value: Field Value) with almost all fields, missing death_year, death_cause and all impossible_dates.
        """
        return {'event': self.event, 'address': self.address, 'age_years': self.age_years,
                'age_months': self.age_months, 'age_weeks': self.age_weeks, 'age_days': self.age_days,
                'age_hours': self.age_hours, 'age_minutes': self.age_minutes, 'parish': self.parish,
                'religion': self.religion, 'death_date': self.death_date,
                'impossible_date_day_death': self.impossible_date_day,
                'impossible_date_month_death': self.impossible_date_month,
                'impossible_date_year_death': self.impossible_date_year}

    def get_burials(self):
        """
        Returns the :model:`bgsite.Burial` set related to :model:`bgsite.Death`.
        """
        return self.death_burials.all()

    def get_graveplots(self):
        """
        Returns a vector with all the burial.graveplot related to the :model:`bgsite.Burial` set.
        """
        return [burial.graveplot for burial in self.get_burials()]

    def get_memorials(self):
        """
        Returns all :model:`bgsite.Memorial` related to Death.
        """
        return self.memorials.all()
        # return [memorial for memorial in Memorial.objects.all_cache() if (self in memorial.death_set.all())]

    def get_first_memorial(self):
        """
        Returns all :model:`bgsite.Memorial` related to Death.
        """
        return self.memorials.all().first()

    def add_burial(self, burial):
        """
        Adds a new :model:`bgsite.Burial` into the death_burials related.
        """
        self.death_burials.add(burial)
        return burial

    def add_address(self, first_line=None, second_line=None, town=None, county=None, postcode=None, country=None):
        """
        Creates a new :model:`main.Address` with the parameters first_line, town, county and postcode.
        If the person already has an address its overwrited.
        """
        # selecting appropriate address if it exists
        if not town:
            town = None
        if not county:
            county = None
        if not postcode:
            postcode = None
        addresses = Address.objects.filter(first_line=first_line, second_line=second_line, town=town, county=county,
                                           postcode=postcode, country=country)
        if addresses.exists():
            self.address = addresses.first()
        else:
            self.address = Address.objects.create(first_line=first_line, second_line=second_line, town=town,
                                                  county=county, postcode=postcode, country=country)
        self.save()
        return self.address

    def add_event(self, name, description):
        """
        Creates a new :model:`main.Event` with the parameters name and description.
        If the person already has an event it is overwritten.
        """
        self.event = name
        self.save()
        return self.event

    def add_parish(self, parish):
        """
        Creates a new :model:`main.Parish` with the parameters parish.
        If the person already has an parish it is overwritten.
        """
        self.parish = parish
        self.save()
        return self.parish

    def add_religion(self, religion):
        """
        Creates a new :model:`main.Religion` with the parameters religion.
        If the person already has an religion it is overwritten.
        """
        self.religion = religion
        self.save()
        return self.religion

    def add_memorial(self, memorial):
        """
        Adds a new :model:`bgsite.Memorial` into the memorials list related.
        """
        self.memorials.add(memorial)
        return memorial

    def remove_memorial(self, memorial):
        """
        Removes a :model:`bgsite.Memorial` from the memorials list related.
        """
        self.memorials.remove(memorial)
        return memorial

    def get_most_recent_burial(self):

        burials = self.death_burials

        if not burials or not burials.first():
            return None

        else:
            # get the most recent burial if multiple
            try:
                return burials.order_by('impossible_date_year').first()
                # return burials.order_by('-impossible_date_year, -impossible_date_month, -impossible_date_day').first()
            except Exception:
                return burials.first()

    def get_most_recent_burial_id(self):

        most_recent_burial = self.get_most_recent_burial()

        if most_recent_burial:
            return most_recent_burial.id
        else:
            return None

    def get_most_recent_burial_date(self):

        most_recent_burial = self.get_most_recent_burial()

        if most_recent_burial:
            return create_date(day=most_recent_burial.impossible_date_day,
                               month=most_recent_burial.impossible_date_month,
                               year=most_recent_burial.impossible_date_year)

        else:
            return None


class Official(SoftDeletionModel):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    job_title = models.CharField(max_length=100, validators=[bleach_validator], verbose_name='Job Title', null=True,
                                 blank=True)
    title = models.CharField(max_length=100, validators=[bleach_validator], verbose_name='Title', null=True, blank=True)
    first_names = models.CharField(max_length=200, validators=[bleach_validator], verbose_name='First Names', null=True,
                                   blank=True)
    last_name = models.CharField(db_index=True, max_length=100, validators=[bleach_validator], verbose_name='Last Name',
                                 null=True, blank=True)
    used_on = models.DateTimeField(null=True, default=timezone.now)
    objects = BurialOfficialQuerySet.as_manager()
    email = models.CharField(max_length=200, validators=[bleach_validator], verbose_name='Email', null=True, blank=True)
    phone_number = models.CharField(max_length=200, validators=[bleach_validator], verbose_name='Phone Number',
                                    null=True, blank=True)
    second_phone_number = models.CharField(max_length=200, validators=[bleach_validator],
                                           verbose_name='Second Phone Number', null=True, blank=True)
    address = models.ForeignKey(Address, null=True, related_name='address', on_delete=models.SET_NULL)
    company_name = models.CharField(max_length=200, validators=[bleach_validator], verbose_name='Company Name',
                                    null=True, blank=True)

    def __str__(self):
        return '{0} , {1} ({2})'.format(self.last_name, self.first_names, self.job_title)


class BurialManager(SoftDeletionManager):
    def _rename_queryset_value(self, values_queryset, name_dict):
        """Renames the fields (called by old_name) in the values queryset
        to new_name"""
        for values_dict in values_queryset:
            for old_name, new_name in name_dict.items():
                values_dict[new_name] = values_dict.pop(old_name)
        return values_queryset

    def _format_address(self, firstline, town, county, postcode):
        addr = ''
        if firstline:
            addr += firstline + ' '
        if town:
            addr += town + ' '
        if county:
            addr += county + ' '
        if postcode:
            addr += postcode + ' '
        return addr

    def get_person_death_burial_values(self, burial_record_image):
        burials = []
        if burial_record_image:
            burials = self.filter(burial_record_image=burial_record_image). \
                order_by('burial_number').values('death__person_id', 'death__person__tag__id',
                                                 'death__person__tag__top_left_bottom_right', \
                                                 'death__person__title', 'death__person__first_names',
                                                 'death__person__other_names', \
                                                 'death__person__birth_name', 'death__person__last_name', \
                                                 'death__person__impossible_date_day',
                                                 'death__person__impossible_date_month', \
                                                 'death__person__impossible_date_year', 'death__person__gender', \
                                                 'death__person__description', 'death__person__profession', \
                                                 'death__person__residence_address__first_line',
                                                 'death__person__residence_address__second_line', \
                                                 'death__person__residence_address__town',
                                                 'death__person__residence_address__county', \
                                                 'death__person__residence_address__postcode',
                                                 'death__person__residence_address__country', \
 \
                                                 'death__event', 'death__event', \
                                                 'death__address__first_line', 'death__address__second_line', \
                                                 'death__address__town', 'death__address__county', \
                                                 'death__address__postcode', 'death__address__country', \
                                                 'death__age_years', 'death__age_months', \
                                                 'death__age_weeks', 'death__age_days', 'death__age_hours',
                                                 'death__age_minutes', \
                                                 'death__parish', 'death__religion', \
                                                 'death__impossible_date_day', 'death__impossible_date_month', \
                                                 'death__impossible_date_year', 'death__death_cause', \
 \
                                                 'burial_official__official_type', 'burial_official__official__title', \
                                                 'burial_official__official__first_names',
                                                 'burial_official__official__last_name', \
                                                 'burial_official__official__id',
                                                 'burial_official__burial_official_type__id', \
                                                 'burial_number', 'impossible_date_day', \
                                                 'impossible_date_month', 'impossible_date_year', \
                                                 'consecrated', 'cremation_certificate_no', 'cremated',
                                                 'impossible_cremation_date_day', \
                                                 'impossible_cremation_date_month', 'impossible_cremation_date_year', \
                                                 'interred', 'depth', 'depth_units', 'burial_remarks', \
                                                 'requires_investigation', 'user_remarks', \
                                                 'situation', 'graveref__grave_number', 'place_from_which_brought')
            for burial in burials:
                burial['death__person_id'] = str(burial['death__person_id'])
        return list(
            merge_values(values=burials, id_field='death__person_id', many_to_many_model_field='burial_official'))

    def upload_photos(self, photos_files, filename_format):
        """
        Upload burial scan photos, will upload image per image as long as none
        of the following errors occur, the image with error wont be uploaded, but the others will:
            - Not a valid image contents
            - Match input mask for the filename
        """
        temp_dir = get_and_clean_temp_dir(connection.schema_name)
        result = {'error': []}

        image_type = ImageType.objects.get(image_type='burial_record')
        image_state = ImageState.objects.get(image_state='unprocessed')

        if filename_format == 'grave_number':
            # sample accepted pattern: 3244_A_00168.jpg
            pattern = re.compile(REGISTER_IMAGE_GRAVENUMBER_PATTERN + '.(jpg|jpeg)$', re.IGNORECASE)
        else:
            # sample accepted pattern: 13244_1867-1952_168_t.jpg or 13244_1867-1952_168.jpg
            pattern = re.compile(REGISTER_IMAGE_PAGENUMBER_PATTERN + '.(jpg|jpeg)$', re.IGNORECASE)

        for pos, photo_file in enumerate(photos_files):
            if pattern.match(photo_file.name):
                # if True: # Remove restriction

                # if image already exists with matching filename
                if Image.objects.filter(url__endswith=photo_file.name, image_type=image_type,
                                        image_state=image_state).exists():
                    result['error'].append("Filename '" + photo_file.name + "' already exists.")
                    continue

                result_val = verify_contents(photo_file)
                if result_val == '':  # image is valid?
                    compressed_image = Image.compressImage(photo_file, 'burial_records_photos')
                    # upload photos to bucket, create record in database, url=photo_file to upload original
                    image = Image(url=compressed_image, image_type=image_type, image_state=image_state)
                    image.save()
                    image.create_thumbnail(photo_file)
                else:
                    result['error'].append(result_val)
            else:
                result['error'].append(
                    'Please make sure the filename "' + photo_file.name + '" meets the correct input format.')

        shutil.rmtree(temp_dir)
        return result

    def get_unlinked_burials_with_transcribed_grave_number(self, grave_number):
        """
        Gets burials not linked to a graveplot and with given grave number.

        Note: this does not take section and sunsection into account. Ideally it would. But there it's currently not possible to add this in data entry and even if I did add it, it would be missing from previous work. 
        
        We can assume that for current transcribed data, the grave number is actually unique regardless of section and/or subsection. In the future we may need a setting that allows some sites to have unique grave numbers and others unique grave ref (grave number, section and subsection)
        """

        burials = self.filter(graveplot__isnull=True, graveref__grave_number=grave_number)
        graveplot_burial_distinct_list = []

        if burials.exists():
            for burial in burials:
                graveplot_burial_distinct_list.append({'person_id': burial.death.person_id, 'burial_id': burial.id,
                                                       'display_name': burial.death.person.get_display_name(),
                                                       'selected': True})

        return graveplot_burial_distinct_list


class Burial(SoftDeletionModel):
    """
    Burial contains the burial record information related to one or multiple bgsite.Death because one bgsite.Person could be buried multiple times.
    The Burial might also share the same bgsite.GravePlot with other Burial.
    """
    UNITS = (
        ('ft/in', 'Feet'),
        ('mtrs', 'Meters'),
    )
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    graveplot = models.ForeignKey(GravePlot, null=True,
                                  help_text="Multiple people buried in same plot eg. family members but only one graveplot per burial record",
                                  related_name='burials', on_delete=models.CASCADE)
    """Multiple people buried in same plot eg. family members but only one graveplot per burial record"""
    burial_officials = models.ManyToManyField(Official, verbose_name='Burial Official', through='Burial_Official',
                                              blank=True)
    """Many officials for same burial and many burials can have the same official"""
    death = models.ForeignKey(Death, help_text="Same Death person can be buried multiple times", editable=False,
                              related_name="death_burials", on_delete=models.CASCADE)
    """Same Death person can be buried multiple times"""
    burial_record_image = models.ForeignKey(Image, null=True, blank=True, editable=False, on_delete=models.CASCADE)
    """Burial record :model:`bgsite.Image` related"""
    burial_number = models.CharField(max_length=30, validators=[bleach_validator],
                                     help_text="Serial number of the entry in physical book", null=True, blank=True)
    """Booking grave number origin: It can take three values: True if it is new or false if it has already existed, and Null if none of the above"""
    new_burial_grave = models.NullBooleanField(null=True, verbose_name='New burial grave')
    """Serial number of the entry in physical book"""
    burial_date = models.DateField(db_index=True, null=True, editable=False)
    """Date of burial: format = dd/mm/yyyy. Incorrect if impossible_date is True. Populated in save override."""
    impossible_date = models.BooleanField(default=False, editable=False)
    """True or False, default = False"""
    impossible_date_day = models.IntegerField(null=True, blank=True, verbose_name='Day of Burial')
    """Day of Burial: 'impossible' is legacy and has no meaning"""
    impossible_date_month = models.IntegerField(null=True, blank=True, verbose_name='Month of Burial')
    """Month of Burial: 'impossible' is legacy and has no meaning"""
    impossible_date_year = models.IntegerField(null=True, blank=True, verbose_name='Year of Burial')
    """Year of Burial: 'impossible' is legacy and has no meaning"""
    order_date = models.DateField(db_index=True, null=True, editable=False)
    """Date of burial: format = dd/mm/yyyy. Incorrect if impossible_order_date is True. Populated in save override."""
    impossible_order_date = models.BooleanField(default=False, editable=False)
    """True or False, default = False"""
    impossible_order_date_day = models.IntegerField(null=True, blank=True, verbose_name='Day of order')
    """Day of order: 'impossible' is legacy and has no meaning"""
    impossible_order_date_month = models.IntegerField(null=True, blank=True, verbose_name='Month of order')
    """Month of order: 'impossible' is legacy and has no meaning"""
    impossible_order_date_year = models.IntegerField(null=True, blank=True, verbose_name='Year of order')
    """Year of order: 'impossible' is legacy and has no meaning"""
    consecrated = models.NullBooleanField(null=True, verbose_name='In consecrated ground')
    """True or False, default = False"""
    cremated = models.NullBooleanField(null=True, verbose_name='Cremated')
    """True or False, default = null"""
    cremation_date = models.DateField(null=True, blank=True, editable=False)
    """Cremation date: format = dd/mm/yyyy. Incorrect if impossible_date is True. Populated in save override."""
    impossible_cremation_date = models.BooleanField(default=False, editable=False)
    """True or False, default = False"""
    impossible_cremation_date_day = models.IntegerField(null=True, blank=True, verbose_name='Day of Cremation')
    """Day of Cremation: 'impossible' is legacy and has no meaning"""
    impossible_cremation_date_month = models.IntegerField(null=True, blank=True, verbose_name='Month of Cremation')
    """Month of Cremation: 'impossible' is legacy and has no meaning"""
    impossible_cremation_date_year = models.IntegerField(null=True, blank=True, verbose_name='Year of Cremation')
    """Year of Cremation: 'impossible' is legacy and has no meaning"""
    cremation_certificate_no = models.CharField(max_length=35, validators=[bleach_validator], null=True, blank=True,
                                                verbose_name='Cremation Certificate No.')
    """In case the person was cremated."""
    interred = models.NullBooleanField(default=False, null=True, verbose_name='Interred')
    """True or False, default = False"""
    coffin_width = models.FloatField(null=True, blank=True)
    """Length of the coffin or casket."""
    coffin_length = models.FloatField(null=True, blank=True)
    """Width of the coffin or casket."""
    coffin_height = models.FloatField(null=True, blank=True)
    """Height of the coffin or casket."""
    coffin_units = models.CharField(max_length=15, validators=[bleach_validator], null=True, blank=True,
                                    verbose_name='Coffin Units(ft/mtrs)', choices=UNITS)
    """Coffin Units(ft/m/cm)"""
    depth = models.CharField(max_length=15, validators=[bleach_validator], null=True, blank=True,
                             verbose_name='Depth of grave')
    """Depth of burial"""
    depth_units = models.CharField(max_length=15, validators=[bleach_validator], null=True, blank=True,
                                   verbose_name='Depth Units(ft/mtrs)', choices=UNITS)
    """Depth units"""
    depth_position = models.CharField(max_length=15, null=True, blank=True, verbose_name='Depth position of grave')
    """Depth position of burial"""
    coffin_comments = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True,
                                       verbose_name='Additional Info about coffin')
    """User comments on coffin"""
    burial_remarks = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True,
                                      verbose_name='Additional Info not elsewhere specified')
    requires_investigation = models.BooleanField(default=False, verbose_name='Needs checking')
    """True or False, default = False"""
    user_remarks = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True,
                                    verbose_name='Comments')
    """location or situation of the grave"""
    situation = models.CharField(max_length=50, validators=[bleach_validator], null=True, blank=True,
                                 verbose_name='Grave Location')
    graveref = models.ForeignKey(GraveRef, null=True, blank=True, verbose_name="Grave Reference",
                                 on_delete=models.SET_NULL, related_name='graveref_burials')
    """place_from_which_brought - Specific to Pershore"""
    place_from_which_brought = models.CharField(max_length=100, validators=[bleach_validator], null=True, blank=True,
                                                verbose_name='Place/Parish from which brought')
    register = models.CharField(max_length=30, validators=[bleach_validator], null=True, blank=True,
                                verbose_name='Register recording burial name/code')
    register_page = models.IntegerField(null=True, blank=True, verbose_name='Page number in register')
    """Register recording burial name/code"""
    registration_number = models.IntegerField(null=True, blank=True, verbose_name='Registration Number')
    """Registration Number"""
    objects = BurialManager()

    def __str__(self):
        return 'Burial number {0}'.format(self.burial_number)

    def save(self, **kwargs):

        full_date, impossible_date = date_elements_to_full_date(self.impossible_date_day, self.impossible_date_month,
                                                                self.impossible_date_year)
        self.burial_date = full_date
        self.impossible_date = impossible_date

        full_order_date, impossible_order_date = date_elements_to_full_date(self.impossible_order_date_day,
                                                                            self.impossible_order_date_month,
                                                                            self.impossible_order_date_year)
        self.order_date = full_order_date
        self.impossible_order_date = impossible_order_date

        full_cremation_date, impossible_cremation_date = date_elements_to_full_date(self.impossible_cremation_date_day,
                                                                                    self.impossible_cremation_date_month,
                                                                                    self.impossible_cremation_date_year)
        self.cremation_date = full_cremation_date
        self.impossible_cremation_date = impossible_cremation_date

        super(Burial, self).save()

    def create_burial_official(self, official_type, title, first_names, last_name, burial_official_type):
        official = Official.objects.get_or_create(title=title, first_names=first_names, last_name=last_name)[0]
        burial_official_type = BurialOfficialType.objects.get(id=burial_official_type)
        Burial_Official.objects.get_or_create(burial=self, official=official,
                                              official_type=burial_official_type.official_type,
                                              burial_official_type=burial_official_type)[0]

    def get_official_type(self, _official):
        ofi_burial_official = Burial_Official.objects.get(official=_official, burial=self)
        return ofi_burial_official.official_type

    def get_official_types(self, _official):
        ofi_burial_official = Burial_Official.objects.get(official=_official, burial=self)
        for botype in BurialOfficialType.objects.all():
            if botype.official_type == ofi_burial_official.official_type:
                return ofi_burial_official.official_type
        return 0

    def add_graveplot(self, graveplot):
        """Add a graveplot to Death"""
        self.graveplot = graveplot
        return self.graveplot

    def add_image(self, image):
        """
        Add a burial record image to this burial record
        """
        # if(image.image_type is 'burial_record')
        self.burial_record_image = image

    def add_burial_details(self, *args, **kwargs):
        """
        Assign all the details passed as parameter to its fields.
        """
        if 'burial_number' in kwargs:
            self.burial_number = kwargs['burial_number']
        if 'burial_date' in kwargs:
            self.burial_date = kwargs['burial_date']
        if 'consecrated' in kwargs:
            self.consecrated = kwargs['consecrated']
        if 'cremation_certificate_no' in kwargs:
            self.cremation_certificate_no = kwargs['cremation_certificate_no']
        if 'cremated' in kwargs:
            self.cremated = kwargs['cremated']
        if 'cremation_date' in kwargs:
            self.cremation_date = kwargs['cremation_date']
        if 'impossible_cremation_date_day' in kwargs and kwargs['impossible_cremation_date_day']:
            self.impossible_cremation_date_day = kwargs['impossible_cremation_date_day'] if kwargs[
                                                                                                'impossible_cremation_date_day'] != '' else 0
        if 'impossible_cremation_date_month' in kwargs and kwargs['impossible_cremation_date_month']:
            self.impossible_cremation_date_month = kwargs['impossible_cremation_date_month'] if kwargs[
                                                                                                    'impossible_cremation_date_month'] != '' else 0
        if 'impossible_cremation_date_year' in kwargs and kwargs['impossible_cremation_date_year']:
            self.impossible_cremation_date_year = kwargs['impossible_cremation_date_year'] if kwargs[
                                                                                                  'impossible_cremation_date_year'] != '' else 0
        self.cremation_date = create_date(self.impossible_cremation_date_year, self.impossible_cremation_date_month,
                                          self.impossible_cremation_date_day)
        if 'interred' in kwargs:
            self.interred = kwargs['interred']
        if 'depth' in kwargs:
            self.depth = kwargs['depth']
        if 'depth_units' in kwargs:
            self.depth_units = kwargs['depth_units']
        if 'burial_remarks' in kwargs:
            self.burial_remarks = kwargs['burial_remarks']
        if 'requires_investigation' in kwargs:
            self.requires_investigation = kwargs['requires_investigation']
        if 'user_remarks' in kwargs:
            self.user_remarks = kwargs['user_remarks']
        if 'situation' in kwargs:
            self.situation = kwargs['situation']
        if 'place_from_which_brought' in kwargs:
            self.place_from_which_brought = kwargs['place_from_which_brought']
        if 'impossible_date_day' in kwargs and kwargs['impossible_date_day']:
            self.impossible_date_day = kwargs['impossible_date_day'] if kwargs['impossible_date_day'] != '' else 0
        if 'impossible_date_month' in kwargs and kwargs['impossible_date_month']:
            self.impossible_date_month = kwargs['impossible_date_month'] if kwargs['impossible_date_month'] != '' else 0
        if 'impossible_date_year' in kwargs and kwargs['impossible_date_year']:
            self.impossible_date_year = kwargs['impossible_date_year'] if kwargs['impossible_date_year'] != '' else 0
        self.burial_date = create_date(self.impossible_date_year, self.impossible_date_month, self.impossible_date_day)
        if 'burial_officials' in kwargs:
            # TODO: delete first burial officials to delete: improved by deleted_forms from FormSets
            oldbo = []
            # import pdb; pdb.set_trace()
            self.remove_burial_officials()
            self.add_burial_officials(kwargs['burial_officials'], oldbo)

        grave_number = kwargs['grave_number'] if 'grave_number' in kwargs else None
        section = kwargs['section'] if 'section' in kwargs else None
        subsection = kwargs['subsection'] if 'section' in kwargs else None
        grave_number_or_section_removed = kwargs[
            'grave_number_or_section_removed'] if 'grave_number_or_section_removed' in kwargs else None
        grave_ref = None

        if grave_number or section:
            original_graveref = self.graveref

            grave_ref = GraveRef.objects.get_or_create_custom(grave_number=grave_number, section=section,
                                                              subsection=subsection)
            self.graveref = grave_ref

            if original_graveref and not hasattr(original_graveref,
                                                 'graveref_graveplot') and not original_graveref.graveref_burials.exists():
                # if this grave ref is no longer used - delete it
                original_graveref.delete()
        elif grave_number_or_section_removed:
            self.graveref = None

        self.save()

        if grave_ref and self.graveplot is not None and self.graveplot.graveref is None:
            # if graveplot exists and has no graveref, set graveref from burial
            self.graveplot.graveref = kwargs['grave_ref']
            self.graveplot.save()

    def add_burial_officials(self, burial_officials, oldbo):
        for burial_official in burial_officials:
            # import pdb; pdb.set_trace()
            if burial_official.get('official_id') != None and burial_official['official_id'] != '':
                bo = Official.objects.get(id=burial_official['official_id'])
                if burial_official['official_id'] not in oldbo:
                    if self.burial_officials.filter(id=burial_official['official_id']).count() == 0:
                        bo.used_on = datetime.datetime.now()
                        bo.save()
                # import pdb; pdb.set_trace()
                if burial_official["official_types"] != '' and burial_official["official_types"] != None:
                    # oft = BurialOfficialType.objects.get(id=burial_official["official_types"])
                    oft = burial_official["official_types"]
                else:
                    oft = burial_official["official_type"]
                nbo = Burial_Official.objects.create(official=bo, burial=self, official_type=oft)

    def remove_burial_officials(self):
        self.burial_officials.clear()

    def get_all_details(self):
        """
        Returns a dictionary with all its details as follows (key: value) ::
        > burial_record_image: Image related url if exist, in other case asigns empty string.
        > burial_number: Burial record number.
        > burial_date: Date of burial.
        > consecrated: True or False.
        > cremation_certificate_no: In case the person was cremated.
        > interret: True or False.
        > depth: How depth the person was buried + depth units.
        > requires_investigation: True or False.
        > user_remarks: user remarks.
        > impossible dates: in case the user has entered a no full date.
        """
        return {'burial_record_image': self.burial_record_image.url.url if self.burial_record_image is not None else '',
                'burial_number': self.burial_number, 'burial_date': self.burial_date, \
                'consecrated': self.consecrated, 'cremation_certificate_no': self.cremation_certificate_no,
                'cremation_date': self.cremation_date,
                'impossible_cremation_date_day': self.impossible_cremation_date_day,
                'impossible_cremation_date_month': self.impossible_cremation_date_month,
                'impossible_cremation_date_year': self.impossible_cremation_date_year, 'cremated': self.cremated,
                'interred': self.interred, 'depth': self.depth, 'requires_investigation': self.requires_investigation, \
                'user_remarks': self.user_remarks, 'burial_remarks': self.burial_remarks,
                'impossible_date_day': self.impossible_date_day, 'impossible_date_month': self.impossible_date_month, \
                'impossible_date_year': self.impossible_date_year,
                'grave_number': self.graveplot.graveref.grave_number if self.graveplot and self.graveplot.graveref is not None else '',
                'grave_plot_uuid': self.graveplot_id,
                'section': self.graveref.section if self.graveplot and self.graveplot.graveref is not None else '',
                'subsection': self.graveref.subsection if self.graveref is not None else ''}

    def get_depth_str(self):
        """Returns the depth of the Burial + depth units in String format"""
        if self.depth is not None:
            return str(self.depth) + ' ' + self.depth_units

    def get_image_url(self):
        if self.burial_record_image is not None:
            return {'image_url': self.burial_record_image.url.url, 'thumbnail_url': (
                self.burial_record_image.thumbnail.url.url if self.burial_record_image.has_thumbnail() else self.burial_record_image.url.url)}
        else:
            return ''

    def get_burial_officials_setlist(self):
        """
        Returns a vector with the :model:`bgsite.Official` information related to the Burial.
        """
        return [{'official_id': burial_official.id, 'official_title': burial_official.title,
                 'official_first_names': burial_official.first_names, 'official_last_name': burial_official.last_name,
                 'official_types': self.get_official_type(burial_official),
                 'official_type': self.get_official_type(burial_official)} for burial_official in
                self.burial_officials.all()]

    def create_burial_record_image(self, url):
        image = Image(url=url, image_type=ImageType.objects.get(image_type='memorial'),
                      image_state=ImageState.objects.get(image_state='unprocessed'))
        image.save()
        image.create_thumbnail(url)
        return image

    def create_image(self, url):
        """
        Add an image related to the burial record assigning the same image_type and create the thumbnail associated to the image
        """
        # compressed_image = Image.compressImage(url, 'burial_records_photos')
        # image = Image(url=compressed_image, image_type=ImageType.objects.get(image_type='burial_record'), image_state=ImageState.objects.get(image_state='unprocessed'))
        self.burial_record_image = self.create_burial_record_image(url)
        self.save()


class Burial_Official(models.Model):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    official = models.ForeignKey(Official, on_delete=models.CASCADE)
    burial = models.ForeignKey(Burial, on_delete=models.CASCADE)
    burial_official_type = models.ForeignKey(BurialOfficialType, null=True, on_delete=models.DO_NOTHING)
    """Burial Official Type"""
    official_type = models.CharField(max_length=50, null=True)

    def __str__(self):
        return 'Official "' + self.official.first_names + ' ' + self.official.last_name + '" related to the burial of "' + self.burial.death.person.first_names + ' ' + self.burial.death.person.last_name + '"'


class ReservedPlot(models.Model):
    """
    Represent the plot reservation, allows more than one person per plot
    """
    reservation_reference = models.CharField(null=True, unique=True, max_length=35)
    person = models.OneToOneField(Person, primary_key=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=200, validators=[bleach_validator], null=True)
    grave_plot = models.ForeignKey(GravePlot, blank=True, null=True, on_delete=models.CASCADE)
    state = models.ForeignKey(ReservePlotState, on_delete=models.CASCADE)
    objects = ReservedPlotQuerySet.as_manager()
    origin = models.ForeignKey(FeatureCode, blank=True, null=True, on_delete=models.CASCADE)
    """
    FeatureCode from which the plot was reserved
    """

    def add_reserved_plot_details(self, *args, **kwargs):
        if args:
            kwargs = args[0]
        if 'notes' in kwargs:
            self.notes = kwargs['notes']
        self.save()

    def delete(self):
        """
        Change status to 'deleted'
        """
        self.state = ReservePlotState.objects.get(state='deleted')
        self.grave_plot = None
        self.save()


class Inspection(models.Model):
    """
    An Inspection is a log entry with a many-to-one relationship with Memorial. This allows
    a Memorial to have a visibile history of Inspections.
    """

    # Use Inspection.XYZ_CONDITION to query rather than '0'
    GOOD_CONDITION = 1
    REASONABLE_CONDITION = 2
    POOR_CONDITION = 3
    CONDITION_CHOICES = (
        (GOOD_CONDITION, 'Good'),
        (REASONABLE_CONDITION, 'Reasonable'),
        (POOR_CONDITION, 'Poor'),
    )

    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4)
    memorial = models.ForeignKey(Memorial, null=False, on_delete=models.CASCADE)
    condition = models.IntegerField(choices=CONDITION_CHOICES, default=GOOD_CONDITION)
    remarks = models.TextField(max_length=200, validators=[bleach_validator], null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    action_required = models.BooleanField(default=False)
    image = models.ForeignKey(Image, null=True, blank=True, editable=False, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    inscription = models.IntegerField(choices=CONDITION_CHOICES, default=GOOD_CONDITION)

    def create_image(self, url):
        """
        Add an image and thumbnail to the inspection
        """
        # compress image to less than 1mb
        # compressed_image = Image.compressImage(url, 'inspection_photos')
        image = Image(url=url, image_type=ImageType.objects.get(image_type='memorial'),
                      image_state=ImageState.objects.get(image_state='unprocessed'))
        image.save()
        image.create_thumbnail(url)
        self.image = image
        self.save()

    def __str__(self):
        return 'Inspection for Memorial(' + str(self.memorial.uuid) + ') on ' + str(self.date)


class MemorialInscriptionDetail(models.Model):
    """
    Names and ages as read from memorials.
    """

    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4)
    memorial = models.ForeignKey(Memorial, null=False, on_delete=models.CASCADE, related_name='memorial_inscriptions')
    first_names = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True,
                                   verbose_name='First names')
    last_name = models.CharField(max_length=35, validators=[bleach_validator], null=True, blank=True,
                                 verbose_name='Last name')
    age = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)


class MeetingLocation(models.Model):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    location_address = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(MeetingLocation, self).save(*args, **kwargs)


class PersonField(models.Model):
    TEXT = 'text'
    SELECT = 'select'

    QUESTION_TYPES = (
        (TEXT, 'text'),
        (SELECT, 'select'),
    )
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
    options = models.TextField(blank=True, null=True,
                               help_text='if the question type is "select," provide a comma-separated list of options for this question.')
    required = models.BooleanField()
    is_default = models.BooleanField()
    content = models.CharField(max_length=200, blank=True, null=True)
    field_form = models.CharField(max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Person Field Customisation'


# avoid circular dependancy
from mapmanagement.serializers import MemorialGeoSerializer, GraveplotGeoSerializer
