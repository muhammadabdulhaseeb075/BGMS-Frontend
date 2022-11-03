import _debounce from "lodash/debounce";
import _pick from "lodash/pick";
import _set from "lodash/set";
import { mapActions } from "vuex";

import InputField from "src/components/fields/input-field";
import FillButton from "src/components/fill-button";

const ADD_EMIT = "add";

function parseIncomingAddress(address) {
    const pickValues = _pick(address, [
        "line_1",
        "line_2",
        "post_town",
        "county",
        "postcode",
        "country",
    ]);
    return Object.values(pickValues)
        .filter(value => !!value)
        .join(", ");
}

const components = {
    InputField,
    FillButton,
};

const props = {
    form: { type: Object },
}

function data() {
    return {
        postcodeValue: "",
        addressSelected: "",
        addressPlaceholder: "No options available",
        addressOptions: [],
    };
}

const methods = {
    ...mapActions("booking", ["findAddressPostcode"]),

    onAdd() {
        this.$emit(ADD_EMIT, this.form);
    },

    async insertPostcode(value) {
        this.addressPlaceholder = "Loading...";
        try {
            const addresses = await this.findAddressPostcode(value);

            if(addresses) {
                this.addressOptions = addresses.map((address) => {
                    const addressFormat = parseIncomingAddress(address);
                    const addressLabel = addressFormat.length >= 32
                        ? addressFormat.slice(0, 32) + "..."
                        : addressFormat;

                    return { 
                        label: addressLabel,
                        value: addressFormat,
                    };
                });
            }
            this.addressPlaceholder = "Address options";
        } catch(error) {
            console.error("ERROR: ", error);
            this.addressPlaceholder = "No options available"
            this.addressOptions = [];
        }
    },

    selectAddress() {
        console.log("test");
    }
};

export default {
    name: "postcode-form",
    emits: [ADD_EMIT],
    props,
    data,
    components,
    methods,
};
