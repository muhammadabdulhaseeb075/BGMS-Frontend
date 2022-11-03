<template>
    <v-row>
          <v-col cols="12" sm="2">
            Deceased
          </v-col>
          <v-col cols="12" sm="10">
              <v-row>
                  <v-col cols="12" sm="4">
                      <v-row align="center">
                          <v-col cols="6" sm="4">
                              Title:
                          </v-col>
                           <v-col cols="6" sm="8">
                              <v-select
                                  v-model="deceasedTitleValue"
                                  :loading="false"
                                  :disabled="false"
                                  :items="titles"
                                  item-text="name"
                                  item-value="id"
                                  required
                                  clearable
                                  :rules="[]"
                                ></v-select>
                          </v-col>
                      </v-row>
                  </v-col>
                   <v-col cols="12" sm="4">
                       <v-row align="center">
                           <v-col cols="6" sm="4">
                             <span>
                                Forename(s):
                            </span>
                           </v-col>
                           <v-col cols="6" sm="8">
                                <v-text-field
                                  placeholder="Forname(s)"
                                  :disabled="false"
                                  maxlength="50"
                                  v-model="deceasedForenameValue"
                                >
                                </v-text-field>
                           </v-col>
                       </v-row>
                   </v-col>
                   <v-col cols="12" sm="4">
                        <v-row align="center">
                           <v-col cols="6" sm="4">
                                <span>
                           Surname:
                        </span>
                           </v-col>
                           <v-col cols="6" sm="8">
                                 <v-text-field
                                  placeholder="Surname*"
                                  :disabled="false"
                                  maxlength="50"
                                  :rules="[() => deceasedSurnameValue.length > 0 || 'This field is required']"
                                  v-model="deceasedSurnameValue">
                                 </v-text-field>
                           </v-col>
                       </v-row>
                   </v-col>
                   <v-col cols="12" sm="4">
                        <v-row align="center">
                           <v-col cols="6" sm="4">
                                 <span>
                                    Age:
                                  </span>
                           </v-col>
                           <v-col cols="6" sm="8">
                             <v-text-field
                              placeholder="Age"
                              :disabled="false"
                              maxlength="50"
                              v-model="deceasedAgeValue"
                             >
                            </v-text-field>
                           </v-col>
                       </v-row>
                   </v-col>
                   <v-col cols="12" sm="4">
                        <v-row align="center">
                           <v-col cols="6" sm="4">
                                <span>
                                    Date of Death:
                                  </span>
                           </v-col>
                           <v-col cols="6" sm="8">
                                 <v-dialog
                                      ref="deceasedDateMenu"
                                      v-model="openDeceasedDateDialog"
                                      :close-on-content-click="false"
                                      transition="scale-transition"
                                      min-width="290px"
                                      max-width="290px"
                                      persistent>
                                      <template v-slot:activator="{ on }">
                                        <v-text-field
                                          label="Date of Death*"
                                          v-model="displayDeceasedDeathDate"
                                          prepend-icon="fa-calendar-day"
                                          @click:prepend="openDeceasedDateDialog = true"
                                          v-on="on"
                                          :disabled="false"
                                          required
                                          readonly>
                                        </v-text-field>
                                      </template>
                                      <v-date-picker no-title scrollable
                                        v-model="dateOfDeathValue"
                                        @click:date="$refs.deceasedDateMenu.save(dateOfDeathValue)"
                                        :max="new Date().toISOString()">
                                        <div class="flex-grow-1"></div>
                                        <v-btn text color="primary" @click="openDeceasedDateDialog = false">Cancel</v-btn>
                                      </v-date-picker>
                                    </v-dialog>
                           </v-col>
                       </v-row>
                   </v-col>
              </v-row>
          </v-col>
          <v-col sm="12" class="pa-0">
               <v-divider style="background-color: #c3af42"/>
           </v-col>
      </v-row>
</template>

<script lang='ts'>

    import moment from "moment";

    export default {
        data: () => ({
            openDeceasedDateDialog: false
        }),
        props: {
            titles: {
                default: () => [{name: 'Mr', id: '1'}, {name: 'Mrs', id: '2'}, {name: 'Miss', id: '3'}, {name: 'Ms', id: '4'}]
            },
            deceasedTitle: {
              default: 1
            },
            deceasedForename: {
                default: ""
            },
            deceasedSurname: {
                default: ""
            },
            deceasedAge: {
                default: ""
            },
            deceasedDateMenu: {
                default: false
            },
            dateOfDeath: {
                default: ""
            }

        },
        computed: {
            displayDeceasedDeathDate: {
              get() {
                return moment(this.dateOfDeath).format("dddd D MMM YYYY")
              }
            },
            deceasedForenameValue: {
              get() {
                return this.deceasedForename;
              },
              set(deceasedForenameValueChanged) {
               this.$emit('updateDeceasedForename', deceasedForenameValueChanged)
              }
            },
             deceasedSurnameValue: {
              get() {
                return this.deceasedSurname;
              },
              set(deceasedSurnameValueChanged) {
               this.$emit('updateDeceasedSurname', deceasedSurnameValueChanged)
              }
            },
             deceasedAgeValue: {
              get() {
                return this.deceasedAge;
              },
              set(deceasedAgeValueChanged) {
               this.$emit('updateDeceasedAge', deceasedAgeValueChanged)
              }
            },
            deceasedTitleValue : {
              get() {
                return this.deceasedTitle;
              },
              set(deceasedTitleValueChanged) {
               this.$emit('updateDeceasedTitle', deceasedTitleValueChanged)
              }
            },
            dateOfDeathValue : {
                get() {
                return this.dateOfDeath;
              },
              set(dateOfDeathChanged) {
               this.$emit('updateDateOfDeath', dateOfDeathChanged)
              }
            }
      }
}

</script>

