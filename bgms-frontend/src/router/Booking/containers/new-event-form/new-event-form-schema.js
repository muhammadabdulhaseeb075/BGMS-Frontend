import { DateTime } from "luxon";

import { getNearMultiple } from "src/utils/math";
import {
    CALENDAR_DATE_FIELD,
    CALENDAR_TIME_FIELD,
    CALENDAR_DURATION_FIELD,
    CALENDAR_TYPE_ASHES,
    CALENDAR_TYPE_BURIAL,
    DURATION_STEP,
} from "./constants";
import deceaseAddressSchema from "./deceased-address-form-schema";
import otherAddressSchema from "./other-address-form-schema";

//const currentDate = DateTime.now().plus({ days: 1 }).toISODate();
const currentDate = DateTime.now().toISODate();
//Hack to calculate 18 year cut-off. Doesn't work on one line. Schema only supports variable assignations not multi-line.
const now = new Date();
const finish = new Date().setFullYear(now.getFullYear()-18);
const eighteenYearsAgo = new Date(finish).toISOString().split("T")[0];

/**
 * 
 */
export default Object.assign({
    // Booking section
    type: {
        id: "type",
        name: "type",
        validate: ["required"],
        type: "radio",
        options: [
            { label: "Ashes", value: CALENDAR_TYPE_ASHES },
            { label: "Burial", value: CALENDAR_TYPE_BURIAL },
        ],
    },
    date: {
        id: "date",
        name: CALENDAR_DATE_FIELD,
        type: "date",
        min: currentDate,
        defaultValue: currentDate,
    },
    time: {
        id: "time",
        name: CALENDAR_TIME_FIELD,
        type: "time",
        defaultValue: "09:00",
        step: 300,
        validate: ["timeRange"]
    },
    duration: {
        id: "duration",
        name: CALENDAR_DURATION_FIELD,
        placeholder: "duration",
        type: "number",
        defaultValue: 30,
        step: DURATION_STEP,
        /**
         * 
         * @param {*} value 
         */
        format(value, resolve) {
            const parsed = getNearMultiple(parseInt(value), DURATION_STEP);
            if(!isNaN(parsed)) {
                resolve(parsed ? parsed : DURATION_STEP);
            }
        },
    },

    // Decease section
    deceaseTitle: {
        id: "deceaseTitle",
        name: "person.title",
        type: "select",
        options: [
            {label: "Mr", value: "1" },
            {label: "Mrs", value: "2" },
            {label: "Miss", value: "3"},
            {label: "Ms", value: "4" },
        ],
    },

    deceaseFirstName: {
        id: "deceaseFirstName",
        name: "person.first_names",
        type: "text",
        validate: ["required"],
    },

    deceaseLastName: {
        id: "deceaseLastName",
        name: "person.last_name",
        type: "text",
        validate: ["required"],
        /**
        * Format last name to uppercase
        */
        format(value, resolve) {
            resolve(value.toUpperCase());
        },

    },

    deceaseAge: {
        id: "deceaseAge",
        name: "person.age",
        type: "number",
        min: "0",
    },

    deceaseAgeType: {
        id: "deceaseAgeType",
        name: "person.age_type",
        type: "select",
        options: [
            { label: "Years", value: "age_years" },
            { label: "Months", value: "age_months" },
            { label: "Weeks", value: "age_weeks" },
            { label: "Days", value: "age_days" },
            { label: "Hours", value: "age_hours" },
        ],
        defaultValue: "age_years",
    },
  
    deceaseDateOfDeath: {
        id: "deceaseDateOfDeath",
        name: "person.death",
        type: "date",
        max: currentDate,
        format(value, resolve) {
            if(value){resolve(value > currentDate? currentDate : value);}
        },
    },

    deceaseAddress: {
        id: "deceaseAddress",
        type: "text",
        disabled: true,
    },

    deceasePlaceOfDeath: {
        id: "deceasePlaceOfDeath",
        name: "person.place_of_death",
        type: "checkbox",
    },

    // Details section
    detailsFuneralDirector: {
        id: "detailsFuneralDirector",
        name: "funeral_director_id",
        section: "details",
        placeholder: "Select",
        type: "select",
        options: [],
    },
    detailsGraveNumber: {
        id: "detailsGraveNumber",
        name: "burial.burial_number",
        section: "details",
        type: "text",
        disabled: true,
        defaultValue: "",
    },
    detailsBurialUUID: {
        id: "detailsBurialUUID",
        name: "burial.burial_uuid",
        section: "details",
        type: "text",
        disabled: true,
        defaultValue: "",
    },
    newBurialGrave : {
        id: "newBurialGrave",
        name: "burial.new_burial_grave",
        section: "details",
        type: "checkbox",
    },
    detailsMapSection: {
        id:"detailsMapSection",
        name: "section_name",
        section: "details",
        type: "select",
        options: [],
    },
    coffinSizeUnits: {
        id: "coffinSizeUnits",
        name: "burial.coffin_units",
        section: "details",
        type: "select",
        options: [
            {label: "mtrs", value: "mtrs"},
            {label: "ft/in", value: "ft/in"},
        ],
        defaultValue: "mtrs",
    },
    coffinSizeLength: {
        id: "coffinSizeLength",
        name: "burial.coffin_length",
        section: "details",
        type: "number",
    },
    coffinSizeWidth: {
        id: "coffinSizeWidth",
        name: "burial.coffin_width",
        section: "details",
        type: "number",
    },
    coffinSizeHeight: {
        id: "coffinSizeHeight",
        name: "burial.coffin_height",
        section: "details",
        type: "number",
    },
    coffinSizeDepth: {
        id: "coffinSizeDepth",
        name: "burial.coffin_depth",
        section: "details",
        type: "number",
    },
    coffinComments:{
        id:"coffinComments",
        name: "burial.coffin_comments",
        section: "details",
        type: "textarea",
    },
    meetingLocation: {
        id: "meetingLocation",
        name: "meeting_location_id",
        section: "details",
        type: "select",
        options: [],
    },

    // Next of Kin section
    kinTitle: {
        id: "kinTitle",
        name: "next_of_kin_person.title",
        section: "kin",
        type: "select",
        options: [
            {label: "Mr", value: "1" },
            {label: "Mrs", value: "2" },
            {label: "Miss", value: "3"},
            {label: "Ms", value: "4" },
        ],
    },

    kinFirstName: {
        id: "kinFirstName",
        name: "next_of_kin_person.first_names",
        section: "kin",
        type: "text",
    },

    kinLastName: {
        id: "kinLastName",
        name: "next_of_kin_person.last_name",
        section: "kin",
        type: "text",
        format(value, resolve) {
            resolve(value.toUpperCase());
        },
    },

    kinRelationship: {
        id: "kinRelationship",
        name: "next_of_kin_person.relationship",
        section: "kin",
        type: "text",
    },

    kinDateOfBirth: {
        id: "kinDateOfBirth",
        name: "next_of_kin_person.birth_date",
        section: "kin",
        type: "date",
        max: currentDate,
        min: eighteenYearsAgo,
        format(value, resolve) {
            if(value){resolve(value > currentDate? currentDate : value);} //if date past today set to current
            if(value){resolve(value < eighteenYearsAgo? "" : value);} //if date less than 18 years ago set to blank
        },
    },

    kinAddress: {
        id: "kinAddress",
        name: "next_of_kin_person.address",
        section: "kin",
        type: "text",
    },

    // Authority section
    authTitle: {
        id: "authTitle",
        name: "authority_for_interment.title",
        section: "auth",
        type: "select",
        options: [
            {label: "Mr", value: "1" },
            {label: "Mrs", value: "2" },
            {label: "Miss", value: "3"},
            {label: "Ms", value: "4" },
        ],
    },

    authFirstName: {
        id: "authFirstName",
        name: "authority_for_interment.first_names",
        section: "auth",
        type: "text",
    },

    authLastName: {
        id: "authLastName",
        name: "authority_for_interment.last_name",
        section: "auth",
        type: "text",
        format(value, resolve) {
            resolve(value.toUpperCase());
        },
    },

    authRole: {
        id: "authRole",
        name: "authority_for_interment.role",
        section: "auth",
        type: "text",
    },

    // Comments section
    comments: {
        id: "comments",
        name: "burial.burial_remarks",
        section: "comments",
        type: "textarea",
    },

    // Booking status section
    status: {
        id: "status",
        name: "status",
        type: "text",
    },
}, ...[deceaseAddressSchema, otherAddressSchema]);
