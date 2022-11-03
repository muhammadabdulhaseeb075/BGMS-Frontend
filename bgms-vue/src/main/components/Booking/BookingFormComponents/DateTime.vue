<template>
  <div>
    <v-row>
      <v-col cols="12" sm="6" class="py-1">
        <v-dialog
          ref="dateMenu"
          v-model="dateMenu"
          :close-on-content-click="false"
          :return-value.sync="bookingDate"
          transition="scale-transition"
          max-width="290px"
          min-width="290px"
          persistent
        >
          <template v-slot:activator="{ on }">
            <v-text-field
              ref="dateInput"
              v-model="displayDate"
              label="Booking Date"
              prepend-icon="fa-calendar-day"
              @click:prepend="dateMenu = true"
              v-on="on"
              readonly
              :disabled="readonly"
              required
              :rules="[() => !!bookingDate || 'This field is required', readonly || validateEventDate]"
            ></v-text-field>
          </template>
          <v-date-picker v-model="bookingDate" no-title scrollable
            @click:date="$refs.dateMenu.save(bookingDate)"
            :min="new Date().toISOString()">
            <div class="flex-grow-1"></div>
            <v-btn text color="primary" @click="dateMenu = false">Cancel</v-btn>
          </v-date-picker>
        </v-dialog>
      </v-col>

    <v-col cols="12" sm="6" class="py-1">
            <TimePicker
              Inputref="timeInput"
              v-bind:value="bookingTime"
              v-bind:time-input-required="true"
              v-on:input="bookingTime = $event"
              timeInputLabel="Booking Time"
              :time-input-rules="[() => !!bookingTime || 'This field is required', readonly || validateEventTime]"
            />
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" sm="6" class="py-1">
        <v-text-field
          v-model="duration"
          label="Duration"
          suffix="minutes"
          type="number"
          interval="1"
          required
          :disabled="readonly"
          :rules="[() => !!duration || 'This field is required', readonly || validateEventTime]"
        ></v-text-field>
      </v-col>
    </v-row>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component, { mixins } from 'vue-class-component';
import { getDisplayTime, DISPLAY_DATE_WITH_DAYNAME_MOMENT_FORMAT } from '@/global-static/dataFormattingAndValidation.ts';
import { Prop } from 'vue-property-decorator';
import moment from 'moment';
import 'moment-timezone';
import { validateEventTime, validateEventDate } from '@/main/static/eventHelperFunctions.ts';
import NotificationMixin from '@/mixins/notificationMixin.ts';
import TimePicker from "@/main/components/Booking/TimePicker.vue";

@Component({
  components: {TimePicker}
})
export default class DateTime extends mixins(NotificationMixin) {

  @Prop() id;
  @Prop() eventTypeID;
  @Prop() siteID;

  dateMenu: boolean = false;
  timeMenu: boolean = false;

  // array of warning that have already been displayed (so we can avoid duplicated warnings)
  previousWarnings = [];

  // this should be true for funeral directors
  enforceTimeRestrictions: boolean = false;

  readonly: boolean = true;

  /*** Lifecycle hooks ***/

  mounted() {
    // this will validate the auto populated data
    if (this.bookingTime)
      (this.$refs.timeInput as HTMLElement).focus();

    if (this.bookingDate) {
      Vue.nextTick(() => {
        (this.$refs.dateInput as HTMLElement).focus();
      });
    }

    if (!this.bookingDetails['status'] || this.bookingDetails['status'] < 4) {
      
      // Note: in the future we might want to do this server side as timezone might be different for a site
      const now = moment().tz("Europe/London").format('YYYY-MM-DDTHH:mm');

      if (now < moment(this.bookingDate + "T" + this.bookingTime).format('YYYY-MM-DDTHH:mm'))
        this.readonly = false;
    }
  }

  /*** Getters and setters ***/

  /**
   * @return details about the selected event
   */
  get selectedEvent() {
    return this.$store.getters.getEventType(parseInt(this.siteID), parseInt(this.eventTypeID));
  }
  
  get bookingDetails() {
    return this.$store.state.Booking.bookingDetails;
  }
  
  get bookingDate() {
    return this.bookingDetails.calendar_event.bookingDate;
  }
  set bookingDate(bookingDate) {
    this.$store.commit('modifyCalendarEventDetails', { key: 'bookingDate', value: bookingDate });
  }

  get bookingTime() {
    return this.bookingDetails.calendar_event.bookingTime;
  }
  set bookingTime(bookingTime) {
    this.$store.commit('modifyCalendarEventDetails', { key: 'bookingTime', value: bookingTime });
  }

  get duration() {
    return this.bookingDetails.calendar_event.duration;
  }
  set duration(duration) {
    this.$store.commit('modifyCalendarEventDetails', { key: 'duration', value: duration });
  }

  get displayDate() {
    if (this.bookingDate)
      return moment(this.bookingDate).format(DISPLAY_DATE_WITH_DAYNAME_MOMENT_FORMAT);
    else
      return null;
  }

  get displayTime() {
    if (this.bookingTime)
      return getDisplayTime(this.bookingTime.substr(0,2), this.bookingTime.substr(3));
    else
      return null;
  }

  /**
   * return start date time
   */
  get startDateTime(): moment.Moment {
    return moment(this.bookingDate + "T" + this.bookingTime);
  }

  /**
   * Validation rules for booking date
   */
  get validateEventDate() {

    if (this.bookingDate) {

      const result = validateEventDate(this.startDateTime, this.selectedEvent, this.getOtherEvents(), this.enforceTimeRestrictions);
      return this.processValidationResult(result);
    }

    return false;
  }
  
  /**
   * Validation rules for booking time and duration
   */
  get validateEventTime() {

    if (this.bookingDate && this.bookingTime && this.duration) {

      const start = this.startDateTime;
      let end = moment(this.bookingDate + "T" + this.bookingTime);
      end.add(this.duration, 'm');

      const result = validateEventTime(start, end, this.selectedEvent, this.getOtherEvents(), this.enforceTimeRestrictions);
      return this.processValidationResult(result);
    }

    return false;
  }

  /*** Methods ***/

  getOtherEvents() {
    if (this.bookingDate) {
      const start = moment(this.bookingDate);
      return this.$store.getters.getEventsInSameCategoryAndDay(parseInt(this.siteID), start.format("YYYY-MM-DD"), this.selectedEvent.event_category_id, this.id);
    }

    return null;
  }

  /**
   * Process result of date and time validation
   * @param {EventValidationResult} result
   */
  processValidationResult(result) {
    if (result) {
      if (result.strict)
        // this is an error so validation fails
        return result.title;
      else if (!this.previousWarnings.includes(result.title + result.detail)) {
        // this is not an error, but the user does need warned about something (if they haven't already seen this exact message)
        this.createInfoConfirmation(result.title, result.detail);
        this.previousWarnings.push(result.title + result.detail);
      }
    }

    return true;
  }
}
</script>