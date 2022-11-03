<template>
  <div>
    <div v-show="!loadingGraveOwners" :key="key">

      <v-row v-if="(radioSelection===0 || isNewNextOfKin) && $store.state.Booking.bookingDetails['status']!==7">
        <v-col cols="12" class="py-0">
          <v-radio-group v-model="radioSelection"
            @change="clearNextOfKinData()">
            <v-radio
              label="No Next of Kin"
              value.number="0"
            ></v-radio>
            <v-radio
              label="Add Next of Kin"
              value.number="1"
            ></v-radio>
            <v-radio
              v-if="graveOwnersList && graveOwnersList.length"
              label="Next of Kin is a grave owner"
              value.number="2"
            ></v-radio>
          </v-radio-group>
        </v-col>
      </v-row>

      <v-row v-else>
        <v-col cols="12" class="py-4">
          <h3 v-if="radioSelection===2" class="pb-4">* Next of Kin is a grave owner *</h3>
          <h3 v-if="radioSelection===0" class="pb-4">* No Next of Kin recorded *</h3>
          <v-btn v-if="!readonly" color="primary" @click="removeNextOfKin">Change Next of Kin</v-btn>
        </v-col>
      </v-row>

      <v-row v-if="radioSelection===2 && graveOwnersList && isNewNextOfKin">
        <v-col cols="12" sm="2" class="py-1">
          <h3>Grave Owners</h3>
        </v-col>
        <v-col cols="12" sm="10" class="py-0">
          <v-select
            v-model="bookingNextOfKin['id']"
            :items="graveOwnersList"
            item-text="display_name"
            item-value="owner_id"
            label="Grave Owners"
            required
            clearable
            @change="graveOwnerSelected"
            :rules="[() => !!bookingNextOfKin['id'] || 'This field is required']"
          ></v-select>
        </v-col>
      </v-row>

      <v-row v-if="radioSelection>0">
        <v-col cols="12" sm="2" class="py-1">
          <h3 style="font-size: 1.1em;">Relationship to Decesased</h3>
        </v-col>
        <v-col cols="12" sm="10" class="py-0">
          <v-row>
            <v-col cols="12" class="py-1">
              <v-text-field
                v-model="bookingPersonDetails['next_of_kin_relationship']"
                label="Relationship to Decesased"
                maxlength="50"
                :disabled="readonly"
                :rules="[() => !!bookingPersonDetails['next_of_kin_relationship'] || 'This field is required']"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      
      <PersonCompanyForm v-if="radioSelection>0" v-show="radioSelection===1 || bookingNextOfKin['id']" :personOrCompany="bookingNextOfKin" :address="personAddress" :readonly="readonly" :readonlyEssential="radioSelection===2"></PersonCompanyForm>

    </div>
    <v-row v-if="loadingGraveOwners"
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
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import axios from 'axios';
import { Prop } from 'vue-property-decorator';

@Component({
  components: {
    PersonCompanyForm: () => import('@/main/components/Booking/BookingFormComponents/PersonCompanyForm.vue'),
  }
})
export default class NextOfKin extends Vue {

  @Prop() id;
  @Prop() siteID;

  dateMenu: boolean = false;
  readonly: boolean = true;

  radioSelection: number = 0;

  graveOwnersList = null;
  loadingGraveOwners = false;

  key: number = 0;

  mounted() {
    if (this.$store.state.Booking.bookingDetails['status'] !== 7)
      this.readonly = false;

    if (this.graveplotID) {

      this.loadingGraveOwners = true;

      // get list of current grave owners
      axios.get(this.site.domain_url + '/api/graveOwnersList/person/current/' + this.graveplotID)
      .then(response => {
        this.graveOwnersList = response.data;
      
        if (this.$store.state.Booking.bookingDetails.next_of_kin_person && this.bookingNextOfKin['id']) {
          this.bookingNextOfKin['is_owner'] = !!this.graveOwnersList.find(obj => obj.owner_id === this.bookingNextOfKin['id']);
          this.radioSelection = this.bookingNextOfKin['is_owner'] ? 2 : 1;
        }
      })
      .catch(response => {
        console.warn('Couldn\'t get data from server: ' + response);
      })
      .finally(() => {
        this.loadingGraveOwners = false;
      });
    }
    else if (this.bookingNextOfKin['id'])
      this.radioSelection = 1;
  }

  /*** Getters and setters ***/

  get site() {
    return this.$store.getters.getSiteFromId(parseInt(this.siteID));
  }
  
  get bookingPersonDetails() { 
    if (this.$store.state.Booking.bookingDetails.person)
      return this.$store.state.Booking.bookingDetails.person; 
    else {
      this.bookingPersonDetails = { death: {} };
      return this.bookingPersonDetails;
    }
  }
  set bookingPersonDetails(val) { this.$store.commit('modifyBookingDetails', { key: 'person', value: {} }); }

  get bookingNextOfKin() { 
    if (this.$store.state.Booking.bookingDetails.next_of_kin_person)
      return this.$store.state.Booking.bookingDetails.next_of_kin_person; 
    else {
      this.bookingNextOfKin = {};
      return this.bookingNextOfKin;
    }
  }
  set bookingNextOfKin(val) { 
    this.$store.commit('modifyBookingDetails', { key: 'next_of_kin_person', value: { current_addresses: [{}] } }); 
  }

  get personAddress() {
    // if no addresses
    if (!this.bookingNextOfKin['current_addresses'] || !this.bookingNextOfKin['current_addresses'].length) {

      // if an existing person, don't allow adding address
      if (this.bookingNextOfKin['id'])
        return null;

      this.bookingNextOfKin['current_addresses'] = [{}];
    }
    
    return this.bookingNextOfKin['current_addresses'][0];
  }
  
  get graveplotID() { 
    if (this.$store.state.Booking.bookingDetails.burial && this.$store.state.Booking.bookingDetails.burial.graveplot_id)
      return this.$store.state.Booking.bookingDetails.burial.graveplot_id; 
    else
      return null;
  }

  get isNewNextOfKin(): boolean {
    if (this.$store.state.Booking.bookingDetails.next_of_kin_person && this.bookingNextOfKin['id'] && this.bookingPersonDetails['next_of_kin'] && this.bookingNextOfKin['id'] === this.bookingPersonDetails['next_of_kin'] )
      return false;
    else
      return true;
  }

  /*** Methods ***/

  /**
   * Called when a grave owner is selected to be used as next of kin
   */
  graveOwnerSelected(): void {
    
    this.clearNextOfKinData(true);
    this.key += 1;

    // if nextOfKinIsOwner selected but no person yet selected, make all fields readonly
    this.readonly = this.radioSelection===2 && !this.bookingNextOfKin['id'];

    if (this.bookingNextOfKin['id']) {
      // get detail of selected person
      axios.get(this.site.domain_url + '/api/person/?id=' + this.bookingNextOfKin['id'])
      .then(response => {
        Object.assign(this.bookingNextOfKin, response.data);
        this.bookingNextOfKin['is_owner'] = true;

        this.key += 1;
      })
      .catch(response => {
        console.warn('Couldn\'t get data from server: ' + response);
      })
      .finally(() => {
        //this.loadingGraveOwners = false;
      });
    }
  }

  /**
   * Removes saved link to next of kin (doesn't actually delete anything!)
   */
  removeNextOfKin(): void {
    this.radioSelection = 0;
    this.clearNextOfKinData();
  }

  /**
   * Clear the next of kin object (without losing reference)
   * @param {boolean} ignoreID
   */
  clearNextOfKinData(ignoreID: boolean=false): void {
    for (let key in this.bookingNextOfKin){
      if ((!ignoreID || key !== 'id') && this.bookingNextOfKin.hasOwnProperty(key)){

        if (key==='current_addresses' && this.bookingNextOfKin[key].length)
          this.bookingNextOfKin[key].length = 0;
        this.bookingNextOfKin[key] = null;
      }
    }

    this.bookingPersonDetails['next_of_kin_relationship'] = null;
  }
}
</script>