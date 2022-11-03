<template>
  <div>
    <v-row>
      <v-col cols="12" sm="2" class="py-4">
        <h3>Name</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-0">
        <v-row>
          <v-col cols="12" sm="2" class="py-1">
            <v-text-field
              v-model="bookingPersonDetails['title']"
              label="Title"
              :disabled="readonly"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="5" class="py-1">
            <v-text-field
              v-model="bookingPersonDetails['first_names']"
              label="First Names"
              :disabled="readonly"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="5" class="py-1">
            <v-text-field
              class='uppercase-text'
              v-model="bookingPersonDetails['last_name']"
              label="Last Name*"
              :disabled="readonly"
              required
              :rules="[() => !!bookingPersonDetails['last_name'] || 'This field is required']"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12" sm="2" class="py-4">
        <h3>Age</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-0">
        <v-row>
          <v-col cols="4" sm="2" class="py-1">
            <v-text-field
              v-model="bookingPersonDetailsDeath['age_years']"
              label="Years"
              type="number"
              :disabled="readonly"
              interval="1"
              min="0">
            </v-text-field>
          </v-col>
          <v-col cols="4" sm="2" class="py-1">
            <v-text-field
              v-model="bookingPersonDetailsDeath['age_months']"
              label="Months"
              type="number"
              :disabled="readonly"
              interval="1"
              min="0">
            </v-text-field>
          </v-col>
          <v-col cols="4" sm="2" class="py-1">
            <v-text-field
              v-model="bookingPersonDetailsDeath['age_weeks']"
              label="Weeks"
              type="number"
              :disabled="readonly"
              interval="1"
              min="0">
            </v-text-field>
          </v-col>
          <v-col cols="4" sm="2" class="py-1">
            <v-text-field
              v-model="bookingPersonDetailsDeath['age_days']"
              label="Days"
              type="number"
              :disabled="readonly"
              interval="1"
              min="0">
            </v-text-field>
          </v-col>
          <v-col cols="4" sm="2" class="py-1">
            <v-text-field
              v-model="bookingPersonDetailsDeath['age_hours']"
              label="Hours"
              type="number"
              :disabled="readonly"
              interval="1"
              min="0">
            </v-text-field>
          </v-col>
          <v-col cols="4" sm="2" class="py-1">
            <v-text-field
              v-model="bookingPersonDetailsDeath['age_minutes']"
              label="Minutes"
              type="number"
              :disabled="readonly"
              interval="1"
              min="0">
            </v-text-field>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12" sm="2" class="py-4">
        <h3>Address</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-0">
        <v-row>
          <v-col cols="12" class="py-1">
            <v-text-field
              v-model="residenceAddress['first_line']"
              label="First Line"
              :disabled="readonly"
              maxlength="200">
            </v-text-field>
          </v-col>
          <v-col cols="12" class="py-1">
            <v-text-field
              v-model="residenceAddress['second_line']"
              label="Second Line"
              :disabled="readonly"
              maxlength="200">
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="residenceAddress['town']"
              label="Town"
              :disabled="readonly"
              maxlength="50">
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="residenceAddress['county']"
              label="County"
              :disabled="readonly"
              maxlength="50">
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="residenceAddress['postcode']"
              label="Post Code"
              :disabled="readonly"
              maxlength="10">
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="residenceAddress['country']"
              label="Country"
              :disabled="readonly"
              maxlength="50">
            </v-text-field>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" sm="2" class="py-4">
        <h3>Death</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-0">
        <v-row>
          <v-col cols="12" sm="6" class="py-1">
            <v-dialog
              ref="dateMenu"
              v-model="dateMenu"
              :close-on-content-click="false"
              transition="scale-transition"
              min-width="290px"
              max-width="290px"
              persistent>
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="displayDate"
                  label="Date of Death"
                  prepend-icon="fa-calendar-day"
                  @click:prepend="dateMenu = true"
                  v-on="on"
                  :disabled="readonly"
                  readonly>
                </v-text-field>
              </template>
              <v-date-picker v-model="dateOfDeath" no-title scrollable
                @click:date="$refs.dateMenu.save(dateOfDeath)"
                :max="new Date().toISOString()">
                <div class="flex-grow-1"></div>
                <v-btn text color="primary" @click="dateMenu = false">Cancel</v-btn>
              </v-date-picker>
            </v-dialog>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="bookingPersonDetailsDeath['death_place']"
              label="Place of Death"
              :disabled="readonly"
              maxlength="50">
            </v-text-field>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import { getDisplayDate } from '@/global-static/dataFormattingAndValidation.ts';
import moment from 'moment';

@Component
export default class Deceased extends Vue {

  @Prop() id;

  dateMenu: boolean = false;
  readonly: boolean = true;

  forceDateUpdate: number = 0;

  mounted() {
    if (this.$store.state.Booking.bookingDetails['status'] !== 7)
      this.readonly = false;
  }

  /*** Getters and setters ***/
  
  get bookingPersonDetails() { 
    if (this.$store.state.Booking.bookingDetails.person)
      return this.$store.state.Booking.bookingDetails.person; 
    else {
      this.bookingPersonDetails = { death: {} };
      return this.bookingPersonDetails;
    }
  }
  set bookingPersonDetails(val) { this.$store.commit('modifyBookingDetails', { key: 'person', value: {} }); }
  
  get bookingPersonDetailsDeath() {

    if (this.bookingPersonDetails.death)
      return this.bookingPersonDetails.death; 
    else {
      this.bookingPersonDetailsDeath = {};
      return this.bookingPersonDetailsDeath;
    }
  }
  set bookingPersonDetailsDeath(val) { this.$store.commit('modifyPersonDetails', { key: 'death', value: {} }); }
  
  get residenceAddress() { 
    if (this.bookingPersonDetails.residence_address)
      return this.bookingPersonDetails.residence_address; 
    else {
      this.residenceAddress = {};
      return this.residenceAddress;
    }
  }
  set residenceAddress(val) { this.$store.commit('modifyPersonDetails', { key: 'residence_address', value: {} }); }

  get displayDate() {
    if (this.dateOfDeath)
      return getDisplayDate(new Date(this.dateOfDeath));
    else
      return null;
  }

  get dateOfDeath() {
    this.forceDateUpdate;

    if (this.bookingPersonDetailsDeath['impossible_date_day'] && this.bookingPersonDetailsDeath['impossible_date_month'] && this.bookingPersonDetailsDeath['impossible_date_year'])
      return this.bookingPersonDetailsDeath['impossible_date_year'] + "-" + ("0" + this.bookingPersonDetailsDeath['impossible_date_month']).slice(-2) + "-" + ("0" + this.bookingPersonDetailsDeath['impossible_date_day']).slice(-2);
    
    return null;
  }
  set dateOfDeath(date) {
    const newDate = moment(date, "YYYY-MM-DD");
    this.bookingPersonDetailsDeath['impossible_date_day'] = newDate.date();
    this.bookingPersonDetailsDeath['impossible_date_month'] = newDate.month() + 1;
    this.bookingPersonDetailsDeath['impossible_date_year'] = newDate.year();

    // forces computed property to update
    this.forceDateUpdate++;
  }
}
</script>