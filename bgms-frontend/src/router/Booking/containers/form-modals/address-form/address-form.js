import _set from "lodash/set";
import InputField from "src/components/fields/input-field";
import FillButton from "src/components/fill-button";

const ADD_EMIT = "add";

const components = {
    InputField,
    FillButton,
};

const props = {
    form: { type: Object },
}

function data() {
    return {};
}

const methods = {
    onAdd() {
        this.$emit(ADD_EMIT, this.form);
    },
};

export default {
    name: "address-form",
    emits: [ADD_EMIT],
    props,
    data,
    components,
    methods,
};
