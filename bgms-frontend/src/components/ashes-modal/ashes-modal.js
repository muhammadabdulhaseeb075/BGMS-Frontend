import ModalPanel from "src/components/modal-panel";
import {BOOKING_ADD_NAME} from "src/router/Booking/constants";


const CLOSE_EMIT = "close";
const RESET_EMIT = "reset";

const props = {
    show: { type: Boolean },
    title: { type: String },
    data_id: { type: String, default: "" },
    message: { type: String },
    query: { type: Object},
};

const components = {
    ModalPanel,
};

function data() {
    return {
        ashes:null,
        showConfirmButton: false,    
        debug:true,
    };
}

const methods = {
    onClose() {
        this.$emit(CLOSE_EMIT);
    },

    onRemoveEvent() {
        this.$emit(RESET_EMIT);
    },

    onContinue(){ //redirect to the Booking form with the updated query
        if(this.debug) console.log("Redirecting to the booking form. " + BOOKING_ADD_NAME);
        //if(this.debug) debugger; // eslint-disable-line no-debugger
        this.$router?.push({ name: BOOKING_ADD_NAME, query: this.query });
        //this.$router?.push({ name: "booking-add-event", query: this.query });
    },

    reset(){ //clear the initial state. State is being kept between show/hide events.  
        this.ashes = null;
        //this.message = null;
        this.showConfirmButton = false;
    },

    valueChanged(event){ //update the type value in the query based on current selection
        this.query.type = this.ashes;
        this.showConfirmButton = true; //once a value is set show the confirm button, can never deselect a radio element so only need to toggle on
        if(this.debug) console.log("Value Changed. " + this.query.type);
    },
};

export default {
    name: "ashes-modal",
    props,
    emits: [CLOSE_EMIT, RESET_EMIT],
    components,
    data,
    methods,
};
