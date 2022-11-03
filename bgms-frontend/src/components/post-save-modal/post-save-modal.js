import ModalPanel from "src/components/modal-panel";
import {BOOKING_ADD_NAME, BOOKING_SPLIT_VIEW, BOOKING_STATUS_NAME} from "src/router/Booking/constants";


const CLOSE_EMIT = "close";
const RESET_EMIT = "reset";

const props = {
    show: { type: Boolean },
    title: { type: String },
    data_id: { type: String, default: "" },
    message: { type: String },
    query: { type: Object},
    //data: { type: Object},
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

    goToCalendar() { //method to go to the calendar with query params set
        //debugger; // eslint-disable-line no-debugger
        var site_id = this.query.site;
        var event_date = this.query.date;;
        const query_data = {
            siteId: site_id,
            calendarDate: event_date,
        };
        this.$router?.push({ name: BOOKING_SPLIT_VIEW, query: query_data });
        //this.$router?.push({ name: BOOKING_CALENDAR, query });
    },

    goToStatus() { //go to the status module with query params set
        debugger; // eslint-disable-line no-debugger
        var site_id = this.query.site;
        var reference_id = this.query.reference;
        const query_data = {
            siteId: site_id,
            ref: reference_id,
        };
        this.$router?.push({ name: BOOKING_STATUS_NAME, query: query_data });
        //this.$router?.push({ name: BOOKING_CALENDAR, query });
    },

    onContinue(){ //redirect to the Booking form with the updated query
    // eslint-disable-next-line no-console
        if(this.debug) console.log("Redirecting to the booking form. " + BOOKING_ADD_NAME);
        //if(this.debug) debugger; // eslint-disable-line no-debugger
        this.$router?.push({name: BOOKING_ADD_NAME, query: this.query}).then();
    },

    reset(){ //clear the initial state. State is being kept between show/hide events.  
        this.ashes = null;
        this.showConfirmButton = false;
    },

    //valueChanged(event){ //update the type value in the query based on current selection
    valueChanged(){ //update the type value in the query based on current selection
        this.query.type = this.ashes;
        this.showConfirmButton = true; //once a value is set show the confirm button, can never deselect a radio element so only need to toggle on
        // eslint-disable-next-line no-console
        if(this.debug) console.log("Value Changed. " + this.query.type);
    },
};

export default {
    name: "post-save-modal",
    props,
    emits: [CLOSE_EMIT, RESET_EMIT],
    components,
    data,
    methods,
};
