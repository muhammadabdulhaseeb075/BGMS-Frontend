import InputField from "src/components/fields/input-field";
import { convertTimeToTwelveHourFormat, convertTimeToTwentyFourHourFormat } from "../../utils/dates";
import _isObject from "lodash/isObject";
import _set from "lodash/set";
import { schemaProps } from "../fields/input-field/input-field";
import {emits} from "../fields/input-field/constants";
import validations from "../fields/input-field/validations";


const props = {
    hour: {
        default: "01"
    },
    minute: {
        default: "00"
    },
    meridiemCategory: {
        default: "p. m."
    },
    open: {
        default: false
    },
    value: {
        default: "13:00"
    },

    timeInputLabel: {
        default: ""
    },

    formData: {type: Object},
    dataField: { type: Object},
    //min: {type: String},
    //max: {type: String},
    //min/max time passed in from site calendar settings
    slotMinTime: {type: String, default: ""},
    slotMaxTime: {type: String, default: ""},

    ...schemaProps
};

function data() {
    return {
        showCardContainer: props.open.default,
        canFocus: false,
        hourSelected: props.hour.default,
        minuteSelected: props.minute.default,
        meridiemCategorySelected: props.meridiemCategory.default,
        meridiemCategories: ["a. m.", "p. m."],
        //hours: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",],
        hours: [],
        //minutes: ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"],
        minutes: ["00", "10", "20", "30", "40", "50"], //ten minute increments
    };
}

const methods = {
    selectHour: function selectHour(hour) {
        this.hourSelected = hour;

        this.timeValue = convertTimeToTwentyFourHourFormat(
            this.timeInDateSimpleFormat
        );
    },
    selectMinutes: function selectMinutes(minute) {
        this.minuteSelected = minute;
        if (this.timeValue.length >= 5) {
            this.timeValue = this.timeValue.replace(/:\d\d/, ":" + minute);
        } else {
            this.timeValue = minute;
        }
    },
    generateMorningHours: function generateMorningHours(time){ //returns a string array containing allowable hours for the am
        var mindatetime = new Date("1970-01-01T" + time + "Z");
        mindatetime =   new Date( mindatetime.getTime() + ( mindatetime.getTimezoneOffset() * 60000 ) ); //hack to set time to current timezone instead of utc
        var minHour = mindatetime.getHours();


        //if selected time is not in valid am range then reset to the minHour
        if(this.hourSelected < minHour) {
            // eslint-disable-next-line no-console
            console.log("Below Hour Range. Change to " + minHour.toString());
            this.hourSelected = minHour;
        }
        if(this.hourSelected > 11) {
            // eslint-disable-next-line no-console
            console.log("Above Hour Range. Change to " + minHour.toString());
            this.hourSelected = minHour;
        }

        //generate a list of hours for the am selection (needs to be "01" to match selection)        var hour_array = [];
        var hour_array = [];
        for(let i=minHour; i<=11; i++){ //count from min hour (ex: 8) to 11am. Will fail if min time is 11am.
            hour_array.push(("0" + i).slice(-2));
        }
        return hour_array;
    },
    generateEveningHours: function generateEveningHours(time){ //returns a string array containing allowable hours for the pm
        var maxdatetime = new Date("1970-01-01T" + time + "Z");
        maxdatetime =   new Date( maxdatetime.getTime() + ( maxdatetime.getTimezoneOffset() * 60000 ) ); //hack to set time to current timezone instead of utc
        var maxhour = maxdatetime.getHours();

        //check if selection is outside range and set to 12pm if so
        if(this.hourSelected > (maxhour - 12)) {
            this.hourSelected = 12;
        }
        //generate a list of hours for the pm selection (needs to be "01" to match selection)
        var hour_array = ["12"]; //start with 12pm since it is not part of the sequence
        for(let i=1; i<=(maxhour-12); i++){ //count from min hour (ex: 8) to 11am. Will fail if min time is 11am.
            hour_array.push(("0" + i).slice(-2));
        }
        return hour_array;
    },
    selectMeridiemCategory: function selectMeridiemCategory(meridiemCategory) {
        this.meridiemCategorySelected = meridiemCategory;
        //debugger; // eslint-disable-line no-debugger
        //change the selectable hours based on AM/PM selection
        if(meridiemCategory == "a. m."){
            this.hours = this.generateMorningHours(this.slotMinTime);
        }
        else if(meridiemCategory == "p. m."){
            this.hours = this.generateEveningHours(this.slotMaxTime);
        }

        this.timeValue = convertTimeToTwentyFourHourFormat(
            this.timeInDateSimpleFormat
        );
    },
    updateTimeParts: function updateTimeParts(event) {
        const newTimeValue = event.target.value;
        const timeTwelveHourFormat = convertTimeToTwelveHourFormat(newTimeValue);
        const partOfTime = timeTwelveHourFormat.split(":"); //TODO: Error if am/pm updates but no time is set. (Changing time ranges counts as time update.)
        const hour = partOfTime[0].padStart(2, "0");
        this.hourSelected = hour;

        const minutesAndTMeridiemCategory = partOfTime[1].split(" ");
        const minute = minutesAndTMeridiemCategory[0];
        const meridiemCategory = minutesAndTMeridiemCategory[1];
        this.minuteSelected = minute;
        this.meridiemCategorySelected = meridiemCategory === "AM" ? "a. m." : "p. m.";
        this.timeValue = newTimeValue ?? this.value;

        if (_isObject(this.formData) && this.name) {
            _set(this.formData, this.name, newTimeValue);
        }
    },
    openOrHideContainer: function (){
        this.showCardContainer = !this.showCardContainer;
    },
    validateTimeField: function (time){
        if( this.validate.length) {
            const errors = [];

            this.validate.forEach(validType => {
                const validFn = validations[validType];
                if (validFn) {
                    const isValid = validFn(time);
    
                    if(!isValid) {
                        errors.push(validType);
                    }
                }
            });
            this.$emit(emits.VALIDATE_EMIT, !errors.length, errors, time, {id: this.id});
        }
    }
};

const computed = {
    timeValue: {
        get() {
            return this.value ?? props.value.default;
        },
        set(timeChanged) {
            this.validateTimeField(timeChanged);
            this.$emit("time-change", timeChanged.padStart(5, "0"));
        }
    },
    timeInDateSimpleFormat: function (){
        const formatMeridiemCategory = this.meridiemCategorySelected === "a. m." ? "AM" : "PM";
        return `${this.hourSelected}:${this.minuteSelected} ${formatMeridiemCategory}`;
    }
};

const watch = {
    timeValue: {
        handler: function (newTime){
            this.updateTimeParts({
                target: {
                    value: newTime
                }
            });
        }
    },
    slotMinTime: {
        handler: function (){
            // eslint-disable-next-line no-console
            console.log("MIN Time Watch Called!" + this.slotMinTime);
            this.selectMeridiemCategory(this.meridiemCategorySelected);
            //this.selectMeridiemCategory("a. m.");
        }
    }

};

function mounted(){
    this.validateTimeField(this.timeValue);
}

function updated(){
    this.$nextTick(function (){
        if (this.showCardContainer) {
            this.$refs.time.focus();
        }
    });
}

const components = {
    InputField
};

export default {
    name: "time-picker",
    props,
    components,
    data,
    watch,
    mounted,
    updated,
    emits: ["time-change", ...Object.values(emits)],
    methods,
    computed
};
