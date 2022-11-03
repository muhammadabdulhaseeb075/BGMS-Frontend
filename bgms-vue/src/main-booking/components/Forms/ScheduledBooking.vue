<template>
    <div>
        <v-row align="center">
          <v-col cols="12" sm="2">
              Date/Time/Duration*
          </v-col>
          <v-col cols="12" sm="2">
              <v-dialog
                  ref="dateMenu"
                  v-model="dialogDateMenu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  max-width="290px"
                  min-width="290px"
                  persistent
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      ref="dateInput"
                      v-model="displayedTimeValue"
                      label="Booking Date"
                      prepend-icon="fa-calendar-day"
                      @click:prepend="dialogDateMenu = true"
                      v-on="on"
                      readonly
                      required
                      :disabled="false"
                    ></v-text-field>
                  </template>
                  <v-date-picker no-title scrollable
                    v-model="bookingDateValue"
                    @click:date="$refs.dateMenu.save(bookingDateValue)"
                    :min="new Date().toISOString()">
                    <div class="flex-grow-1"></div>
                    <v-btn text color="primary" @click="dialogDateMenu = false">Cancel</v-btn>
                  </v-date-picker>
                </v-dialog>
          </v-col>
          <v-col cols="12" sm="2" class="py-1">
            <TimePicker
                  Inputref="timeInput"
                  v-bind:value="bookingTimeValue"
                  v-bind:time-input-required="true"
                  v-on:input="bookingTimeValue = $event"
                  timeInputLabel="Booking Time"
            />
          </v-col>
          <v-col cols="12" sm="2" class="py-1">
                <v-text-field
                  v-model="bookingDurationValue"
                  @blur="validate"
                  label="Duration"
                  suffix="minutes"
                  type="number"
                  step="5"
                  :rules="[]"
                  required
                ></v-text-field>
          </v-col>
           <v-col sm="12" class="pa-0">
               <v-divider style="background-color: #c3af42"/>
           </v-col>
      </v-row>
    </div>
</template>

<script>
    import TimePicker from "../TimePicker";
    import moment from "moment";

    export default {
        components: {TimePicker},
        props: {
            bookingTime: {
                 default: "13:00"
            },
            bookingDate: {
                 default: moment.now()
            },
            bookingDuration: {
                 default: 30
            }
        },
        data: () => ({
            dialogDisplayed: false,
        }),
        computed: {
            bookingDateValue: {
                get() {
                    return this.bookingDate;
                },
                set(bookingDateChanged){
                    this.$emit('updateBookingDate', bookingDateChanged)
                }
            },
            displayedTimeValue:
            {
                get() {
                    return this.bookingDate ? moment(this.bookingDate).format("dddd D MMM YYYY") : ''
                }
            },
            bookingTimeValue: {
                get() {
                    return this.bookingTime;
                },
                set(bookingTimeChanged){
                    this.$emit('updateBookingTime', bookingTimeChanged)
                }
            },
            bookingDurationValue: {
                  get() {
                    return this.bookingDuration;
                  },
                  set(bookingDurationChanged) {
                     this.$emit('updateBookingDuration', bookingDurationChanged)
                  }
            },
            dialogDateMenu:{
                get() {
                    return this.dialogDisplayed;
                },
                set(open){
                    this.dialogDisplayed = open;
                }
            }
        },
        methods: {
          validate(){
            let value = this.bookingDurationValue;
            if (value % 5 != 0){
              this.bookingDurationValue = (value % 5) >= 2.5 ? parseInt(value / 5) * 5 + 5 : parseInt(value / 5) * 5;
            }
             
          }
        }

    }
</script>