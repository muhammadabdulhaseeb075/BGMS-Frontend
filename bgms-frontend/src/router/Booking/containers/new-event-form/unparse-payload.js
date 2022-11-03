import _merge from "lodash/merge";
import _cloneDeep from "lodash/cloneDeep";
import { DateTime, Duration } from "luxon";

import {
    CALENDAR_TYPE_ASHES,
    CALENDAR_TYPE_BURIAL,
} from "./constants";
import { CALENDAR_SLOT_DURATION } from "../../constants";
import {next} from "lodash/seq";

function createDateFromDeceasedDeathDate(deceasedDateOfDeath) {
    //debugger; // eslint-disable-line no-debugger
    const { impossible_date_day, impossible_date_month , impossible_date_year} = deceasedDateOfDeath;
    const dateOfDeathInDateTime = DateTime.utc(impossible_date_year, impossible_date_month, impossible_date_day);
    return dateOfDeathInDateTime.toFormat("yyyy-MM-dd");
}

function createDateFromKinBirthDate(kinDateOfBirth) {
    //debugger; // eslint-disable-line no-debugger
    const { birth_date_day, birth_date_month , birth_date_year} = kinDateOfBirth;
    const dateOfBirthInDateTime = DateTime.utc(birth_date_year, birth_date_month, birth_date_day);
    return dateOfBirthInDateTime.toFormat("yyyy-MM-dd");
}

function splitCalendarDate(start, end) {
    const startDate = DateTime.fromISO(start);
    const endDate = DateTime.fromISO(end);
    const { minutes } = endDate.diff(startDate, ["minutes"]).toObject();

    return {
        date: startDate.toFormat("yyyy-MM-dd"),
        time: startDate.toLocaleString(DateTime.TIME_24_SIMPLE),
        duration: minutes,
    };
}

function parseDateFromMillisecondsToCalendarEvent(start) {
    const startDate = DateTime.fromMillis(Number(start));
    const { values } = Duration.fromISOTime(CALENDAR_SLOT_DURATION);

    return {
        date: startDate.toFormat("yyyy-MM-dd"),
        time: startDate.toLocaleString(DateTime.TIME_24_SIMPLE).padStart(5,"0"),
        duration: values.minutes
    };
}

/**
 * create a calendar event related form given by a start date in milliseconds
 * @param formSchema
 * @param dataMatch
 * @returns {*}
 */

export function unparseEventDate(formSchema, dataMatch){
    const { calendar_event } = dataMatch;
    const { date, time, duration} = parseDateFromMillisecondsToCalendarEvent(calendar_event.start);

    const formCopy = _cloneDeep(formSchema);

    return _merge(formCopy, {
        date: {
            defaultValue: date,
        },
        time: {
            defaultValue: time,
        },
        duration: {
            defaultValue: duration
        }
    });
    
}

/**
 * 
 * @param {*} formData 
 */
export function unparseEventPayload(
    formSchema,
    dataMatch,
) {
    //debugger; // eslint-disable-line no-debugger
    const {
        calendar_event,
        next_of_kin_person,
        burial,
        person,
    } = dataMatch;

    const {
        death
    } = person;

    /*const {
        birth
    } = next_of_kin_person;*/

    const calendarEvents = splitCalendarDate(
        calendar_event.start,
        calendar_event.end
    );
    const burialType = dataMatch?.burial?.cremated
        ? CALENDAR_TYPE_ASHES
        : CALENDAR_TYPE_BURIAL;

    const deceasedDeathDate = createDateFromDeceasedDeathDate(death);

    let kinBirthDate = null;
    if(next_of_kin_person != null) {
        kinBirthDate = createDateFromKinBirthDate(next_of_kin_person);
    }

    const formCopy = _cloneDeep(formSchema);

    return _merge(formCopy, {
        burialId: {
            name: "burial.id",
            defaultValue: burial.id,
        },
        calendarId: {
            name: "calendar_event.id",
            defaultValue: calendar_event.id
        },
        nextOfKinPersonId: {
            name: "next_of_kin_person.id",
            defaultValue: next_of_kin_person?.id,
        },
        kinDateOfBirth: {
            defaultValue: kinBirthDate,
        },
        personId: {
            name: "person.id",
            defaultValue: person.id,
        },
        deceaseDateOfDeath: {
            defaultValue: deceasedDeathDate,
        },
        type: {
            defaultValue: burialType,
        },
        date: {
            defaultValue: calendarEvents.date,
        },
        time: { 
            defaultValue: calendarEvents.time.padStart(5, "0"),
        },
        duration: {
            defaultValue: calendarEvents.duration,
        },
    });
}