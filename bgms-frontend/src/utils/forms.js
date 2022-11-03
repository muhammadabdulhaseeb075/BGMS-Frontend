import _get from "lodash/get";
import _isNil from "lodash/isNil";
import _isArray from "lodash/isArray";
import _isObject from "lodash/isObject";
import _merge from "lodash/merge";
import _set from "lodash/set";

/**
 * 
 */
function getFieldsToValidate(fieldNames, fields) {
    const fieldsToValidate = fieldNames.filter((fieldName) => {
        const { validate } = fields[fieldName];
        const hasValidate = validate && validate.length;

        return hasValidate;
    });
    let validFields = {};

    fieldsToValidate.forEach(fieldName => {
        validFields[fieldName] = {
            valid: false,
            errors: [],
        };
    });

    return {fieldsToValidate, validFields};
}

/**
 * 
 * @param {*} fieldNames 
 * @param {*} fieldSchema
 */
function setFieldValues(fieldNames, fieldSchema, persist) {    
    const fields = { ...fieldSchema };
    const data = {};

    fieldNames.forEach(fieldName => {
        const field = fields[fieldName];
        const { defaultValue, value } = field;

        if(field.type == "multiselect"){            
            /* 
            console.log("Multiselect Set Field Value.");            
            if(field.multiselect_labels){
                console.log("Clearing!");
                field.multiselect_labels = [];
            }*/            
        }

        if (!_isNil(defaultValue) || !_isNil(value)) {
            const name = field.name;

            field.value = persist ? value : defaultValue;

            // Saving default value on form data
            if (name) {
                _set(data, field.name, defaultValue);
            }
        } else {
            field.value = "";
        }

    });

    return { fields, data };
}

/**
 * 
 * @param {*} fields
 * @return {Object}
 */
export function createForm(fieldSchema, options = { persist: false }) {    
    const fieldNames = Object.keys(fieldSchema);
    const { fieldsToValidate, validFields } = getFieldsToValidate(
        fieldNames,
        fieldSchema
    );
    const { fields, data } = setFieldValues(fieldNames, fieldSchema, options.persist);
    
    return {
        data,
        fields,
        errors: {},
        validFields,
        fieldsToValidate,
        validateField(fieldName, isValid) {
            if (this.validFields[fieldName]) {
                this.validFields[fieldName].valid = isValid;
            }
        },
    };
}

/**
 * 
 * @param {*} fieldSchema 
 * @param {*} dataMatch 
 * @returns 
 */
export function matchForm(fieldSchema, dataMatch, options = { keepData: false, persist: false }) {
    //debugger; // eslint-disable-line no-debugger
    const fields = Object.keys(fieldSchema).reduce((acc, fieldKey) => {
        //debugger; // eslint-disable-line no-debugger
        const field = fieldSchema[fieldKey];
        let defaultValue = _get(dataMatch, field.name);

        if (_isArray(defaultValue)) {
            defaultValue = defaultValue[0] || undefined;
        } else if (_isObject(defaultValue)) {
            defaultValue = undefined;
        }

        acc[fieldKey] = {
            ...field,
        };

        if(defaultValue !== undefined) {
            acc[fieldKey].defaultValue = defaultValue;
        }

        return acc;
    }, {});
    const form = createForm(fields, options.persist);

    return form;
}
