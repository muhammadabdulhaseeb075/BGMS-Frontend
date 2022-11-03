import _pick from "lodash/pick";
import _set from "lodash/set";
import { mapActions } from "vuex";

import InputField from "src/components/fields/input-field";
import FillButton from "src/components/fill-button";
import ModalPanel from "src/components/modal-panel";
import { createForm } from "src/utils/forms";

import addressFormSchema from "./address-event-schema";

const MANUAL_ADDRESS_EMIT = "manual-address";
const FIND_ADDRESS_EMIT = "find-address";
const REMOVE_ADDRESS_EMIT = "remove-address";
const SAVE_ADDRESS_EMIT = "save-address";

const MANUAL_TYPE = "manual";
const POSTCODE_TYPE = "postcode";
import NotificationsList from "../../../../components/notifications-list";

function parseIncomingAddress(address) {
    
    return {
        first_line: address.line_1,
        second_line: address.line_2,
        town: address.post_town,
        county: address.county,
        postcode: address.postcode,
        country: address.country,
    };
}

const components = {
    InputField,
    FillButton,
    ModalPanel,
    NotificationsList
};

const props = {
    editMode: { type: Boolean, default: false },

    // accepts "manual" or "find"
    addressMode: { type: String, default: ""},
}

function data() {
    return {
        modalTitle: "",
        addressType: "",
        postcodeAddress: "",
        addressForm: null,
        openModal: false,

        postcodeValue: "",
        addressSelected: "",
        addressPlaceholder: "No options available",
        addressSuggested: [],
        addressOptions: [],
    };
}

const methods = {
    ...mapActions(["addNotification"]),
    ...mapActions("booking", ["findAddressPostcode"]),

    onFindAddress(event) {
        event.preventDefault();
        this.openModal = true;
        this.modalTitle = "Address Lookup:";
        this.addressType = POSTCODE_TYPE;
        this.addressForm = createForm(addressFormSchema);
        this.$emit(FIND_ADDRESS_EMIT);
    },

    onManualAddress() {
        this.openModal = true;
        this.modalTitle = "Enter Address:";
        this.addressType = MANUAL_TYPE;
        this.addressForm = createForm(addressFormSchema);
        this.$emit(MANUAL_ADDRESS_EMIT);
    },

    onEdit() {
        this.addressForm = null;
        this.removeAddress();
    },

    removeAddress() {
        this.$emit(REMOVE_ADDRESS_EMIT);
    },

    onClose() {
        this.openModal = false;
        this.addressSelected = "";
        this.postcodeValue = "";
        this.addressPlaceholder = "No options available";
        this.addressOptions =  [];
        this.addressForm = null;
    },

    onConfirm() {
        const addressData = this.addressForm.data.address;

        this.$emit(SAVE_ADDRESS_EMIT, addressData);
        this.onClose();
    },

    async insertPostcode(value) {
        this.addressPlaceholder = "Loading...";
        try {
            const addresses = await this.findAddressPostcode(value);

            if (addresses) {
                this.addressSuggested = addresses;
                this.addressOptions = addresses.map((address, index) => {
                    const addressFormat = address;//parseIncomingAddress(address);
                    const addressLabel = address.line_1 >= 32
                        ? address.line_1.slice(0, 32) + "..."
                        : address.line_1;

                    return {
                        label: addressLabel,
                        value: index,
                    };
                });
            }
            this.addressPlaceholder = "Address options";
        } catch (error) {
            console.error("ERROR: ", error);
            this.showAlert(error);
            this.addressPlaceholder = "No options available";
            this.addressOptions = [];
        }
    },

    selectPostcodeAddress(value) {
        try{
            const indexOpt = parseInt(value);
            const address = this.addressSuggested[indexOpt];
            const addressParsed = parseIncomingAddress(address);

            this.addressForm.data = { address: addressParsed };
        }catch (error) {
            this.showAlert(error);
        }
    },

    showAlert(error=undefined) {
        if (typeof error === "undefined"){
            this.addNotification({
                type: "success",
                message: "The event was successfully saved."
            });
        }
        else{
            let error_message = "";
            if (error.response && error.response.data && error.response.data.detail)
                error_message = error.response.data.detail;
            else if (error.message)
                error_message = error.message;
            else
                error_message = "No addresses found";

            this.addNotification({
                type: "error",
                message: error_message
            });
        }
    },

}

const computed = {

}

export default {
    name: "address-event-field",
    emits: [
        MANUAL_ADDRESS_EMIT,
        FIND_ADDRESS_EMIT,
        REMOVE_ADDRESS_EMIT,
        SAVE_ADDRESS_EMIT,
    ],
    props,
    data,
    computed,
    components,
    methods,
};
