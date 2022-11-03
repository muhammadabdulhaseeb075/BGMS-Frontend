""" Serializer classes for cemeteryadmin """

import datetime

from django.utils.timezone import make_aware, make_naive, is_naive

from rest_framework import serializers

from BGMS.utils import get_display_name_from_firstnames_lastname
from bgsite.common_apis.serializers import DeathPersonSerializer, BurialDetailsSerializer, AuthorityForIntermentSerializer
from bgsite.models import Burial, Official, Address, MeetingLocation, ReservedPlot, Person
from bgsite.serializers import FuneralDirectorAddressSerializer
from cemeteryadmin.models import CalendarEvents, FuneralEvent, FuneralEventStatus, PreburialCheck, PostburialCheck, Cancelburial, Settings
from main.models import BurialGroundSite, PublicPerson, ReservePlotState
from main.serializers import PersonSerializer, CompanySerializer, PublicAddressSerializer

class FuneralCreatorsSerializer(serializers.ModelSerializer):
    """
    Serializer class for fields relating to the creator of a funeral event
    """

    created_by_id = serializers.CharField(source='created_by.id', read_only=True)
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = CalendarEvents
        fields = ['created_by_id', 'created_by_name']

    def get_created_by_name(self, obj):
        """ Returns the name of the user who created this record formatted for display """

        return obj.created_by.first_name + " " + obj.created_by.last_name

class SettingsSerializer(serializers.ModelSerializer):
    """
    Serializer class for fields relating to Settings
    """
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    preferences = serializers.JSONField(read_only=True)
    class Meta:
        model = Settings
        fields = ['id', 'name', 'preferences']

class CalendarEventsSerializer(serializers.ModelSerializer):
    """
    Serializer class for fields relating to calendar events
    """

    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    name = serializers.CharField(source='event_type.name', read_only=True)
    event_category = serializers.CharField(source='event_type.event_category.name', read_only=True)
    details = serializers.SerializerMethodField()
    status  = serializers.SerializerMethodField()

    class Meta:
        model = CalendarEvents
        fields = ['id', 'start', 'end', 'name', 'display_date', 'created_date', 'created_by', 'event_type_id', 'event_category', 'details', 'reference', 'status', 'reference_number']

    def get_start(self, obj):
        """ Returns start datetime in site's timezone """
        if is_naive(obj.start):
            return obj.start
        else:
            return make_naive(obj.start, self.context.get("timezone"))




    def get_end(self, obj):
        """ Returns end datetime in site's timezone """
        if is_naive(obj.start):
            return obj.end
        else:
            return make_naive(obj.end, self.context.get("timezone"))



    def get_created_date(self, obj):

        """ Returns created date datetime in site's timezone with rounded milliseconds """
        if is_naive(obj.created_date):
            naive_date = obj.created_date
        else:
            naive_date = make_naive(obj.created_date, self.context.get("timezone"))
        rounded_naive_date = naive_date - datetime.timedelta(microseconds=naive_date.microsecond)
        return rounded_naive_date


    def get_created_by(self, obj):
        """ Returns the name of the user who created this record formatted for display """

        if obj.created_by:
            return obj.created_by.first_name + " " + obj.created_by.last_name
        else:
            return 'Unknown'

    def get_details(self, obj):
        """ Returns brief details about the event """

        if obj.event_type.event_category.name == "Funeral" and hasattr(obj, 'funeral_event'):
            person = obj.funeral_event.person
            return get_display_name_from_firstnames_lastname(person.first_names, person.last_name)

        return None

    def get_status(self, obj):
        if obj.event_type.event_category.name == "Funeral" and hasattr(obj, 'funeral_event'):
            status = obj.funeral_event.status
            return status

    def to_internal_value(self, data):
        """
        Override method to validate otherwise unvalidated data
        """

        internal_value = super(CalendarEventsSerializer, self).to_internal_value(data)

        if 'start' in data:
            value = data.get('start')
            internal_value.update({
                'start': value
            })

        if 'end' in data:
            value = data.get('end')
            internal_value.update({
                'end': value
            })

        if 'event_type_id' in data:
            value = data.get('event_type_id')
            internal_value.update({
                'event_type_id': value
            })

        return internal_value

    def update(self, instance, validated_data):
        """
        Update and return an existing `CalendarEvents` instance, given the validated data.
        """

        fmt = '%Y-%m-%dT%H:%M'
        site_tz = BurialGroundSite.get_site_timezone()

        if 'start' in validated_data:
            start = validated_data.pop('start', instance.start)
            if(not isinstance(start, datetime.date)): # If object has already been saved then the date will be an object
                start = datetime.datetime.strptime(start, fmt)
                start_tz_aware = make_aware(datetime.datetime(start.year, start.month, start.day, start.hour, start.minute), site_tz)
                instance.start = start_tz_aware
            else:
                instance.start = start

        if 'end' in validated_data:
            end = validated_data.pop('end', instance.end)
            if (not isinstance(end, datetime.date)):
                end = datetime.datetime.strptime(end, fmt)
                end_tz_aware = make_aware(datetime.datetime(end.year, end.month, end.day, end.hour, end.minute), site_tz)
                instance.end = end_tz_aware
            else:
                instance.end = end

        keys = list(validated_data.keys())
        for key in keys:
            setattr(instance, key, validated_data.pop(key, getattr(instance, key)))

        instance.save()

        return instance

class PreburialCheckSerializer(serializers.ModelSerializer):
  """
  Serializer class for fields relating to preburial check
  """
  class Meta:
    model = PreburialCheck
    fields = ['grave_details', 'grave_on_ground', 'notice_of_interment', 'burial_certificate', 'noi_details', 'burial_grant_noi', 'indemnity', 'gravedigger', 'signed_off', 'invoice','id','grave_details_by_user','grave_on_ground_by_user','notice_of_interment_by_user','burial_certificate_by_user','noi_details_by_user','burial_grant_noi_by_user','indemnity_by_user','gravedigger_by_user','signed_off_by_user','invoice_by_user']

    def create(self, validated_data):
      return PreburialCheck.objects.create()
 
class CancelburialSerializer(serializers.ModelSerializer):
  """
  Serializer class for fields relating to preburial check
  """
  class Meta:
    model = Cancelburial
    fields = ['cancel_reason', 'cancel_date', 'id']

    def create(self, validated_data):
      return Cancelburial.objects.create()

class PostburialCheckSerializer(serializers.ModelSerializer):
  """
  Serializer class for fields relating to postburial check
  """     
  class Meta:
    model = PostburialCheck
    fields = ['backfill_completed', 'plot_inspected', 'id','backfill_completed_by_user','plot_inspected_by_user']

    def create(self, validated_data):
      return PostburialCheck.objects.create()


class FuneralEventSerializer(serializers.ModelSerializer):
    """
    Serializer class for fields relating to funeral events
    """
    calendar_event = CalendarEventsSerializer()
    next_of_kin_person = PersonSerializer(source='person.next_of_kin', read_only=True)
    funeral_director_id = serializers.CharField(source='funeral_director.id', default=None, required=False, allow_null=True)
    meeting_location_id = serializers.CharField(source='meeting_location.id', default=None, required=False, allow_null=True)
    # reservation_id = serializers.CharField(source='reservation.id', default=None, required=False, allow_null=True)
    status = serializers.IntegerField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['person'] = DeathPersonSerializer(context=self.context, required=False)
        self.fields['burial'] = BurialDetailsSerializer(context=self.context)
        self.fields['authority_for_interment'] = AuthorityForIntermentSerializer(context=self.context, required=False)
        self.fields['preburial_check'] = PreburialCheckSerializer(context=self.context, required=False)
        self.fields['postburial_check'] = PostburialCheckSerializer(context=self.context, required=False)
        self.fields['cancelburial'] = CancelburialSerializer(context=self.context, required=False)

    class Meta:
        model = FuneralEvent
        fields = ['calendar_event', 'person', 'next_of_kin_person', 'burial', 'reservation_id', 'authority_for_interment', 'preburial_checklist',
                  'postburial_checklist', 'funeral_director_id', 'meeting_location_id', 'status', 'preburial_check','postburial_check',]

    def save_next_of_kin(self, next_of_kin, user):
        """
        Create/update next of kin Person when funeral is being created/updated.
        Returns next of kin's Person id.
        """

        if not next_of_kin:
            return None

        public_person_obj = None

        if 'id' in next_of_kin and next_of_kin['id']:
            # this is an existing person record that might need updated

            if 'is_owner' in next_of_kin and next_of_kin['is_owner']:
                # restrict fields that can be updated when person is an owner
                next_of_kin_data = {
                    'email': next_of_kin['email'],
                    'phone_number': next_of_kin['phone_number'],
                    'phone_number_2': next_of_kin['phone_number_2'],
                    }
            else:
                next_of_kin_data = next_of_kin

            if next_of_kin['id']:
                public_person_serializer = PersonSerializer(PublicPerson.objects.get(id=next_of_kin['id']), data=next_of_kin_data, partial=True)
                public_person_serializer.is_valid(True)
                public_person_obj = public_person_serializer.save(last_edit_by=user)

        elif ('last_name' in next_of_kin and next_of_kin['last_name']) or ('first_name' in next_of_kin and next_of_kin['first_name']):
            # this is a new person

            address = None

            if next_of_kin['current_addresses']:
                # if an address has been included
                address = next_of_kin['current_addresses'][0]

            public_person_serializer = PersonSerializer(data=next_of_kin)
            public_person_serializer.is_valid(True)
            public_person_obj = public_person_serializer.save(created_by=user, address=address)

        else:
            return None

        return public_person_obj.id

    def create(self, validated_data):
        """
        Create and return a new `FuneralEvent` instance, given the validated data.
        """

        # always update this field when updating calendar
        created_by = validated_data.pop('created_by')

        ''' Calendar event table '''
        validated_calendar_event_object = validated_data.pop('calendar_event')
        calendar_event = CalendarEvents.objects.create(created_by=created_by, **validated_calendar_event_object)
        calendar_event_id = calendar_event.id

        ''' Person table '''
        validated_person_object = validated_data.pop('person')

        if 'next_of_kin' in self.context:
            # create/update next of kin
            validated_person_object['next_of_kin'] = self.save_next_of_kin(self.context['next_of_kin'], created_by)
        if 'death' in validated_person_object:
            if 'religion' in validated_person_object['death'] and validated_person_object['death']['religion']:
                # without this, validation fail. Not sure why...
                validated_person_object['death']['religion'] = validated_person_object['death']['religion'].id

        death_person_serializer = DeathPersonSerializer(data=validated_person_object, context={'user': self.context['user']})
        death_person_serializer.is_valid(True)
        death_person_serializer.save()
        person_id = death_person_serializer.data['id']

        authority_for_interment_id = None

        if 'authority_for_interment' in validated_data:
            validated_authority_for_interment = validated_data.pop('authority_for_interment')
            authority_for_interment_serializer = AuthorityForIntermentSerializer(data=validated_authority_for_interment, context={'user': self.context['user']})
            authority_for_interment_serializer.is_valid(True)
            authority_for_interment_serializer.save()
            authority_for_interment_id = authority_for_interment_serializer.data['id']

        ''' Burial table '''
        validated_burial_object = validated_data.pop('burial')
        burial = Burial.objects.create(death_id=person_id, **validated_burial_object)

        '''PreburialCheck'''
        preburial_check = PreburialCheck.objects.create()
        preburial_check_id = preburial_check.id

        '''PostburialCheck'''
        postburial_check = PostburialCheck.objects.create()
        postburial_check_id = postburial_check.id

        '''Cancelburial'''
        cancelburial = Cancelburial.objects.create()
        cancelburial_id = cancelburial.id

        if 'graveplot_id' in self.initial_data['burial']:
            burial.graveplot_id = self.initial_data['burial']['graveplot_id']
            burial.save()

        burial_id = burial.id

        ''' Reserved Plot Section (Always create even if no grave_id) '''
        plot_state = ReservePlotState.objects.get(id=1)
        person_obj = Person.objects.get(id=person_id)
        reservation = ReservedPlot(person=person_obj, date=calendar_event.start, state=plot_state)
        if(burial.graveplot_id):
            reservation.grave_plot = burial.graveplot_id
        reservation.save()  # New reservation object so should always save?


        ''' FuneralEvent table '''
        if 'funeral_director' in validated_data:
            validated_funeral_director_object = validated_data.pop('funeral_director')
            validated_data['funeral_director_id'] = validated_funeral_director_object['id']

        '''meeting_location_id'''
        if 'meeting_location' in validated_data:
            validated_meeting_location_object = validated_data.pop('meeting_location')
            validated_data['meeting_location_id'] = validated_meeting_location_object['id']

        return FuneralEvent.objects.create(
            calendar_event_id=calendar_event_id,
            person_id=person_id, burial_id=burial_id,
            authority_for_interment_id=authority_for_interment_id,
            status=FuneralEventStatus.PRE_BURIAL_CHECKS.value,
            preburial_check_id=preburial_check_id,
            postburial_check_id=postburial_check_id,
            cancelburial_id=cancelburial_id,
            reservation=reservation,
            **validated_data
        )

    def update(self, instance, validated_data):
        """
        Update and return an existing `FuneralEvent` instance, given the validated data.
        """

        # always update this field when updating calendar
        last_edit_by = None
        if('last_edit_by' in validated_data):
            last_edit_by = validated_data.pop('last_edit_by')

        ''' CalendarEvents table '''
        if 'calendar_event' in validated_data:
            validated_calendar_event_object = validated_data.pop('calendar_event')
            calendar_event_serializer = CalendarEventsSerializer(instance.calendar_event, data=validated_calendar_event_object, partial=True)
            calendar_event_serializer.is_valid(True)
            if(last_edit_by):
                calendar_event_serializer.save(last_edit_by=last_edit_by)
            else:
                calendar_event_serializer.save()

        ''' Person table '''
        if 'person' in validated_data:
            validated_person_object = validated_data.pop('person')

            if 'next_of_kin' in self.context:
                # create/update next of kin
                validated_person_object['next_of_kin'] = self.save_next_of_kin(self.context['next_of_kin'], last_edit_by)


            if 'death' in validated_person_object and 'religion' in validated_person_object['death'] and validated_person_object['death']['religion']:
                validated_person_object['death']['religion'] = validated_person_object['death']['religion'].id

            death_person_serializer = DeathPersonSerializer(instance.person, data=validated_person_object, partial=True, context=self.context)
            death_person_serializer.is_valid(True)
            death_person_serializer.save()

        if 'authority_for_interment' in validated_data:
            validated_authority_for_interment = validated_data.pop('authority_for_interment')
            if 'id' in validated_authority_for_interment:
                instance.authority_for_interment_id = validated_authority_for_interment['id']

            authority_for_interment_serializer = AuthorityForIntermentSerializer(instance.authority_for_interment ,data=validated_authority_for_interment, partial=True)
            authority_for_interment_serializer.is_valid(True)
            authority_for_interment_serializer.save()

        ''' Burial table '''
        if 'burial' in validated_data:
            validated_burial_object = validated_data.pop('burial')

            context = None
            if 'graveplot_id' in self.initial_data['burial']:
                context = {'graveplot_id': self.initial_data['burial']['graveplot_id'], 'user': self.context['user']}
            
            burial_details_serializer = BurialDetailsSerializer(instance.burial, data=validated_burial_object, partial=True, context=context)
            burial_details_serializer.is_valid(True)
            burial_details_serializer.save()

        ''' FuneralEvent table '''
        if 'funeral_director' in validated_data:
            validated_funeral_director_object = validated_data.pop('funeral_director')
            instance.funeral_director_id = validated_funeral_director_object['id']

        if 'meeting_location' in validated_data:
            validated_meeting_location_object = validated_data.pop('meeting_location')
            if 'id' in validated_meeting_location_object:
                instance.meeting_location_id = validated_meeting_location_object['id']

        keys = list(validated_data.keys())
        for key in keys:
            setattr(instance, key, validated_data.pop(key, getattr(instance, key)))

        instance.save()

        return instance

class FuneralDirectorsListSerializer(serializers.ModelSerializer):
    """
    Serializer class for fields needed in a list of funeral directors
    """
    address = FuneralDirectorAddressSerializer()

    class Meta:
        model = Official
        fields = ['id', 'title', 'first_names', 'last_name', 'used_on', 'email', 'phone_number', 'second_phone_number', 'address', 'company_name', 'job_title']


class FuneralDirectorSerializer(serializers.ModelSerializer):
    """
    Serializer class for fields needed relating to funeral directorss
    """
    address = FuneralDirectorAddressSerializer()

    class Meta:
        model = Official
        fields = ['id', 'title', 'job_title', 'first_names', 'last_name', 'used_on', 'email', 'phone_number', 'second_phone_number', 'address', 'company_name']

    def create(self, validated_data):
        """
        Create and return a new `FuneralDirector` instance, given the validated data.
        """

        ''' Address table '''
        address = None

        if 'address' in validated_data:
            address = validated_data.pop('address')

        if 'created_by' in validated_data:
            validated_data.pop('created_by')

        if address:
            address_serializer = FuneralDirectorAddressSerializer(data=address)
            address_serializer.is_valid(True)
            new_address = address_serializer.save()
            FuneralDirector = Official.objects.create(address=new_address, **validated_data)
        else:
            FuneralDirector = Official.objects.create(**validated_data)
            # FuneralDirector.address = Address.objects.get(id=new_address.id)

        return FuneralDirector

    def update(self, instance, validated_data):
        """
        Update and return a new `FuneralDirector` instance, given the validated data.
        """

        ''' Address table '''
        address = None

        if 'address' in validated_data:
            address = validated_data.pop('address')

        if 'created_by' in validated_data:
            validated_data.pop('created_by')

        if address:
            address_serializer = FuneralDirectorAddressSerializer(instance.address, data=address, partial=True, context=self.context)            
            address_serializer.is_valid(True)
            address_serializer.save()

        keys = list(validated_data.keys())
        for key in keys:
            setattr(instance, key, validated_data.pop(key, getattr(instance, key)))
        instance.save()

        return instance

class MeetingLocationListSerializer(serializers.ModelSerializer):
    """Serializer class for fields needed in a list of Meeting locations"""

    class Meta:
        model = MeetingLocation
        fields = ['id', 'location_address']

class MeetingLocationSerializer(serializers.ModelSerializer):
    """
    Serializer class for fields relating to Meeting location
    """
    class Meta:
        model = MeetingLocation
        fields = ['id', 'location_address']