import _isBoolean from "lodash/isBoolean";
import _isNil from "lodash/isNil";
import _isObject from "lodash/isObject";
import _set from "lodash/set";

import  {
    emits,
    fieldTypes,
    nonInputTypes
} from "./constants";
import validations from "./validations";

export const schemaProps = {
    name: {type: String},
    id: {type: String},
    options: {type: Array},
    type: {type: String, default: fieldTypes.TEXT},
    validate: {type: Array, default: []},
    validateRules: {type: Object},
    placeholder: {type: String, default: ""},
    checkValue: {type: [String, Boolean], default: true},
    disabled: {type: Boolean},
    step: {type: Number},
    min: {type: [Number, Date, String]},
    max: {type: [Number, Date, String]},
    highlight: {type: Boolean, default: false},
};

export const inputFieldProps = {
    ...schemaProps,
    modelValue: { type: [String, Date, Boolean, Number], default: "" },
    formData: {type: Object},
};

export var multiselect_labels = [];

function setup(prop) {
    const {
        type,
    } = prop;
    const setupObj = {};

    if(type === fieldTypes.RADIO) {
        setupObj.radioId = String(Date.now());
    }

    setupObj.regularInput = !nonInputTypes.includes(type);
    return setupObj;
}

function data() {
    return {};
}

function mounted(){    
    if (this.validate.length) {
        const { isValid, errors } = this.validating(this.modelValue);
        const inputSchema = this.getInputSchema();
        this.$emit(emits.VALIDATE_EMIT, isValid, errors, this.modelValue, inputSchema);
    }
}

const methods = {

onInput(event){
    if(event.target.parentElement.classList.contains("noNeg")){
        this.$refs.input.value
            if(event.keyCode === 45){
                event.preventDefault();
            }
        }
    },

    /**
     * 
     * @param {*} event 
     */
    onChange(event) {
        this.updateInput(event, event.target.value);
    },

    /**
     * 
     * @param {*} event 
     */
    onChangeCheckbox(event) {
        const { checkValue } = this;
        const { checked } = event.target;
        const value = checked
            ? checkValue
            : (_isBoolean(checkValue) ? false : "");
        
        this.updateInput(event, value);
    },

    /**
     * 
     * @param {*} event 
     */
    onkeyup(event) {
        this.$emit(emits.KEY_UP_EMIT, event.target.value, event);
    },

    /**
     * 
     * @param {*} event 
     * @param {*} value 
     */
    updateInput(event, value) {        
        // validate here first
        const { isValid, errors } = this.validating(value);
        if( event && event.target && event.target.id == 'multiselect' ){            
            if (!multiselect_labels[this.name]) { //if a nested multiselect doesn't exist create it.
                multiselect_labels[this.name] = [];
             }
            if( event.target._value != "" ){
                value = event.target._value.includes(value) ? event.target._value : event.target._value + ", " + value;
            }
            event.target._value.includes(value) ? "":multiselect_labels[this.name].push(event.target.options[event.target.selectedIndex].text);
        }

        this.triggerEventsUpdate(value, event, {isValid, errors});        
        if(isValid) {
            this.updateFormData(value);
        }
    },

    /**
     * 
     * @param {*} value 
     */
    updateFormData(value) {
        const { formData, name } = this;

        if (_isObject(formData) && name) {
            _set(formData, name, value);
        }
    },

    /**
     * 
     * @param {*} isValid 
     * @param {*} value 
     * @param {*} event 
     */
    triggerEventsUpdate(value, event, {isValid, errors}) {
        const inputSchema = this.getInputSchema();
        if(this.validate.length) {
            this.$emit(emits.VALIDATE_EMIT, isValid, errors, value, inputSchema);
        }
        
        this.$emit(emits.UPDATE_EMIT, value);
        this.$emit(emits.FORMAT_EMIT, value, this.formatting);
        this.$emit(emits.CHANGE_EMIT, value, event, inputSchema);
        this.$emit(emits.UPDATE_FORM_EMIT, value, this.name, this.formData);
    },

    /**
     * 
     */
    getInputSchema() {
        return Object.keys(schemaProps).reduce((acc, propName) => {
            const value = this[propName];

            if (!_isNil(value)) {
                acc[propName] = value;
            }

            return acc;
        }, {});
    },

    /**
     * 
     * @param {*} value 
     * @param {*} validate 
     */
    validating(value) {
        const noPassedValidation = [];

        this.validate.forEach(validType => {
            const validFn = validations[validType];
            if (validFn) {
                const isValid = validFn(value);

                if(!isValid) {
                    noPassedValidation.push(validType);
                }
            }
        });

        return {
            isValid: !noPassedValidation.length,
            errors: noPassedValidation,
        };
    },

    formatting(newValue) {        
        this.updateFormData(newValue);
        this.$emit(emits.UPDATE_EMIT, newValue);
        // force update b/c if the parsed value is equal to
        // previous parsed value, the value is not going to change
        this.$forceUpdate();
    },

    cleanValue(event){
        const { isValid, errors } = this.validating("");
        event.target.value = "";
        multiselect_labels = [];
        this.triggerEventsUpdate("", event, {isValid, errors});
        if(isValid) {
            this.updateFormData("");
        }
    },

    cleanMultiSelectLabels(){ //this doesn't really work
        console.log("Clearing MultiSelect Labels in InputFields.")
        multiselect_labels = [];                
        this.updateFormData("");        
    },

    getLabels(model_name){           
        if(!this.formData[model_name]){ //Hack to clear labels if there is no form data set. ClearForm only clears the form element not the labels.            
            multiselect_labels[model_name] = [];
        }        
        return multiselect_labels[model_name];
    }

};

export default {
    name: "input-field",
    emits: Object.values(emits),
    props: inputFieldProps,
    mounted,
    setup,
    data,
    methods,
};
