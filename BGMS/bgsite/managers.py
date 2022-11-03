from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Centroid, Envelope
from fuzzywuzzy import fuzz
import datetime
from django.db import connection
from django.db.models import F, Q, Func
from itertools import chain
import itertools
from django.db.models.query import QuerySet
from BGMS.utils import get_and_clean_temp_dir, verify_contents, scorer, rename_queryset_value, fuzzy_search_fullname
from main.models import ReservePlotState
from main.models_abstract import SoftDeletionManager
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import csv
import shutil
from PIL import Image, ExifTags
import io
from django.core.files.base import ContentFile
from geometries.models import TopoPolygons, Layer

"""
When you call values() on a queryset where the Model has a ManyToManyField
and there are multiple related items, it returns a separate dictionary for each
related item. This function merges the dictionaries so that there is only
one dictionary per id at the end, with lists of related items for each.
"""
def merge_values(values, id_field, many_to_many_model_field):
    grouped_results = itertools.groupby(values, key=lambda value: value[id_field])
    merged_values = []
    for k, g in grouped_results:
        groups = list(g)
        merged_value = {}
        merged_value[many_to_many_model_field] = []
        for group in groups:
            many_to_many = {}
            for key, val in group.items():
                if key.startswith(many_to_many_model_field):
                    many_to_many[key] = val
                else:
                    merged_value[key] = val
            merged_value[many_to_many_model_field].append(many_to_many)
        merged_values.append(merged_value)
    return merged_values

#queryset to handle cache, used by person, death and memorial

class CacheQuerySet(QuerySet):
    """This class extends the functionality of the queryset to include caching support. The
    pre-existing methods like filter, all, create etc. work as before. The new methods filter_cache,
    all_cache and get_cache return lists and are not chainable."""

    def _get_cache_key(self):
        return self.model._meta.verbose_name.title() #todo - get this from config file

    def _create_cache_queryset(self):
        "generates a base query"
        return super(CacheQuerySet, self).all()

    def _cache_queryset(self):
        """caches the base query"""
        # self.cache = Cache()
        # key = self._get_cache_key() #todo - get this from config file
        # print('key:'+key)
        # queryset = self.cache.get_queryset(key)
        # if queryset is None:
        #     #queryset has expired
        #     print('query set has expired')
        queryset = self._create_cache_queryset()
        #     self.cache.cache_queryset(key, queryset)
        # else:
        #     print('queryset fetched from cache')
        return queryset

    def all_cache(self):
        """Returns a list of all the objects in the cache."""
        return list(self._cache_queryset())

    def filter_cache(self, **kwargs):
        """Returns a list of objects that match the given parameters from the cache."""
        return [obj for obj in self.all_cache() if all(getattr(obj, key)==kwargs.get(key) for key in kwargs)]

    def get_cache(self, **kwargs):
        """Returns a single object based on the parameters passed. If the parameter match multiple objects, raises a
        MultipleObjectsReturned exception. If no objects match the parameters, raises an ObjectDoesNotExist exception."""
        result = self.filter_cache(**kwargs)
        if(len(result) is 1):
            return result[0]
        elif len(result) is 0:
            raise ObjectDoesNotExist("The object could not be found in the cache")
        else:
            raise MultipleObjectsReturned("The query returned {0} objects from the cache".format(len(result)))

    def clear_cache(self):
        """Removes the query from the cache"""
        self.cache.delete_key(self._get_cache_key())

class MarkerQuerySet(CacheQuerySet):
    """Queries common to both memorials and graveplots."""

    def get_from_uuid(self, uuid, marker_type=None):
        try:
            # import pdb; pdb.set_trace()
            markers = self.filter(uuid=uuid)
            if not markers.exists():
                markers = self.filter(memorialgraveplot__uuid=uuid)
            if marker_type:
                # (Pdb) markers[0].topopolygon.layer.feature_code.feature_type
                # Feature code related to memorial: 'lych_gate' or 'bench' needs to remove the 'memorials_' preceding added when created layerGeneratorService.createMemorialLayers
                tmp_arr = marker_type.split('memorials_')
                if len(tmp_arr) > 1:
                    marker_type = tmp_arr[1]
                markers = markers.filter(topopolygon__layer__feature_code__feature_type=marker_type)
            if markers.exists():
                    return markers.first()
            else:
                return None
        except:
            return None

    def get_from_ref_id(self, grave_ref_id):
        try:
            # import pdb; pdb.seet_trace()

            markers = self.filter(graveref_id=grave_ref_id)
            if markers.exists():
                return markers.first()
            else:
                return None
        except:
            return None

    def get_centrepoint_json_values(self):
        graveplot_queryset = self.filter(topopolygon__geometry__isnull=False).annotate(centrepoint=Centroid('topopolygon__geometry')).values('centrepoint', 'topopolygon__layer__feature_code__feature_type', 'uuid')
        rename_queryset_value(graveplot_queryset, {'uuid': 'id', 'topopolygon__layer__feature_code__feature_type':'marker_type'})
        for value in graveplot_queryset:
            value['id'] = str(value['id'])
            if value['centrepoint']:
                value['centrepoint'] = value['centrepoint'].coords
            else:
                value['centrepoint'] = None
        
        print("centrepoint finished\n\n\n")
        return graveplot_queryset

    def get_headpoint_json_values(self, plots_only=False):
        graveplot_queryset = self.annotate(centrepoint=Centroid('topopolygon__geometry')).filter(topopolygon__geometry__isnull=False).values('centrepoint', 'id')

        if plots_only:
            graveplot_queryset = graveplot_queryset.filter(topopolygon__layer__feature_code__feature_type='plot')

        for value in graveplot_queryset:
            try:
                value['id'] = str(value['id'])
                if value['centrepoint']:
                    value['centrepoint'] = value['centrepoint'].coords
                    value['marker_type'] = 'headpoint'
                else:
                    value['centrepoint'] = None
            except Exception as err:
                print(err)
        return graveplot_queryset


class MemorialQuerySet(MarkerQuerySet):
    """Used by the Angular View - to obtain a list of all memorials in the map, even
    those that don't have a person associated with them."""
    def _values_queryset(self):
        """DRY method to encapsulate the base values queryset"""
        queryset_headstone = super(CacheQuerySet, self).filter(headstone__isnull=False).annotate(head_point=Centroid('topopolygon__geometry')).values('head_point', 'topopolygon__layer__feature_code__feature_type', 'id')
        for item in queryset_headstone:
            item['topopolygon__layer__feature_code__feature_type'] = 'headpoint'
            item['id'] = str(item['id'])
        queryset_headstone = rename_queryset_value(queryset_headstone, {'topopolygon__layer__feature_code__feature_type': 'marker_type'})
        return queryset_headstone

    # TODO: DRY this out by moving to superclass
    def _create_cache_queryset(self):
        """Method extended from CacheQuerySet to store the returned value in cache."""
        values = self._values_queryset()
        return values

    def values_cache(self):
        """Returns a list of all the objects in the cache."""
        return self._cache_queryset()

    def delete_memorial_with_no_person(self, memorial_uuid, marker_type):
        #memorial = self.get_from_uuid(memorial_uuid, marker_type) #is this failing? 
        memorial = self.get_from_uuid(memorial_uuid)
        # import pdb; pdb.set_trace()
        if not memorial:
            raise ObjectDoesNotExist(' The memorial does not exist.')
        has_person = memorial.memorial_deaths.all().exists()
        if has_person:
            raise ObjectDoesNotExist(' A person is linked to the memorial.')
        try:
            if memorial.topopolygon:
                memorial.topopolygon.delete()
            else:
                memorial.delete()
        except Exception as e:
            print(e)
            raise ObjectDoesNotExist(' An unknown error occurred.')

    def get_memorials_features_id(self):
        memorials_queryset = self.filter(topopolygon__geometry__isnull=False).values('uuid', 'feature_id')
        for value in memorials_queryset:
            value['uuid'] = str(value['uuid'])
        return memorials_queryset


    def upload_photos_and_relate_memorial(self, csv_file , photos_files):
        #TODO: Validate names match the names of the csv file, it might change with additional columnd in the csv file

        temp_dir = get_and_clean_temp_dir(connection.schema_name)
        result = {'error': []}
        with open(temp_dir+'data.csv', 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        #Validate the memorials numbers exists and have a memorial related
        with open(temp_dir+'data.csv', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                memorial_number = row['memorial_number']
                if memorial_number:
                    filename = row['filename']
                    try:
                        memorialtmp = self.get(feature_id=memorial_number)
                    except ObjectDoesNotExist:
                        result['error'].append('The memorial number '+ memorial_number + ' does not have any memorial related. Please verify this number.')
                else:
                    result['error'].append('The memorial number is empty for image with filename "' + filename + '"')

        if len(result['error']) > 0:
            shutil.rmtree(temp_dir)
            return result
        else:
            #No Errors, then process memorials photos
            with open(temp_dir+'data.csv', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    memorial_number = row['memorial_number']
                    filename = row['filename']
                    memorialtmp = self.get(feature_id=memorial_number)
                    file_found = False
                            
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation]=='Orientation':
                            break
                    
                    for pos, photo_file in enumerate(photos_files):
                    
                        if filename.startswith('"') and filename.endswith('"'):
                            filename = filename[1:-1]
                        elif filename.startswith("'") and filename.endswith("'"):
                            filename = filename[1:-1]
                            
                        if photo_file.name.lower() == filename.lower():
                            file_found = True
                            resultVal = verify_contents(photo_file)
                            result['error'].append(resultVal) if resultVal != '' else ''
                            if len(result['error']) > 0:
                                shutil.rmtree(temp_dir)
                                return result
                            
                            # get image exif
                            image=Image.open(photo_file)
                            getExif = image._getexif()

                            if getExif:
                                exif=dict(getExif.items())
                                
                                modified = False
                                
                                if exif and orientation in exif:
                                    # rotate image if it needs rotated
                                    if exif[orientation] == 3:
                                        image=image.rotate(180, expand=True)
                                        modified = True
                                    elif exif[orientation] == 6:
                                        image=image.rotate(270, expand=True)
                                        modified = True
                                    elif exif[orientation] == 8:
                                        image=image.rotate(90, expand=True)
                                        modified = True
                                
                                if modified:
                                    # convert back to image that can be added to db
                                    image_io = io.BytesIO()
                                    image.save(image_io, format='JPEG')
                                    
                                    content_type = photo_file.content_type
                                    name = photo_file.name
                                    
                                    photo_file = ContentFile(image_io.getvalue())
                                    
                                    photo_file.content_type = content_type
                                    photo_file.name = name
                            
                            # photos_files.pop(pos) #Commented in order to allow same file to multiple memorials
                            #
                            memorialtmp.create_image(photo_file)
                            image.close()
                            break
                    if not file_found:
                        result['error'].append('The filename "' + filename + ' for memorial number '+ memorial_number + ' does not exist in the uploaded photos.')
                        break
                        
        shutil.rmtree(temp_dir)
        return result


class GraveplotQuerySet(MarkerQuerySet):
    """
    Query set graveplot specific
    """

    def graveplots_with_ref_exist(self):
        """
        Returns true if at least one graves with a grave ref exists.
        """

        graveplots = self.all()

        if graveplots.exists():

            if graveplots.filter(graveref__isnull=False).exists():
                return True
        
        return False

    def get_or_create_from_uuid(self, uuid, graveplot_polygon):
        graveplot = self.get_from_uuid(uuid)
        if not graveplot:
            graveplot = self.create(topopolygon=graveplot_polygon)
        return graveplot
    
    def get_graveplots_from_grave_ref(self, grave_number, section_id, subsection_id, ignoreIfNull, exact_grave_number=True):

        graveplots = self.select_related('graveref')

        if grave_number:
            if exact_grave_number:
                graveplots = graveplots.filter(graveref__grave_number__iexact=grave_number)
            else:
                graveplots = graveplots.filter(graveref__grave_number__icontains=grave_number)
        elif not ignoreIfNull:
            graveplots = graveplots.filter(graveref__grave_number__isnull=True)

        if section_id:
            graveplots = graveplots.filter(graveref__section=section_id)
        elif not ignoreIfNull:
            graveplots = graveplots.filter(graveref__section__isnull=True)

        if subsection_id:
            graveplots = graveplots.filter(graveref__subsection=subsection_id)
        elif not ignoreIfNull:
            graveplots = graveplots.filter(graveref__subsection__isnull=True)

        return graveplots

    def search_graveplots(self, grave_number, section_id, subsection_id, graveplot_layer, fuzzy_value, call_purpouse):
        
        # Get the results and required values
        # If fuzzy value is 100, get exact grave number
        graveplot_queryset = self.prefetch_related('topopolygon').get_graveplots_from_grave_ref(grave_number, section_id, subsection_id, True, fuzzy_value==100)

        if graveplot_layer:
            graveplot_queryset = graveplot_queryset.filter(topopolygon__layer__feature_code__feature_type=graveplot_layer)

        graveplot_queryset = graveplot_queryset.order_by('graveref__section__section_name', 'graveref__subsection__subsection_name', 'graveref__grave_number') \
        .values('uuid', 'topopolygon_id', 'topopolygon__layer__feature_code__feature_type', 'graveref__grave_number', 'graveref__section__section_name', 'graveref__subsection__subsection_name')
        
        # rename fields
        rename_queryset_value(graveplot_queryset, {'uuid': 'graveplot_uuid', 'topopolygon__layer__feature_code__feature_type': 'graveplot_layer', 'graveref__section__section_name': 'section_name', 'graveref__subsection__subsection_name': 'subsection_name'})
        if call_purpouse:
            for grave in graveplot_queryset:
                if grave['topopolygon_id']:
                    topopolygon = TopoPolygons.objects.get(id=grave['topopolygon_id'])
                    grave['topopolygon_centroid'] = topopolygon.geometry.centroid.coords
        return graveplot_queryset

class PersonManager(SoftDeletionManager):
    """Used by the Search Form - to obtain a list of persons matching search criteria in
    the map, even those that don't have a memorial associated with them."""

    def _values_queryset(self, search_type='burial', memorial_type=None):
        """DRY method to encapsulate the base values queryset"""

        values = ['id', 'first_names', 'last_name']

        if search_type=='burial':
            person_queryset = self.exclude(death=None).prefetch_related('death').order_by('id', 'death__death_burials__id', 'death__memorials__uuid').distinct('id', 'death__death_burials__id', 'death__memorials__uuid')
            values.extend(['death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__age_minutes', 'death__death_burials__burial_date', 'death__death_burials__id', 'death__death_burials__graveplot__uuid', 'death__memorials__uuid', 'death__memorials__topopolygon__layer__feature_code__feature_type'])

            if memorial_type:
                person_queryset = person_queryset.exclude(death__memorials=None).filter(death__memorials__topopolygon__layer__feature_code=memorial_type)

        elif search_type=='data_matching':
            person_queryset = self.exclude(death=None).prefetch_related('death').order_by('id').distinct('id')
            values.extend(['death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__age_minutes', 'death__death_burials__burial_date', 'death__memorials__id'])

            if memorial_type:
                person_queryset = person_queryset.exclude(death__memorials=None).filter(death__memorials__topopolygon__layer__feature_code=memorial_type)

        else:
            """ reservation """
            values.extend(['reservedplot__grave_plot__uuid', 'reservedplot__grave_plot__topopolygon_id', 'reservedplot__grave_plot__topopolygon__layer__feature_code__feature_type'])
            state=ReservePlotState.objects.get(state='reserved')
            person_queryset = self.exclude(reservedplot__isnull=True).filter(reservedplot__state=state).order_by('id').distinct('id')

        person_queryset = person_queryset.values(*values)
        return person_queryset

    def all_persons_values(self):
        """
        DRY method to encapsulate the base values queryset

        Note: this is VERY slow for large sites.
        """
        person_memorial = self.exclude(death=None).filter(death__memorials__uuid__isnull=False).order_by('id', 'death__memorials__uuid').values('id', 'first_names', 'other_names', 'last_name', 'death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__age_minutes', 'death__age_minutes', 'death__memorials__uuid', 'death__death_burials__burial_date').distinct('id', 'death__memorials__uuid')
        person_graveplot = self.exclude(death=None).filter(death__death_burials__graveplot__uuid__isnull=False).order_by('id', 'death__death_burials__graveplot__uuid').values('id', 'first_names', 'other_names', 'last_name', 'death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__age_minutes', 'death__death_burials__graveplot__uuid', 'death__death_burials__burial_date').distinct('id', 'death__death_burials__graveplot__uuid')
        person_no_memorial_graveplot = self.exclude(death=None).filter(death__death_burials__graveplot__uuid__isnull=True, death__memorials__uuid__isnull=True).order_by('id').values('id', 'first_names', 'other_names', 'last_name', 'death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__age_minutes', 'death__death_burials__graveplot__uuid', 'death__death_burials__burial_date').distinct('id')
        person_headpoints = None
        if self.exclude(death=None).filter(death__death_burials__graveplot__uuid__isnull=False).exists():
            person_headpoints = self.exclude(death=None).filter(death__death_burials__graveplot__uuid__isnull=False).order_by('id', 'death__death_burials__graveplot__id').values('id', 'first_names', 'other_names', 'last_name', 'death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__age_minutes', 'death__death_burials__graveplot__id', 'death__death_burials__burial_date').distinct('id', 'death__death_burials__graveplot__id')
            rename_queryset_value(person_headpoints, {'death__death_date': 'death_date', 'death__death_burials__burial_date': 'burial_date', 'death__age_years': 'age_years', 'death__age_months': 'age_months', 'death__age_weeks': 'age_weeks', 'death__age_days': 'age_days', 'death__age_hours': 'age_hours', 'death__age_minutes': 'age_minutes', 'death__death_burials__graveplot__id': 'memorial_id'})
        else:
            person_headpoints = self.exclude(death=None).filter(death__memorials__uuid__isnull=False).order_by('id', 'death__memorials__id').values('id', 'first_names', 'other_names', 'last_name', 'death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__age_minutes', 'death__memorials__id', 'death__death_burials__burial_date').distinct('id', 'death__memorials__id')
            rename_queryset_value(person_headpoints, {'death__death_date': 'death_date', 'death__death_burials__burial_date': 'burial_date', 'death__age_years': 'age_years', 'death__age_months': 'age_months', 'death__age_weeks': 'age_weeks', 'death__age_days': 'age_days', 'death__age_hours': 'age_hours', 'death__age_minutes': 'age_minutes', 'death__memorials__id': 'memorial_id'})
        rename_queryset_value(person_memorial, {'death__death_date': 'death_date', 'death__death_burials__burial_date': 'burial_date', 'death__age_years': 'age_years', 'death__age_months': 'age_months', 'death__age_weeks': 'age_weeks', 'death__age_days': 'age_days', 'death__age_hours': 'age_hours', 'death__age_minutes': 'age_minutes', 'death__memorials__uuid': 'memorial_id'})
        rename_queryset_value(person_graveplot, {'death__death_date': 'death_date', 'death__death_burials__burial_date': 'burial_date', 'death__age_years': 'age_years', 'death__age_months': 'age_months', 'death__age_weeks': 'age_weeks', 'death__age_days': 'age_days', 'death__age_hours': 'age_hours', 'death__age_minutes': 'age_minutes', 'death__death_burials__graveplot__uuid': 'memorial_id'})
        rename_queryset_value(person_no_memorial_graveplot, {'death__death_date': 'death_date', 'death__death_burials__burial_date': 'burial_date', 'death__age_years': 'age_years', 'death__age_months': 'age_months', 'death__age_weeks': 'age_weeks', 'death__age_days': 'age_days', 'death__age_hours': 'age_hours', 'death__age_minutes': 'age_minutes', 'death__death_burials__graveplot__uuid': 'memorial_id'})
        values = list(itertools.chain(person_memorial,person_graveplot,person_no_memorial_graveplot,person_headpoints))
        for value in values:
            value['memorial_id'] = str(value['memorial_id'])
            value['id'] = str(value['id'])
        return values

    # This returns each Person with a memorial_id, graveplot_id & headpoint_id
    # rather than the person having seperate JSON objects for each ID type
    # def all_persons_values(self):
    #     """DRY method to encapsulate the base values queryset"""
    #     person = None
    #     if self.exclude(death=None).filter(death__death_burials__graveplot__uuid__isnull=False).exists():
    #         person = self.exclude(death=None).values('id', 'first_names', 'other_names', 'last_name', 'death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__memorials__uuid', 'death__death_burials__burial_date', 'death__death_burials__graveplot__uuid', 'death__death_burials__graveplot__id').distinct('id')
    #         rename_queryset_value(person, {'death__death_date': 'death_date', 'death__death_burials__burial_date': 'burial_date', 'death__age_years': 'age_years', 'death__age_months': 'age_months', 'death__age_weeks': 'age_weeks', 'death__age_days': 'age_days', 'death__age_hours': 'age_hours', 'death__memorials__uuid': 'memorial_id', 'death__death_burials__graveplot__uuid': 'graveplot_id', 'death__death_burials__graveplot__id': 'headpoint_id'})
    #     else:
    #         person = self.exclude(death=None).values('id', 'first_names', 'other_names', 'last_name', 'death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__memorials__uuid', 'death__death_burials__burial_date', 'death__death_burials__graveplot__uuid', 'death__memorials__id').distinct('id')
    #         rename_queryset_value(person, {'death__death_date': 'death_date', 'death__death_burials__burial_date': 'burial_date', 'death__age_years': 'age_years', 'death__age_months': 'age_months', 'death__age_weeks': 'age_weeks', 'death__age_days': 'age_days', 'death__age_hours': 'age_hours', 'death__memorials__uuid': 'memorial_id', 'death__death_burials__graveplot__uuid': 'graveplot_id', 'death__memorials__id': 'headpoint_id'})
    #     values = list(person)
    #     for value in values:
    #         value['id'] = str(value['id'])
    #         value['memorial_id'] = str(value['memorial_id'])
    #         value['graveplot_id'] = str(value['graveplot_id'])
    #         value['headpoint_id'] = str(value['headpoint_id'])
    #     return values

    def persons_by_memorial_id_values(self, memorial_id_array):
        """DRY method to encapsulate the base values queryset"""
        person_memorial = self.exclude(death=None).select_related("death__death_burials").filter(death__memorials__uuid__isnull=False, death__memorials__uuid__in=memorial_id_array).order_by('id', 'death__memorials__uuid').values('id', 'first_names', 'other_names', 'last_name', 'death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__age_minutes', 'death__memorials__uuid', 'death__death_burials__burial_date', 'death__death_burials__impossible_date_month').distinct('id', 'death__memorials__uuid')
        person_graveplot = self.exclude(death=None).select_related("death__death_burials").filter(death__death_burials__graveplot__uuid__isnull=False, death__death_burials__graveplot__uuid__in=memorial_id_array).order_by('id', 'death__death_burials__graveplot__uuid').values('id', 'first_names', 'other_names', 'last_name', 'death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__age_minutes', 'death__death_burials__graveplot__uuid', 'death__death_burials__burial_date', 'death__death_burials__impossible_date_month').distinct('id', 'death__death_burials__graveplot__uuid')
        rename_queryset_value(person_memorial, {'death__death_date': 'death_date', 'death__death_burials__burial_date': 'burial_date', 'death__age_years': 'age_years', 'death__age_months': 'age_months', 'death__age_weeks': 'age_weeks', 'death__age_days': 'age_days', 'death__age_hours': 'age_hours', 'death__age_minutes': 'age_minutes', 'death__memorials__uuid': 'memorial_id', 'death__death_burials__impossible_date_month': 'impossible_date_month'})
        rename_queryset_value(person_graveplot, {'death__death_date': 'death_date', 'death__death_burials__burial_date': 'burial_date', 'death__age_years': 'age_years', 'death__age_months': 'age_months', 'death__age_weeks': 'age_weeks', 'death__age_days': 'age_days', 'death__age_hours': 'age_hours', 'death__age_minutes': 'age_minutes', 'death__death_burials__graveplot__uuid': 'memorial_id', 'death__death_burials__impossible_date_month': 'impossible_date_month'})
        values = list(itertools.chain(person_memorial,person_graveplot))
        for value in values:
            value['memorial_id'] = str(value['memorial_id'])
            value['id'] = str(value['id'])
        return values
    
    def persons_by_id_values(self, person_id_array):
        """DRY method to encapsulate the base values queryset"""
        person_memorial = self.exclude(death=None).filter(death__memorials__uuid__isnull=False, id__isnull=False, id__in=person_id_array).order_by('id', 'death__memorials__uuid').values('id', 'first_names', 'other_names', 'last_name', 'death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__age_minutes', 'death__memorials__uuid', 'death__death_burials__burial_date').distinct('id', 'death__memorials__uuid')
        person_graveplot = self.exclude(death=None).filter(death__death_burials__graveplot__uuid__isnull=False, id__isnull=False, id__in=person_id_array).order_by('id', 'death__death_burials__graveplot__uuid').values('id', 'first_names', 'other_names', 'last_name', 'death__death_date', 'death__age_years', 'death__age_months', 'death__age_weeks', 'death__age_days', 'death__age_hours', 'death__age_minutes', 'death__death_burials__graveplot__uuid', 'death__death_burials__burial_date').distinct('id', 'death__death_burials__graveplot__uuid')
        rename_queryset_value(person_memorial, {'death__death_date': 'death_date', 'death__death_burials__burial_date': 'burial_date', 'death__age_years': 'age_years', 'death__age_months': 'age_months', 'death__age_weeks': 'age_weeks', 'death__age_days': 'age_days', 'death__age_hours': 'age_hours', 'death__age_minutes': 'age_minutes', 'death__memorials__uuid': 'memorial_id'})
        rename_queryset_value(person_graveplot, {'death__death_date': 'death_date', 'death__death_burials__burial_date': 'burial_date', 'death__age_years': 'age_years', 'death__age_months': 'age_months', 'death__age_weeks': 'age_weeks', 'death__age_days': 'age_days', 'death__age_hours': 'age_hours', 'death__age_minutes': 'age_minutes', 'death__death_burials__graveplot__uuid': 'memorial_id'})
        values = list(itertools.chain(person_memorial,person_graveplot))
        for value in values:
            value['memorial_id'] = str(value['memorial_id'])
            value['id'] = str(value['id'])
        return values

    def _rename_values(self, values):
        """DRY method to rename the values returned by the _values_queryset so that
        the queryset is transparent to view, whether it is returned by Person, Death or Memorial"""
        for person in values:
            # print(type(person))
            # print(person)
            death_date = person.pop('death__death_date')
            if(death_date is not None):
                death_date = death_date.strftime('%d %b %Y')
            person['death_date'] = death_date
            burial_date = person.pop('death__death_burials__burial_date')
            if(burial_date is not None):
                burial_date = burial_date.strftime('%d %b %Y')
            person['burial_date'] = burial_date
            person['age_years'] = person.pop('death__age_years')
            person['age_months'] = person.pop('death__age_months')
            person['age_weeks'] = person.pop('death__age_weeks')
            person['age_days'] = person.pop('death__age_days')
            person['age_hours'] = person.pop('death__age_hours')
            person['age_minutes'] = person.pop('death__age_minutes')
            person['memorial_id'] = person.pop('death__memorials__id')
        return values

    def values_cache(self):
        """Returns a list of all the objects in the cache."""
        return self._cache_queryset()

    def _filter_by_graveplot(self, queryset, graveplot_grave_number, search_type='burial'):
        """DRY method to filter by graveplot"""
        if search_type=='reservation':
            return queryset.exclude(reservedplot__isnull=True).filter(reservedplot__grave_plot__graveref__grave_number__iexact=graveplot_grave_number)
        else:
            return queryset.exclude(death=None).filter(death__death_burials__graveplot__graveref__grave_number__iexact=graveplot_grave_number)

    def _filter_by_section(self, queryset, section_id, search_type='burial'):
        """DRY method to filter by section"""
        if search_type=='reservation':
            return queryset.exclude(reservedplot__isnull=True).filter(reservedplot__grave_plot__graveref__section__id=section_id)
        else:
            return queryset.exclude(death=None).filter(death__death_burials__graveplot__graveref__section__id=section_id)

    def _filter_by_subsection(self, queryset, subsection_id, search_type='burial'):
        """DRY method to filter by subsection"""
        if search_type=='reservation':
            return queryset.exclude(reservedplot__isnull=True).filter(reservedplot__grave_plot__graveref__subsection__id=subsection_id)
        else:
            return queryset.exclude(death=None).filter(death__death_burials__graveplot__graveref__subsection__id=subsection_id)

    def _filter_by_featureid(self, queryset, feature_id):
        """DRY method to filter by subsection"""
        return queryset.filter(Q(death__death_burials__graveplot__feature_id=feature_id) | Q(death__memorials__feature_id=feature_id))

    def _filter_by_death_date(self, queryset, date_start, date_end):
        """DRY method to filter by death date range"""
        return queryset.filter(death__death_date__range=[date_start, date_end])

    def _filter_by_burial_date(self, queryset, date_start, date_end):
        """DRY method to filter by burial date range"""
        return queryset.filter(death__death_burials__burial_date__range=[date_start, date_end])

    def _filter_by_age(self, queryset, age_start, age_end):
        """DRY method to filter by age range"""
        return queryset.filter(death__age_years__range=[age_start, age_end])

    """ search_type argument can be 'burial' or 'reservation'. Default is 'burial' """
    def search_persons(self, age=None, age_to=None, death_date=None, death_date_to=None,
        burial_date=None, burial_date_to=None, first_names=None, last_name=None, fuzzy_value=None, memorial_type=None, 
        graveplot_grave_number=None, section_id=None, subsection_id=None, feature_id=None, search_type='burial'):
        """Returns a list for all person who match the search parameters"""

        if ((age is None) and (death_date is None) and (burial_date is None) and (not first_names) and (not last_name) 
        and (not memorial_type) and (not graveplot_grave_number) and (not section_id) and (not subsection_id) and (not feature_id)):
            # if nothing to search for, raise error
            raise ObjectDoesNotExist("Search parameters are null")

        result = self._values_queryset(search_type, memorial_type)

        if(graveplot_grave_number is not None):
            result = self._filter_by_graveplot(result, graveplot_grave_number, search_type)
        if(section_id is not None):
            result = self._filter_by_section(result, section_id, search_type)
        if(subsection_id is not None):
            result = self._filter_by_subsection(result, subsection_id, search_type)
        
        if (feature_id is not None):
            result = self._filter_by_featureid(result, feature_id)

        if(age is not None):
            if(age_to is None):
                age_to = age
            result = self._filter_by_age(result, age, age_to)
        if(death_date is not None):
            if(death_date_to is None):
                death_date_to = death_date
            result = self._filter_by_death_date(result, death_date, death_date_to)
        if(burial_date is not None):
            if(burial_date_to is None):
                burial_date_to = burial_date
            result = self._filter_by_burial_date(result, burial_date, burial_date_to)
        if((first_names or last_name)):
            # key_list should contain distinct fields
            key_list = []
            if search_type=='burial':
                key_list = ['id', 'death__death_burials__id', 'death__memorials__uuid']
            else:
                key_list = ['id']
            result = fuzzy_search_fullname(first_names, last_name, result, fuzzy_value, key_list)

        rename_queryset_value(result, {
            'death__death_date': 'death_date', 'death__death_burials__burial_date': 'burial_date', 'death__age_years': 'age_years', 
            'death__age_months': 'age_months', 'death__age_weeks': 'age_weeks', 'death__age_days': 'age_days', 
            'death__age_hours': 'age_hours', 'death__age_minutes': 'age_minutes', 'death__memorials__id':'first_memorial_id', 'death__memorials__uuid':'memorial_uuid', 'death__death_burials__id':'first_burial_id', 'death__death_burials__graveplot__uuid':'graveplot_uuid', 'death__memorials__topopolygon__layer__feature_code__feature_type':'memorial_layer', 'reservedplot__grave_plot__uuid': 'graveplot_uuid', 'reservedplot__grave_plot__topopolygon__layer__feature_code__feature_type':'graveplot_layer', 'reservedplot__grave_plot__topopolygon_id':'topopolygon_id' })
        for value in result:
            value['id'] = str(value['id'])
            if value['last_name']: value['last_name'] = value['last_name'].upper()

            if search_type=='burial' or search_type=='data_matching':
                if value['death_date']: value['death_date'] = str(value['death_date'])
                if value['burial_date']: value['burial_date'] = str(value['burial_date'])

                if search_type=='data_matching':
                    if value['first_memorial_id']: value['first_memorial_id'] = str(value['first_memorial_id'])

                if search_type=='burial':
                    if value['memorial_uuid']: value['memorial_uuid'] = str(value['memorial_uuid'])
                    if value['graveplot_uuid']: value['graveplot_uuid'] = str(value['graveplot_uuid'])
                    if value['first_burial_id']: value['first_burial_id'] = str(value['first_burial_id'])
        return result


class TenantSiteManager(models.Manager):
    def get_queryset(self):
        return super(TenantSiteManager, self).get_queryset().filter(site_groups__burialgroundsite__schema_name__exact=connection.schema_name).distinct()

class BurialOfficialQuerySet(QuerySet):
    def get_all(self):
        bolist = []
        qob = self.extra(select={'date_is_null': 'used_on IS NULL'},order_by=['date_is_null','-used_on'])
        count = 1
        for bo in qob[:3]:
            bolist.append({'optgroup':'top', 'id':str(bo.id), 'score':0, 'label': '{0}, {1} ({2})'.format(bo.last_name,bo.first_names, bo.title)})
        # qobob = qob[3:].sort(key = lambda x: x.official.last_name)
        qobob = self.order_by('last_name')
        for bo in qobob:
            # import pdb; pdb.set_trace()
            last_name_temp = bo.last_name
            if last_name_temp and last_name_temp[0].isalpha():
                bolist.append({'id':str(bo.id), 'score':count, 'label': '{0}, {1} ({2})'.format(bo.last_name,bo.first_names, bo.title)})
                count = count + 1
            else:
                bolist.append({'id':str(bo.id), 'score':999, 'label': '{0}, {1} ({2})'.format(bo.last_name,bo.first_names, bo.title)})
        # import pdb; pdb.set_trace()
        return bolist


# class BurialQuerySet(QuerySet):
#     def _format_address(self, firstline, town, county, postcode):
#         addr = ''
#         if firstline:
#             addr+=firstline+' '
#         if town:
#             addr+=town+' '
#         if county:
#             addr+=county+' '
#         if postcode:
#             addr+=postcode+' '
#         return addr
#
#     def get_person_death_burial_values(self, burial_record_image):
#         burials = []
#         if burial_record_image:
#             burials = self.filter(burial_record_image=burial_record_image). \
#                         order_by('burial_number').values('death__person_id',
#                             'death__person__title', 'death__person__first_names', 'death__person__other_names',\
#                             'death__person__birth_name', 'death__person__last_name',\
#                             'death__person__impossible_date_day', 'death__person__impossible_date_month',\
#                             'death__person__impossible_date_year', 'death__person__gender',\
#                             'death__person__description', 'death__person__profession__profession',\
#                             'death__person__residence_address__first_line', 'death__person__residence_address__town',\
#                             'death__person__residence_address__county', 'death__person__residence_address__postcode',\
#
#                             'death__event__name', 'death__event__description',\
#                             'death__address__first_line', 'death__address__town',\
#                             'death__address__county', 'death__address__postcode',\
#                             'death__age_years', 'death__age_months',\
#                             'death__age_weeks', 'death__age_days', 'death__age_hours', \
#                             'death__parish__parish', 'death__religion__religion',\
#                             'death__impossible_date_day', 'death__impossible_date_month',\
#                             'death__impossible_date_year', 'death__death_cause',\
#
#                             'burial_official__official_type', 'burial_official__official__title',
#                             'burial_official__official__first_names', 'burial_official__official__last_name',\
#                             'burial_official__official__id', \
#
#                             'burial_number', 'impossible_date_day', \
#                             'impossible_date_month', 'impossible_date_year', \
#                             'consecrated', 'cremation_certificate_no', \
#                             'interred', 'depth', 'depth_units', 'burial_remarks', \
#                             'requires_investigation', 'user_remarks', \
#                             'situation','grave_number','place_from_which_brought')
#             for burial in burials:
#                 burial['death__person_id'] = str(burial['death__person_id'])
#         return list(merge_values(values=burials, id_field='death__person_id', many_to_many_model_field='burial_official'))


class TagQuerySet(QuerySet):
    def tag_values_from_image(self, image):
        return self.filter(image=image).annotate(envelope=Envelope('top_left_bottom_right')).values('id', 'image__id', 'person__id', 'envelope', 'person__deleted_at')

class ReservedPlotQuerySet(QuerySet):

    def all_reserved_persons_values(self):
        person_queryset = self.filter(state__state='reserved').values('person_id', 'person__first_names', 'person__other_names', 'person__last_name', 'grave_plot__uuid', 'grave_plot_id', 'origin__feature_type')
        return person_queryset

    def get_details_by_person_id(self, person_id):
        person_reserved = self.filter(person_id=person_id)
        if person_reserved.exists():
            person_details = person_reserved[0].person.get_all_details()
            reserved_plot_details = person_reserved.values('notes')[0]
            #combine both details
            person_reserved_details = person_details.copy()
            person_reserved_details.update(reserved_plot_details)
            return person_reserved_details
        else:
            return {}


class IsNull(Func):
    template = '%(expressions)s IS NULL'

class ProfessionManager(models.Manager):
    def ordered_list(self):
        return list(self.all().values('id', 'profession').annotate(profession_null=IsNull('profession')).order_by('-profession_null', 'profession'))

class EventManager(models.Manager):
    def ordered_list(self):
        return list(self.all().values('id', 'name', 'description').annotate(event_null=IsNull('name')).order_by('-event_null', 'name'))

class ParishManager(models.Manager):
    def ordered_list(self):
        return list(self.all().values('id', 'parish').annotate(parish_null=IsNull('parish')).order_by('-parish_null', 'parish'))

class ReligionManager(models.Manager):
    def ordered_list(self):
        return list(self.all().values('id', 'religion').annotate(religion_null=IsNull('religion')).order_by('-religion_null', 'religion'))

class GraveRefManager(models.Manager):

    def get_or_create_custom(self, grave_number, section, subsection):
        """
        Get or create, but takes into account grave refs without a grave_number.
        In these cases we'll have different graveref records containing the same data.
        """

        grave_ref = None

        if grave_number == '':
            grave_number = None

        if grave_number or section:
            if not grave_number:
                grave_ref_no_grave_number = self.filter(grave_number=None, section=section, subsection=subsection)

                if grave_ref_no_grave_number.exists() and hasattr(grave_ref_no_grave_number[0], 'graveref_graveplot'):
                    # if grave ref exists and is assigned to a graveplot already, create a new one
                    grave_ref = self.create(grave_number=None, section=section, subsection=subsection)
            
            if not grave_ref:
                grave_ref = self.get_or_create(grave_number=grave_number, section=section, subsection=subsection)[0]
        
        return grave_ref