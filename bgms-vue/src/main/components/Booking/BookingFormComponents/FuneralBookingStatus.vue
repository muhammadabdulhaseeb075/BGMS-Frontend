<template>
  <div>
    <v-row>
      <v-col cols="12" class="pt-4 pb-0 font-weight-bold">
        Booking Status:  
        <v-chip class="green lighten-2">{{ bookingStatus }}</v-chip>
      </v-col>
    </v-row>
    <div v-if="!bookingDetails.status || bookingDetails.status < 4">
      <v-row v-for="item in preburialCheckListItems" :key="item.value">
        <v-col cols="12" class="py-0">
          <v-checkbox 
            v-model="preburialChecklist"
            :label="item.label"
            :value="item.value"
            hide-details
            :disabled="readonly"
          ></v-checkbox>
        </v-col>
      </v-row>
    </div>
    <div v-if="bookingDetails.status && (bookingDetails.status===4 || bookingDetails.status===5)">
      <v-row v-for="item in postburialCheckListItems" :key="item.value">
        <v-col cols="12" class="py-0">
          <v-checkbox 
            v-model="postburialChecklist"
            :label="item.label"
            :value="item.value"
            hide-details
            :disabled="readonly"
          ></v-checkbox>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop, Watch } from 'vue-property-decorator';

@Component
export default class FuneralBookingStatus extends Vue {

  // In the future this should come from database table
  preburialCheckListItems = [
    { label: 'Check grave details entered in booking are valid', value: 'grave_details' },
    { label: 'Check grave on the ground and that the depth is available', value: 'grave_on_ground' },
    { label: 'Notice of interment form received and copy loaded to system', value: 'notice_of_interment' },
    { label: 'Certificate for Burial/Cremation received', value: 'burial_certificate' },
    { label: 'Details on NOI form confirmed and accepted', value: 'noi_details' },
    { label: 'Check burial grant details agree with NOI', value: 'burial_grant_noi' },
    { label: 'Indemnity received where no burial grant', value: 'indemnity' },
    { label: 'Completed instruction to gravedigger form', value: 'gravedigger' },
    { label: 'Signed off by team leader', value: 'signed_off' },
    { label: 'Invoice sent/paid', value: 'invoice' }
  ]

  postburialCheckListItems = [
    { label: 'Backfill completed', value: 'backfill_completed' },
    { label: 'Plot inspected', value: 'plot_inspected' }
  ]

  preburialChecklist: [] = [];
  postburialChecklist: [] = [];

  readonly: boolean = true;

  created() {
    if (this.bookingDetails['preburial_checklist'])
      this.preburialChecklist = JSON.parse(this.bookingDetails['preburial_checklist']);

    if (this.bookingDetails['postburial_checklist'])
      this.postburialChecklist = JSON.parse(this.bookingDetails['postburial_checklist']);

    if (this.$store.state.Booking.bookingDetails['status'] !== 7)
      this.readonly = false;
  }
  
  get bookingDetails() {
    return this.$store.state.Booking.bookingDetails;
  }
  
  get bookingStatus() {
    if (this.bookingDetails.status != null)
      return this.$store.state.Booking.bookingStatusChoices.find((stat) => stat.value===this.bookingDetails.status).text;
    else
      return this.$store.state.Booking.bookingStatusChoices.find((stat) => stat.value===2).text;
  }

  @Watch('preburialChecklist')
  onPreburialChecklistChanged(val: any, oldVal: any) {
    this.bookingDetails['preburial_checklist'] = JSON.stringify(val);
  }

  @Watch('postburialChecklist')
  onPostburialChecklistChanged(val: any, oldVal: any) {
    this.bookingDetails['postburial_checklist'] = JSON.stringify(val);
  }
}
</script>