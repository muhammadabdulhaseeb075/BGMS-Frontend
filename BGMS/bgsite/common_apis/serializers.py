from datetime import datetime
from django.contrib.contenttypes import fields

from rest_framework import serializers

from bgsite.models import GraveOwner, Address, Image, Death, Burial, create_date, Person, Memorial, ReservePlotState, \
    Burial_Official, Official, BurialOfficialType, MemorialInscriptionDetail, AuthorityForInterment, PersonField, GravePlot, MeetingLocation


def get_owner_display_name(obj):
    if obj.owner:
        if obj.content_type.model == 'publicperson':
            return obj.owner.get_display_name()
        # company
        return obj.owner.name
    return 'UNKNOWN'

def user_authenticated(user):
    """
    Returns True if the request user is authenticated
    """
    return user and user.is_authenticated

class GraveOwnersListSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()
    owner_type = serializers.SerializerMethodField()

    class Meta:
        model = GraveOwner
        fields = ('id', 'owner_type', 'owner_id', 'display_name', 'owner_from_date_day', 'owner_from_date_month', 'owner_from_date_year')

    def get_display_name(self, obj):
        return get_owner_display_name(obj)

    def get_owner_id(self, obj):
        if obj.owner:
            return obj.owner.id
        else:
            return None

    def get_owner_type(self, obj):

        if obj.owner:
            owner_type = obj.content_type.model

            if owner_type == 'publicperson':
                owner_type = 'person'

            return owner_type
        else:
            return None

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'

class DeathSerializer(serializers.ModelSerializer):

    class Meta:
        model = Death
        fields = ('event', 'age_years', 'age_months', 'age_weeks', 'age_days', 'age_hours', 'age_minutes', 'parish', 'religion', 'impossible_date_day', 'impossible_date_month', 'impossible_date_year', 'death_cause')

class BurialListSerializer(serializers.ModelSerializer):

    person_id = serializers.CharField(source='death.person.id', read_only=True)
    display_name = serializers.SerializerMethodField()
    death_date = serializers.DateField(source='death.death_date', allow_null=True, read_only=True)
    age_years = serializers.IntegerField(source='death.age_years', allow_null=True, read_only=True)
    age_months = serializers.IntegerField(source='death.age_months', allow_null=True, read_only=True)
    age_weeks = serializers.IntegerField(source='death.age_weeks', allow_null=True, read_only=True)
    age_days = serializers.IntegerField(source='death.age_days', allow_null=True, read_only=True)
    age_hours = serializers.IntegerField(source='death.age_hours', allow_null=True, read_only=True)
    age_minutes = serializers.IntegerField(source='death.age_minutes', allow_null=True, read_only=True)
    burial_date = serializers.SerializerMethodField()

    class Meta:
        model = Burial
        fields = ('id', 'person_id', 'display_name', 'death_date', 'burial_date',
                  'age_years', 'age_months', 'age_weeks', 'age_days', 'age_hours', 'age_minutes',
                  'impossible_date_month')

    def get_display_name(self, obj):
        return obj.death.person.get_display_name()

    def get_burial_date(self, obj):
        if obj.burial_date:
            return obj.burial_date
        else:
            return create_date(day=obj.impossible_date_day, month=obj.impossible_date_month, year=obj.impossible_date_year)

class ImageSerializer(serializers.ModelSerializer):

    image_url = serializers.CharField(source='get_image_url')
    thumbnail_url = serializers.CharField(source='get_thumbnail_url')

    class Meta:
        model = Image
        fields = ('image_url', 'thumbnail_url',)


class MemorialListSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='uuid')
    layer_name = serializers.SerializerMethodField()
    layer_display_name = serializers.SerializerMethodField()
    images = ImageSerializer(many=True,)

    class Meta:
        model = Memorial
        fields = ('id', 'feature_id', 'layer_name', 'layer_display_name', 'images')

    def get_layer_name(self, obj):
        return obj.topopolygon.layer.feature_code.feature_type

    def get_layer_display_name(self, obj):
        return obj.topopolygon.layer.feature_code.display_name

class DeathPersonSerializer(serializers.ModelSerializer):

    residence_address = AddressSerializer(read_only=False, allow_null=True, required=False)
    other_address = AddressSerializer(read_only=False, allow_null=True, required=False)
    death = DeathSerializer(read_only=False, allow_null=True, required=False)
    burials = BurialListSerializer(many=True, read_only=True, source="death.death_burials", required=False)
    memorials = MemorialListSerializer(many=True, read_only=True, source="death.memorials")
    most_recent_burial_date = serializers.SerializerMethodField()
    next_of_kin_display_name = serializers.SerializerMethodField(read_only=True)
    reservation_reference = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(DeathPersonSerializer, self).__init__(*args, **kwargs)

        if not user_authenticated(self.context['user']):
            self.fields.pop('next_of_kin')
            self.fields.pop('next_of_kin_display_name')
            self.fields.pop('next_of_kin_relationship')

    class Meta:
        model = Person
        fields = ('id', 'title', 'first_names', 'last_name', 'birth_name', 'other_names', 'impossible_date_day',
         'impossible_date_month', 'impossible_date_year', 'gender', 'age', 'age_type', 'description', 'profession', 
         'death', 'residence_address', 'other_address', 'memorials', 'burials', 'most_recent_burial_date', 'next_of_kin',
          'next_of_kin_display_name', 'next_of_kin_relationship', 'reservation_reference', 'place_of_death','file')

    def get_most_recent_burial_date(self, obj):
        if obj.get_death():
            return obj.death.get_most_recent_burial_date()
        else:
            return None

    def get_reservation_reference(self, obj):

        if hasattr(obj, 'reservedplot') and obj.reservedplot.state != ReservePlotState.objects.get(state='deleted'):
            return obj.reservedplot.reservation_reference

    def get_next_of_kin_display_name(self, obj):
        # hidden in public access
        if user_authenticated(self.context['user']) and obj.next_of_kin_id and obj.next_of_kin:
            return obj.next_of_kin.get_display_name()
        else:
            return None

    def create(self, validated_data):

        address_object = None
        other_address = None
        validated_other_address_object = None

        ''' Address table '''
        if 'residence_address' in validated_data:
            validated_address_object = validated_data.pop('residence_address')

            # optional
            if validated_address_object:
                address_object = Address.objects.create(**validated_address_object)
        if 'place_of_death' in validated_data:
            if validated_data['place_of_death'] and address_object is not None:
                other_address = address_object
            if validated_data['place_of_death'] is False and 'other_address' in validated_data:
                validated_other_address_object = validated_data.pop('other_address')

        if 'other_address' in validated_data and 'place_of_death' not in validated_data:
            validated_other_address_object = validated_data.pop('other_address')

        if validated_other_address_object:
            other_address = Address.objects.create(**validated_other_address_object)

        validated_death_object = None
        ''' Person table '''
        if 'death' in validated_data:
            validated_death_object = validated_data.pop('death')

        person = Person.objects.create(residence_address=address_object, **validated_data)
        person.other_address = other_address
        person.save()

        if validated_death_object is None:
            validated_death_object = {}
        ''' Death table '''
        # not optional
        Death.objects.create(person=person, **validated_death_object)

        return person

    def update(self, instance, validated_data):
        validated_other_address_object = None

        if 'residence_address' in validated_data:
            validated_address_object = validated_data.pop('residence_address')
        else:
            validated_address_object = None

        if 'death' in validated_data:
            validated_death_object = validated_data.pop('death')
        else:
            validated_death_object = None

        if 'other_address' in validated_data and 'place_of_death' not in validated_data:
            validated_other_address_object = validated_data.pop('other_address')

        if 'place_of_death' in validated_data and 'other_address' in validated_data:
            validated_other_address_object = validated_data.pop('other_address')

        validated_data_copy = validated_data.copy()
        ''' Person table '''
        keys = list(validated_data.keys())
        for key in keys:
            setattr(instance, key, validated_data.pop(key, getattr(instance, key)))

        if 'place_of_death' in validated_data_copy and validated_data_copy['place_of_death'] is False:
            instance.other_address = None

        field_names_to_clean = ('first_line', 'second_line', 'town', 'county', 'postcode', 'country')

        if instance.residence_address:
            if (validated_address_object is not None and len(validated_address_object) == 0) or validated_address_object is None:
                address_object = Address.objects.get(id=instance.residence_address.id)
                if instance.other_address and address_object.id == instance.other_address.id:
                    instance.other_address = None
                #instance.residence_address = None
                #address_object.delete() #why does this delete? #//TMN_Temp


        ''' Address table '''
        if validated_address_object:
            if validated_address_object.get('first_line') or validated_address_object.get('second_line') or validated_address_object.get('town') or validated_address_object.get('county') or validated_address_object.get('postcode') or validated_address_object.get('country'):

                if instance.residence_address and instance.residence_address.id:
                    address_object = Address.objects.get(id=instance.residence_address.id)

                    keys = list(validated_address_object.keys())
                    for field_to_clean in field_names_to_clean:
                        setattr(address_object, field_to_clean, '')
                    for key in keys:
                        setattr(address_object, key, validated_address_object.pop(key, getattr(address_object, key)))
                else:
                    address_object = Address.objects.create(**validated_address_object)
                    instance.residence_address = address_object

                address_object.save()
                # when there is an address object independent if it is new or old then we remove that address only if the residence address is not
                # the same as the old one.
                if 'place_of_death' in validated_data_copy:
                    if validated_data_copy['place_of_death']:
                        old_address_object = instance.other_address
                        #if old_address_object and old_address_object.id != address_object.id:
                            #old_address_object.delete() #//TMN_Temp
                        if address_object:
                            instance.other_address = address_object

        ''' Address table, other address instance '''
        if validated_other_address_object:
            if validated_other_address_object.get('first_line') or validated_other_address_object.get('second_line') or validated_address_object.get('town') or validated_other_address_object.get('county') or validated_other_address_object.get('postcode') or validated_other_address_object.get('country'):
                instance_other_address = instance.other_address
                other_address_object = None
                if instance_other_address and instance_other_address.id:
                    address_object = Address.objects.get(id=instance.residence_address.id)
                    if address_object and address_object.id == instance_other_address.id:
                        other_address_object = Address.objects.create(**validated_other_address_object)
                        instance.other_address = other_address_object
                    else:
                        other_address_object = Address.objects.get(id=instance.other_address.id)
                        keys = list(validated_other_address_object.keys())
                        for field_to_clean in field_names_to_clean:
                            setattr(other_address_object, field_to_clean, '')
                        for key in keys:
                            setattr(other_address_object, key,
                                    validated_other_address_object.pop(key, getattr(other_address_object, key)))
                else:
                    other_address_object = Address.objects.create(**validated_other_address_object)
                    instance.other_address = other_address_object

                if other_address_object:
                    other_address_object.save()

        ''' Death table '''
        if validated_death_object:

            death_object = Death.objects.get(person=instance.id)
            if validated_death_object.get('impossible_date_day') or validated_death_object.get(
                    'impossible_date_month') or validated_death_object.get('impossible_date_year'):
                keys = list(validated_death_object.keys())
                for key in keys:
                    setattr(death_object, key, validated_death_object.pop(key, getattr(death_object, key)))

                death_object.save()
        instance.save()

        return instance

class AuthorityForIntermentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthorityForInterment
        fields = ['id', 'first_names', 'last_name', 'title']

class Burial_OfficialSerializer(serializers.ModelSerializer):

    label = serializers.SerializerMethodField()
    official_id = serializers.CharField(source='official.id')
    official_title = serializers.CharField(source='official.title', allow_null=True, read_only=True)
    official_first_names = serializers.CharField(source='official.first_names', allow_null=True, read_only=True)
    official_last_name = serializers.CharField(source='official.last_name', allow_null=True, read_only=True)
    burial_official_type_id = serializers.CharField(source='burial_official_type.id', allow_null=True)

    class Meta:
        model = Burial_Official
        fields = ('id', 'label', 'official_id', 'official_title', 'official_first_names', 'official_last_name', 'burial_official_type_id')

    def get_label(self, obj):
        """ This must match the label used in the select in Burial sidebar """

        return '{0}, {1} ({2})'.format(obj.official.last_name, obj.official.first_names, obj.official.title)

class BurialDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer class for burial fields
    """
    coffin_height = serializers.FloatField(allow_null=True, required=False)
    coffin_width = serializers.FloatField(allow_null=True, required=False)
    coffin_length = serializers.FloatField(allow_null=True, required=False)
    burial_officials = Burial_OfficialSerializer(source="burial_official_set", many=True, required=False, allow_null=True)
    burial_record_image = ImageSerializer(required=False, allow_null=True)
    transcribed_grave_number = serializers.CharField(source='graveref.grave_number', allow_null=True, read_only=True)

    def __init__(self, *args, **kwargs):
        super(BurialDetailsSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Burial
        fields = ('id', 'graveplot_id', 'burial_officials', 'burial_number', 'impossible_date_day', 'impossible_date_month', 'impossible_date_year', 'impossible_order_date_day', 'impossible_order_date_month', 'impossible_order_date_year', 'consecrated', 'cremated', 'impossible_cremation_date_day', 'impossible_cremation_date_month', 'impossible_cremation_date_year', 'cremation_certificate_no', 'interred', 'coffin_length', 'coffin_width', 'coffin_height', 'coffin_units', 'depth', 'depth_units', 'depth_position','coffin_comments', 'burial_remarks', 'requires_investigation', 'user_remarks', 'place_from_which_brought', 'register', 'register_page', 'registration_number', 'burial_record_image', 'transcribed_grave_number', 'new_burial_grave')

    def update(self, instance, validated_data):
        ''' Burial official '''
        burial_officials = []

        if 'burial_official_set' in validated_data:
            burial_officials = validated_data.pop('burial_official_set')

        # remove deleted officials
        list_of_burial_official_ids = [burial_official['official']['id'] for burial_official in burial_officials if 'official' in burial_official]
        Burial_Official.objects.filter(burial_id=instance.id).exclude(official_id__in=list_of_burial_official_ids).delete()

        for burial_official in burial_officials:

            official = Official.objects.get(id=burial_official['official']['id'])

            burial_official_record, _ = Burial_Official.objects.get_or_create(burial=instance, official=official)

            if str(burial_official_record.burial_official_type_id) != str(burial_official['burial_official_type']['id']):
                burial_official_record.burial_official_type = BurialOfficialType.objects.get(id=burial_official['burial_official_type']['id'])
                burial_official_record.save()

            # update used on date
            official.used_on = datetime.now()
            official.save()

        ''' Burial data '''
        keys = list(validated_data.keys())
        for key in keys:
            setattr(instance, key, validated_data.pop(key, getattr(instance, key)))

        instance.save()

        return instance

class MemorialInscriptionSerializer(serializers.ModelSerializer):

    memorial = serializers.SlugRelatedField(slug_field='uuid', queryset=Memorial.objects.all())

    class Meta:
        model = MemorialInscriptionDetail
        fields = ('id', 'memorial', 'first_names', 'last_name', 'age', 'date')

class PersonFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonField
        fields = ['id', 'name', 'type', 'options', 'required', 'is_default', 'content', 'field_form', 'order']

# class BurialNumberSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model =Burial
#         fields =['id', 'burial_number','graveplot_id','death_id']

    
class BurialGraveNumberSerializer(serializers.ModelSerializer):
    
    id = serializers.CharField(source='uuid')
    burial_number = serializers.CharField(source='burial.burial_number', allow_null=False, read_only=True)
    topopolygon_id = serializers.CharField(allow_null=True, read_only=True) 
    class Meta:
        model = Burial
        fields = ('id', 'burial_number','topopolygon_id')

class BurialNumberSerializer(serializers.ModelSerializer): 
    burial_number = serializers.CharField(allow_null=True, read_only=True)   
    topopolygon_id = serializers.CharField(allow_null=True, read_only=True) 
    
    class Meta:
        model = GravePlot
        fields = ('id','graveplot_memorials','topopolygon_id','burial_number')
        #fields = ('id','memorial_feature_id','topopolygon_id','burial_number')
        
