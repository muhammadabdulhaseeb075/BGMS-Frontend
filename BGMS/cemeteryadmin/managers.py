import datetime
import pytz

from datetime import timedelta  

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils import timezone
from django.utils.timezone import make_aware, make_naive,is_naive

from cemeteryadmin.utils import python_time_to_display_string
from main.models import BurialGroundSite

def do_times_overlap(start_time_1, end_time_1, start_time_2, end_time_2):

    return ((start_time_1 >= start_time_2 and start_time_1 < end_time_2)
        or (end_time_1 > start_time_2 and end_time_1 < end_time_2)
        or (start_time_1 < start_time_2 and end_time_1 > start_time_2))

class CalendarEventsManager(models.Manager):
    def validate_event_datetime(self, start, end, event_type_id, event_id, status=None):

        site_tz = BurialGroundSite.get_site_timezone()

        # TODO this should be true for funeral directors
        # Possibly need a preference for bereavement staff
        enforce_time_restrictions = False

        event_types = cemeteryadmin_models.EventType.objects.filter(id=event_type_id).prefetch_related('event_category')

        if not event_types.exists():
            raise ValidationError("Event type does not exist")
        else:
            event_type = event_types[0]

        start_tz_aware = make_aware(datetime.datetime(start.year, start.month, start.day, start.hour, start.minute), site_tz)
        end_tz_aware = make_aware(datetime.datetime(end.year, end.month, end.day, end.hour, end.minute), site_tz)

        # if event already exists
        if event_id:
            calendar_obj = self.get(id=event_id)

            # Get saved datetime
            start_saved = calendar_obj.start.astimezone(site_tz)
            end_saved = calendar_obj.end.astimezone(site_tz)

            """ Validate: datatime can only be changed if event hasn't happened yet and not cancelled"""
            if status and status > 3:

                # if datetime has been changed
                if start_tz_aware != start_saved or end_tz_aware != end_saved:
                    raise ValidationError("Past event's datetime cannot be changed")
                # if datetime has not changed
                else:
                    return True
        
        """ Validate: event must be in the future """
        if (not event_id or (start_tz_aware != start_saved or end_tz_aware != end_saved)) and start_tz_aware <= make_aware(datetime.datetime.now() - timedelta(days = 1),site_tz):
           
            # if new event or datetime has changed and the new datetime is in the past
            raise ValidationError("Event must start in the future")

        """ Validate: event must start and finish on same day """
        if start.date() != end.date():
            raise ValidationError("Event must start and finish on the same day")

        """ Validate: start time must be earlier than end time """
        if start.time() > end.time():
            raise ValidationError("Event\'s start time must be before it\'s end time")

        if enforce_time_restrictions:
            day_of_week_abr = start.strftime('%a').lower()
            earliest_time = getattr(event_type, 'event_earliest_time_' + day_of_week_abr)
            latest_time = getattr(event_type, 'event_latest_time_' + day_of_week_abr)

            """ Validate: are booking allowed on this day """
            if not earliest_time or not latest_time:
                raise ValidationError("Bookings are not available on a %s" % (start.strftime('%A')))

            """ Validate: start time must not be before open time """
            if start.time() < earliest_time:
                raise ValidationError("Start time cannot be before %s on a %s" % (python_time_to_display_string(earliest_time), start.strftime('%A')))

            """ Validate: end time must not be after close time """
            if end.time() > latest_time:
                raise ValidationError(
                    "End time cannot be after %s on a %s"  % (latest_time.strftime('%I:%M%p').lower(), start.strftime('%A')))

        day_start_tz_aware = make_aware(datetime.datetime(start.year, start.month, start.day, 0, 0), site_tz)
        # Convert time to same timezone as db server
        day_start_local = day_start_tz_aware.astimezone(pytz.timezone(settings.TIME_ZONE))
        day_end_local = day_start_local + timedelta(1)

        # find events that are in same day
        events_in_same_category = self.filter(start__gte=day_start_local, start__lt=day_end_local, event_type__event_category=event_type.event_category)

        if event_id:
            # if this is an existing event that is moving time or date, exclude it from the validation
            events_in_same_category = events_in_same_category.exclude(id=event_id)

        # if events exist on this same day
        if events_in_same_category.exists():
            
            if event_type.event_category.booking_buffer_duration > 0 or event_type.event_category.simultaneous_bookings:

                start_time_with_buffer = start - timedelta(minutes=event_type.event_category.booking_buffer_duration)
                end_time_with_buffer = end + timedelta(minutes=event_type.event_category.booking_buffer_duration)

                simultaneous_bookings = 0

                for other_event in events_in_same_category:
                    if is_naive(other_event.start):
                        other_event_start = other_event.start
                    else:
                        other_event_start = make_naive(other_event.start, site_tz)
                    if is_naive(other_event.end):
                        other_event_end = other_event.end
                    else:
                        other_event_end = make_naive(other_event.end, site_tz)


                    if do_times_overlap(
                        other_event_start.time(), other_event_end.time(), start_time_with_buffer.time(), end_time_with_buffer.time()):
                        simultaneous_bookings += 1

                        """ Validate: must not be more than the maximum simultaneous booking (inc. buffer) """
                        if simultaneous_bookings > event_type.event_category.simultaneous_bookings:
                            msg = ("This event overlaps an event with: start time %s; end time %s"
                                % (python_time_to_display_string(other_event_start.time()), python_time_to_display_string(other_event_end.time())))

                            if event_type.event_category.booking_buffer_duration > 0:
                                msg += "; buffer duration %i minutes" % event_type.event_category.booking_buffer_duration

                            raise ValidationError(msg)

        return True

from cemeteryadmin import models as cemeteryadmin_models