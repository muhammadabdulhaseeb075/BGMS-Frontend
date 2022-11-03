<template>
<div id="popup" class="ol-popup">
  <!-- <a href="#" id="popup-closer" class="ol-popup-closer"></a> -->
  <button type="button" class="close" data-dismiss="alert" aria-label="Close" @click='scope.closeHandler()'>
    <span aria-hidden="true">&times;</span>
  </button>
  <div id="popup-content"><h4><strong>{{scope.first_names}} {{scope.last_name}}</strong></h4></div>
  <div id="popup-content" v-if="scope.burial && scope.burial_date"><p>Date of burial:&nbsp;{{showYearIfImpossibleMonthIsNotDefined(scope)}}</p></div>
  <div id="popup-content" v-if="scope.burial && scope.age"><p>Age:&nbsp;{{scope.age.age}} {{scope.age.units}}</p></div>
  <div id="popup-content" v-if="scope.burial && graveNumber && graveUUID && $store.getters.getBookingForm" @click="sendToBooking"><a class="">Link to booking</a></div>
  <!--<button type="button" class="btn btn-bgms" aria-label="More Details" ng-click='moreDetails(id)'> More Details </button>-->
</div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component, { mixins } from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import axios from 'axios'
import {  formatDate } from '@/global-static/dataFormattingAndValidation.ts';
import NotificationMixin from '@/mixins/notificationMixin.ts';

@Component
export default class BasicDetailsMarker extends mixins(NotificationMixin) {

  @Prop() scope;
  
  formatDate = formatDate;
  graveNumber = null;
  graveUUID = null;

  mounted() {
    const graveDetailsURL = '/mapmanagement/graveDetails/?graveplot_uuid=' + this.scope.grave_id
    
    axios.get(graveDetailsURL)
    .then((response) => {
      debugger; // eslint-disable-line no-debugger
      if(response.data && response.data.grave_number){
        this.graveNumber = response.data.grave_number
      }
      if(response.data && response.data.id){
        this.graveUUID = response.data.id;
      }
    });
  }

  readonly YEAR = 0;
  showYearIfImpossibleMonthIsNotDefined(person) {
    if((!person.has_impossible_month || !person.impossible_date_month) && person.burial_date){
      return person.burial_date.split('-')[this.YEAR];
    } else {
      return formatDate(person.burial_date)
    }
  }

  sendToBooking() {
    debugger; // eslint-disable-line no-debugger
    this.createConfirmation(
      "Confirmation needed",
      "Send to Booking form", 
      () => {
        debugger; // eslint-disable-line no-debugger
        let booking_link = this.generateLinkToBooking();
        window.location.assign(booking_link);
      }
    )
  }

  // Passing booking form cache via URL
  generateLinkToBooking() {
    debugger; // eslint-disable-line no-debugger
    const bookingForm = this.$store.getters.getBookingForm;
    const {adminDomain, siteId} = this.$store.getters.getRedirectMetadata;
    let bookingURL = "";

    if (bookingForm) {
      bookingForm.detailsGraveNumber = this.graveNumber;
      bookingForm.detailsBurialUUID = this.graveUUID;
      const adminOrigin = adminDomain
        ? decodeURIComponent(adminDomain)
        : window.location.origin;
      const parseForm = btoa(JSON.stringify(bookingForm));
      bookingURL = `${adminOrigin}/main/#/booking/add-event?bookingForm=${parseForm}&siteId=${siteId}`;
    }

    return bookingURL;
  }
}
</script>
