from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Group, AbstractBaseUser,\
    PermissionsMixin, UserManager
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db import models
from django.core import validators
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

from django.utils.http import urlsafe_base64_decode

from fuzzywuzzy import fuzz
from mail_templated import send_mail
from tenant_schemas.models import TenantMixin
from tenant_schemas.utils import schema_context

from BGMS.utils import date_elements_to_full_date, scorer, sort_list_by_score, fuzzy_search, get_display_name_from_firstnames_lastname, rename_queryset_value, fuzzy_search_fullname
from main.templatetags.zstaticfiles import static_sign
from main.models_abstract import  CreatedEditedFields
from main.validators import bleach_validator

import datetime
import random
import json
import pytz
import uuid

json.encoder.FLOAT_REPR = lambda o: format(o, '.2f')

class Address(models.Model):
    """
    Represents an address, the only field rquired is first_line.
    """
    first_line = models.CharField(max_length=200, null=True, blank=True)
    """First line"""
    second_line = models.CharField(max_length=200, null=True, blank=True)
    """Second line"""
    town = models.CharField(max_length=50, null=True, blank=True)#get from webservice
    """Town/Village"""
    county = models.CharField(max_length=50, null=True, blank=True)#get from webservice
    """County"""
    postcode = models.CharField(max_length=10, null=True, blank=True)
    """Postcode"""
    country = models.CharField(max_length=50, null=True, blank=True)#get from webservice
    """County"""
    current = models.BooleanField(default=True)
    """True if this is a current address"""
    from_date = models.DateField(null=True, blank=True)
    """Date address became current. Incorrect if impossible_date is True. Populated in save override."""
    impossible_from_date = models.BooleanField(default=False, editable=False)
    """True if from date is an impossible date, default = False"""
    from_date_day = models.IntegerField(null=True, blank=True)
    """Day address became current"""
    from_date_month = models.IntegerField(null=True, blank=True)
    """Month address became current"""
    from_date_year = models.IntegerField(null=True, blank=True)
    """Year address became current"""
    to_date = models.DateField(null=True, blank=True)
    """Date address ended being current. Incorrect if impossible_date is True. Populated in save override."""
    impossible_to_date = models.BooleanField(default=False, editable=False)
    """True if to date is an impossible date, default = False"""
    to_date_day = models.IntegerField(null=True, blank=True)
    """Day address ended being current"""
    to_date_month = models.IntegerField(null=True, blank=True,)
    """Month address ended being current"""
    to_date_year = models.IntegerField(null=True, blank=True)
    """Year address ended being current"""

    def __str__(self):
        return '{0}, {1}, {2}, {3}'.format(self.first_line, self.town, self.county, self.postcode)

    def save(self, **kwargs):

        full_date,impossible_date = date_elements_to_full_date(self.from_date_day, self.from_date_month, self.from_date_year)
        self.from_date = full_date
        self.impossible_from_date = impossible_date

        full_date_to,impossible_date_to = date_elements_to_full_date(self.to_date_day, self.to_date_month, self.to_date_year)
        self.to_date = full_date_to
        self.impossible_to_date = impossible_date_to

        super(Address, self).save()

    def get_address(self):
        """
        Returns the site address for the site in a dictionary
        """
        return {'first_line': self.first_line, 'town': self.town, 'county': self.county, 'postcode': self.postcode,'second_line': self.second_line}


class SiteDetails(models.Model):
    """
    Contains details related to a particular site, including the center point and zoom level
    to initiate the  map once the application is loaded. It also include the parameters to use
    WMTS service and load the aerial image.
    """
    class Meta:
        verbose_name_plural = "Site Details"

    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    """Endpoint for the WMST service, where the Aerial image is being tailed."""
    layer = models.CharField(max_length=20, null=True, help_text='WMTS Layer name / Schema name', verbose_name="Schema name")
    """Layer of the WMST service"""
    extent = models.CharField(max_length=300, null=True, help_text='Extend for the tile grid')
    """Extend for the tile grid, also used to find centre of site and set initial zoom by openlayers."""
    aerial = models.BooleanField(default=True, verbose_name="Aerial?")
    """Checkbox that identify whether there is aerial for the site or not"""
    plans = models.BooleanField(default=False, verbose_name="Plans?")
    """Checkbox that identify whether there is plans for the site or not"""

    @property
    def name(self):
        return self.burialgroundsite.name

    def __str__(self):
        return self.name + ', '+ self.burialgroundsite.schema_name


class Client(models.Model):
    """
    A client will be the parent of one or more sites.
    Some data will be shared between sites in a client.
    """
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class BurialGroundSite(TenantMixin):
    """
    This table contains the Sites configurations, which extends from TenantMixin in order to allow
    a different schema in the database per site. This model includes:
    - Domain URL: The subdomain assign for the site
    - Schema name: The schema will be created with this name, and the subdomain will trigger this schema along with the main schema.
    """
    name = models.CharField(max_length=100, verbose_name="burial ground site name")
    """Name, max length = 100"""
    client = models.ForeignKey(Client, help_text="Parent client that this site belongs to", related_name="sites", on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True, help_text="Date the site is added")
    """Date the site is added."""
    site_details = models.OneToOneField(SiteDetails, null=True, on_delete=models.CASCADE)

    def get_site_domain_url(self):
        """
        Returns the domain_url for a site
        """
        if settings.DEBUG:
            # post number needed for dev
            #url = "https://{0}:8000"
            url = "https://{0}"
        else:
            url = "https://{0}"

            if hasattr(settings, 'STAGING_PORT'):
                # post number needed for staging
                url += ':' + str(settings.STAGING_PORT)

        return url.format(self.domain_url)

    @classmethod
    def get_site_details(cls):
        """
        Returns the site details in a dictionary (name, address) for the connection that has been established.
        """
        site = BurialGroundSite.objects.get(schema_name=connection.schema_name)
        # import pdb; pdb.set_trace()

        if site and site.schema_name == 'public':
            return {'name': site.name, 'homepage': settings.HOMEPAGE}
        else:
            return {'name': site.name, 'address': site.get_address(), 'homepage': settings.HOMEPAGE}

    @classmethod
    def get_site_documents(cls):
        """
        Returns the site documents in a dictionary
        """
        # import pdb; pdb.set_trace()
        return {'user_guide': static_sign('docs/BGMS_User_Guide.pdf'), 'public_user_guide': static_sign('docs/BGMS_Public_User_Guide.pdf'), 'privacy_notice': static_sign('docs/BGMS_Privacy_Notice.pdf'), 'terms_conditions': static_sign('docs/BGMS_Terms_Conditions.pdf')}

    @classmethod
    def get_domain_url(cls):
        """
        Returns the domain_url for the connection that has been established.
        """
        site = BurialGroundSite.objects.get(schema_name=connection.schema_name)
        return "https://{0}".format(site.domain_url)

    @classmethod
    def get_public_url(cls):
        """
        Returns the public_url.
        """
        site = BurialGroundSite.objects.get(schema_name='public')
        return "https://{0}".format(site.domain_url)

    @classmethod
    def get_login_domain_url(cls):
        """
        Returns the login domain_url for the connection that has been established.
        """
        return BurialGroundSite.get_domain_url() + '/login/'

    @classmethod
    def get_register_domain_url(cls):
        """
        Returns the register domain_url for the connection that has been established.
        """
        return BurialGroundSite.get_public_url() + '/register/'

    @classmethod
    def get_name(cls):
        """
        Returns the site name for the connection that has been established.
        """
        site = BurialGroundSite.objects.get(schema_name=connection.schema_name)
        return site.name

    @classmethod
    def get_client(cls):
        """
        Returns the client for the connection that has been established.
        """
        site = BurialGroundSite.objects.get(schema_name=connection.schema_name)
        return site.client

    @classmethod
    def get_client_sites(cls):
        """
        Returns all sites that belong to the client for the connection that has been established.
        """
        client = BurialGroundSite.objects.get(schema_name=connection.schema_name).client
        return client.sites.all().values('schema_name', 'name')

    @classmethod
    def get_site_timezone(cls):
        """
        Returns the site timezone for the connection that has been established.
        """
        site = BurialGroundSite.objects.get(schema_name=connection.schema_name)
        return pytz.timezone(site.site_details.site_preferences.site_timezone)

    @classmethod
    def site_has_public_access(cls):
        """
        True if this site has public access
        """
        site = BurialGroundSite.objects.get(schema_name=connection.schema_name)
        return site.site_details.site_preferences.public_access

    def __str__(self):
        return self.schema_name + ';' + self.domain_url

    def get_address(self):
        """
        Returns the site address for the site
        """
        if self.site_details.address:
            return self.site_details.address.get_address()
        else:
            return {}

    def get_map_initialization_details(self):
        #layer = self.schema_name.capitalize()

        urlTemplate = '/wmts/%s/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png'
        layer = self.site_details.layer

        aerialURL = None
        plansURL = None

        if self.site_details.aerial:
            aerialURL = settings.AERIAL_SERVER_URL + urlTemplate % layer

        if self.site_details.plans:
            plansURL = settings.PLANS_SERVER_URL + urlTemplate % (layer + "plans")

        return {'name': self.name, 'aerialURL': aerialURL, 'plansURL':plansURL, 'baseMapUrl':settings.BASE_SERVER_URL, 'layer':layer, 'style':'default', 'extent': self.site_details.extent, 'resolutions': settings.RESOLUTIONS, 'matrixIds':settings.MATRIXIDS}

    def create_sitegroups(self):
        """
        Create site groups per feature
        """
        groups = Group.objects.all()
        for group in groups:
            SiteGroup.objects.update_or_create(group=group, burialgroundsite=self)
    
    def get_single_site_admin_user(self):
        """
        Gets the first available active SiteAdmins belonging to this site
        """

        # get SiteAdmin SiteGroup belonging to this site
        admin_site_group = SiteGroup.objects.filter(burialgroundsite__schema_name__exact=self.schema_name).filter(group__name='SiteAdmin')

        if admin_site_group.exists():
            admin_site_group = admin_site_group.first()

            # get active users belonging to SiteAdmin SiteGroup
            site_admins = BGUser.objects.filter(is_active=True,_is_staff=False, site_groups__in=[admin_site_group])

            if site_admins.exists():
                # This is what we need, so return it.
                # Note: this could actually be the current user if they themselves are a SiteAdmin.
                return site_admins.first()
        
        return None


class SitePreferences(models.Model):

    TIMEZONES = [
        ('Europe/London', 'Europe/London'),
    ]

    """
    This table contains the Sites preferences
    """
    site_color = models.CharField(max_length=7, null=True)
    """ Colour used to identify this site """
    site_timezone = models.CharField(max_length=100, choices=TIMEZONES, default='Europe/London')
    """ This site's timezone (currently only one option) """
    site_details = models.OneToOneField(SiteDetails, null=True, on_delete=models.CASCADE, related_name="site_preferences")
    public_access = models.BooleanField(default=False, help_text=('If true, a restricted site will be available to the public without needing to log in.'))


class SiteManager(models.Manager):
    def get_queryset(self):
        if connection.schema_name=='public':
            return super(SiteManager, self).get_queryset()
        else:
            return super(SiteManager, self).get_queryset().filter(burialgroundsite__schema_name__exact=connection.schema_name)


class SiteGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    burialgroundsite = models.ForeignKey(BurialGroundSite, on_delete=models.CASCADE, related_name="site_groups")
    objects = SiteManager()
    def __str__(self):
        return self.burialgroundsite.name + ';'+ self.burialgroundsite.schema_name + ';' + self.group.name


class SiteGroupSite(SiteGroup):
    class Meta:
        proxy = True

    def __str__(self):
        return self.group.name

#custom user model

class BGUserManager(UserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        return UserManager.create_user(self, username, email=email, password=password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        return UserManager.create_superuser(self, username, email, password, **extra_fields)


class BGUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(('username'), max_length=30, unique=True, null=True,
        help_text=('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$', ('Enter a valid username.'), 'invalid')
        ], error_messages={'unique': 'User with this username already exists.'})
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    email = models.EmailField(('email address'), unique=True, help_text=('Required.'), error_messages={'unique': 'User with this email already exists.'})
    _is_staff = models.BooleanField(('staff status'), default=False,
        help_text=('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(('active'), default=True,
        help_text=('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)
    site_groups = models.ManyToManyField(SiteGroup, blank=True)

    objects = BGUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
            verbose_name = "User"
            verbose_name_plural = "Users"

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, template, extra_context):
        """
        Sends an email to this User.
        subject: String
        template: url to the .tpl File
        extra_context: Dictionary with extra context used by the template
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]
        context_basic = {'username': self.username, 'full_name': self.get_full_name(), 'signup_date':self.date_joined, 'subject_text': subject}
        context_dict = context_basic.copy()
        context_dict.update(extra_context)
        # print(context_dict)
        #Send text mail
        # send_mail(subject, message, from_email, recipient_list,fail_silently=False,auth_user=None, auth_password=None,connection=None, html_message=None)

        #Send HTML mail using django templates
        send_mail(template, context_dict, from_email, recipient_list)

    def in_site_groups(self, group_name):
        """ Returns true if user belongs to permission group for connection schema """

        return self.site_groups.filter(burialgroundsite__schema_name__exact=connection.schema_name).filter(group__name=group_name).exists()

    def in_schema_site_groups(self, group_name, schema_name):
        """ Returns true if user belongs to permission group for given schema """

        return self.site_groups.filter(burialgroundsite__schema_name__exact=schema_name).filter(group__name=group_name).exists()

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_superuser | self.in_site_groups('SiteAdmin') | self._is_staff

    def has_data_entry_permission(self, schema_name):
        """Does user have permission to access data entry?"""
        return self.is_superuser | self.in_schema_site_groups('SiteAdmin', schema_name) | self.in_schema_site_groups('SiteWarden', schema_name) | self.in_schema_site_groups('DataEntry', schema_name)

    def has_data_matcher_permission(self, schema_name):
        """Does user have permission to access data matching?"""
        return self.is_superuser | self.in_schema_site_groups('SiteAdmin', schema_name) | self.in_schema_site_groups('SiteWarden', schema_name) | self.in_schema_site_groups('DataMatcher', schema_name)

    def has_site_admin_permission(self, schema_name):
        """Does user have permission to access data matching?"""
        return self.is_superuser | self.in_schema_site_groups('SiteAdmin', schema_name)

    def has_bereavement_staff_permission(self, schema_name):
        """Does user have bereavement staff permission?"""
        return self.is_superuser | self.in_schema_site_groups('BereavementStaff', schema_name)

    @property
    def is_staff_anywhere(self):
        # is_staff works on a per-schema basis, this method will search over
        # all schemas

        isa = self.is_superuser | self._is_staff
        if not isa:
            with schema_context('public'):
            # Not immediately obvious this person is staff. Go public and try to see if they're a SiteAdmin anywhere else...
                isa = self.site_groups.filter(group__name='SiteAdmin').exists()

        return isa

    def remove_all_site_groups_for_schema(self, schema_name):
        sgs = self.site_groups.filter(burialgroundsite__schema_name__exact=schema_name)
        for sg in sgs:
            self.site_groups.remove(sg)

    def add_me_current_site_connection(self):
        """
        Adds the user to the SiteUser sitegroup for the current connection
        schema and activates the user
        """
        site_group_to_add = SiteGroup.objects.filter(burialgroundsite__schema_name__exact=connection.schema_name).filter(group__name='SiteUser').first()
        self.site_groups.add(site_group_to_add)
        self.is_active = True
        self.save()

    def get_password_authorizer(self):
        """
        If a user is staff, AG admins can authorize their password reset
        requests. Otherwise, the site administrator for the site that they
        are now affiliated with can authorize their password reset.
        """

        message = ''
        admin_email = None

        # Don't actually send email to site admin if dev or staging

        if self.is_staff_anywhere:
            if settings.DEBUG or hasattr(settings, 'STAGING_PORT'):
                message = "*** Testing on dev or staging. ***"

            # "Staff" (site admin anywhere) go to AG. We authorize their resets.
            message += "You are receiving this email because the user in question is a SiteAdmin."
            admin_email = settings.EMAIL_AG_ADMIN

        else:
            # Site managers do it.

            if connection.schema_name != 'public':
                # get admin from current site
                site = BurialGroundSite.objects.get(schema_name=connection.schema_name)
                site_admin = site.get_single_site_admin_user()
            else:
                # get admin from a site this user belongs to (i.e. this is not being accessed from a subdomain)
                site_admin = self.get_admin_user_for_user()

            message = ""

            if settings.DEBUG or hasattr(settings, 'STAGING_PORT'):
                message = "*** Testing on dev or staging. ***  "

            if site_admin:
                message += "You are receiving this email because you are registered as a site administrator for this user. Please log in to your BGMS and visit the Admin Portal to issue a new password.\n\nIf you have any concerns regarding this email, please reply to this email or contact Atlantic Geomatics on 017684 83310\n\nThank you.\n\nAG BGMS Team"

                if settings.DEBUG or hasattr(settings, 'STAGING_PORT'):
                    message += " [%s]" % (site_admin.email)
                    admin_email = settings.EMAIL_AG_ADMIN
                else:
                    admin_email = site_admin.email

            else:
                # fallback
                message += "You are receiving this email because we have failed to find an appropriate site administrator."
                admin_email = settings.EMAIL_AG_ADMIN

            if settings.DEBUG or hasattr(settings, 'STAGING_PORT'):
                # Don't actually send email to site admin if dev or staging
                admin_email = settings.EMAIL_AG_ADMIN

        return admin_email, message
    
    def get_admin_user_for_user(self):
        """
        Returns an administrator responsible for this user
        """

        if self.site_groups.all():

            # get list of sites this user belongs to
            site_groups = self.site_groups.order_by('burialgroundsite').distinct('burialgroundsite')

            # iterate sites until an admin is found
            for site_group in site_groups.all():

                admin = site_group.burialgroundsite.get_single_site_admin_user()

                if admin:
                    return admin

        return None


# class LinkedBurials(models.Model):
#     burials = models.ForeignKey(Burial)
#     death = models.OneToOneField(Death)
#     burial_site = models.ForeignKey(BurialGroundSite) #how are we implementing this


class RegisteredUser(models.Model):
    """
    Represents the first step for registration.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    """:model:`main.User` associated"""
#     user = models.OneToOneField(User)
    isMailVerified = models.BooleanField(default=False)
    """True: The user has clicked on he link sended to his mail, False: is not yet verified"""
    activation_key = models.CharField(max_length=40, blank=True)
    """Creates an activation key for the user to register"""
    key_expires = models.DateTimeField(default=timezone.now)
    """Set the time of 48 hours to activate the account"""


class Surveyor(models.Model):
    surveyor_name = models.CharField(max_length=100, validators=[bleach_validator])

#site independent bgsite models

class ImageType(models.Model):
    """
    Represents the image type for example::
    - Memorial
    - Burial record
    """
    image_type = models.CharField(max_length=20, validators=[bleach_validator], unique=True)
    """Image type, max length = 20"""


class ImageState(models.Model):
    """Represents the image state"""
    image_state = models.CharField(max_length=15, validators=[bleach_validator], unique=True)
    """Image state, max length = 15"""


class Nicknames(models.Model):
    """Nicknames"""
    nickname = models.CharField(max_length=20, validators=[bleach_validator])
    """Nickname, max length = 20"""
    actual_name = models.CharField(max_length=30, validators=[bleach_validator])
    """Actual name, max length = 30"""


class BurialOfficialTypeQuerySet(QuerySet):
    def get_all(self):
        return [(bot.official_type,bot.official_type) for bot in self.all().exclude(official_type='')]


class BurialOfficialType(models.Model):
    """Burial Official Type"""
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    official_type = models.CharField(max_length=50, validators=[bleach_validator])
    """Official type, max length = 50"""
    objects = BurialOfficialTypeQuerySet.as_manager()

    def __str__(self):
        return self.official_type


class ReservePlotState(models.Model):
    """
    Contains possible states for reserve plot
    """
    state = models.CharField(max_length=20, unique=True)
    """State, max length = 20"""


class RelationshipType(models.Model):
    """
    List of types of relationships between features
    """
    type = models.CharField(max_length=40, unique=True)


class Currency(models.Model):
    """
    List of currencies
    """
    name = models.CharField(max_length=20, validators=[bleach_validator], unique=True)
    symbol = models.CharField(max_length=1, validators=[bleach_validator], null=True, blank=True)
    subunit1_symbol = models.CharField(max_length=1, validators=[bleach_validator], null=True, blank=True)
    subunit2_symbol = models.CharField(max_length=1, validators=[bleach_validator], null=True, blank=True)
    unit_name = models.CharField(max_length=20, validators=[bleach_validator], null=True, blank=True)
    """Name of unit e.g. pounds"""
    subunit1_name = models.CharField(max_length=20, validators=[bleach_validator], null=True, blank=True)
    """Name of subunit e.g. shillings"""
    subunit2_name = models.CharField(max_length=20, validators=[bleach_validator], null=True, blank=True)
    """Name of 2nd subunit e.g. pence"""

    class Meta:
        verbose_name_plural = "Currencies"


""" Filters used for person and company searches """

def _filter_by_email(queryset, email):
    """DRY method to filter by email"""
    email = email.strip()
    return queryset.filter(email=email)

class PublicPersonManager(models.Manager):

    def get_queryset(self):
        """Only include Persons that are linked to this client"""
        return super(PublicPersonManager, self).get_queryset().filter(clients__in=[BurialGroundSite.get_client()])


class PublicPersonQuerySet(QuerySet):

    def _values_queryset(self, search_type=None):
        """DRY method to encapsulate the base values queryset"""

        values = ['id', 'first_names', 'last_name', 'addresses__first_line', 'addresses__town', 'addresses__postcode', 'email']

        if search_type=='owner':
            values.extend(['graves_owned__deed__graveplot__uuid', 'graves_owned__deed__graveplot__topopolygon_id', 'graves_owned__deed__graveplot__topopolygon__layer__feature_code__feature_type'])
            person_queryset = self.exclude(graves_owned__isnull=True).order_by('id', 'graves_owned__deed__graveplot__uuid').distinct('id', 'graves_owned__deed__graveplot__uuid')
        else:
            person_queryset = self.order_by('id').distinct('id')

        person_queryset = person_queryset.values(*values)
        return person_queryset

    def search_persons(self, first_names=None, last_name=None, email=None, fuzzy_value=87, search_type=None):
        """Returns a list for all person who match the search parameters"""
        if (not first_names) and (not last_name) and (not email):
            # if nothing to search for, raise error
            raise ObjectDoesNotExist("Search parameters are null")

        result = self._values_queryset(search_type)

        if((first_names or last_name)):
            key_list = ['id']
            if search_type=='owner':
                key_list += ['graves_owned__deed__graveplot__uuid']
            result = fuzzy_search_fullname(first_names, last_name, result, fuzzy_value, key_list)

        if(email is not None):
            result = _filter_by_email(result, email)

        rename_queryset_value(result, {
            'graves_owned__deed__graveplot__uuid': 'graveplot_uuid', 'graves_owned__deed__graveplot__topopolygon_id': 'topopolygon_id', 'graves_owned__deed__graveplot__topopolygon__layer__feature_code__feature_type': 'graveplot_layer' })

        for value in result:
            value['id'] = str(value['id'])
            value['last_name'] = value['last_name'].upper() if value['last_name'] else None
            value['name'] = get_display_name_from_firstnames_lastname(value['first_names'], value['last_name'])
            value['type'] = 'person'

        return result

class PublicPerson(CreatedEditedFields):
    """
    Person details.
    Note: this is similar, but different, to the Person table in bgsite.
    The difference is that the persons in bgsite are occupants or reserved occupants of that site.
    """
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    clients = models.ManyToManyField(Client)
    """Clients that have permission to access this record"""
    # TODO: ensure that all names taken together are not all null in model save request
    title = models.CharField(max_length=30, validators=[bleach_validator], null=True, blank=True, verbose_name='Title')
    """Title"""
    first_names = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True, verbose_name='First names')
    """First and Second names in the same field"""
    birth_name = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True, verbose_name='Birth name')
    """Birth name"""
    other_names = models.CharField(max_length=100, validators=[bleach_validator], null=True,blank=True, verbose_name='Nicknames')
    last_name = models.CharField(max_length=35, validators=[bleach_validator], null=True,blank=True, verbose_name='Last name')
    """Last name"""
    birth_date = models.DateField(null=True, editable=False)
    """Birth date, format = dd/mm/yyyy. Incorrect if impossible_date is True. Populated in save override."""
    impossible_birth_date = models.BooleanField(default=False, editable=False, help_text="If true means the others day/month/year fields have the non real date entered in the registry for the person")
    """If true means the others day/month/year fields have the non real date entered in the registry for the person"""
    birth_date_day = models.IntegerField(null=True, blank=True, verbose_name="Day of Birth")
    """Day of Birth"""
    birth_date_month = models.IntegerField(null=True, blank=True, verbose_name="Month of Birth")
    """Month of Birth"""
    birth_date_year = models.IntegerField(null=True, blank=True, verbose_name="Year of Birth")
    """Year of Birth"""
    gender = models.CharField(max_length=10, validators=[bleach_validator], null=True, blank=True, verbose_name='Gender')
    """Gender"""
    place_living = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True)
    """ Town/City """
    postcode = models.CharField(max_length=50, validators=[bleach_validator], null=True, blank=True)
    """ PostCode """
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    phone_number_2 = models.CharField(max_length=20, null=True, blank=True)
    remarks = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True, verbose_name='Remarks about Person')
    """Description, max length = 200 characteres"""
    addresses = models.ManyToManyField(Address)
    """:model:`main.Address` associated"""
    from_data_upload = models.BooleanField(default=False)
    """Data upload - true if this paerson was added by a data upload"""
    graves_owned = GenericRelation('bgsite.GraveOwner', related_query_name='person')
    

    objects = PublicPersonManager.from_queryset(PublicPersonQuerySet)()

    def save(self, **kwargs):

        if self.last_name:
            self.last_name = self.last_name.upper()

        full_date,impossible_date = date_elements_to_full_date(self.birth_date_day, self.birth_date_month, self.birth_date_year)
        self.birth_date = full_date
        self.impossible_birth_date = impossible_date

        super(PublicPerson, self).save()

#getter functions
    def get_display_name(self):

        return get_display_name_from_firstnames_lastname(self.first_names, self.last_name)


class CompanyManager(models.Manager):

    def get_queryset(self):
        """Only include Companies that are linked to this client"""
        return super(CompanyManager, self).get_queryset().filter(clients__in=[BurialGroundSite.get_client()])

class CompanyQuerySet(QuerySet):

    def _values_queryset(self, search_type=None):
        """DRY method to encapsulate the base values queryset"""

        values = ['id', 'name', 'addresses__first_line', 'addresses__town', 'addresses__postcode', 'email']

        if search_type=='owner':
            values.extend(['graves_owned__deed__graveplot__uuid', 'graves_owned__deed__graveplot__topopolygon_id', 'graves_owned__deed__graveplot__topopolygon__layer__feature_code__feature_type'])
            company_queryset = self.exclude(graves_owned__isnull=True).order_by('id', 'graves_owned__deed__graveplot__uuid').distinct('id', 'graves_owned__deed__graveplot__uuid')
        else:
            company_queryset = self.order_by('id').distinct('id')

        company_queryset = company_queryset.values(*values)
        return company_queryset

    def _fuzzy_search_name(self, name, queryresult, fuzzy_value, key_list):
        """Returns a list of companies based on fuzzy matching of name returning companies with the higher score as a whole"""
        company_name = []
        fuzziness = fuzzy_value
        if(name):
            name = name.strip()
        # for double-barrel names in search, increase matching score - currently increasing from 60% to 75%
            fuzziness = fuzzy_value
            if (' ' in name) or ('-'in name):
                fuzziness = fuzzy_value/1.25
            company_name = fuzzy_search(name, 'name', queryresult)
            company_name = list(filter(lambda company_score: company_score[1][0] >= fuzziness, company_name))
            if(name):
                #set the queryset for first name search as the last names search result
                queryresult = [company[0] for company in company_name]
        # print(company_name)

        sorted_result = sort_list_by_score(company_name, key_list)
        sorted_result = list(filter(lambda company_score: company_score[1][0] >= fuzziness, sorted_result))
        #print(sorted_result)
        result = [company[0] for company in sorted_result]
        return result

    def search_companies(self, name=None, email=None, fuzzy_value=87, search_type=None):
        """Returns a list for all companies who match the search parameters"""
        if (not name) and (not email):
            # if nothing to search for, raise error
            raise ObjectDoesNotExist("Search parameters are null")

        result = self._values_queryset(search_type)

        if(name):
            key_list = ['id']
            if search_type=='owner':
                key_list += ['graves_owned__deed__graveplot__uuid']
            result = self._fuzzy_search_name(name, result, fuzzy_value, key_list)

        if(email is not None):
            result = _filter_by_email(result, email)

        rename_queryset_value(result, {
            'graves_owned__deed__graveplot__uuid': 'graveplot_uuid', 'graves_owned__deed__graveplot__topopolygon_id': 'topopolygon_id', 'graves_owned__deed__graveplot__topopolygon__layer__feature_code__feature_type': 'graveplot_layer' })

        for value in result:
            value['id'] = str(value['id'])
            value['type'] = 'company'
        return result


class Company(CreatedEditedFields):
    """
    Company details
    """
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    clients = models.ManyToManyField(Client)
    """Clients that have permission to access this record"""
    name = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True, verbose_name='Company name')
    contact_name = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True, verbose_name='Contact name')
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    phone_number_2 = models.CharField(max_length=20, null=True, blank=True)
    remarks = models.CharField(max_length=200, validators=[bleach_validator], null=True, blank=True, verbose_name='Remarks about company')
    addresses = models.ManyToManyField(Address)
    """:model:`main.Address` associated"""
    persons = models.ManyToManyField(PublicPerson)
    """Persons associated with company"""
    from_data_upload = models.BooleanField(default=False)
    """Data upload - true if this paerson was added by a data upload"""
    graves_owned = GenericRelation('bgsite.GraveOwner', related_query_name='company')
    objects = CompanyManager.from_queryset(CompanyQuerySet)()


class FuneralDirector(CreatedEditedFields):
    """
    Funeral Director model.
    Note one to one with Company.
    Funeral Director may also be a BGMS user.
    """
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    retired = models.BooleanField(default=False)

    @classmethod
    def get_funeral_directors_in_current_client(cls):
        """
        Returns all funeral directors for the client of the connection that has been established.
        """
        return FuneralDirector.objects.filter(company__clients=BurialGroundSite.get_client())


class UserPasswordRequests(models.Model):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    date_update = models.DateTimeField(auto_now=True, null=True)
    count = models.IntegerField(null=True, blank=True, default=0)
    status = models.TextField(max_length=20, validators=[bleach_validator], null=False, default="Open")

    def set_status(self, new_status):
        self.status = new_status
        self.save()

    def increment_count(self):
        self.count += 1

    def make_fresh(self):
        self.date = timezone.now()
        self.set_status("Open")

    def make_complete(self):
        self.increment_count()
        self.set_status("Reset complete")
        self.save()

    def authorize_reset(self):
        # Import here so that the auth model is known.
        from django.contrib.auth.forms import PasswordResetForm

        reset_form = PasswordResetForm({'email': self.user.email})

        if reset_form.is_valid():

            self.set_status("Actioned")
            domain_url = settings.HOMEPAGE.replace('http://', '').replace('https://', '')
            use_https = not(settings.DEBUG)

            reset_form.save(domain_override=domain_url,
                subject_template_name='mail_templated/password_reset_subject.txt',
                use_https=use_https,
                from_email=settings.DEFAULT_FROM_EMAIL,
                html_email_template_name='mail_templated/email_reset_link.tpl')

    @classmethod
    def active_reqs_staff(cls):
        # AG Admins see everything.
        reqs = UserPasswordRequests.objects.exclude(status="Reset complete")
        for_staff_ids = [req.id for req in reqs]
        return UserPasswordRequests.objects.filter(id__in=for_staff_ids)

    @classmethod
    def active_reqs_admins(cls):
        # admins need to have additional schema filters.
        reqs = UserPasswordRequests.objects.exclude(status="Reset complete").filter(user__site_groups__burialgroundsite__schema_name=connection.schema_name)
        for_staff_ids = [req.id for req in reqs if req.user.is_staff == False]
        return UserPasswordRequests.objects.filter(id__in=for_staff_ids)

    @classmethod
    def inactive_reqs_staff(cls):
        # AG Admins see everything.
        reqs = UserPasswordRequests.objects.filter(status="Reset complete")
        for_staff_ids = [req.id for req in reqs]
        return UserPasswordRequests.objects.filter(id__in=for_staff_ids)

    @classmethod
    def inactive_reqs_admins(cls):
        # admins need to have additional schema filters.
        reqs = UserPasswordRequests.objects.filter(status="Reset complete").filter(user__site_groups__burialgroundsite__schema_name=connection.schema_name)
        for_staff_ids = [req.id for req in reqs if req.user.is_staff == False]
        return UserPasswordRequests.objects.filter(id__in=for_staff_ids)


class ReportTemplate(models.Model):
    name = models.CharField(max_length=100)
    table_schema = JSONField()
    creation_date = models.DateTimeField(auto_now_add=True)

class ReferenceNumStyles(models.Model):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    ref_style_format = models.CharField(max_length=500, null=True, blank=True)
    re_style_sample = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.ref_style_format + ' (' + self.re_style_sample + ')'

class siteReferenceSettings(models.Model):
    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    ref_style = models.ForeignKey(ReferenceNumStyles, on_delete=models.CASCADE, null=True)
    burialgroundsite = models.ForeignKey(BurialGroundSite, on_delete=models.CASCADE)
    start_number = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return self.ref_style.ref_style_format + ' (' + self.ref_style.re_style_sample + ')'