export const emits = {
    CHANGE_EMIT: "change",
    VALIDATE_EMIT: "on-validate",
    UPDATE_EMIT: "update:modelValue",
    KEY_UP_EMIT: "keyup",
    FORMAT_EMIT: "format",
    UPDATE_FORM_EMIT: "update-form",
};

// Supported inputs
// @TODO add more input types
export const fieldTypes = {
    SELECT: "select",
    RADIO: "radio",
    TEXTAREA: "textarea",
    CHECKBOX: "checkbox",
    TEXT: "text",
    DATE: "date",
    TIME: "time",
    NUMBER: "number",
};

export const nonInputTypes = [
    fieldTypes.SELECT,
    fieldTypes.RADIO,
    fieldTypes.TEXTAREA,
    fieldTypes.CHECKBOX,
];
