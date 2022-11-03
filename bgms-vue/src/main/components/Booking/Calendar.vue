<template>
  <v-container id="calendar" :style="{ height: calendarHeight + 'px' }">
    
    <SiteSelection></SiteSelection>
    
    <v-sheet id="calendar_header_sheet"
      @wheel="wheelEvent">
      <v-toolbar flat color="white">
        <v-btn outlined class="mr-4" @click="setToday">
          Today
        </v-btn>
        <v-btn fab text small @click="prev">
          <i class="fas fa-chevron-left"/>
        </v-btn>
        <v-btn fab text small @click="next">
          <i class="fas fa-chevron-right"/>
        </v-btn>
        <v-toolbar-title class="ml-4">{{ title }}</v-toolbar-title>
        <v-spacer></v-spacer>

        <v-btn
          class="d-none d-md-flex calendar-views"
          v-for="key in Object.keys(types)" :key="key"
          text
          @click="type = key"
          :disabled="type===key"
          :input-value="type===key">
            {{ types[key] }}
        </v-btn>

        <v-menu bottom right class="d-md-none">
          <template v-slot:activator="{ on }">
            <v-btn
              class="d-md-none"
              outlined
              v-on="on"
            >
              <span>{{ types[type] }}</span>
              <v-icon right>fas fa-caret-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="type = 'day'">
              <v-list-item-title>Day</v-list-item-title>
            </v-list-item>
            <v-list-item @click="type = 'week'">
              <v-list-item-title>Week</v-list-item-title>
            </v-list-item>
            <v-list-item @click="type = 'month'">
              <v-list-item-title>Month</v-list-item-title>
            </v-list-item>
            <v-list-item @click="type = '4day'">
              <v-list-item-title>4 days</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

      </v-toolbar>
    </v-sheet>

    <v-sheet id="calendar_sheet">
      <v-calendar
        ref="calendar"
        v-model="focus"
        :events="currentDisplayEvents"
        :event-color="(event) => event.site_color ? event.site_color : 'secondary'"
        :type=type
        locale="en"
        :weekdays="[1, 2, 3, 4, 5, 6, 0]"
        @change="calendarChanged"
        @click:more="viewDay"
        @click:date="viewDay"
        @click:event="eventClick"
        @mousedown:event="moveEvent"
        @mouseenter:day="changeEventDatetime"
        @mousemove:time="changeEventDatetime"
        @click:day="newBooking"
        @click:time="newBooking">
      </v-calendar>

      <v-menu
        v-model="selectedOpen"
        :close-on-content-click="false"
        :activator="selectedElement"
        offset-y
        max-width="350px">
        <v-card
          color="grey lighten-4"
          min-width="350px"
          max-width="350px"
          flat>
          <v-toolbar :color="selectedEvent.site_color" dark>
            <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
            <div class="flex-grow-1"></div>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn icon @click="cancelEvent(selectedEvent)" v-on="on">
                  <i class="fas fa-ban"/>
                </v-btn>
              </template>
              <span>Cancel Event</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn icon @click="editEvent(selectedEvent)" v-on="on">
                  <i class="fas fa-edit"/>
                </v-btn>
              </template>
              <span>Edit Event</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn icon @click="selectedOpen = false" v-on="on">
                  <i class="fas fa-times"/>
                </v-btn>
              </template>
              <span>Close</span>
            </v-tooltip>
          </v-toolbar>
          <v-card-text>
            <div>{{ selectedEvent.display_date }}</div>
            <div>Created By: {{ selectedEvent.created_by }}</div>
            <div>Details: {{ selectedEvent.details }}</div>
          </v-card-text>
        </v-card>
      </v-menu>
    </v-sheet>

    <router-view v-if="bereavementStaffAccessSites && bereavementStaffAccessSites.length"></router-view>

  </v-container>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component, { mixins } from 'vue-class-component';
import { Watch } from 'vue-property-decorator'
import axios from 'axios'
import NotificationMixin from '@/mixins/notificationMixin.ts';
import { DISPLAY_DATE_WITH_DAYNAME_MOMENT_FORMAT, DISPLAY_TIME_MOMENT_FORMAT, SERVER_DATE_MOMENT_FORMAT, getDisplayTimeFromDatetime } from '@/global-static/dataFormattingAndValidation.ts';
import { validateEventTime, validateEventDate } from '@/main/static/eventHelperFunctions.ts';
//import * as moment from 'moment-timezone';
import moment from 'moment';
import 'moment-timezone';
import DateTime from './BookingFormComponents/DateTime.vue';
import SiteSelection from '@/main/components/Booking/SiteSelection.vue';

// Register the router hooks with their names
Component.registerHooks([
  'beforeRouteUpdate'
])

@Component({
  components: {
    SiteSelection
  }
})
export default class Calendar extends mixins(NotificationMixin) {
  
  type: string = 'month';
  types = {
    month: 'Month',
    week: 'Week',
    day: 'Day',
    '4day': '4 Days'
  }

  start = null;
  end = null;
  focus = null;
  currentDisplayEvents = [];

  selectedEvent= {};
  selectedElement = null;
  selectedOpen: boolean = false;

  bookingDateTime = null;
  newBookingInitialSiteId = null;

  eventMovingByDrag: boolean = false;
  dragEvent = null;
  originalDragEvent = null;
  mousePositionMinutes: number = null;

  // this should be true for funeral directors
  enforceTimeRestrictions: boolean = false;

  calendarHeight: number = 0;

  selectedSitesIdsOriginal = null;

  /*** Lifecycle hooks ***/

  mounted() {
    let today = new Date();
    this.focus = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();

    this.resetCalendarHeight();
    window.addEventListener('resize', this.resetCalendarHeight);

    // listen for mouse up events
    document.body.addEventListener('mouseup', this.stopMoveEvent); 
  }

  destroyed() {
    window.removeEventListener('resize', this.resetCalendarHeight);
  }

  /*** Getters and setters ***/

  get allEvents() {
    return this.$store.state.Booking.allEvents;
  }

  get loadedMonths() {
    return this.$store.state.Booking.loadedMonths;
  }

  /**
   * Get sites user has bereavement staff access to
   */
  get bereavementStaffAccessSites() {
    return this.$store.getters.getBereavementStaffAccessSites;
  }


  /**
   * Get sites that user is wanting to display
   */
  get selectedSitesIds() {
    return this.$store.state.Booking.selectedSitesIds;
  }
  
  private get calendarInstance (): Vue & { prev: () => void, next: () => void,
    getFormatter: (format: any) => any, scrollToTime: (time: any) => any } {
      return this.$refs.calendar as Vue & { prev: () => void, next: () => void, getFormatter: (format: any) => any, scrollToTime: (time: any) => any };
    }
  
  /**
   * @returns {string} Title for current calendar period
   */
  private get title(): string {
    if (!this.start || !this.end)
      return '';

    const startMonth = this.monthFormatter(this.start);
    const endMonth = this.monthFormatter(this.end);

    const startYear = this.start.year;
    const endYear = this.end.year;

    const startDay = this.start.day;
    const endDay = this.end.day;

    switch (this.type) {
      case 'month':
        return `${startMonth} ${startYear}`;
      case 'week':
      case '4day':
        return `${startDay} ${startMonth} ${startYear} - ${endDay} ${endMonth} ${endYear}`;
      case 'day':
        return `${startDay} ${startMonth} ${startYear}`;
    }
    return '';
  }
  
  get monthFormatter() {
    return this.calendarInstance.getFormatter({
      timeZone: 'UTC', month: 'long',
    });
  }

  /*** Watchers ***/
  
  /**
   * Watcher: When the list of selected sites is changed
   */
  @Watch('selectedSitesIds')
  eventsChanged(val: any, oldVal: any) {
    if (val && this.selectedSitesIdsOriginal && JSON.stringify(val)!=JSON.stringify(this.selectedSitesIdsOriginal)) {
      // For some reason oldVal always = val. It might be because the array ref isn't changed.
      // selectedSitesIdsOriginal is always null initially.
      this.updateCurrentDisplayEvents();
      this.updateEvents();
    }
    
    if (!this.selectedSitesIdsOriginal)
      this.selectedSitesIdsOriginal = val.slice(0);
  }

  @Watch('type')
  typeChanged(val: any, oldVal: any) {
    this.dragEvent = null;
    this.originalDragEvent = null;

    Vue.nextTick(() => {
      this.calendarInstance.scrollToTime('08:00');
    });
  }

  /*** Methods ***/

  resetCalendarHeight() {
    // Set min height for the calendar. (I can't figure out how to make this work in css...)
    this.calendarHeight = window.innerHeight - (document.getElementsByClassName('top-nav')[0].clientHeight + document.getElementsByClassName('v-footer')[0].clientHeight);
  }
  
  /**
   * Called when the calendar is changed.
   */
  calendarChanged({ start, end }) {
    if (this.start && this.start.date == start.date && this.end && this.end.date == end.date)
      return;

    this.start = start;
    this.end = end;

    this.updateEvents();
  }
  
  /**
   * Loads (if not already) the selected month's events plus one month buffer on either side.
   */
  updateEvents() {

    if (!this.start || !this.end)
      return;

    this.dragEvent = null;
    this.originalDragEvent = null;

    const prev = new Date(this.start.year, this.start.month-2); // prev month
    const next = new Date(this.end.year, this.end.month); // next month

    this.selectedSitesIds.forEach(id => {

      let start = this.start;
      let end = this.end;
      let monthsToAdd = [];

      // if no months are currently loaded
      if ((Object.keys(this.loadedMonths).length === 0 && this.loadedMonths.constructor === Object) ||
      !this.loadedMonths[id]) {
        monthsToAdd.push([prev.getFullYear(), prev.getMonth() + 1]);
        monthsToAdd.push([start.year, start.month]);
        monthsToAdd.push([next.getFullYear(), next.getMonth() + 1]);
      }
      else {
        // if previous month's events are not already loaded
        if (!this.loadedMonths[id][prev.getFullYear()] || !this.loadedMonths[id][prev.getFullYear()].includes(prev.getMonth() + 1))
          monthsToAdd.push([prev.getFullYear(), prev.getMonth() + 1]);
          
        // if current month's events are not already loaded
        if (!this.loadedMonths[id][start.year] || !this.loadedMonths[id][start.year].includes(start.month))
          monthsToAdd.push([start.year, start.month]);

        // if next month's events are not already loaded
        if (!this.loadedMonths[id][next.getFullYear()] || !this.loadedMonths[id][next.getFullYear()].includes(next.getMonth() + 1))
          monthsToAdd.push([next.getFullYear(), next.getMonth() + 1]);
      }

      // if there are months that need events loaded
      if (monthsToAdd.length > 0) {
        this.loadEventsFromServer(id, monthsToAdd);
      }
      else
        this.updateCurrentDisplayEvents();
    });
  }

  /**
   * @param {number} siteID 
   * @param {[[number, number]]} monthsToAdd Array of arrays containing [year, month] in increasing order
   */
  loadEventsFromServer(siteID, monthsToAdd) {
    
    const site = this.bereavementStaffAccessSites.find(s => s.id === siteID);

    const start = monthsToAdd[0][0] + "-" + monthsToAdd[0][1] + "-" + 1; // earliest date needing loaded
    const end = moment(monthsToAdd[monthsToAdd.length-1][0] + "-" + monthsToAdd[monthsToAdd.length-1][1] + "-" + 1).endOf('month').format("YYYY-MM-DD");// latest date needing loaded

    axios.get(site.domain_url + "/cemeteryadmin/calendarEvents/" + start + "/" + end + "/")
    .then(response => {
      if (response.data) {

        // add site data to each event
        let result = response.data.map(event => {
          let o = Object.assign({}, event);
          o.site_id = siteID;
          o.site_color = site.preferences.site_color;
          return o;
        })

        if (!this.allEvents[siteID])
          this.allEvents[siteID] = [];

        this.allEvents[siteID] = this.allEvents[siteID].concat(result);
        this.updateCurrentDisplayEvents();

        // record loaded months so they don't need to be reloaded
        monthsToAdd.forEach(obj => {
          if (!this.loadedMonths[siteID])
            this.loadedMonths[siteID] = {};

          if (!this.loadedMonths[siteID][obj[0]])
            this.loadedMonths[siteID][obj[0]] = [];
          
          if (!this.loadedMonths[siteID][obj[0]].includes(obj[1]))
            this.loadedMonths[siteID][obj[0]].push(obj[1]);
        });
      }
    })
    .catch(response => {
      console.warn('Couldn\'t get data from server: ' + response);
    });
  }

  /**
   * Put the focus back to today's date
   */
  setToday(): void {
    this.focus = null;
  }

  /**
   * Move calendar back
   */
  prev(): void {
    this.calendarInstance.prev();
  }

  /**
   * Move calendar forward
   */
  next(): void {
    this.calendarInstance.next();
  }

  /**
   * Wheel event updates calendar view
   */
  wheelEvent(e){
    if (e.deltaY > 0)
      this.prev();
    else if (e.deltaY < 0)
      this.next();
  }

  /**
   * Updates the array of events currently shown in calendar
   */
  updateCurrentDisplayEvents() {
    let currentDisplayEvents = [];
    if (this.selectedSitesIds) {
      this.selectedSitesIds.forEach(id => {
        if (this.allEvents[id])
          currentDisplayEvents = currentDisplayEvents.concat(this.allEvents[id]);
      });
    }
    this.currentDisplayEvents = currentDisplayEvents;
  }
  
  /**
   * View given day
   */
  viewDay ({ date }) {
    this.focus = date
    this.type = 'day'
  }

  /**
   * Called by click event on an event.
   * If event not being dragged, displays the clicked on event.
   * If event being dragged, stops the drag.
   */
  eventClick ({ nativeEvent, event }) {
    
    // two parts are needed to confirm a drag is taking place
    if (this.eventMovingByDrag && this.dragEvent) {
      this.selectedOpen = false;

      let v = this;

      // stop the event drag
      window.setTimeout(() => {
        v.stopMoveEvent(null);
      });
    }
    else {

      // prevents a drag event beginning
      this.eventMovingByDrag = false;
      this.dragEvent = null;

      const open = () => {
        this.selectedEvent = event;
        this.selectedElement = nativeEvent.target;
        setTimeout(() => this.selectedOpen = true, 10);
      }

      if (this.selectedOpen) {
        this.selectedOpen = false;
        setTimeout(open, 10);
      } else {
        open();
      }
    }

    nativeEvent.stopPropagation();
  }

  /**
   * Called with mousedown on an event.
   * This will begin a drag (which may be immediately cancelled by eventClick if a mouseup occurs)
   */
  moveEvent ({ nativeEvent, event }) {
    if (!this.eventMovingByDrag) {
      // Note: in the future we might want to do this server side as timezone might be different for a site
      const now = moment().tz("Europe/London").format('YYYY-MM-DDTHH:mm');

      if (now < event.start) {
        // shallow clone of original
        this.originalDragEvent = Object.assign({}, event);
        this.dragEvent = event;
        this.mousePositionMinutes = null;
        this.eventMovingByDrag = false; // this gets set to true when the event has actually moved
      }
    }
    nativeEvent.stopPropagation();
  }

  /**
   * Changes an event's datetime during drag
   */
  changeEventDatetime(newDatetime) {
    if (this.dragEvent) {
      
      const currentStart = moment(this.dragEvent.start);
      const currentEnd = moment(this.dragEvent.end);

      let selectedDateTimeDateObj = new Date(newDatetime.year, newDatetime.month-1, newDatetime.day, newDatetime.hour, newDatetime.minute);

      if (!newDatetime.hasTime) {
        // month view, hence no time, so append original time
        selectedDateTimeDateObj.setHours(currentStart.hour());
        selectedDateTimeDateObj.setMinutes(currentStart.minute());
      }

      const selectedDateTime = moment(selectedDateTimeDateObj);

      // don't allow drag if selected datetime is in past
      if (moment().isSameOrAfter(selectedDateTime))
        return;

      // if moved to different day in month view
      if (!newDatetime.hasTime) {

        if (!currentStart.isSame(selectedDateTime, 'day')) {

          // set start datetime
          this.dragEvent.start = selectedDateTime.format("YYYY-MM-DDTHH:mm:ss");
          
          // set end datetime
          selectedDateTimeDateObj.setHours(currentEnd.hour());
          selectedDateTimeDateObj.setMinutes(currentEnd.minute());
          this.dragEvent.end = moment(selectedDateTimeDateObj).format("YYYY-MM-DDTHH:mm:ss");

          this.eventMovingByDrag = true;
        }
      }
      
      // if moved to different time in day view
      else {
        // get the length of the event
        const eventLengthMinutes = this.getEventDurationInMinutes(currentStart, currentEnd);

        // get mouse position from start in minutes
        if (!this.mousePositionMinutes) this.mousePositionMinutes = this.getEventDurationInMinutes(currentStart, selectedDateTime);

        // Get the new start date rounded to the closest 15 minutes.
        // 'newDatetime' is interpreted as a midway point. So to get event start time subtract mousePositionMinutes
        const newStart = this.getRoundedDate(selectedDateTime.clone().subtract(this.mousePositionMinutes, 'minutes'));

        // only allow drag if time has actually changed and time is not in past
        if (!newStart.isSame(currentStart, 'minutes') && !moment().isSameOrAfter(newStart)) {
          const newEnd = this.getRoundedDate(selectedDateTime.clone().add(eventLengthMinutes - this.mousePositionMinutes, 'minutes'));

          // set the new start and end dates
          this.dragEvent.start = newStart.format("YYYY-MM-DDTHH:mm:ss");
          this.dragEvent.end = newEnd.format("YYYY-MM-DDTHH:mm:ss");

          this.eventMovingByDrag = true;
        }
      }
    }
  }

  /**
   * Restore event date to the original
   */
  undoMove() {

    this.dragEvent.start = this.originalDragEvent.start;
    this.dragEvent.end = this.originalDragEvent.end;
    this.dragEvent = null;
    this.originalDragEvent = null;
  }

  /**
   * If an event is being moved, this will stop it and offer to save the new datetime.
   */
  stopMoveEvent (e) {
    
    if (this.eventMovingByDrag) {

      let v = this;
    
      window.setTimeout(() => {

        // this ends the drag
        v.eventMovingByDrag = false;

        if (v.dragEvent.start !== v.originalDragEvent.start) {

          const newStart = moment(v.dragEvent.start);
          const newEnd = moment(v.dragEvent.end);

          const eventType = v.$store.getters.getEventType(parseInt(v.dragEvent.site_id), v.dragEvent.event_type_id);
          const otherEvents = v.$store.getters.getEventsInSameCategoryAndDay(parseInt(v.dragEvent.site_id), newStart.format("YYYY-MM-DD"), v.dragEvent.event_category, v.dragEvent.id);

          // validate new date and time
          let validationResult = validateEventDate(newStart, eventType, otherEvents, v.enforceTimeRestrictions);

          if (!validationResult)
            validationResult = validateEventTime(newStart, newEnd, eventType, otherEvents, v.enforceTimeRestrictions);
          
          if (validationResult) {
            if (validationResult.strict) {
              // v is an error so validation fails
              v.createErrorNotification(validationResult.title, validationResult.detail ? validationResult.detail : "");
              v.undoMove();
              return;
            }
          }

          const originalStartDate = moment(v.originalDragEvent.start);

          const originalDisplayDate = originalStartDate.format(DISPLAY_DATE_WITH_DAYNAME_MOMENT_FORMAT);
          const newDisplayDate = newStart.format(DISPLAY_DATE_WITH_DAYNAME_MOMENT_FORMAT);

          let confirmationMsg = "You have moved v event's start from ";

          // if date has changed
          if (!originalStartDate.isSame(newStart, 'day'))
            confirmationMsg += `${originalDisplayDate} at ${originalStartDate.format(DISPLAY_TIME_MOMENT_FORMAT)} to ${newDisplayDate} at ${newStart.format(DISPLAY_TIME_MOMENT_FORMAT)}.`;
            
          // just time changed
          else
            confirmationMsg += `${originalStartDate.format(DISPLAY_TIME_MOMENT_FORMAT)} to ${newStart.format(DISPLAY_TIME_MOMENT_FORMAT)}.`;

          // if there is a validation warning the user needs to see
          if (validationResult) {
            confirmationMsg += `

              ${validationResult.title}. ${validationResult.detail}`;
          }

          confirmationMsg += `
            
            Do you want to save this change?`;

          v.createConfirmation('Event Moved', confirmationMsg,
          () => {
            const site = v.bereavementStaffAccessSites.find(s => s.id === v.dragEvent.site_id);
            const data = {
              calendar_event: {
                start: newStart.format(SERVER_DATE_MOMENT_FORMAT),
                end: newEnd.format(SERVER_DATE_MOMENT_FORMAT),
              }
            }

            // save new datetime
            axios.patch(site.domain_url + "/cemeteryadmin/funeralEvent/" + v.dragEvent.id + "/", data)
            .then(response => {
              v.createSuccessNotification("Event saved successfully");
              v.dragEvent.display_date = response.data.display_date;
            })
            .catch(error => {
              v.createHTTPErrorNotificationandLog(error, "Event change failed.");
              v.dragEvent.start = v.originalDragEvent.start;
              v.dragEvent.end = v.originalDragEvent.end;
            })
            .finally(() => {
              v.dragEvent = null;
              v.originalDragEvent = null;
            });
          },
          () => {
            v.undoMove();
          },
          'Yes', 'Cancel');
        }
        else {
          v.dragEvent = null;
          v.originalDragEvent = null;
        }
      });
    }
  }

  /**
   * Create a new booking
   */
  newBooking( datetime ) {
    // two parts are needed to confirm a drag is taking place
    if (this.eventMovingByDrag && this.dragEvent) {
      // stop the event drag
      this.stopMoveEvent(null);
      return;
    }

    // ignore past and present
    if (!datetime.future) {
      return;
    }

    // prevents a drag event beginning
    this.dragEvent = null;

    const newBookingDatetime = this.getRoundedDate(moment(new Date(datetime.year, datetime.month-1, datetime.day, datetime.hour, datetime.minute)));
    const newBookingDate = newBookingDatetime.format("YYYY-MM-DD");
    let newBookingTime = null;
    
    if (datetime.hasTime)
      newBookingTime = newBookingDatetime.format("HH:mm");
    
    let newBookingDetails = {
      bookingDate: newBookingDate,
      bookingTime: newBookingTime
    }

    // store date and time
    this.$store.commit('commitBookingDetails', newBookingDetails);

    // preselect first site selected in calendar
    if (this.selectedSitesIds && this.selectedSitesIds[0])
      this.newBookingInitialSiteId = this.selectedSitesIds[0];
    else
      this.newBookingInitialSiteId = '-1';

    this.$router.push({ name: (this.$route.matched[1].meta.parentRouteID + "_bookingdialog"), params: { id: "add", siteID: this.newBookingInitialSiteId, eventTypeID: null } });
  }
  
  /**
   * Round date to closest minute interval
   * @param date Date to be rounded
   * @param minutes Interval in minutes to be rounded to
   */
  getRoundedDate = (date: moment.Moment, minutes: number=15): moment.Moment => {

    date.seconds(Math.round(date.seconds() / 60) * 60);
    date.minutes(Math.round(date.minutes() / minutes) * minutes);

    return date;
  }
  
  /**
   * @returns Length of the event in minutes
   */
  getEventDurationInMinutes(startDate: moment.Moment, endDate: moment.Moment): number {

    let duration = moment.duration(endDate.diff(startDate));
    return duration.asMinutes();
  }

  editEvent(event) {
    this.$router.push({ name: (this.$route.matched[1].meta.parentRouteID + "_bookingdialog"), params: { id: event.id, siteID: event.site_id, eventTypeID: event.event_type_id } });
    this.selectedOpen = false;
  }

  /**
   * Cancels an event (soft delete, event will still exist but with a cancelled status)
   * @param event The event to be cancelled
   */
  cancelEvent(event) {
    this.createConfirmation("Cancel Event", "Are you sure you want to cancel this event?", () => {
      const site = this.bereavementStaffAccessSites.find(s => s.id === event.site_id);

      axios.put(site.domain_url + "/cemeteryadmin/funeralEvent/" + event.id + "/cancel/")
      .then(response => {
        this.createSuccessNotification("Event cancelled successfully");
        const index: number = this.allEvents[event.site_id].findIndex((e) => { return e.id === event.id });

        if (index > -1) {
          this.allEvents[event.site_id].splice(index, 1);
          this.updateCurrentDisplayEvents();
        }
      })
      .catch(error => {
        this.createHTTPErrorNotificationandLog(error, "Event cancel failed.");
      })
      .finally(() => {
        this.selectedOpen = false;
      });
    })
  }

  /**
   * Vue router beforeRouteUpdate in-component guard
   * Check to see if an event has been created/modified/deleted.
   */
  beforeRouteUpdate (to, from, next) {

    // if navigating back to this component (i.e. closing dialog)
    if (to.name === 'calendar') {
      // refreshes events
      this.updateEvents();
    }
    
    next();
  }
}
</script>