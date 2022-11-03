import moment from 'moment';
import { DISPLAY_TIME_MOMENT_FORMAT, DISPLAY_DATETIME_WITH_DAYNAME_MOMENT_FORMAT } from '@/global-static/dataFormattingAndValidation.ts';

const IRREGULAR_BOOKING_WARNING: string = "Warning: this is outside the normal booking times";

/**
 * @param { string } currentStartDatetime Event's start time (ISOString)
 * @param { number } duration Duration of event in minutes
 * @returns { string } ISOString for end datetime
 */
export function convertStartDatetimeAndDurationToEndDatetime(startDatetime: string, duration: number): string {

  let newEnd: moment.Moment = moment(startDatetime);
  newEnd.add(duration, 'm');
  return newEnd.format("YYYY-MM-DDTHH:mm");
}

interface EventValidationResult {
  strict: boolean;
  title: string;
  detail: string;
}

/**
 * Validate event's date
 * @param {moment} start 
 * @param eventType 
 * @param otherEvents Other events in the same event type category and same day
 * @param enforceTimeRestrictions 
 */
export function validateEventDate(start: moment.Moment, eventType, otherEvents: [], enforceTimeRestrictions: boolean): EventValidationResult {
  let returnValue = { strict: false, title: '', detail: '' };

  /** Validate: booking must be in future
   */
  if (!start.isAfter(moment())) {
    returnValue.strict = true;
    returnValue.title = "The booking must be in the future";
    return returnValue;
  }

  /** Validate: must not already be max number of bookings (if max exists)
   * 
   *  Note: this will not work for rare cases when this month's events have not been loaded.
   *  But validation will then happen on the server.
   */
  if (otherEvents && eventType['event_category__max_booking_per_day'] && eventType['event_category__max_booking_per_day'] <= otherEvents.length) {
    returnValue.strict = true;
    returnValue.title = "The maximum number of bookings for this day has already been reached";
    return returnValue;
  }

  /** Validate: are booking allowed on this day */

  const dayOfWeekAbr = start.format("ddd").toLowerCase();
  const earliestTime = eventType['event_earliest_time_' + dayOfWeekAbr];
  const latestTime = eventType['event_latest_time_' + dayOfWeekAbr];

  if (!earliestTime || !latestTime) {
    returnValue.strict = enforceTimeRestrictions;

    if (enforceTimeRestrictions) {
      returnValue.title = "Bookings are not available on a " + start.format("dddd");
    }
    else {
      returnValue.title = IRREGULAR_BOOKING_WARNING;
      returnValue.detail = "Bookings are not normally available on a " + start.format("dddd") + ".";
    }
    return returnValue;
  }
  
  return null;
}

/**
 * 
 * @param {moment} start 
 * @param {moment} end 
 * @param eventType 
 * @param otherEvents Other events in the same event type category and same day
 * @param enforceTimeRestrictions 
 */
export function validateEventTime(start: moment.Moment, end: moment.Moment, eventType, otherEvents, enforceTimeRestrictions: boolean): EventValidationResult {
  let returnValue = { strict: false, title: '', detail: '' };

  /* Validate: event must start and finish on same day */
  if (!start.isSame(end, 'day') || !start.isSame(end, 'month') || !start.isSame(end, 'year')) {
    returnValue.strict = true;
    returnValue.title = "Event must start and finish on the same day";
    return returnValue;
  }

  /* Validate: start time must be earlier than end time */
  if (end.isBefore(start)) {
    returnValue.strict = true;
    returnValue.title = "Event's start time must be before it's end time";
    return returnValue;
  }

  if (otherEvents && otherEvents.length) {
    /** Validate: must not be more than the maximum simultaneous booking (inc. buffer)
     * 
     *  Note: this will not work for rare cases when this month's events have not been loaded.
     *  But validation will then happen on the server.
     */

    const bookingBufferDuration = eventType['event_category__booking_buffer_duration'];
    const maxSimultaneousBookings = eventType['event_category__simultaneous_bookings'];

    if (bookingBufferDuration > 0 || maxSimultaneousBookings) {
      const startWithBuffer = start.clone().subtract(bookingBufferDuration, 'minutes');
      const endWithBuffer = end.clone().add(bookingBufferDuration, 'minutes');

      let simultaneousBookings: number = 0;
      let msg = null;

      for (let i = 0; i < otherEvents.length; i++) {

        let otherEvent = otherEvents[i];
    
        // check if events overlap
        const otherEventStart = moment(otherEvent.start);
        const otherEventEnd = moment(otherEvent.end);
        
        if (otherEventStart.isBetween(startWithBuffer, endWithBuffer, null, '[)')
          || otherEventEnd.isBetween(startWithBuffer, endWithBuffer, null, '[)')) {
            
          simultaneousBookings += 1;

          if (simultaneousBookings > maxSimultaneousBookings) {
            msg = `Other event: start time ${otherEventStart.format(DISPLAY_DATETIME_WITH_DAYNAME_MOMENT_FORMAT)}; end time ${otherEventEnd.format(DISPLAY_DATETIME_WITH_DAYNAME_MOMENT_FORMAT)}`;
            
            if (bookingBufferDuration > 0)
              msg += `; buffer duration ${bookingBufferDuration} minutes`;

            break;
          }
        }
      }

      // if msg has been populated then there is an error
      if (msg) {
        returnValue.strict = true;
        returnValue.title = "This event overlaps another event";
        returnValue.detail = msg;
        return returnValue;
      }
    }
  }

  const dayOfWeekAbr = start.format("ddd").toLowerCase();
  const earliestTime = moment(eventType['event_earliest_time_' + dayOfWeekAbr], "HH:mm:ss");
  const latestTime = moment(eventType['event_latest_time_' + dayOfWeekAbr], "HH:mm:ss");

  /** Validate: start time must not be before open time */
  if (moment(start.format("HH:mm"), "HH:mm").isBefore(earliestTime)) {
    returnValue.strict = enforceTimeRestrictions;

    if (enforceTimeRestrictions)
      returnValue.title = `Start time cannot be before ${earliestTime.format(DISPLAY_TIME_MOMENT_FORMAT)} on a ${start.format("dddd")}`;
    else {
      
      returnValue.title = IRREGULAR_BOOKING_WARNING;
      returnValue.detail = `Start time cannot normally be before ${earliestTime.format(DISPLAY_TIME_MOMENT_FORMAT)} on a ${start.format("dddd")}.`;
    }
    return returnValue;
  }

  /** Validate: end time must not be after close time */
  if (moment(end.format("HH:mm"), "HH:mm").isAfter(latestTime)){
    returnValue.strict = enforceTimeRestrictions;

    if (enforceTimeRestrictions)
      returnValue.title = `End time cannot be after ${latestTime.format(DISPLAY_TIME_MOMENT_FORMAT)} on a ${start.format("dddd")}`;
    else {
      
      returnValue.title = IRREGULAR_BOOKING_WARNING;
      returnValue.detail = `End time cannot normally be after ${latestTime.format(DISPLAY_TIME_MOMENT_FORMAT)} on a ${start.format("dddd")}.`;
    }
    return returnValue;

  }
  
  return null;
}