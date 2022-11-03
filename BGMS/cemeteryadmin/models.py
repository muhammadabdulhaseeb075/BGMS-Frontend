""" Models for cemetryadmin """

import datetime
import json
import uuid

from enum import Enum

from django.db import models
from django.utils import timezone
from django.utils.timezone import make_naive, is_naive
from django.contrib.postgres.fields import JSONField

from bgsite.models import Person, Burial, AuthorityForInterment, Official, MeetingLocation, ReservedPlot
from cemeteryadmin.managers import CalendarEventsManager
from cemeteryadmin.utils import python_time_to_display_string, python_date_to_display_string
from main.models_abstract import  CreatedEditedFields
from main.models import BurialGroundSite, FuneralDirector, siteReferenceSettings, ReferenceNumStyles
from django.db import connection



class EventCategory(models.Model):
    """
    Categories of events i.e. funerals and diggings (user can not add or remove from this table)
    """
    name = models.CharField(primary_key=True, max_length=30, editable=False)
    booking_buffer_duration = models.IntegerField(default=0, help_text="Minimum length of time between other bookings in this category")
    simultaneous_bookings = models.IntegerField(default=0, help_text="Number of bookings in this category that can take place simultaneously (including any buffer)")
    max_booking_per_day = models.IntegerField(null=True, blank=True, help_text="Maximum number of bookings in this category that can take place on one day")

    class Meta:
        verbose_name_plural = "Event categories"


class EventType(models.Model):
    """
    Events that occur at this site
    "E.g. burials, cremations, digging
    """

    name = models.CharField(max_length=30)
    event_category = models.ForeignKey('EventCategory', on_delete=models.CASCADE)
    default_duration = models.IntegerField(default=60, verbose_name="Default duration of event in minutes")
    """ Default event length """

    event_earliest_time_mon = models.TimeField(default=datetime.time(10, 00), verbose_name="Earliest start time: Monday", null=True, blank=True)
    """ Earliest time event can begin on a monday """
    event_latest_time_mon = models.TimeField(default=datetime.time(16, 00), verbose_name="Latest end time: Monday", null=True, blank=True)
    """ Latest time event can end on a monday """
    event_earliest_time_tue = models.TimeField(default=datetime.time(10, 00), verbose_name="Earliest start time: Tuesday", null=True, blank=True)
    """ Earliest time event can begin on a tuesday """
    event_latest_time_tue = models.TimeField(default=datetime.time(16, 00), verbose_name="Latest end time: Tuesday", null=True, blank=True)
    """ Latest time event can end on a tuesday """
    event_earliest_time_wed = models.TimeField(default=datetime.time(10, 00), verbose_name="Earliest start time: Wednesday", null=True, blank=True)
    """ Earliest time event can begin on a wednesday """
    event_latest_time_wed = models.TimeField(default=datetime.time(16, 00), verbose_name="Latest end time: Wednesday", null=True, blank=True)
    """ Latest time event can end on a wednesday """
    event_earliest_time_thu = models.TimeField(default=datetime.time(10, 00), verbose_name="Earliest start time: Thursday", null=True, blank=True)
    """ Earliest time event can begin on a thursday """
    event_latest_time_thu = models.TimeField(default=datetime.time(16, 00), verbose_name="Latest end time: Thursday", null=True, blank=True)
    """ Latest time event can end on a thursday """
    event_earliest_time_fri = models.TimeField(default=datetime.time(10, 00), verbose_name="Earliest start time: Friday", null=True, blank=True)
    """ Earliest time event can begin on a friday """
    event_latest_time_fri = models.TimeField(default=datetime.time(16, 00), verbose_name="Latest end time: Friday", null=True, blank=True)
    """ Latest time event can end on a friday """
    event_earliest_time_sat = models.TimeField(default=datetime.time(10, 00), verbose_name="Earliest start time: Saturday", null=True, blank=True)
    """ Earliest time event can begin on a saturday """
    event_latest_time_sat = models.TimeField(default=datetime.time(16, 00), verbose_name="Latest end time: Saturday", null=True, blank=True)
    """ Latest time event can end on a saturday """
    event_earliest_time_sun = models.TimeField(default=datetime.time(10, 00), verbose_name="Earliest start time: Sunday", null=True, blank=True)
    """ Earliest time event can begin on a sunday """
    event_latest_time_sun = models.TimeField(default=datetime.time(16, 00), verbose_name="Latest end time: Sunday", null=True, blank=True)
    """ Latest time event can end on a sunday """


class CalendarEvents(CreatedEditedFields):
    """ Calendar events """

    id = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    reference = models.IntegerField(default=1, unique=True)
    event_type = models.ForeignKey(EventType, null=True, on_delete=models.SET_NULL)
    reference_number = models.CharField(max_length=100, null=True, blank=True)
    
    objects = CalendarEventsManager()

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_reference = CalendarEvents.objects.all().aggregate(largest=models.Max('reference'))['largest']
            site = BurialGroundSite.objects.get(schema_name=connection.schema_name)
            try:
                ref_format = siteReferenceSettings.objects.get(burialgroundsite_id=site.id).first()
                try:
                    ref_style = ReferenceNumStyles.objects.get(id=ref_format.ref_style_id).first()
                except ReferenceNumStyles.DoesNotExist:
                    ref_style = None
            except siteReferenceSettings.DoesNotExist:
                ref_format = None
                ref_style = None           

            new_reference = 1
            if ref_style is not None: 
                default_num = ref_format.start_number                        
                if last_reference is not None:                    
                    if last_reference < default_num:
                        new_reference = default_num
                    else:
                        new_reference = last_reference + 1
                else:
                    new_reference = default_num

                refStr = str(new_reference)
                if ref_style.ref_style_format == 'nnnn':                    
                    self.reference_number = refStr.zfill(4)
                elif ref_style.ref_style_format == 'yyyy/nnnn':                    
                    self.reference_number = str(timezone.now().year) + '/' + refStr.zfill(4)
                elif ref_style.ref_style_format == 's/nnnn':
                    self.reference_number = site.schema_name[0] + '/' + refStr.zfill(4)
                elif ref_style.ref_style_format == 's/yyyy/nnnn':
                    self.reference_number = site.schema_name[0] + '/' + str(timezone.now().year) + '/' + refStr.zfill(4)
                else:
                    self.reference_number = refStr
            else:
                if last_reference is not None: 
                    new_reference = last_reference + 1
                self.reference_number = new_reference
            self.reference = new_reference
        super().save(*args, **kwargs)

    def display_date(self):
        site_tz = BurialGroundSite.get_site_timezone()

        if is_naive(self.start):
            start = self.start
        else:
            start = make_naive(self.start, site_tz)

        if is_naive(self.end):
            end = self.end
        else:
            end = make_naive(self.end, site_tz)
        #start = make_naive(self.start, site_tz)
        #end = make_naive(self.end, site_tz)
        #start = self.start
        #end = self.end
            

        # This formating removes leading zero from hour and makes am/pm lowercase
        start_date_time = python_date_to_display_string(start, True) + " " + python_time_to_display_string(start.time())
        end_time = python_time_to_display_string(end.time())

        # if event starts and ends on the same day
        if start.date() == end.date():
            formated_date = start_date_time + " - " + end_time

        # if event starts and ends on different days
        else:
            formated_date = start_date_time + " - " + end.strftime("%A %d %b %Y ") + end_time

        return formated_date

class FuneralEventStatus(Enum):

    # TODO: this is currently duplicated on frontend

    PROVISIONAL = 0
    """ Booking created but not paid for """
    PENDING = 1
    """ Booking created by fd, paid for but not accepted by bereavement services """
    PRE_BURIAL_CHECKS = 2
    """ Booking confirmed and paid for """
    AWAITING_BURIAL = 3
    """ Pre-burial checks completed and awaiting burial """
    POST_BURIAL_CHECKS = 4
    """ Burial has taken place """
    COMPLETED = 5
    """ Post-burial checks completed """
    DECLINED = 6
    """ Booking declined """
    CANCELLED = 7
    """ Booking declined """

class FuneralEventManager(models.Manager):

    def get_queryset(self):

        qs = super(FuneralEventManager, self).get_queryset().all()
        try:
            # find any events that need status updated
            events_without_status = qs.filter(status=FuneralEventStatus.AWAITING_BURIAL.value, calendar_event__start__lte=timezone.now())
            events_without_status.update(status=FuneralEventStatus.POST_BURIAL_CHECKS.value)
        except:
            return super(FuneralEventManager, self).get_queryset()

        return super(FuneralEventManager, self).get_queryset()

class PostburialCheck(models.Model):
  backfill_completed = models.DateTimeField(null=True)
  backfill_completed_by_user = models.CharField(max_length=100, null=True, blank=True)
  plot_inspected = models.DateTimeField(null=True)
  plot_inspected_by_user = models.CharField(max_length=100, null=True, blank=True)
  
  def save(self, *args, **kwargs):
    super(PostburialCheck, self).save(*args, **kwargs)

class Cancelburial(models.Model):
  cancel_reason = models.CharField(max_length=500, null=True, blank=True)
  cancel_date   = models.DateTimeField(null=True)
  
  def save(self, *args, **kwargs):
    super(Cancelburial, self).save(*args, **kwargs)


class PreburialCheck(models.Model):
  grave_details = models.DateTimeField(null=True)
  grave_details_by_user = models.CharField(max_length=100, null=True, blank=True)
  grave_on_ground = models.DateTimeField(null=True)
  grave_on_ground_by_user = models.CharField(max_length=100, null=True, blank=True)
  notice_of_interment = models.DateTimeField(null=True)
  notice_of_interment_by_user = models.CharField(max_length=100, null=True, blank=True) 
  burial_certificate = models.DateTimeField(null=True)
  burial_certificate_by_user = models.CharField(max_length=100, null=True, blank=True) 
  noi_details = models.DateTimeField(null=True)
  noi_details_by_user = models.CharField(max_length=100, null=True, blank=True) 
  burial_grant_noi = models.DateTimeField(null=True)
  burial_grant_noi_by_user = models.CharField(max_length=100, null=True, blank=True) 
  indemnity = models.DateTimeField(null=True)
  indemnity_by_user = models.CharField(max_length=100, null=True, blank=True) 
  gravedigger = models.DateTimeField(null=True)
  gravedigger_by_user = models.CharField(max_length=100, null=True, blank=True) 
  signed_off = models.DateTimeField(null=True)
  signed_off_by_user = models.CharField(max_length=100, null=True, blank=True) 
  invoice = models.DateTimeField(null=True)
  invoice_by_user = models.CharField(max_length=100, null=True, blank=True) 

  def save(self, *args, **kwargs):
    super(PreburialCheck, self).save(*args, **kwargs)

class FuneralEvent(models.Model):
    """ Funeral events linked to a calendar event """

    STATUS_CHOICES = [
        (FuneralEventStatus.PROVISIONAL.value, 'Provisional'),
        (FuneralEventStatus.PENDING.value, 'Pending'),
        (FuneralEventStatus.PRE_BURIAL_CHECKS.value, 'Pre-Burial Checks'),
        (FuneralEventStatus.AWAITING_BURIAL.value, 'Awaiting Burial'),
        (FuneralEventStatus.POST_BURIAL_CHECKS.value, 'Post-Burial Checks'),
        (FuneralEventStatus.COMPLETED.value, 'Completed'),
        (FuneralEventStatus.DECLINED.value, 'Declined'),
        (FuneralEventStatus.CANCELLED.value, 'Cancelled'),
    ]

    PREBURIAL_CHECKLIST = set([
        'grave_details',
        'grave_on_ground',
        'notice_of_interment',
        'burial_certificate',
        'noi_details',
        'burial_grant_noi',
        'indemnity',
        'gravedigger',
        'signed_off',
        'invoice'
    ])

    POSTBURIAL_CHECKLIST = set([
        'backfill_completed',
        'plot_inspected'
    ])

    calendar_event = models.OneToOneField(CalendarEvents, primary_key=True, on_delete=models.CASCADE, related_name="funeral_event")
    funeral_director = models.ForeignKey(Official, on_delete=models.SET_NULL, null=True)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    burial = models.ForeignKey(Burial, on_delete=models.SET_NULL, null=True)
    reservation = models.ForeignKey(ReservedPlot, on_delete=models.SET_NULL, blank=True, null=True)
    authority_for_interment = models.ForeignKey(AuthorityForInterment, related_name='authority_for_interment', on_delete=models.SET_NULL, null=True)
    
    preburial_checklist = models.CharField(max_length=500, null=True, blank=True)
    """ Pre-burial Checklist: json containing ids of check items (currently hardcoded on frontend for now) """
    postburial_checklist = models.CharField(max_length=500, null=True, blank=True)
    """ Post-burial Checklist: json containing ids of check items (currently hardcoded on frontend for now) """
    status = models.IntegerField(choices=STATUS_CHOICES, default=FuneralEventStatus.PROVISIONAL.value)
    objects = FuneralEventManager()
    preburial_check = models.ForeignKey(PreburialCheck, on_delete=models.SET_NULL, null=True, blank=True)
    postburial_check = models.ForeignKey(PostburialCheck, on_delete=models.SET_NULL, null=True, blank=True)
    cancelburial     = models.ForeignKey(Cancelburial, on_delete=models.SET_NULL, null=True, blank=True)
    meeting_location = models.ForeignKey(MeetingLocation, related_name='meeting', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
      super(FuneralEvent, self).save(*args, **kwargs)
    
class Settings(models.Model):
    class Meta:
        verbose_name_plural = "settings"
    name = models.CharField(max_length=200)
    preferences = JSONField()
 
    def __str__(self):
        return self.name
