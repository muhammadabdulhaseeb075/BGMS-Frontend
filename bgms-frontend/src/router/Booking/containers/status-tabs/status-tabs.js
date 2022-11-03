import { reactive, toRefs } from 'vue';
import { Tabs, Tab, TabPanels, TabPanel } from 'vue3-tabs';
import InputField from "src/components/fields/input-field";
import { DateTime } from "luxon";
import { mapGetters, mapActions } from 'vuex';
import NotificationsList from "../../../../components/notifications-list";
import FormSection from "../../components/form-section";
import FormSectionField from "../../components/form-section-field";
import store from "../../../../store/index";


const currentDate = DateTime.now().toISODate();
const BASE_TIME = "11:59:00";
const DATE_FORMAT = "yyyy-MM-dd'T'T";
const loggedInUser = store.state.user.username.substr(0, store.state.user.username.indexOf('@'));

const tabs = [
  "Pre Burial Check",
  "Post Burial Check",
  "Cancel",
];

const preburialList = [
  { date: null, title: 'Check grave details entered in booking are valid', field: 'grave_details', active: false, username: '', usernameTitle:'grave_details_by_user' },
  { date: null, title: 'Check grave on the ground and that the depth is available', field: 'grave_on_ground', active: false, username: '', usernameTitle:'grave_on_ground_by_user' },
  { date: null, title: 'Notice of interment form received and copy loaded to system', field: 'notice_of_interment', active: false, username: '', usernameTitle:'notice_of_interment_by_user' },
  { date: null, title: 'Certificate for Burial/Cremation received', field: 'burial_certificate', active: false, username: '', usernameTitle:'burial_certificate_by_user' },
  { date: null, title: 'Details on NOI form confirmed and accepted', field: 'noi_details', active: false, username: '', usernameTitle:'noi_details_by_user' },
  { date: null, title: 'Check burial grant details agree with NOI', field: 'burial_grant_noi', active: false, username: '', usernameTitle:'burial_grant_noi_by_user' },
  { date: null, title: 'Indemnity received where no burial grant', field: 'indemnity', active: false, username: '', usernameTitle:'indemnity_by_user' },
  { date: null, title: 'Completed instruction to gravedigger form', field: 'gravedigger', active: false, username: '', usernameTitle:'gravedigger_by_user' },
  { date: null, title: 'Signed off by team leader', field: 'signed_off', active: false, username: '', usernameTitle:'signed_off_by_user' },
  { date: null, title: 'Invoice sent/paid', field: 'invoice', active: false, username: '', usernameTitle:'invoice_by_user' },
];

const postburialList = [
  { date: null, title: 'Backfill completed', field: 'backfill_completed', active: false, username: '', usernameTitle:'backfill_completed_by_user' },
  { date: null, title: 'Plot inspected', field: 'plot_inspected', active: false, username: '', usernameTitle:'plot_inspected_by_user' },
];

const cancelburialList = [
  { date: null, field: 'cancel_date', text: null, field_text: 'cancel_reason' },
];

function setup() {
  const state = reactive({
    selectedTab: tabs[0],
    preburialList,
    postburialList,
    cancelburialList
  });

  return {
    tabs,
    ...toRefs(state),
    currentDate,
    loggedInUser,
  };
}

function mounted() {
  this.resetStatus(this.preburialList);
  this.checkStatus(this.preburialList, this.statusFromCurrentBooking.pre);
  this.resetStatus(this.postburialList);
  this.checkStatus(this.postburialList, this.statusFromCurrentBooking.post);
  this.resetCancel(this.cancelburialList);
  this.populateCancelStatus(this.cancelburialList, this.statusFromCurrentBooking.cancel);
}

const components = {
  Tabs,
  Tab,
  TabPanels,
  TabPanel,
  InputField,
  NotificationsList,
  FormSection,
  FormSectionField
}

const methods = {
  ...mapActions(["addNotification"]),
  ...mapActions('booking', ['updateStatus']),
  ...mapActions('booking', ['updatePostBurial']),
  ...mapActions('booking', ['updateCancelBurial']),

  resetStatus(list) {

    for (let itr = 0; itr < list.length; itr++) {
      list[itr].date = null;
      list[itr].active = false;
    }
  },

  resetCancel(list) {

    for (let itr = 0; itr < list.length; itr++) {
      list[itr].date = null;
      list[itr].text = null;
    }
  },

  format(value, resolve) {
    resolve(value > currentDate ? currentDate : value);
  },
  
  checkStatus(list, status) {
    if (status !== null) {
      for (let itr = 0; itr < list.length; itr++) {
        const item = list[itr].field;
        const userItem = list[itr].usernameTitle;
        const value = status[item];
        const userValue = status[userItem];

        if (value != null) {
            list[itr].active = true;
            list[itr].date = DateTime.fromISO(value).toISODate();
            list[itr].username = userValue;
        }
      }
    }
  },

  populateCancelStatus(list, status) {
    if (status !== null) {
      for (let itr = 0; itr < list.length; itr++) {
        const item_date = list[itr].field;
        const value_date = status[item_date];
        const item_reason = list[itr].field_text;
        const value_reason = status[item_reason];

        if (value_date != null) {
          list[itr].text = value_reason;
          list[itr].date = DateTime.fromISO(value_date).toISODate();
        }
      }
    }
  },

  submitStatus() {
    const parseObjectPre = {};
    const parseObjectPost = {};
    let parseObjectCancel = {};
    for (let itr = 0; itr < this.preburialList.length; itr++) {
      parseObjectPre[this.preburialList[itr].field]= this.preburialList[itr].date === null ? null :
        DateTime.fromISO(this.preburialList[itr].date + 'T' + BASE_TIME).toFormat(DATE_FORMAT);
      parseObjectPre[this.preburialList[itr].usernameTitle]= this.preburialList[itr].username === null ? null : this.preburialList[itr].username;
    }
    for (let itr = 0; itr < this.postburialList.length; itr++) {
      parseObjectPost[this.postburialList[itr].field] = this.postburialList[itr].date === null ? null :
        DateTime.fromISO(this.postburialList[itr].date + 'T' + BASE_TIME).toFormat(DATE_FORMAT);
        parseObjectPost[this.postburialList[itr].usernameTitle] = this.postburialList[itr].username === null ? null : this.postburialList[itr].username;
    }

    for (let itr = 0; itr < this.cancelburialList.length; itr++) {

      if (this.cancelburialList[itr].text === null) {
        parseObjectCancel = {
          'cancel_date': null,
          'cancel_reason': null
        };
      } else {
        parseObjectCancel = {
          'cancel_date': this.cancelburialList[itr].date === null ? null : DateTime.fromISO(this.cancelburialList[itr].date + 'T' + BASE_TIME).toFormat(DATE_FORMAT),
          'cancel_reason': this.cancelburialList[itr].text
        };
      }
    }
    try {
      this.updateStatus({
        preburialId: this.statusFromCurrentBooking.pre.id,
        dataPre: parseObjectPre,
        postburialId: this.statusFromCurrentBooking.post.id,
        dataPost: parseObjectPost,
        cancelburialId: this.statusFromCurrentBooking.cancel.id,
        dataCancel: parseObjectCancel
      })

      this.addNotification({
        type: "success",
        message: "Status updated"
      });


    } catch (error) {
      this.addNotification({
        type: "error",
        message: "Error, updating status"
      });
    }
  }
}



const computed = {
  ...mapGetters('booking', ['statusFromCurrentBooking']),

  isPreBurialComplete(){
    //debugger; // eslint-disable-line no-debugger
    for (let itr = 0; itr < this.preburialList.length; itr++) {
      //debugger; // eslint-disable-line no-debugger
      //console.log(this.preburialList[itr].active);
      if(!this.preburialList[itr].active) return false;
    }
    return true; //if the for loop completes without returning then all checkboxes are selected.
  }
}


export default {
  name: "status-tabs",
  setup,
  components,
  computed,
  mounted,
  methods,
};
