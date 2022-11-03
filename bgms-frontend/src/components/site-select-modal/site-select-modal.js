import ModalPanel from "src/components/modal-panel";
import { mapActions, mapMutations, mapState } from "vuex";
import { BOOKING_CALENDAR } from "../../../src/router/Booking/constants.js";

const props = {
  show: { type: Boolean },
  title: { type: String },
  message: { type: String },
};

const components = {
  ModalPanel,
};

function data() {
  return {};
}

const methods = {
  ...mapActions([
    "selectSite",
    "requestFuneralDirectors",
    "requestMeetingLocations",
    "requestMapSections"
  ]),
  ...mapMutations([
      "changeCurrentSiteId"
  ]),
  ...mapState([
    "showSiteSelectConfirm", "currentSiteId", "previousSiteId"
  ]),
  onClose() {
    const previousSiteId = this.$store.state.previousSiteId;
    this.changeCurrentSiteId(previousSiteId);
    this.$store.state.showSiteSelectConfirm = false;
    this.requestFuneralDirectors();
    this.requestMeetingLocations();
    this.requestMapSections();
  },

  onNoStay() { 
    const previousSiteId = this.$store.state.previousSiteId;
    this.changeCurrentSiteId(previousSiteId);
    this.$store.state.showSiteSelectConfirm = false;
  },

  onYesContinue() {
    const siteId = this.$store.state.selectedSiteId;
    this.changeCurrentSiteId(siteId);
    this.$store.state.showSiteSelectConfirm = false;
    this.requestFuneralDirectors();
    this.requestMeetingLocations();
    this.requestMapSections();
  },

  onYesCancel() {
    const siteId = this.$store.state.selectedSiteId;
    this.changeCurrentSiteId(siteId);
    this.$store.state.showSiteSelectConfirm = false;
    this.$router?.push({ name: BOOKING_CALENDAR });    
  },
};

export default {
  name: "site-select-modal",
  props,
  components,
  data,
  methods,
};
