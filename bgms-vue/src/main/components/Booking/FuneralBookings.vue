<template>
  <v-container id="funeralBookings">
    
    <SiteSelection></SiteSelection>

    <v-card
      class="mb-4"
      outlined>
      <v-card-title class="pt-2 pb-0">
        Filter
        <v-btn 
          class="mx-4"
          text
          @click="$store.commit('resetFuneralTableFilters')">Reset</v-btn>
      </v-card-title>
      <v-card-text class="py-2">
        
        <v-row>
          <v-col cols="12" sm="3" lg="2" class="pt-5 px-4">
            <h3>Deceased</h3>
          </v-col>
          <v-col cols="12" sm="6" lg="4" class="py-0">
            <v-row>
              <v-col cols="12" class="py-0">
                <v-text-field
                  v-model="funeralTableFilters['name']"
                  label="Name"
                  hide-details
                  clearable
                ></v-text-field>
              </v-col>
            </v-row>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" sm="3" lg="2" class="pt-5 px-4">
            <h3>Funeral Director</h3>
          </v-col>
          <v-col cols="12" sm="9" lg="4" class="py-0">
            <v-select
              :loading="loadingFuneralDirectors"
              :disabled="loadingFuneralDirectors || !funeralDirectorsList || !funeralDirectorsList.length"
              v-model="funeralTableFilters['funeral_director_id']"
              :items="funeralDirectorsList"
              item-text="name"
              item-value="id"
              label="Funeral Director"
              clearable
              hide-details
            ></v-select>
          </v-col>
          <v-col cols="12" sm="3" lg="2" class="pt-5 px-4">
            <h3>Funeral Date</h3>
          </v-col>
          <v-col cols="12" sm="9" lg="4" class="py-0">
            <v-row>
              <v-col cols="3" class="py-0">
                <v-select
                  v-model="funeralTableFilters['day']"
                  label="Day"
                  :items="days"
                  hide-details
                  clearable
                ></v-select>
              </v-col>
              <v-col cols="5" class="py-0">
                <v-select
                  class="d-flex"
                  v-model="funeralTableFilters['month']"
                  label="Month"
                  :items="months"
                  hide-details
                  clearable
                ></v-select>
              </v-col>
              <v-col cols="4" class="py-0">
                <v-text-field
                  v-model="funeralTableFilters['year']"
                  label="Year"
                  hide-details
                  clearable
                ></v-text-field>
              </v-col>
            </v-row>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" sm="3" lg="2" class="pt-5 px-4">
            <h3>Booking Person</h3>
          </v-col>
          <v-col cols="12" sm="9" lg="4" class="py-0">
            <v-row>
              <v-col cols="12" class="py-0">
                <v-select
                  v-model="funeralTableFilters['created_by_id']"
                  label="Name"
                  :items="funeralBookingCreatorsSorted"
                  hide-details
                  item-text="created_by_name"
                  item-value="created_by_id"
                  clearable
                  :loading="loadingFuneralCreators"
                ></v-select>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="12" sm="3" lg="2" class="pt-5 px-4">
            <h3>Booking Date</h3>
          </v-col>
          <v-col cols="12" sm="9" lg="4" class="py-0">
            <v-row>
              <v-col cols="3" class="py-0">
                <v-select
                  v-model="funeralTableFilters['created_day']"
                  label="Day"
                  :items="days"
                  hide-details
                  clearable
                ></v-select>
              </v-col>
              <v-col cols="5" class="py-0">
                <v-select
                  class="d-flex"
                  v-model="funeralTableFilters['created_month']"
                  label="Month"
                  :items="months"
                  hide-details
                  clearable
                ></v-select>
              </v-col>
              <v-col cols="4" class="py-0">
                <v-text-field
                  v-model="funeralTableFilters['created_year']"
                  label="Year"
                  hide-details
                  clearable
                ></v-text-field>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
        
        <v-row>
          <v-col cols="12" sm="3" lg="2" class="pt-5 px-4">
            <h3>Booking Status</h3>
          </v-col>
          <v-col cols="12" sm="9" lg="10" class="py-0">
            <v-row>
              <v-col cols="12" class="py-0">
                <v-select
                  :value="funeralTableFilters['status']"
                  @change="updateFilterStatus"
                  :items="$store.state.Booking.bookingStatusChoices"
                  item-text="text"
                  item-value="value"
                  label="Booking Status"
                  hide-details
                  multiple
                  chips
                  clearable>

                  <template v-slot:prepend-item>
                    <v-list-item
                      ripple
                      @click="toggleSelectedStatus">
                      <v-list-item-action>
                        <v-icon :color="funeralTableFilters['status'].length > 0 ? 'indigo darken-4' : ''">{{ statusSelectIcon }}</v-icon>
                      </v-list-item-action>
                      <v-list-item-content>
                        <v-list-item-title>{{ allStatusesSelected ? 'Unselect All' : 'Select All' }}</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <v-divider class="mt-2"></v-divider>
                  </template>

                  <template slot="selection" slot-scope="data">
                    <v-chip v-if="data.index <= 10"
                      close
                      @click:close="data.parent.selectItem(data.item)">
                      <strong>{{ data.item.text }}</strong>
                    </v-chip>
                  </template>

                </v-select>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-data-table
      :headers="headers"
      :items="items"
      :options.sync="funeralTableOptions"
      class="elevation-1"
      :server-items-length="serverItemsLength"
      must-sort
      @click:row="editEvent"
      :loading="loadingEvents">
      <template v-slot:item.site_id="{ item }">
        <v-chip :color="getSiteObject(item.site_id).preferences.site_color" dark>{{ getSiteObject(item.site_id).name }}</v-chip>
      </template>
      <template v-if="funeralDirectorsList && funeralDirectorsList.length" v-slot:item.funeral_director_id="{ item }">
        {{ getFuneralDirectorName(item.funeral_director_id) }}
      </template>
      <template v-slot:item.status="{ item }">
        {{ $store.state.Booking.bookingStatusChoices.find((stat) => stat.value===item.status).text }}
      </template>
    </v-data-table>

    <router-view v-if="bereavementStaffAccessSites && bereavementStaffAccessSites.length"></router-view>

  </v-container>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component, { mixins } from 'vue-class-component';
import { Watch } from 'vue-property-decorator'
import axios from 'axios'
import NotificationMixin from '@/mixins/notificationMixin.ts';
import SiteSelection from '@/main/components/Booking/SiteSelection.vue';

// Register the router hooks with their names
Component.registerHooks([
  'beforeRouteUpdate'
])

/**
 * Component for displaying table of funeral events
 */
@Component({
  components: {
    SiteSelection
  }
})
export default class FuneralBookings extends mixins(NotificationMixin) {

  selectedEvent = {};
  selectedElement = null;
  selectedOpen: boolean = false;
  loadingFuneralCreators: boolean = false;
  loadingEvents: boolean = false;
  loadingFuneralDirectors: boolean = false;
  
  typeNameTimer = null;

  serverItemsLength: number = 0;

  headers = [
    { text: 'Site', value: 'site_id' },
    { text: 'Date', value: 'start_date' },
    { text: 'Time', value: 'start_time', sortable: false },
    { text: 'First Names', value: 'first_names' },
    { text: 'Last Name', value: 'last_name' },
    { text: 'Funeral Director', value: 'funeral_director_id'},
    { text: 'Status', value: 'status'}
  ]
  items = [];

  months = [
    { text: 'January', value: 1 },
    { text: 'February', value: 2 },
    { text: 'March', value: 3 },
    { text: 'April', value: 4 },
    { text: 'May', value: 5 },
    { text: 'June', value: 6 },
    { text: 'July', value: 7 },
    { text: 'August', value: 8 },
    { text: 'September', value: 9 },
    { text: 'October', value: 10 },
    { text: 'November', value: 11 },
    { text: 'December', value: 12 },
  ]

  days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31];

  /*** Lifecycle hooks ***/

  created() {
    if (!this.funeralBookingCreators.length) {

      // get list of funeral booking creators from each site
      this.bereavementStaffAccessSites.forEach(site => {
        this.loadingFuneralCreators = true;

        axios.get(site.domain_url + "/cemeteryadmin/funeralCreators/")
        .then(response => {
          this.loadingFuneralCreators = true;

          if (response.data) {
            response.data.forEach(funeralCreator => {
              if (!this.funeralBookingCreators.find(item => {
                return item.created_by_id === funeralCreator.created_by_id;
              }))
                // add unique users to list
                this.funeralBookingCreators.push(funeralCreator);
            });
          }
        })
        .finally(() => {
          this.loadingFuneralCreators = false;
        });
      });
    }

    if (!this.funeralDirectorsList || !this.funeralDirectorsList.length) {
      // If list of funeral directors has not already been loaded, this will load from server.
      this.loadingFuneralDirectors = true;

      // We're assuming that all sites are in the same client. So just use the first site.
      const siteID = this.$store.getters.getBereavementStaffAccessSites[0].id;

      this.$store.dispatch('getFuneralDirectors', siteID)
      .catch(error => {
        this.createHTTPErrorNotificationandLog(error, "Failed to load list of funeral directors.");
      })
      .finally(() => {
        this.loadingFuneralDirectors = false;
      });
    }

    // show scrollbar
    document.documentElement.style.overflowY = 'scroll';
  }

  destroyed() {
    // return scrollbar to default
    document.documentElement.style.overflowY = 'auto';
  }

  /*** Getters and setters ***/

  get funeralDirectorsList() {
    // Note: this will get funeral directors for one client only
    return this.$store.state.Booking.funeralDirectors;
  }

  /**
   * Get sites user has bereavement staff access to
   */
  get bereavementStaffAccessSites() {
    return this.$store.getters.getBereavementStaffAccessSites;
  }

  get funeralBookingCreators() {
    return this.$store.state.Booking.funeralBookingCreators;
  }

  get funeralBookingCreatorsSorted() {
    return this.funeralBookingCreators.sort((a, b) => a.last_name > b.last_name);
  }

  /**
   * Get sites that user is wanting to display
   */
  get selectedSitesIds() {
    return this.$store.state.Booking.selectedSitesIds;
  }

  /**
   * Get/set table options (note: sorting initial value set in vuex) 
   */
  get funeralTableOptions() {
    return this.$store.state.Booking.funeralTableOptions;
  }
  set funeralTableOptions(options) {
    this.$store.commit('commitFuneralTableOptions', options)
  }

  /**
   * Get table filters
   */
  get funeralTableFilters() {
    return this.$store.state.Booking.funeralTableFilters;
  }

  get allStatusesSelected() {
    return this.funeralTableFilters['status'].length === this.$store.state.Booking.bookingStatusChoices.length;
  }

  get someStatusesSelected() {
    return this.funeralTableFilters['status'].length > 0 && !this.allStatusesSelected;
  }

  get statusSelectIcon() {
    if (this.allStatusesSelected) return 'fas fa-window-close'
    if (this.someStatusesSelected) return 'fas fa-minus-square'
    return 'far fa-square'
  }

  /*** Watchers ***/
  
  /**
   * Reload data when a table option gets changed
   */
  @Watch('funeralTableOptions')
  onOptionsChanged(val: any, oldVal: any) {
    this.getDataFromApi();
  }
  
  /**
   * Reload data when selected sites gets changed
   */
  @Watch('selectedSitesIds')
  onSelectedSitesIdsChanged(val: any, oldVal: any) {
    this.getDataFromApi();
  }
  
  /**
   * Reload data when a table filter gets changed
   */
  @Watch('funeralTableFilters', { deep: true })
  onFiltersChanged(val: any, oldVal: any) {
    this.delay(() => {
      // go back to page 1 before new request
      this.funeralTableOptions['page'] = 1
      this.getDataFromApi();
    }, 400);
  }

  /*** Methods ***/

  /** Retrieve paginated data from server */
  getDataFromApi() {

    if (!this.selectedSitesIds)
      return;
    
    this.loadingEvents = true;

    const limit = this.funeralTableOptions['itemsPerPage'];

    let query_params = "limit=" + limit;
    query_params += "&offset=" + (this.funeralTableOptions['page'] - 1) * limit;

    if (this.funeralTableOptions['sortBy'] && this.funeralTableOptions['sortBy'].length) {
      query_params += "&order_by=" + this.funeralTableOptions['sortBy'][0];

      if (this.funeralTableOptions['sortDesc'] && this.funeralTableOptions['sortDesc'].length && this.funeralTableOptions['sortDesc'][0])
        query_params += "&order_desc=" + true;
    }

    query_params += "&site_ids=" + JSON.stringify(this.selectedSitesIds);

    // if filter exists
    if (this.funeralTableFilters && Object.keys(this.funeralTableFilters).length > 0)
      query_params += "&filters=" + JSON.stringify(this.funeralTableFilters);

    axios.get("/cemeteryadminpublic/funeralEvents/?" + query_params)
    .then(response => {
      this.serverItemsLength = response.data.total_rows;
      this.items = response.data.events;
    })
    .catch(response => {
      console.warn('Couldn\'t get data from server: ' + response);
    })
    .finally(() => {
      this.loadingEvents = false;
    });
  }

  /**
   * Opens dialog for editing a booking
   */
  editEvent(event) {
    this.$router.push({ name: (this.$route.matched[1].meta.parentRouteID + "_bookingdialog"), params: { id: event.id, siteID: event.site_id, eventTypeID: event.event_type_id } });
  }

  /**
   * Get site object by site id
   */
  getSiteObject(siteID: number) {
    return this.bereavementStaffAccessSites.find(s => s.id === siteID);
  }

  /**
   * Delays function being called for keyup event.
   * If another keyup (or keydown) event occurs, the first function is cancelled.
   * Hence function does not run until user stops typing.
   * @param func Function to be called after delay.
   * @param lengthInMs Delay in ms before function is called.
   */
  delay(func, lengthInMs) {
    
    clearTimeout(this.typeNameTimer);
    if (func) this.typeNameTimer = setTimeout(func, lengthInMs);
  }

  /**
   * @param funeralDirectorID
   * @returns Funeral director's full name
   */
  getFuneralDirectorName(funeralDirectorID) {
    const fd = this.funeralDirectorsList.find((fd) => fd.id===funeralDirectorID);
    if (fd)
      return fd.name;
    else
      return null;
  }

  /**
   * Select all statuses if not all already selected.
   * Unselect all statuses if all already selected.
   */
  toggleSelectedStatus() {
    
    const statusesToAdd = this.allStatusesSelected ? [] : this.$store.state.Booking.bookingStatusChoices.map((status) => status.value);

    this.updateFilterStatus(statusesToAdd);
  }

  /**
   * Update filter status array without new reference
   * @param selected
   */
  updateFilterStatus(selected) {

    this.funeralTableFilters['status'].length = 0;
    this.funeralTableFilters['status'].push.apply(this.funeralTableFilters['status'], selected);
    this.getDataFromApi();
  }

  /**
   * Vue router beforeRouteUpdate in-component guard
   * Check to see if an event has been created/modified/deleted.
   */
  beforeRouteUpdate (to, from, next) {

    // if navigating back to this component (i.e. closing dialog)
    if (to.name === 'funeralBookings') {

      // refreshes the table
      this.getDataFromApi();
    }
    
    next();
  }
}
</script>