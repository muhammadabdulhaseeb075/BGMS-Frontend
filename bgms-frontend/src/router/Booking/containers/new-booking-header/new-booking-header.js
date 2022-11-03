import {mapActions, mapGetters, mapState} from "vuex";
import InputField from "src/components/fields/input-field";
import ConfirmModal from "src/components/confirm-modal";
import SiteSelectModal from "src/components/site-select-modal";

const SAVE_EMIT = "save-event";
const EDIT_MODE = "edit-event";
const REMOVE_EMIT = "remove-event";
const RESET_EMIT = "reset-event";

const props = {
    editMode: { type: Boolean, default: false },
    saveDisabled: { type: Boolean },
    updateEvent: { type: Boolean },
    redirect: { type: Boolean },
    reference: { type: Number },
    reference_number: { type: String },
};

const components = {
    InputField,
    ConfirmModal,
    SiteSelectModal,
};

const methods = {
    onSaveEvent() {
      this.$emit(SAVE_EMIT);       
    },

    onRemoveEvent() {
        this.$emit(REMOVE_EMIT);
        this.showConfirmModal = false;
    },

    openConfirmModal() {
        //this.formModalName = modalName;
        this.showConfirmModal = true;
    },

    openEditConfirm() {
        this.showEditConfirm = true;
    },

    changeEditMode() {
        this.$emit(EDIT_MODE);
    },

    changeViewMode() {
        this.$emit(REMOVE_EMIT);
    },
};

function data() {
    return {
        showConfirmModal: false,
        showEditConfirm: false,        
    };
}

const computed = {
    ...mapGetters(["currentSiteName"]),
    ...mapState(["showSiteSelectConfirm"]),
    ...mapGetters("booking", ["currentBookingDate"]),
    bookingDate: (state) => {
    var autoDate
    var currentTime = new Date()
    var month = currentTime.getMonth() + 1
    var day = currentTime.getDate()
    var year = currentTime.getFullYear()
        return state.currentBookingDate ?? month + "/" + day + "/" + year;
    }
}

export default {
    props,
    name: "new-booking-header",
    emits: [SAVE_EMIT, REMOVE_EMIT, RESET_EMIT, EDIT_MODE],
    data,
    methods,
    computed,
    components,
};
