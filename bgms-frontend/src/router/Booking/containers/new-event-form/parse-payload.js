import _cloneDeep from "lodash/cloneDeep";
import _get from "lodash/get";
import _merge from "lodash/merge";
import {DateTime} from "luxon";

import {
    BURIAL_FIELD,
    CALENDAR_DATE_FIELD,
    CALENDAR_DATE_FORMAT,
    CALENDAR_DURATION_FIELD,
    CALENDAR_FIELD,
    CALENDAR_TIME_FIELD,
    CALENDAR_TYPE_ASHES,
    KIN_ADDRESS_FIELD,
    KIN_FIELD,
    PERSON_DEATH_FIELD,
    PERSON_FIELD,
} from "./constants";

/**
 * 
 * @param {*} address 
 * @returns 
 */
function formatAddress(address) {
    return address
        ? Object.values(address)
            .filter(value => !!value)
            .join(", ")
        : "";
}

/**
 * 
 * @param {*} formData 
 */
function parseDeceaseDeathDate(formData) {
    const deceaseDate = _get(formData, PERSON_DEATH_FIELD);
    const date = DateTime.fromISO(deceaseDate);

    return deceaseDate 
        ? {
            "impossible_date_day": date.day,
            "impossible_date_month": date.month,
            "impossible_date_year": date.year,
        }
        : {};
}

function parseKinBirthDate(formData) {
    const birthDate = _get(formData, "next_of_kin_person.birth_date");
    const date = DateTime.fromISO(birthDate);
    return "birth_date_day: " + date.day + ",birth_date_month: " + date.month + ",birth_date_year: " + date.year + ",";
    /*
    return birthDate
        ? {
            "impossible_date_day": date.day,
            "impossible_date_month": date.month,
            "impossible_date_year": date.year,
        }
        : {};
     */
}
function parseKinBirthDay(formData) {
    const birthDate = _get(formData, "next_of_kin_person.birth_date");
    const date = DateTime.fromISO(birthDate);
    return date.day;
}

function parseKinBirthMonth(formData) {
    const birthDate = _get(formData, "next_of_kin_person.birth_date");
    const date = DateTime.fromISO(birthDate);
    return date.month;
}

function parseKinBirthYear(formData) {
    const birthDate = _get(formData, "next_of_kin_person.birth_date");
    const date = DateTime.fromISO(birthDate);
    return date.year;
}

/**
 * 
 * @param {*} value 
 * @param {*} name 
 * @param {*} formData 
 */
function parseStarEndDate(formData) {
    const date = _get(formData, CALENDAR_DATE_FIELD);
    const time = _get(formData, CALENDAR_TIME_FIELD);
    const duration = _get(formData, CALENDAR_DURATION_FIELD);
    const baseDate = DateTime.fromISO(`${date}T${time}`);
    const start = baseDate.toFormat(CALENDAR_DATE_FORMAT);
    const end = baseDate.plus({ minutes: parseInt(duration) })
        .toFormat(CALENDAR_DATE_FORMAT);

    return {start, end};
}

/**
 * 
 * @param {*} formData 
 */
export default function parseEventPayload(formData, formFields) {
    const copyFormData = _cloneDeep(formData);
    const parsedDeathDate = parseDeceaseDeathDate(formData);
    const parsedBirthDate = parseKinBirthDate(formData);

    const parsedData = _merge(copyFormData, {
        [CALENDAR_FIELD]: {
            ...parseStarEndDate(formData),
            "event_type_id": 1
        },
        [BURIAL_FIELD]: {
            ...parsedDeathDate,
            "cremated": formData.type === CALENDAR_TYPE_ASHES,
            "burial_number": formFields.detailsGraveNumber.value,
        },
        [PERSON_FIELD]: {
            "death": parsedDeathDate,
            "residence_address": {},
        },    
        [KIN_FIELD]: {
            "current_addresses": [
                _get(formData, KIN_ADDRESS_FIELD)
            ],
            "birth_date_day": parseKinBirthDay(formData).toString(),
            "birth_date_month": parseKinBirthMonth(formData).toString(),
            "birth_date_year": parseKinBirthYear(formData).toString(),
            "postcode": "",
            "city": "",
        },
    });
    debugger; // eslint-disable-line no-debugger
    return parsedData;
}
