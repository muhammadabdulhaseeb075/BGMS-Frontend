from datetime import datetime, date

from django.db.models import Q

from rest_framework import serializers

from main.models import PublicPerson, Address as PublicAddress, BurialGroundSite, Company as PublicCompany, siteReferenceSettings

class PublicAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicAddress
        fields = ('id', 'first_line', 'second_line', 'town', 'county', 'postcode', 'country', 'current', 'from_date_day', 'from_date_month', 'from_date_year', 'to_date_day', 'to_date_month', 'to_date_year')

class PublicAddressListSerializer(serializers.ModelSerializer):

    display_address = serializers.SerializerMethodField()
    current = serializers.SerializerMethodField()

    class Meta:
        model = PublicAddress
        fields = ('id', 'display_address', 'current')

    def get_display_address(self, obj):

        return_value = ''

        if obj.first_line:
            return_value = obj.first_line

        if obj.second_line:
            return_value += (', ' if return_value else '') + obj.second_line

        if obj.town:
            return_value += (', ' if return_value else '') + obj.town

        if obj.county:
            return_value += (', ' if return_value else '') + obj.county

        if obj.postcode:
            return_value += (', ' if return_value else '') + obj.postcode.upper()

        if obj.country:
            return_value += (', ' if return_value else '') + obj.country

        return return_value

    def get_current(self, obj):
        if obj.current and obj.to_date and obj.to_date < date(datetime.now().year, datetime.now().month, datetime.now().day):
            return False
        else:
            return obj.current

class PersonSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField()
    current_addresses = serializers.SerializerMethodField()
    previous_addresses = serializers.SerializerMethodField()

    class Meta:
        model = PublicPerson
        fields = ('id', 'display_name', 'title', 'first_names', 'last_name', 'birth_name', 'other_names', 'birth_date_day', 'birth_date_month', 'birth_date_year', 'gender', 'email', 'phone_number', 'phone_number_2', 'remarks', 'current_addresses', 'previous_addresses')

    def get_display_name(self, obj):
        return obj.get_display_name()

    def get_current_addresses(self, obj):
        current_addresses = obj.addresses.filter(Q(current=True) & (Q(to_date__isnull=True) | Q(to_date__gte=datetime.now()))).order_by('-from_date')
        return PublicAddressListSerializer(instance=current_addresses, many=True, read_only=True).data

    def get_previous_addresses(self, obj):
        previous_addresses = obj.addresses.exclude(Q(current=True) & (Q(to_date__isnull=True) | Q(to_date__gte=datetime.now()))).order_by('-from_date')
        return PublicAddressListSerializer(instance=previous_addresses, many=True, read_only=True).data

    def to_internal_value(self, data):
        internal_value = super(PersonSerializer, self).to_internal_value(data)

        if 'address' in data:
            value = data.get('address')
            internal_value.update({
                'address': value
            })

        return internal_value

    def create(self, validated_data):

        address = None

        if 'address' in validated_data:
            address = validated_data.pop('address')

        person_obj = PublicPerson.objects.create(**validated_data)

        if address:
            address_serializer = PublicAddressSerializer(data=address)
            address_serializer.is_valid(True)
            new_address = address_serializer.save()
            person_obj.addresses.add(new_address)

        person_obj.clients.add(BurialGroundSite.get_client())

        return person_obj

class CompanySerializer(serializers.ModelSerializer):

    current_addresses = serializers.SerializerMethodField()
    previous_addresses = serializers.SerializerMethodField()

    class Meta:
        model = PublicCompany
        fields = ('id', 'name', 'contact_name', 'email', 'phone_number', 'phone_number_2', 'remarks', 'current_addresses', 'previous_addresses')

    def get_current_addresses(self, obj):
        current_addresses = obj.addresses.filter(Q(current=True) & (Q(to_date__isnull=True) | Q(to_date__gte=datetime.now()))).order_by('-from_date')
        return PublicAddressListSerializer(instance=current_addresses, many=True, read_only=True).data

    def get_previous_addresses(self, obj):
        previous_addresses = obj.addresses.exclude(Q(current=True) & (Q(to_date__isnull=True) | Q(to_date__gte=datetime.now()))).order_by('-from_date')
        return PublicAddressListSerializer(instance=previous_addresses, many=True, read_only=True).data

    def to_internal_value(self, data):
        internal_value = super(CompanySerializer, self).to_internal_value(data)

        if 'address' in data:
            value = data.get('address')
            internal_value.update({
                'address': value
            })

        return internal_value

    def create(self, validated_data):

        address = None

        if 'address' in validated_data:
            address = validated_data.pop('address')

        company_obj = PublicCompany.objects.create(**validated_data)

        if address:
            address_serializer = PublicAddressSerializer(data=address)
            address_serializer.is_valid(True)
            new_address = address_serializer.save()
            company_obj.addresses.add(new_address)

        company_obj.clients.add(BurialGroundSite.get_client())

        return company_obj

class siteReferenceSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer class for fields relating to site reference settings
    """
    class Meta:
        model = siteReferenceSettings
        fields = ['id', 'ref_style_id', 'burialgroundsite_id', 'start_number']