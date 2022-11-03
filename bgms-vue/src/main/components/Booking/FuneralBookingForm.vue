<template>
  <v-card>
    <v-card-title>
      <span class="headline">{{ selectedEvent.name }}</span>
      <div class="flex-grow-1"></div>
      <span :style="{'color': site.preferences.site_color}">{{ site.name }}</span>
      <v-tooltip top v-if="!newEvent && bookingDetails['status'] < 4">
        <template v-slot:activator="{ on }">
          <v-btn icon @click="cancelEvent()" v-on="on">
            <i class="fas fa-ban"/>
          </v-btn>
        </template>
        <span>Cancel Event</span>
      </v-tooltip>
      <v-tooltip top v-if="!newEvent && bookingDetails['status'] === 7">
        <template v-slot:activator="{ on }">
          <v-btn icon @click="deleteEvent()" v-on="on">
            <i class="fas fa-trash"/>
          </v-btn>
        </template>
        <span>Delete Event</span>
      </v-tooltip>
      <v-tooltip top>
        <template v-slot:activator="{ on }">
          <v-btn icon @click="closeDialog(true)" v-on="on">
            <i class="fas fa-times"/>
          </v-btn>
        </template>
        <span>{{ newEvent ? 'Cancel' : 'Close' }}</span>
      </v-tooltip>
    </v-card-title>
    <v-card-text>
      <v-form ref="form" v-if="!loadingData">
        <v-tabs 
          v-if="parentRouteID !== null"
          height="35px" 
          dark
          v-model="currentTab"
          show-arrows>
    
          <v-tab
            v-for="(tab, index) in tabs"
            :key="index"
            :to="{ name: tab.routeName }"
            :disabled="newEvent && index>furthestValidatedTab">
            {{ tab.label }}
          </v-tab>
        </v-tabs>

        <router-view></router-view>

      </v-form>
      <v-row v-else
        align-content="center"
        justify="center">
        <v-col
          class="subtitle-1 text-center"
          cols="12">
          Loading
        </v-col>
        <v-col cols="6">
          <v-progress-linear
            indeterminate
            rounded
            height="4"
          ></v-progress-linear>
        </v-col>
      </v-row>

    </v-card-text>
    <v-card-actions>
      <div class="flex-grow-1"></div>
      <v-btn @click="closeDialog(true)"><i class="fas fa-times"/>{{ newEvent ? 'Cancel' : 'Close' }}</v-btn>
      <v-btn :disabled="$route.name === tabs[0].routeName" @click="changeTab($event, -1)"><i class="fas fa-arrow-left"/>Previous</v-btn>
      <v-btn :disabled="$route.name === tabs[tabs.length-1].routeName" @click="changeTab($event, 1)">Next<i class="fas fa-arrow-right"/></v-btn>
      <v-btn 
        v-if="bookingDetails['status']!==7"
        :disabled="saving || !unsavedChanges || (newEvent && $route.name !== tabs[tabs.length-1].routeName)" 
        @click="saveFuneralEvent"
        :loading="saving">
        <i class="fas fa-save"/>Save</v-btn>
    </v-card-actions>

  </v-card>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component, { mixins } from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import axios from 'axios'
import NotificationMixin from '@/mixins/notificationMixin.ts';
import { convertStartDatetimeAndDurationToEndDatetime } from '@/main/static/eventHelperFunctions.ts';
import moment from 'moment';

const hash = require('object-hash');

// Register the router hooks with their names
Component.registerHooks([
  'beforeRouteUpdate'
])

@Component
export default class FuneralBookingForm extends mixins(NotificationMixin) {

  @Prop() bookingDatetime;
  @Prop() siteID;
  @Prop() eventTypeID;
  @Prop() id;

  tabs = null;
  currentTab: string = null;
  furthestValidatedTab: number = 0; // when creating a new booking, all tabs must be opened and validated

  parentRouteID = null;

  newEvent: boolean = false;

  loadingData: boolean = true;
  saving: boolean = false;

  originalDataHash = null;

  /*** Lifecycle hooks ***/

  created() {
    
    // this is a new booking
    if (this.id === "add") {

      this.newEvent = true;

      // we'll use this later
      let initialBookingDate = this.bookingDetails.bookingDate ? this.bookingDetails.bookingDate : null;
      let initialBookingTime = this.bookingDetails.bookingTime ? this.bookingDetails.bookingTime : null;

      // create object containing required form items
      let formObject = {
        /** Date & Time */
        calendar_event: {
          event_type_id: parseInt(this.eventTypeID),
          bookingDate: null,
          bookingTime: null,
          duration: this.selectedEvent['default_duration']
        }
      };

      this.bookingDetails = formObject;

      // populate the date and time if it exists
      // (doing this now will make sure this gets picked up as a data change)

      // if no time set, select earliest available
      if (initialBookingDate && !initialBookingTime) {
        initialBookingTime = this.selectedEvent['event_earliest_time_' + moment(initialBookingDate).format("ddd").toLowerCase()];

        if (initialBookingTime)
          // remove seconds
          initialBookingTime = initialBookingTime.substr(0,initialBookingTime.length - 3);
      }

      this.bookingDetails['calendar_event']['bookingDate'] = initialBookingDate;
      this.bookingDetails['calendar_event']['bookingTime'] = initialBookingTime;

      this.loadingData = false;
    }
    // this is an existing booking
    else {
      axios.get(this.site.domain_url + "/cemeteryadmin/funeralEvent/" + this.id + "/")
      .then(response => {
        let data = response.data;

        // this should always be true
        if (data.calendar_event.start) {
          const start = moment(data.calendar_event.start, "YYYY-MM-DDTHH:mm:ss");
          data['calendar_event']['bookingDate'] = start.format("YYYY-MM-DD");
          data['calendar_event']['bookingTime'] = start.format("HH:mm");

          // this should always be true
          if (data.calendar_event.end) {
            const end = moment(data.calendar_event.end, "YYYY-MM-DDTHH:mm:ss");
            data['calendar_event']['duration'] = end.diff(start, 'minutes');
          }
        }

        if (!data.person.residence_address)
          data.person.residence_address = {};

        if (!data.burial)
          data.burial = {};

        this.bookingDetails = data;
        this.originalDataHash = hash(data);

        this.loadingData = false;
      })
      .catch(error => {
        this.createHTTPErrorNotificationandLog(error, "Failed to return event details.");
        this.closeDialog(true);
      });
    }

    this.parentRouteID = this.$route.matched[1].meta.parentRouteID;

    this.tabs = [
    { label: "Date & Time", routeName: this.parentRouteID + '_datetime' },
    { label: "Deceased", routeName: this.parentRouteID + '_deceased' },
    { label: "Funeral Director", routeName: this.parentRouteID + '_funeralDirector' },
    { label: "Burial", routeName: this.parentRouteID + '_burial' },
    { label: "Next Of Kin", routeName: this.parentRouteID + '_nextOfKin' },
    { label: "Status", routeName: this.parentRouteID + '_funeralBookingStatus' }];
  }

  mounted() {
    // set initial tab
    this.changeTab(null, 0)
  }

  /*** Getters and setters ***/

  get site() {
    return this.$store.getters.getSiteFromId(parseInt(this.siteID));
  }

  /**
   * @return details about the selected event
   */
  get selectedEvent() {
    return this.$store.getters.getEventType(parseInt(this.siteID), parseInt(this.eventTypeID));
  }
  
  get bookingDetails() {
    return this.$store.state.Booking.bookingDetails;
  }
  set bookingDetails(bookingDetails) {
    this.$store.commit('commitBookingDetails', bookingDetails);
  }
  
  get unsavedChanges(): boolean {
    return hash(this.bookingDetails) !== this.$store.state.Booking.unmodifiedBookingDetailsHash;
  }
  
  /**
   * @returns True if original data of existing event has been changed and saved
   */
  get savedChanges(): boolean {
    return !this.newEvent && this.originalDataHash !== this.$store.state.Booking.unmodifiedBookingDetailsHash;
  }

  /*** Methods ***/

  /**
   * Select a new tab in the form.
   */
  changeTab(e, direction) {
    const currentIndex = Math.max(0, this.tabs.findIndex(tab => tab.routeName === this.$route.name));
    this.$router.replace({ name: this.tabs[currentIndex + direction].routeName });
  }

  /**
   * Vue router beforeRouteUpdate in-component guard
   * Enforces validation before moving away from form
   */
  beforeRouteUpdate (to, from, next) {
    if (from.name === (this.parentRouteID + "_funeralbooking") || !this.$refs.form || (this.$refs.form as HTMLFormElement).validate()) {

      if (this.newEvent)
        // update the furthest tab the user can navigate to
        this.furthestValidatedTab = Math.max(this.furthestValidatedTab, this.tabs.findIndex(tab => tab.routeName === to.name));

      next();
    }
    else
      next(false);
  }

  /**
   * Closes the dialog
   */
  closeDialog(cancel: boolean = false): void {

    const closeTasks = () => {

      // if this is a saved event that has been created/updated/deleted
      if (!cancel || this.savedChanges) {

          // remove relavent stored data for the calendar (this will be reuploaded by calendar)
          const loadedMonths = this.$store.state.Booking.loadedMonths;

          // check to see if events from this site are currently loaded
          if (loadedMonths && loadedMonths[this.siteID]) {
            // remove events for this site
            loadedMonths[this.siteID] = [];
            this.$store.state.Booking.allEvents[this.siteID] = [];
          }
      }

      this.bookingDetails = null;

      // closes the dialog
      this.$router.push({ path: this.$route.matched[1].path });
    }

    if (cancel && this.unsavedChanges) {
      this.createConfirmation("Unsaved Changes", "You have unsaved changes that will be lost if you close this screen.\n\nDo you want to continue?", closeTasks)
    }
    else
      closeTasks();
    
  }

  saveFuneralEvent(): void {

    if (!(this.$refs.form as HTMLFormElement).validate())
      return;
    
    this.saving = true;

    let data = this.bookingDetails;
    data.calendar_event.start = data.calendar_event.bookingDate + "T" + data.calendar_event.bookingTime;
    data.calendar_event.end = convertStartDatetimeAndDurationToEndDatetime(data.calendar_event.start, data.calendar_event.duration);
    data.burial.impossible_date_year = data.calendar_event.bookingDate.substring(0,4);
    data.burial.impossible_date_month = data.calendar_event.bookingDate.substring(5,7);
    data.burial.impossible_date_day = data.calendar_event.bookingDate.substring(8);

    let url: string = this.site.domain_url + "/cemeteryadmin/funeralEvent/";

    if (!this.newEvent)
      url += this.id + "/";

    axios({
      method: this.newEvent ? 'post' : 'patch',
      url: url,
      data: data
    })
    .then(response => {
      this.createSuccessNotification("Event saved successfully");

      // update the booking status
      this.bookingDetails.status = response.data.status;
      this.bookingDetails.next_of_kin_person = response.data.next_of_kin_person;
      this.bookingDetails.person.next_of_kin = response.data.next_of_kin_person ? response.data.next_of_kin_person.id : null;


      if (this.newEvent)
        this.closeDialog();
      else
        // this will create a new hash of saved data
        this.bookingDetails = this.bookingDetails;

    })
    .catch(error => {
      this.createHTTPErrorNotificationandLog(error, "Event save failed.");
    })
    .finally(() => {
      this.saving = false;
    });
  }

  /**
   * Cancels event (soft delete, event will still exist but with a cancelled status)
   */
  cancelEvent() {
    // can only cancel existing events that have not taken place yet
    if (!this.newEvent && this.bookingDetails['status'] < 4) {
      this.createConfirmation("Cancel Event", "Are you sure you want to cancel this event?", () => {
        axios.put(this.site.domain_url + "/cemeteryadmin/funeralEvent/" + this.id + "/cancel/")
        .then(response => {
          this.bookingDetails['status'] = 7;
          
          // this will create a new hash of saved data
          this.bookingDetails = this.bookingDetails;

          this.createSuccessNotification("Event cancelled successfully");
        })
        .catch(error => {
          this.createHTTPErrorNotificationandLog(error, "Event cancel failed.");
        });
      })
    }
  }

  /**
   * Deletes event (hard delete)
   */
  deleteEvent() {
    // can only cancel existing events that have been cancelled
    if (!this.newEvent && this.bookingDetails['status'] === 7) {
      this.createConfirmation("Delete Event", "Are you sure you want to permanently delete this event? This cannot be undone!", () => {
        axios.delete(this.site.domain_url + "/cemeteryadmin/funeralEvent/" + this.id + "/")
        .then(response => {
          this.createSuccessNotification("Event deleted successfully");
          
          this.bookingDetails['status'] = -1;
          
          // this will create a new hash of saved data
          this.bookingDetails = this.bookingDetails;

          this.closeDialog();
        })
        .catch(error => {
          this.createHTTPErrorNotificationandLog(error, "Event delete failed.");
        });
      })
    }
  }
}
</script>