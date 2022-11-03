<template>
  <div id="booking">
    <v-navigation-drawer
      mini-variant
      permanent
      stateless>

      <v-list nav>
        <v-tooltip right>
          <template v-slot:activator="{ on }">
            <v-list-item link exact v-on="on" :to="{ name: 'home' }">
              <v-list-item-icon>
                <v-icon>fas fa-home</v-icon>
              </v-list-item-icon>
            </v-list-item>
          </template>
          <span>Home</span>
        </v-tooltip>

        <v-divider></v-divider>

        <v-tooltip right>
          <template v-slot:activator="{ on }">
            <v-list-item link exact v-on="on" @click="createNewEvent">
              <v-list-item-icon>
                <v-icon>fas fa-plus</v-icon>
              </v-list-item-icon>
            </v-list-item>
          </template>
          <span>Create new event</span>
        </v-tooltip>

        <v-tooltip right>
          <template v-slot:activator="{ on }">
            <v-list-item link exact v-on="on" :to="{ name: 'calendar' }">
              <v-list-item-icon>
                <v-icon>fas fa-calendar</v-icon>
              </v-list-item-icon>
            </v-list-item>
          </template>
          <span>Calendar</span>
        </v-tooltip>
        <v-tooltip right>
          <template v-slot:activator="{ on }">
            <v-list-item link exact v-on="on" :to="{ name: 'funeralBookings' }">
              <v-list-item-icon>
                <v-icon>fas fa-table</v-icon>
              </v-list-item-icon>
            </v-list-item>
              </template>
          <span>Funeral Bookings</span>
        </v-tooltip>
      </v-list>
    </v-navigation-drawer>

    <v-content>
      <router-view v-if="bereavementStaffAccessSites && bereavementStaffAccessSites.length"></router-view>
    </v-content>

</div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';

@Component
export default class Booking extends Vue {
  
  get bereavementStaffAccessSites() {
    return this.$store.getters.getBereavementStaffAccessSites;
  }

  createNewEvent(){
    let selectedSitesIds = this.$store.state.Booking.selectedSitesIds;
    let newBookingInitialSiteId = '-1';

    // preselect first site selected in calendar
    if (selectedSitesIds && selectedSitesIds[0])
      newBookingInitialSiteId = selectedSitesIds[0];

    this.$router.push({ name: (this.$route.matched[1].meta.parentRouteID + "_bookingdialog"), params: { id: "add", siteID: newBookingInitialSiteId, eventTypeID: '-1' } });
  }
}
</script>