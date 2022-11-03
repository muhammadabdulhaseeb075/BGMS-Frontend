<template>
  <div v-if="!loadingData">
    <v-row>
      <v-col cols="12" sm="2" class="py-4">
        <h3>Grave</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-0">
        <v-row>
          <v-col cols="12" sm="4" class="py-1" v-if="allSections && allSections.length > 0">
            <v-autocomplete
              label="Section"
              item-text="section_name"
              item-value="id"
              v-model="selectedSection"
              :disabled="readonly"
              :items="allSections"
              clearable>
            </v-autocomplete>
          </v-col>
          <v-col cols="12" sm="4" class="py-1" v-if="allSubsections && allSubsections.length > 0">
            <v-autocomplete
              label="Subsection"
              item-text="subsection_name"
              item-value="id"
              v-model="selectedSubsection"
              :items="allSubsectionsFiltered"
              :disabled="!allSubsectionsFiltered.length || readonly"
              clearable>
            </v-autocomplete>
          </v-col>
          <v-col cols="12" sm="4" class="py-1" v-if="allGraves && allGraves.length > 0">
            <v-autocomplete
              label="Grave Number"
              item-text="grave_number"
              item-value="id"
              v-model="graveNumber"
              :items="allGravesFiltered"
              :disabled="!allGravesFiltered.length || readonly"
              clearable>
            </v-autocomplete>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row v-if="site.religion && site.religion.length">
      <v-col cols="12" sm="2" class="py-4">
        <h3>Religion</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-1">
        <v-select 
          v-model="$store.state.Booking.bookingDetails.person.death['religion']"
          :items="site.religion"
          item-value="id"
          item-text="religion"
        ></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="2" class="py-1">
        <h3 style="font-size: 1.1em;">Coffin/Casket Size</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-1">
        <v-row>
          <v-col cols="12" sm="4" class="py-1" v-if="coffinSizeOptions && coffinSizeOptions.length > 0">
            <v-autocomplete
              label="Width"
              v-model="bookingBurialDetails['coffin_width']"
              :disabled="readonly"
              :items="coffinSizeOptions"
              clearable
              :suffix="bookingBurialDetails['coffin_units']">
            </v-autocomplete>
          </v-col>
          <v-col cols="12" sm="4" class="py-1" v-if="coffinSizeOptions && coffinSizeOptions.length > 0">
            <v-autocomplete
              label="Height"
              v-model="bookingBurialDetails['coffin_height']"
              :items="coffinSizeOptions"
              :disabled="readonly"
              clearable
              :suffix="bookingBurialDetails['coffin_units']">
            </v-autocomplete>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="2" class="py-4">
        <h3>Ashes</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-0">
        <v-checkbox 
          class="py-0"
          v-model="bookingBurialDetails['cremated']"
          :disabled="readonly"
        ></v-checkbox>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="2" class="py-1">
        <h3>Meeting Location</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-1">
        <v-text-field
          v-model="$store.state.Booking.bookingDetails['meeting_location']"
          label="Meeting Location"
          maxlength="50"
          :disabled="readonly"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="2" class="py-4">
        <h3>Comments</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-0">
        <v-row>
          <v-col cols="12" class="py-1">
            <v-textarea
              v-model="bookingBurialDetails['burial_remarks']"
              label="Comments"
              auto-grow
              :disabled="readonly"
              maxLength="200"
              rows="1">
            </v-textarea>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
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
</template>

<script lang='ts'>
import Vue from 'vue';
import Component, { mixins } from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import GraveLocation from '@/mixins/graveLocation.ts';
import NotificationMixin from '@/mixins/notificationMixin.ts';

@Component
export default class Burial extends mixins(GraveLocation, NotificationMixin) {

  @Prop() id;
  @Prop() siteID;
  @Prop() eventTypeID;
  
  readonly: boolean = true;

  coffinSizeOptions = [{text: 1, value: 1},{text: 2, value: 2},{text: 3, value: 3},{text: 4, value: 4},{text: 5, value: 5},{text: 6, value: 6},{text: 7, value: 7},{text: 8, value: 8},{text: 9, value: 9}];


  created() {
    this.domainURL = this.site.domain_url;

    if (this.$store.state.Booking.bookingDetails['status'] !== 7)
      this.readonly = false;

    if (this.id==='add' && this.bookingBurialDetails['cremated'] == null) {
      const eventType = this.$store.getters.getEventType(parseInt(this.siteID), parseInt(this.eventTypeID));

      if (eventType) {
        const eventTypeName = eventType.name.toLowerCase();

        // if new event and event name contains 'ash' or 'cremat' then automatically set cremated field to true
        if (eventTypeName.includes("ash") || eventTypeName.includes("cremat"))
          this.bookingBurialDetails['cremated'] = true;
      }
    }

    if (!this.bookingBurialDetails['coffin_units'])
      this.bookingBurialDetails['coffin_units'] = 'ft';
  }

  get site() {
    return this.$store.getters.getSiteFromId(parseInt(this.siteID));
  }
  
  get bookingBurialDetails() { 
    if (this.$store.state.Booking.bookingDetails.burial)
      return this.$store.state.Booking.bookingDetails.burial; 
    else {
      this.bookingBurialDetails = { burial: {} };
      return this.bookingBurialDetails;
    }
  }
  set bookingBurialDetails(val) { this.$store.commit('modifyBookingDetails', { key: 'burial', value: {} }); }

  get graveNumber() {
    if (this.selectedGraveId !== this.bookingBurialDetails['graveplot_id'])
      this.selectedGraveId = this.bookingBurialDetails['graveplot_id'];

    return this.bookingBurialDetails['graveplot_id'];
  }
  set graveNumber(grave) {
    this.selectedGraveId = grave;
    this.bookingBurialDetails['graveplot_id'] = grave;
  }

  get loadingData() {
    return this.loadingSections || this.loadingSubsections || this.loadingGraves;
  }

}
</script>