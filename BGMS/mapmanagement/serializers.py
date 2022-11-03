from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from django.contrib.gis.geos import MultiPolygon
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
import uuid
from datetime import datetime, date

from bgsite.models import Memorial, MemorialInscriptionDetail, Inspection, Image, MemorialGraveplot, GravePlot, Section, Subsection, Burial, Death, Address, Person, Burial_Official, BurialOfficialType, Official, GraveDeed, GraveOwner, ReservePlotState, Marker, OwnerStatus, GraveRef
from bgsite.common_apis.serializers import get_owner_display_name, GraveOwnersListSerializer, ImageSerializer
from main.models import Address as PublicAddress, Company as PublicCompany, BurialGroundSite
from geometriespublic.models import PublicAttribute

class InspectionSerializer(serializers.ModelSerializer):

    memorial = serializers.SlugRelatedField(slug_field='uuid', queryset=Memorial.objects.all())
    date = serializers.DateTimeField(format="%d %b %Y", input_formats=['%d %b %Y'])
    image = ImageSerializer(required=False)

    class Meta:
        model = Inspection
        fields = ('id', 'memorial', 'condition', 'inscription', 'remarks', 'date', 'action_required', 'image')

    def create(self, validated_data):
        inspection = Inspection.objects.create(**validated_data)
        inspection.created_by = self.context['user']
        inspection.save()

        if 'imageBase64' in self.context and self.context['imageBase64']:
            inspection.create_image(Image.base64_to_image(self.context['imageBase64']))

        return inspection

class GraveplotRefSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='uuid')
    grave_number = serializers.CharField(source='graveref.grave_number', allow_null=True, read_only=True)
    section = serializers.CharField(source='graveref.section.section_name', allow_null=True, read_only=True)
    subsection = serializers.CharField(source='graveref.subsection.subsection_name', allow_null=True, read_only=True)

    class Meta:
        model = GravePlot
        fields = ('id', 'grave_number', 'section', 'subsection', 'feature_id')

class GraveplotGraveNumberSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='uuid')
    grave_number = serializers.CharField(source='graveref.grave_number', allow_null=False, read_only=True)

    class Meta:
        model = GravePlot
        fields = ('id', 'grave_number', 'feature_id')

class MemorialGraveplotSerializer(serializers.ModelSerializer):

    graveplot_memorials = GraveplotRefSerializer(many=True, read_only=True)

    class Meta:
        model = Memorial
        fields = ('graveplot_memorials',)

class PlotNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraveRef
        fields=["id",'grave_number',]


class MemorialGraveNumbersSerializer(serializers.ModelSerializer):

    graveplot_memorials = GraveplotGraveNumberSerializer(many=True, read_only=True)
    topopolygon_id = serializers.CharField(allow_null=True, read_only=True)
    class Meta:
        model = Memorial
        fields = ('id', 'graveplot_memorials', 'topopolygon_id')

class GraveNumberSerializer(serializers.ModelSerializer):

    grave_number = serializers.CharField(source='graveref.grave_number', allow_null=True, read_only=True)
    section = serializers.IntegerField(source='graveref.section.id', allow_null=True, read_only=True)
    subsection = serializers.IntegerField(source='graveref.subsection.id', allow_null=True, read_only=True)

    class Meta:
        model = GravePlot
        fields = ('id', 'grave_number', 'section', 'subsection', 'memorial_feature_id')

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('graveref')
        queryset = queryset.select_related('graveref__section')
        queryset = queryset.select_related('graveref__subsection')
        return queryset

class SectionSerializer(serializers.ModelSerializer):
    #centrepoint = GeometrySerializerMethodField()
    topopolygon = GeometrySerializerMethodField()
    class Meta:
        model = Section
        fields = ('id', 'section_name', 'topopolygon')
        #fields = ('id', 'section_name', 'centrepoint', 'topopolygon')
        #geo_field = "centrepoint"
        geo_field = "topopolygon"

    def get_centrepoint(self, obj):
        if obj.topopolygon and obj.topopolygon.geometry and obj.topopolygon.geometry.centroid:
            return obj.topopolygon.geometry.centroid
        else:
            return None

    def get_topopolygon(self, obj):
        #geo = obj.topopolygon.geometry
        #extent = geo.extent
        #return extent
        if obj.topopolygon and obj.topopolygon.geometry:            
            return obj.topopolygon.geometry
        else:
            return None
class SubsectionSerializer(serializers.ModelSerializer):

    section = serializers.IntegerField(source='section.id')

    class Meta:
        model = Subsection
        fields = ('id', 'subsection_name', 'section')

class FeatureIDSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='uuid', read_only=True)

    class Meta:
        model = GravePlot
        fields = ('id', 'feature_id',)

class HeadpointGeoSerializer(GeoFeatureModelSerializer):

    geometry = GeometrySerializerMethodField()
    marker_type = serializers.SerializerMethodField()

    class Meta:
        model = Marker
        fields = ('id', 'geometry', 'marker_type')
        geo_field = "geometry"
        abstract = True

    def get_geometry(self, obj):
        return obj.topopolygon.geometry.centroid

    def get_marker_type(self, obj):
        return 'headpoint'

class MemorialHeadpointGeoSerializer(HeadpointGeoSerializer):
    class Meta(HeadpointGeoSerializer.Meta):
        model = Memorial

class GraveplotHeadpointGeoSerializer(HeadpointGeoSerializer):
    class Meta(HeadpointGeoSerializer.Meta):
        model = GravePlot

class GraveDetailsSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='uuid')
    grave_number = serializers.CharField(source='graveref.grave_number', allow_null=True, read_only=True)
    section_id = serializers.CharField(source='graveref.section_id', allow_null=True, read_only=True)
    section_name = serializers.CharField(source='graveref.section.section_name', allow_null=True, read_only=True)
    subsection_id = serializers.CharField(source='graveref.subsection_id', allow_null=True, read_only=True)
    subsection_name = serializers.CharField(source='graveref.subsection.subsection_name', allow_null=True, read_only=True)

    class Meta:
        model = GravePlot
        fields = ('id',
        'status', 'state', 'type', 'size', 'size_units', 'depth', 'depth_units',
        'perpetual', 'consecrated', 'memorial_comment', 'remarks',
        'grave_number', 'section_id', 'section_name', 'subsection_id', 'subsection_name', 'feature_id')

class GraveDeedsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = GraveDeed
        fields = ('id', 'ownership_register',
        'purchase_date', 'purchase_date_day', 'purchase_date_month', 'purchase_date_year', 'tenure', 'tenure_years')

class DeedSerializer(serializers.ModelSerializer):

    current_grave_owners = serializers.SerializerMethodField()
    previous_grave_owners = serializers.SerializerMethodField()
    image_1 = serializers.SerializerMethodField()
    image_2 = serializers.SerializerMethodField()
    tenure_years = serializers.IntegerField(allow_null=True, default=None, required=False)

    class Meta:
        model = GraveDeed
        fields = ('id', 'ownership_register', 'deed_url', 'deed_reference', 'current_grave_owners',
        'previous_grave_owners', 'cost_currency', 'cost_unit', 'cost_subunit', 'cost_subunit2',
        'purchase_date_day', 'purchase_date_month', 'purchase_date_year', 'tenure', 'tenure_years',
        'remarks', 'image_1', 'image_2')

    def to_internal_value(self, data):
        # convert 'null' to None
        if 'tenure_years' in data and data.get('tenure_years') == "null":
            data['tenure_years'] = None

        return super(DeedSerializer, self).to_internal_value(data)
    
    def get_current_grave_owners(self, obj):
        current_owners = obj.grave_owners.filter(Q(active_owner=True) & (Q(owner_to_date__isnull=True) | Q(owner_to_date__gte=datetime.now()))).order_by('-owner_from_date')
        return GraveOwnersListSerializer(instance=current_owners, many=True).data
    
    def get_previous_grave_owners(self, obj):
        previous_owners = obj.grave_owners.exclude(Q(active_owner=True) & (Q(owner_to_date__isnull=True) | Q(owner_to_date__gte=datetime.now()))).order_by('-owner_from_date')
        return GraveOwnersListSerializer(instance=previous_owners, many=True).data
    
    def get_image_1(self, obj):
        # if at least one image exists, return the first one
        if obj.id and obj.images and len(obj.images.all()) > 0:
            image_data = ImageSerializer(instance=obj.images.all()[0]).data
            image_data['id'] = obj.images.all()[0].id
            return image_data
        else:
            None
    
    def get_image_2(self, obj):
        # if at least two images exists, return the second one
        if obj.id and obj.images and len(obj.images.all()) > 1:
            return ImageSerializer(instance=obj.images.all()[1]).data
        else:
            None

class OwnerStatusSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField(required=False)

    class Meta:
        model = OwnerStatus
        fields = ('id', 'status')

"""
Abstract serializer
"""
class GraveOwnerSerializer_Base(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField()
    owner_id = serializers.CharField(source='object_id')

    class Meta:
        model = GraveOwner
        fields = ('id', 'owner_id', 'display_name', 'active_owner', 'owner_from_date_day', 'owner_from_date_month', 'owner_from_date_year', 'owner_to_date_day', 'owner_to_date_month', 'owner_to_date_year', 'remarks')
        abstract = True

    def get_display_name(self, obj):
        return get_owner_display_name(obj)

"""
Same field as GraveOwnerSerializer but without owner_status
"""
class NewGraveOwnerSerializer(GraveOwnerSerializer_Base):

    class Meta(GraveOwnerSerializer_Base.Meta):
        pass

class GraveOwnerSerializer(GraveOwnerSerializer_Base):

    display_name = serializers.SerializerMethodField()
    owner_id = serializers.CharField(source='object_id')
    owner_status = OwnerStatusSerializer(many=True)

    class Meta(GraveOwnerSerializer_Base.Meta):
        model = GraveOwner
        fields = GraveOwnerSerializer_Base.Meta.fields + ('owner_status',)

    def update(self, instance, validated_data):
        instance.active_owner = validated_data.pop('active_owner', instance.active_owner)
        instance.owner_from_date_day = validated_data.pop('owner_from_date_day', instance.owner_from_date_day)
        instance.owner_from_date_month = validated_data.pop('owner_from_date_month', instance.owner_from_date_month)
        instance.owner_from_date_year = validated_data.pop('owner_from_date_year', instance.owner_from_date_year)
        instance.owner_to_date_day = validated_data.pop('owner_to_date_day', instance.owner_to_date_day)
        instance.owner_to_date_month = validated_data.pop('owner_to_date_month', instance.owner_to_date_month)
        instance.owner_to_date_year = validated_data.pop('owner_to_date_year', instance.owner_to_date_year)
        instance.remarks = validated_data.pop('remarks', instance.remarks)

        ''' Owner status table '''
        if 'owner_status' in validated_data:

            # if this has changed, it's safest to just remove all current statuses and add/readd the ones we still need
            instance.owner_status.clear()

            owner_status = validated_data.pop('owner_status')

            for status in owner_status:
                instance.owner_status.add(OwnerStatus.objects.get(id=status.get('id')))

        instance.save()

        return instance

class PersonCompanyOwnershipListSerializer(serializers.ModelSerializer):

    deed_id = serializers.CharField(source='deed.id')
    grave_id = serializers.CharField(source='deed.graveplot.uuid')
    grave_number = serializers.CharField(source='deed.graveplot.graveref.grave_number', allow_null=True, read_only=True)
    section_name = serializers.CharField(source='deed.graveplot.graveref.section.section_name', allow_null=True, read_only=True)
    subsection_name = serializers.CharField(source='deed.graveplot.graveref.subsection.subsection_name', allow_null=True, read_only=True)
    site = serializers.SerializerMethodField()
    
    class Meta:
        model = GraveOwner
        fields = ('deed_id', 'grave_id', 'grave_number', 'section_name', 'subsection_name', 'site')

    def get_site(self, obj):
        return self.context['site_name']

class PersonNextOfKinToSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField()
    site = serializers.SerializerMethodField()
    reserved_graveplot_uuid = serializers.SerializerMethodField()
    most_recent_burial = serializers.SerializerMethodField()
    first_memorial = serializers.SerializerMethodField()

    
    class Meta:
        model = Person
        fields = ('id', 'display_name', 'site', 'reserved_graveplot_uuid', 'most_recent_burial', 'first_memorial')

    def get_site(self, obj):
        return self.context['site_name']

    def get_display_name(self, obj):
        return obj.get_display_name()
    
    def get_reserved_graveplot_uuid(self, obj):
        if hasattr(obj, 'reservedplot') and obj.reservedplot.state==ReservePlotState.objects.get(state='reserved'):
            return obj.reservedplot.grave_plot.uuid
        
    def get_most_recent_burial(self, obj):
        if hasattr(obj, 'death'):
            most_recent_burial = obj.death.get_most_recent_burial()

            if most_recent_burial:
                return { 'id':most_recent_burial.id, 'graveplot_uuid':most_recent_burial.graveplot.uuid }

        return None

    def get_first_memorial(self, obj):
        if hasattr(obj, 'death'):
            memorial = obj.death.get_first_memorial()

            if memorial:
                return { 'memorial_uuid': memorial.uuid, 'layer': memorial.topopolygon.layer.feature_code.feature_type }
        
        return None

class PersonListSerializer(serializers.ModelSerializer):

    person_id = serializers.CharField(source='person.id', read_only=True)
    first_names = serializers.CharField(source='person.first_names', allow_null=True, read_only=True)
    last_name = serializers.CharField(source='person.last_name', allow_null=True, read_only=True)
    display_name = serializers.SerializerMethodField()
    most_recent_burial_id = serializers.SerializerMethodField()
    most_recent_burial_date = serializers.SerializerMethodField()

    class Meta:
        model = Death
        fields = ('person_id', 'first_names', 'last_name', 'display_name', 'death_date',
        'age_years', 'age_months', 'age_weeks', 'age_days', 'age_hours', 'age_minutes', 'most_recent_burial_id', 'most_recent_burial_date')

    def get_display_name(self, obj):
        return obj.person.get_display_name()

    def get_most_recent_burial_id(self, obj):
        return obj.get_most_recent_burial_id()

    def get_most_recent_burial_date(self, obj):
        return obj.get_most_recent_burial_date()

class ReservedPersonListSerializer(serializers.ModelSerializer):

    person_id = serializers.CharField(source='id', read_only=True)
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('person_id', 'display_name')

    def get_display_name(self, obj):
        return obj.get_display_name()

class MemorialSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='uuid', read_only=True)
    feature_type = serializers.SerializerMethodField()

    class Meta:
        model = Memorial
        fields = ('id', 'feature_id', 'description', 'user_generated', 'inscription', 'feature_type')

    def get_feature_type(self, obj):
        return obj.topopolygon.layer.feature_code.feature_type

class BurialInformationSerializer(serializers.ModelSerializer):

    graveplot = GraveplotRefSerializer(read_only=True)
    death = PersonListSerializer(read_only=True)

    class Meta:
        model = Burial
        fields = ('id','register', 'death', 'graveplot')


class MarkerGeoSerializer(GeoFeatureModelSerializer):

    id = serializers.CharField(source='uuid')
    geometry = GeometrySerializerMethodField()
    real_feature_id = serializers.SerializerMethodField()

    class Meta:
        model = Marker
        fields = ('id', 'geometry', 'marker_type', 'real_feature_id')
        geo_field = "geometry"
        abstract = True

    def get_geometry(self, obj):
        return obj.topopolygon.geometry

    def get_real_feature_id(self, obj):
        return str(obj.topopolygon.id)


class MemorialGeoSerializer(MarkerGeoSerializer):

    images_count = serializers.IntegerField()
    linked_graves_count = serializers.IntegerField()
    material = serializers.SerializerMethodField()
    marker_type = serializers.SerializerMethodField()

    class Meta(MarkerGeoSerializer.Meta): 
        model = Memorial
        fields = MarkerGeoSerializer.Meta.fields + ('feature_id', 'images_count', 'linked_graves_count', 'material')

    def get_marker_type(self, obj):
        marker_type = self.context.get("marker_type")

        if marker_type=='bench' or marker_type=='lych_gate' or marker_type=='mausoleum':
            # features in multiple groups including memorials
            return 'memorials_' + marker_type
        else:
            return marker_type

    def get_material(self, obj):
        try:
            material = PublicAttribute.objects.get(name='Material')
        except:
            print("The 'material' public attribute is missing!")
            return None

        if obj.topopolygon.feature_attributes.exists():
            featureMaterialAttributes = obj.topopolygon.feature_attributes.filter(public_attribute=material)

            if featureMaterialAttributes.exists():
                return featureMaterialAttributes[0].char_value
                
        return None
        

class GraveplotGeoSerializer(MarkerGeoSerializer):

    class Meta(MarkerGeoSerializer.Meta):
        model = GravePlot

