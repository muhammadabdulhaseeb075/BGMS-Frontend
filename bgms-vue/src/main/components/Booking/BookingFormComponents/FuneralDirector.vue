<template>
  <div>
    <v-row>
      <v-col cols="12" sm="2" class="py-4">
        <h3>Funeral Director</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-0">
        <v-row>
          <v-col cols="9" class="py-1">
            <v-select
              :loading="loadingFuneralDirectors"
              :disabled="loadingFuneralDirectors || !funeralDirectorsList || !funeralDirectorsList.length || readonly"
              v-model="bookingDetails['funeral_director_id']"
              :items="funeralDirectorsList"
              item-text="name"
              item-value="id"
              label="Funeral Director"
              required
              clearable
              :rules="[() => !!bookingDetails['funeral_director_id'] || 'This field is required']"
            ></v-select>
          </v-col>
          <v-col cols="3" class="py-1">
            <v-btn
              @click="createNewDialog=true"
              :loading="createNewDialog"
              :disabled="readonly"
            >Create new</v-btn>
          </v-col>
        </v-row>
        <v-row v-if="selectedFuneralDirector && selectedFuneralDirector.company.contact_name">
          <v-col cols="9" class="py-1">
            {{ 'Contact Name: ' + selectedFuneralDirector.company.contact_name }}
          </v-col>
        </v-row>
        <v-row v-if="selectedFuneralDirector && selectedFuneralDirector.company.email">
          <v-col cols="9" class="py-1">
            {{ 'Email Address: ' + selectedFuneralDirector.company.email }}
          </v-col>
        </v-row>
        <v-row v-if="selectedFuneralDirector && selectedFuneralDirector.company.phone_number">
          <v-col cols="9" class="py-1">
            {{ 'Phone Number: ' + selectedFuneralDirector.company.phone_number }}
          </v-col>
        </v-row>
        <v-row v-if="selectedFuneralDirector && selectedFuneralDirector.company.current_addresses && selectedFuneralDirector.company.current_addresses.length">
          <v-col cols="9" class="py-1">
            {{ 'Address: ' + selectedFuneralDirector.company.current_addresses[0].display_address }}
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <FuneralDirectorDialog 
      v-if="createNewDialog"
      @close-dialog="createNewDialog=false"
      @new-fd="newFDCreated($event)"
      :domain="site.domain_url"
    ></FuneralDirectorDialog>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component, { mixins } from 'vue-class-component';
import { Prop, Watch } from 'vue-property-decorator';
import axios from 'axios';
import NotificationMixin from '@/mixins/notificationMixin.ts';

@Component({
  components: {
    FuneralDirectorDialog: () => import('@/main/components/Booking/BookingFormComponents/FuneralDirectorDialog.vue'),
  }
})
export default class FuneralDirector extends mixins(NotificationMixin)  {

  @Prop() id;
  @Prop() siteID;

  createNewDialog: boolean = false;
  loadingFuneralDirectors: boolean = false;
  readonly: boolean = true;

  selectedFuneralDirector = null;

  /*** Lifecycle hooks ***/

  mounted() {
    if (!this.funeralDirectorsList || !this.funeralDirectorsList.length) {
      // If list of funeral directors has not already been loaded, this will load from server.
      this.loadingFuneralDirectors = true;

      this.$store.dispatch('getFuneralDirectors', this.site.id)
      .catch(error => {
        this.createHTTPErrorNotificationandLog(error, "Failed to load list of funeral directors.");
      })
      .finally(() => {
        this.loadingFuneralDirectors = false;
      });
    }

    if (this.$store.state.Booking.bookingDetails['status'] !== 7)
      this.readonly = false;
  }

  /*** Getters and setters ***/

  get funeralDirectorsList() {
    // Note: this will get funeral directors for one client only
    return this.$store.state.Booking.funeralDirectors;
  }
  
  get bookingDetails() {
    return this.$store.state.Booking.bookingDetails;
  }

  get site() {
    return this.$store.getters.getSiteFromId(parseInt(this.siteID));
  }

  /**
   * @returns ID for selected funeral director
   */
  get selectedFuneralDirectorId() {
    if (!this.bookingDetails['funeral_director_id'])
      return false;
    else
      return this.bookingDetails['funeral_director_id'];
  }

  /**
   * @returns Returns list of funeral directors without retirees.
   * Unless a retiree has previously been selected.
   */
  get funeralDirectorsListActive() {
    return this.funeralDirectorsList.filter(fd => 
      !fd.retired || fd.id === this.bookingDetails['funeral_director_id']
    );
  }

  /*** Watchers ***/

  /**
   * Loads funeral director info when a new fd has been selected.
   */
  @Watch('selectedFuneralDirectorId', { immediate: true })
  onFuneralDirectorChanged(val: any, oldVal: any) {
    this.selectedFuneralDirector = null;

    if (val) {
      axios.get(this.site.domain_url + "/cemeteryadmin/funeralDirector/" + val)
      .then(response => {
        this.selectedFuneralDirector = response.data;
      })
      .catch(response => {
      });
    }
  }

  /**
   * Called when a new funeral director has been successfully saved in the dialog.
   */
  newFDCreated(fd) {
    this.funeralDirectorsList.push(fd);
    this.bookingDetails['funeral_director_id'] = fd.id;
  }
}
</script>