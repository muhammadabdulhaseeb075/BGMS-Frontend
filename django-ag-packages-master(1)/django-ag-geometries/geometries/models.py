from django.db import models
from django.db.models import Q, Prefetch
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models as geodjango_models
from django.contrib.gis.db.models.functions import Perimeter, Centroid, Area
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.contrib.postgres.fields import JSONField, ArrayField
import json
json.encoder.FLOAT_REPR = lambda o: format(o, '.2f')
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models.aggregates import Max
from math import sqrt
from geometries.managers import LayerQuerySet
from geometries.utils import getGeojson
from geometriespublic import models as main_models
from geometriespublic.models import FeatureCode, FeatureGroup, FieldType, PublicAttribute
import datetime
import uuid

class Attribute(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    feature_codes = models.ManyToManyField(FeatureCode, related_name='attributes')
    type = models.ForeignKey(FieldType, on_delete=models.CASCADE, limit_choices_to={'attributes': True})
    options = ArrayField(base_field=models.CharField(max_length=50), null=True, blank=True, verbose_name="Options (for 'Select' type only)")
    feature_attributes = GenericRelation('geometries.FeatureAttributes', related_query_name='schema_attribute')

    def __str__(self):
        return self.name.title()

class Layer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    feature_code = models.ForeignKey(FeatureCode, null=True, on_delete=models.CASCADE)
    feature_code_idfk = models.IntegerField(null=True)
    display_name = models.CharField(max_length=20)
    show_in_toolbar = models.BooleanField()
    initial_visibility = models.BooleanField(default=False)
    min_resolution = models.FloatField()
    max_resolution = models.FloatField()
    objects = LayerQuerySet.as_manager()

    def __str__(self):
          return "%s" % (self.display_name)

    class Meta:
            ordering = ['display_name']

    def get_layer_geojson_cache(self, auto_update):
        """
        Returns a cache (if it exists) of the geojson data for this layer, ready to be uploaded to OpenLayers.
        """
        try:
            layer_cache_query_set = self.layer_cache.get(auto_update=auto_update)
            if layer_cache_query_set.cache:
                return layer_cache_query_set.cache
            else:
                raise ObjectDoesNotExist()
        except:
            return False
    
    def remove_layer_geojson_cache(self):
        """
        Removes a cache of the geojson data for this layer (if it exists).
        """
        cache = LayerCache.objects.filter(layer=self)

        if cache.exists():
            cache.delete()
    
    def update_layer_geojson_cache(self, geoj, auto_update):
        """
        Updates/creates a cache of the geojson data for this layer.

        Note: it's possible to have two caches for the same layer. This is because some layers 
        are in both memorials group and another group. The groups will have different serializers, 
        hence the need for two caches.
        Memorial layer will be auto_update=False, non-Memorial layer will be auto_update=True.
        """
        cache,created = LayerCache.objects.get_or_create(layer=self, auto_update=auto_update)
        cache.cache = geoj
        cache.save()
    
    def update_feature_in_layer_geojson_cache(self, feature_id, geoj, auto_update, **kwargs):

        created = kwargs.get('created', False)
        deleted = kwargs.get('deleted', False)

        cache = None
        
        try:
            cache = LayerCache.objects.get(layer=self, auto_update=auto_update)

            features = cache.cache['features']

            if created:
                # this is a new record
                features.append(geoj)

            else:
                found = False

                for feature in [x for x in features if x['id'] == str(feature_id)]:
                    if deleted:
                        features.remove(feature)
                    else:
                        feature.update(geoj)
                    found = True
                
                if not found:
                    # If not found then this feature has probably changed layer.
                    # Look in layer cache and remove before adding to new layer.
                    whole_cache = LayerCache.objects.exclude(layer=self)

                    for layer_cache in whole_cache:
                        layer_cache_features = layer_cache.cache['features']
                        for feature in [x for x in layer_cache_features if x['id'] == str(feature_id)]:
                            # remove from old layer cache
                            layer_cache_features.remove(feature)
                            layer_cache.cache['features'] = layer_cache_features
                            layer_cache.save()
                            found = True
                            break
                        
                        if found:
                            break
                    
                    # add to new layer cache
                    features.append(geoj)

            cache.save()

        except:
            if cache:
                # if cache does exist but an error occured, wipe the cache, it will be recreated on next refresh
                cache.delete()
            else:
                # pass over if cache doesn't exist
                pass


class FeatureManager(models.Manager):
    def get_layer(self, layerName):
        return self.filter(layer__feature_code__feature_type__iexact=layerName).annotate(marker_type=Max('layer__feature_code__feature_type')).values("id", "marker_type", "geometry")

    def delete_feature(self, pk, layerName):
        self.get(id=pk, layer__feature_code=main_models.FeatureCode.objects.get(feature_type=layerName)).delete()

    def get_or_create_from_geojson(self, feature_geojson):
        """
        This function is now misnamed, should be called something along the lines of
        get_from_id_or_create_from_geojson
        """
        #TODO: make plot availability attribute of existing object rather than new feature
        feature_dict = json.loads(feature_geojson)
        feature_type = feature_dict["properties"]["marker_type"]
        feature_code = main_models.FeatureCode.objects.get(feature_type=feature_type)
        # layer = Layer.objects.get(feature_code=feature_code)
        layer, created = Layer.objects.get_or_create(
            feature_code=feature_code,
            defaults={'display_name':feature_code.display_name,
                    'show_in_toolbar':feature_code.show_in_toolbar,
                    'initial_visibility':feature_code.feature_groups.first().initial_visibility})
        geometry = None
        geometry_geojson = getGeojson(feature_geojson)
        if (feature_dict["geometry"]['type'].lower() == 'polygon'):
            plot_polygon = GEOSGeometry(geometry_geojson, srid=27700)
            geometry = MultiPolygon([plot_polygon])
        else:
            geometry = GEOSGeometry(geometry_geojson, srid=27700)

        try:
            # Get feature by ID
            created_feature = self.get(id=feature_dict["id"])
            created_feature = (created_feature, False) # response needs to be a tuple
        except:
            # Create feature if ID doesn't exist
            created_feature = self.get_or_create(id=feature_dict["id"], geometry=geometry, layer=layer,
                                                 defaults={'feature_id': "0", 'user_created': True})

        # import pdb; pdb.set_trace()
        return created_feature

    def get_layer_label(self, layerName, include_centre_spread=False, topopoint=False):
        label_attribute = PublicAttribute.objects.get(name__iexact='LABEL')

        features = self.filter(layer__feature_code__feature_type__iexact=layerName).annotate(marker_type=Max('layer__feature_code__feature_type'))

        if include_centre_spread:
            features = features.annotate(perimeter=Perimeter('geometry')).annotate(area=Area('geometry')).annotate(centroid=Centroid('geometry'))
        
        features = features.prefetch_related(Prefetch('feature_attributes', queryset=FeatureAttributes.objects.filter(public_attribute=label_attribute), to_attr='label_feature_attributes'))

        return_features = []

        for feature in features:
            return_feature = {}
            return_feature['id'] = feature.id
            return_feature['marker_type'] = feature.marker_type
            return_feature['geometry'] = feature.geometry

            if topopoint:
                return_feature['veg_spread'] = feature.veg_spread

            if include_centre_spread:
                radius_perimeter = (feature.perimeter.m)/2/3.14
                radius_area = sqrt((feature.area.sq_m)/3.14)
                if(abs(radius_area-radius_perimeter)<0.05):
                    return_feature['veg_spread'] = radius_perimeter
                    return_feature['geometry'] = feature.centroid

            if feature.label_feature_attributes:
                return_feature['label'] = feature.label_feature_attributes[0].char_value
            else:
                return_feature['label'] = None

            return_features.append(return_feature)
        return return_features
    

class Raster(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    url = models.CharField(max_length=200)


class FeatureAttributes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={ Q(app_label='geometriespublic', model='publicattribute') | Q(app_label='geometries', model='attribute') })
    object_id = models.UUIDField()
    attribute = GenericForeignKey('content_type', 'object_id')
    """Attribute - can link to attribute models in publicgeometries or geometries"""
    char_value = models.CharField(max_length=255, null=True, blank=True)
    integer_value = models.IntegerField(null=True, blank=True)
    float_value = models.FloatField(null=True, blank=True)
    boolean_value = models.NullBooleanField()
    date_value = models.DateField(null=True)
    textarea_value = models.CharField(max_length=400, null=True, blank=True)


class Feature(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    feature_id = models.CharField(max_length=10)
    surveyor = models.ForeignKey(main_models.Surveyor, null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=25, null=True, blank=True)
    created_date = models.DateField(null=True)
    last_edit_by = models.CharField(max_length=25, null=True, blank=True)
    last_edit_date = models.DateField(null=True)
    date_uploaded = models.DateField(null=True, default=timezone.now)
    map_accura = models.NullBooleanField()
    geom_acc = models.FloatField(null=True, blank=True)
    source_id = models.CharField(max_length=25, null=True, blank=True)
    user_created = models.BooleanField(default=False)
    feature_attributes = models.ManyToManyField(FeatureAttributes, blank=True)

    def __str__(self):
        return "feature id: %s" % (self.feature_id)

    class Meta:
        abstract = True

    def delete_feature(self, feature_type):
        if self.layer.feature_code.feature_type==feature_type:
            return self.delete()
        else:
            raise ObjectDoesNotExist('Feature not found')

    def update_feature_code(self, feature_type):
        feature_code = FeatureCode.objects.get(feature_type=feature_type)
        layer, created = Layer.objects.get_or_create(
            feature_code=feature_code,
            defaults={
                'display_name': feature_code.display_name,
                'show_in_toolbar': feature_code.show_in_toolbar,
                'initial_visibility': feature_code.feature_groups.first().initial_visibility
            }
        )
        self.layer = layer
        self.save()

    def add_or_update_attribute(self, attr_name, attr_value, attr_type='char'):
        '''check if attribute already exist, if so it updates value for current attribute, otherwise creates a new one'''

        try:
            attr_type_record = FieldType.objects.get(name=attr_type)
        except:
            raise ObjectDoesNotExist('Attribute type does not exist')

        try:
            public_attribute = PublicAttribute.objects.get(name__iexact=attr_name)

            if public_attribute.type!=attr_type_record:
                raise ObjectDoesNotExist('Attribute found but it is of a different type')
        except:
            public_attribute = PublicAttribute.objects.create(name=attr_name, type=attr_type_record)
        
        public_attribute.feature_codes.add(self.layer.feature_code)

        feature_attrs = self.feature_attributes.all()
        feature_attribute = None
        create_attr = True
        for feature_attr in feature_attrs:
            if feature_attr.public_attribute == public_attribute:
                feature_attribute = feature_attr
                create_attr = False
                break

        if create_attr:
            feature_attribute = FeatureAttributes.objects.create(attribute=public_attribute)
            self.feature_attributes.add(feature_attribute)

        setattr(feature_attribute, attr_type + '_value', attr_value)
        feature_attribute.save()


    def addShapeFileAttributes(self, ogr_feature):
        '''Create or update common attributes for Polygons, Lines, Points from Shapefile
        '''

        if ogr_feature.get('created_us'):
            self.created_by = ogr_feature.get('created_us')
        if ogr_feature.get('created_da'):
            self.created_date = ogr_feature.get('created_da')
        if ogr_feature.get('last_edite'):
            self.last_edit_by = ogr_feature.get('last_edite')
        if ogr_feature.get('last_edi_1'):
            self.last_edit_date = ogr_feature.get('last_edi_1')
        if ogr_feature.get('MAP_ACCURA'):
            self.map_accura = ogr_feature.get('MAP_ACCURA').lower() in ['yes', 'y', 'true']
        if ogr_feature.get('SOURCE_ID'):
            self.last_edit_by = ogr_feature.get('SOURCE_ID')
        if ogr_feature.get('LABEL'):
            self.add_or_update_attribute('LABEL', ogr_feature.get('LABEL'), 'char')
        
        self.save()

    def update_layer_cache(self, created):
        """
        Use after updating feature to update cache. Called from signal
        """
        geoj = self.get_geojson()

        self.layer.update_feature_in_layer_geojson_cache(self.id, geoj, True, created=created)


class TopoPolygons(Feature):
    geometry = geodjango_models.MultiPolygonField(srid=27700)
    objects = FeatureManager()

    def update_geometry(self, geometryGeoJSON):
        geometry_type = json.loads(geometryGeoJSON)['type']
        if (geometry_type.lower() == 'polygon'):
            plot_polygon = GEOSGeometry(geometryGeoJSON, srid=27700)
            multipolygon_plot = MultiPolygon([plot_polygon])
            self.geometry = multipolygon_plot
        elif (geometry_type.lower() == 'multipolygon'):
            self.geometry = GEOSGeometry(geometryGeoJSON, srid=27700)
        self.user_created = True
        self.save()

    def get_centre(self):
        return self.geometry.centroid
    
    class Meta:
            verbose_name = "TopoPolygon"
            verbose_name_plural = "TopoPolygons"

    def get_geojson(self):
        """
        Returns topopolygon geojson
        """
        serializer = TopoPolygonGeoSerializer(self)
        return serializer.data


class TopoPolylines(Feature):
    width = models.FloatField(null=True)
    geometry = geodjango_models.MultiLineStringField(srid=27700)
    objects = FeatureManager()

    class Meta:
            verbose_name = "TopoPolyline"
            verbose_name_plural = "TopoPolylines"

    def get_geojson(self):
        """
        Returns topopolyline geojson
        """
        serializer = TopoPolylineGeoSerializer(self)
        return serializer.data


class TopoPointsManager(FeatureManager):
    def get_layer(self, layerName):
        return self.filter(layer__feature_code__feature_type__iexact=layerName).annotate(marker_type=Max('layer__feature_code__feature_type')).values("id", "marker_type", "geometry", "veg_spread")

class TopoPoints(Feature):
    veg_spread = models.FloatField(null=True)
    geometry = geodjango_models.PointField(srid=27700)
    objects = TopoPointsManager()

    class Meta:
            verbose_name = "TopoPoint"
            verbose_name_plural = "TopoPoints"

    def get_geojson(self):
        """
        Returns topopoint geojson
        """
        serializer = TopoPointGeoSerializer(self)
        return serializer.data

class LayerCache(models.Model):
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE, related_name="layer_cache")
    cache = JSONField(null=True)
    auto_update = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together=('layer','auto_update')

from geometries.serializers import TopoPolygonGeoSerializer, TopoPolylineGeoSerializer, TopoPointGeoSerializer