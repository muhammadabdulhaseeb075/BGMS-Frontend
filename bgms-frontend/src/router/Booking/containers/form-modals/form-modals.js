import _get from "lodash/get";
import _set from "lodash/set";
import ModalPanel from "src/components/modal-panel";

import FuneralDirectorForm from "./funeral-director-form";
import AddressForm from "./address-form";
import PostcodeForm from "./postcode-form";
import { createForm } from "../../../../utils/forms";

const CLOSE_EMIT = "close";
const SEND_DATA_EMIT = "submit-form";

const props = {
    show: { type: Boolean },
    modalName: { type: String, default: "" },
    title: { type: String, default: "" },
    data_id: { type: String, default:""},
    form: { type: Object, default: "" },
    namespaceFields: { type: String, default: "" },
};

const components = {
    ModalPanel,
    FuneralDirectorForm,
    AddressForm,
    PostcodeForm,
};

function data() {    
    // gathering all fields by name
    const formNamespace = {};
    //Note: namespace fields seem to allow you to specify a subset of the usual form fields.   
    if(this.namespaceFields) {
        Object.keys(this.form.fields).map((fieldNameSchema) => {
            if (field.name && field.name.includes(this.namespaceFields)) {
                formNamespace[fieldNameSchema] = Object.assign({}, field);
            }
        });
    }

    return {
        formData: createForm(formNamespace),        
    };
}


const methods = {
    receiveDataForm() {        
        this.onClose();
    },

    onClose() {
        this.$emit(CLOSE_EMIT);
    },

    onSendData(formData) {        
        this.$emit(SEND_DATA_EMIT, formData, "manual");
        this.onClose();
    }
};

export default {
    name: "form-modals",
    props,
    emits: [CLOSE_EMIT, SEND_DATA_EMIT],
    components,
    data,
    methods,
    /*mounted() {
        console.log('fm - mounted!')
     },
     updated() {
        console.log('fm - updated!')
     }*/
};
