import { mapGetters } from "vuex";
import InputField from "src/components/fields/input-field";

import FormSectionField from "../../components/form-section-field";

const components = {
    InputField,
    FormSectionField,
};

function data() {
    return {
        reference: "",
        firstname: "",
        lastname: "",
        reference_number: "",
    }
}

function mounted() {
    if(this.currentBooking) {
        this.reference = this.currentBooking.calendar_event?.reference;
        this.reference_number = this.currentBooking.calendar_event?.reference_number;
        this.firstname = this.currentBooking.person?.first_names;
        this.lastname = this.currentBooking.person?.last_name;
    }
}

const computed = {
    ...mapGetters("booking", ["currentBooking"]),
}

export default {
    name: "status-form",
    components,
    data,
    mounted,
    computed,
};
