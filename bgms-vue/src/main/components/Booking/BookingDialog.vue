<template>
  <v-dialog
    value="true"
    persistent
    content-class="booking-dialog">
    <v-card v-show="$route.name===(parentRouteID + '_bookingdialog')">
      <v-card-title>
        <span class="headline">New Booking</span>
      </v-card-title>
      <v-card-text>
        <v-form>        
          <v-row v-if="sitesWithEventTypes">
            <v-col cols="12" class="py-1">
              <v-select 
                v-model="selectedSiteId"
                :items="sitesWithEventTypes"
                item-text="name"
                item-value="id"
                label="Site"
                required
                :rules="[() => !!selectedSiteId || 'This field is required']">
              </v-select>
            </v-col>
          </v-row>

          <v-row v-if="selectedSiteId">
            <v-col cols="12" class="py-1">
              <v-btn-toggle v-model="selectedEventTypeID" @change="openForm()">
                <v-btn text v-for="event in selectedSite.event_types" :value="event.id" :key="event.id">
                  {{ event.name }}
                </v-btn>
              </v-btn-toggle>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <div class="flex-grow-1"></div>
        <v-btn @click="closeDialog"><i class="fas fa-times"/>Cancel</v-btn>
      </v-card-actions>
    </v-card>
    
    <router-view v-if="parentRouteID != null"></router-view>

  </v-dialog>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop, Watch } from 'vue-property-decorator';

@Component({
  components: {
    FuneralBookingForm: () => import('@/main/components/Booking/FuneralBookingForm.vue'),
  }
})
export default class BookingDialog extends Vue {

  @Prop() id;
  @Prop() siteID;
  @Prop() eventTypeID;

  selectedSiteId = null;
  selectedEventTypeID = null;

  parentRouteID: number = null;

  /*** Lifecycle hooks ***/

  created() {
    const siteID = parseInt(this.siteID);

    this.parentRouteID = this.$route.matched[1].meta.parentRouteID;

    if (!this.$store.state.Booking.bookingDetails)
      this.$store.commit('commitBookingDetails', {});
    
    /** New event - load site and event type selection */
    if (this.id === 'add') {
      // if only one site with events, preselect it
      if (this.sitesWithEventTypes.length === 1) {
        this.selectedSiteId = this.sitesWithEventTypes[0].id;

        // if site has only one registered event, preselect it
        if (this.sitesWithEventTypes[0].event_types.length === 1) {
          this.selectedEventTypeID = this.sitesWithEventTypes[0].event_types[0].id;
          this.openForm();
        }
      }
      // if site has been preselected (-1 if not)
      else if (siteID !== -1 && this.sitesWithEventTypes.find(obj => obj.id === siteID)) {
        this.selectedSiteId = siteID;
      }
    }
    /** Existing event - load form */
    else {
      this.selectedSiteId = siteID;
      this.selectedEventTypeID = this.eventTypeID;
      this.openForm();
    }
  }

  mounted() {
    // Manually set z-index as Vuetify doesn't get this right.
    // (Something to do with top-nav having z-index of 1030)
    (document.getElementsByClassName('v-dialog__content--active')[0] as HTMLElement).style.zIndex = '1032';

    window.setTimeout(() => {
      (document.getElementsByClassName('v-overlay')[0] as HTMLElement).style.zIndex = '1031';
    });
  }

  /*** Getters and setters ***/

  /**
   * Get sites user has bereavement staff access to and that have event types registered
   */
  get sitesWithEventTypes() {
    const sites = this.$store.getters.getBereavementStaffAccessSites;
    let sitesWithEventTypes = null;

    if (sites) {
      // initially display all sites
      sitesWithEventTypes = sites.filter(obj => {
        if (obj.event_types && obj.event_types.length > 0)
          return obj;
      });
    }
    
    return sitesWithEventTypes;
  }

  /**
   * @returns the currently selected site
   */
  get selectedSite() {
    if (!this.selectedSiteId)
      return null;

    let temp = this.sitesWithEventTypes.find(obj => obj.id === this.selectedSiteId);
    
    return this.sitesWithEventTypes.find(obj => obj.id === this.selectedSiteId)
  }

  /**
   * @returns the currently selected event type
   */
  get selectedEventType() {
    return this.selectedSite.event_types.find(event => event.id === this.selectedEventTypeID);
  }

  /*** Methods ***/

  /**
   * Once a site and event has been choosen, open the form
   */
  openForm() {
    if (this.selectedEventType) {
      if (this.selectedEventType['event_category_id'] === "Funeral") {
        this.$router.replace({ name: this.parentRouteID + "_funeralbooking", params: { siteID: ("" + this.selectedSiteId), eventTypeID: this.selectedEventTypeID } });
      }
    }
  }

  /**
   * Close dialog (from initial selection form)
   */
  closeDialog(): void {
    this.$router.push({ path: this.$route.matched[1].path });
  }
}
</script>