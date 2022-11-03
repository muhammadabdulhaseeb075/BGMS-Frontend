<template>
  <div>
      <v-form ref="form" v-model="valid">
        <div class="fixed-menu nav">
          <v-row align="center" align-content="space-between" class="pl-4 ma-0">
              <v-col cols="12" sm="3" class="pa-0">
                  <v-row align="center">
                      <v-col cols="12" sm="3" class="pa-2">
                           <v-btn><v-icon>fas fa-edit</v-icon></v-btn>
                      </v-col>
                      <v-col cols="12" sm="3" class="pa-2">
                           <v-btn @click="createBookingEvent" :disabled="!valid"><v-icon>fas fa-save</v-icon></v-btn>
                      </v-col>
                      <v-col cols="12" sm="3" class="pa-2">
                          <v-btn><v-icon>fas fa-trash</v-icon></v-btn>
                      </v-col>
                  </v-row>
              </v-col>
              <v-col cols="12" sm="3">
                    <v-text-field
                        placeholder="Burial Ground 2"
                        v-model="site.name"
                        :disabled="true"
                        maxlength="50">
                    </v-text-field>
              </v-col>
              <v-col cols="12" sm="2" class="pa-0">
                  <v-row align="center">
                      <v-col cols="12" sm="4">
                        Reference
                      </v-col>
                      <v-col cols="12" sm="8">
                          <v-text-field
                            v-model="bookingForm.reference"
                            :disabled="true"
                            maxlength="50">
                    </v-text-field>
                      </v-col>
                  </v-row>
              </v-col>
              <v-col cols="12" sm="2">
                  <v-btn class="btn-bgms">
                      reset
                  </v-btn>
              </v-col>
              <v-col sm="12" class="pa-0">
                    <v-divider  style="background-color: #c3af42"/>
              </v-col>
          </v-row>
      </div>

       <div id="booking" class="pl-8 pr-8">
       <div class="mt-64">
      

      <!-- TYPE -->
      <burial-type v-bind:value="bookingForm.burialType" v-on:input="changeBurialType($event)"/>

      <!-- DATE TIME DURATION -->
      <scheduled-booking
           v-bind:bookingTime="bookingForm.bookingTime"
           v-bind:booking-date="bookingForm.bookingDate"
           v-bind:booking-duration="bookingForm.bookingDuration"
           v-on:updateBookingDate="bookingForm.bookingDate = $event"
           v-on:updateBookingTime="bookingForm.bookingTime = $event"
           v-on:updateBookingDuration="bookingForm.bookingDuration = $event"
       />

      <!--  DECEASED -->
       <deceased
           v-bind:deceased-title="bookingForm.deceasedTitle"
           v-bind:deceased-forename="bookingForm.deceasedForename"
           v-bind:deceased-surname="bookingForm.deceasedSurname"
           v-bind:deceased-age="bookingForm.deceasedAge"
           v-bind:date-of-death="bookingForm.dateOfDeath"
           v-on:updateDeceasedForename="bookingForm.deceasedForename = $event"
           v-on:updateDeceasedSurname="bookingForm.deceasedSurname = $event"
           v-on:updateDeceasedAge="bookingForm.deceasedAge = $event"
           v-on:updateDeceasedTitle="bookingForm.deceasedTitle = $event"
           v-on:updateDateOfDeath="bookingForm.dateOfDeath = $event"
       />

      <!--  Address -->
      <v-row>
          <v-col cols="12" sm="2">
              Address
          </v-col>
          <v-col cols="12" sm="4">
              <v-row align="center">
                  <v-col cols="6" sm="4">
                      <span>
                          Address:
                      </span>
                  </v-col>
                  <v-col cols="6" sm="8">
                      <v-text-field
                         v-model="bookingForm.address"
                         placeholder="Postcode"
                         :disabled="false"
                         maxlength="50">
                      </v-text-field>
                  </v-col>
              </v-row>
          </v-col>
          <v-col sm="12" class="pa-0">
               <v-divider style="background-color: #c3af42"/>
           </v-col>
      </v-row>

      <!--  Place of Death -->
       <v-row>
          <v-col cols="12" sm="2">
              Place of Death
          </v-col>
          <v-col cols="12" sm="4">
              <v-row align="center">
                  <v-col cols="12" sm="4"></v-col>
                   <v-col cols="12" sm="8">
                      <v-text-field
                         placeholder="As Address"
                         :disabled="false"
                         maxlength="50"
                         v-model="bookingForm.placeOfDeath">
                      </v-text-field>
                  </v-col>
              </v-row>
              <v-row align="center">
                  <v-col cols="12" sm="4">
                      <span>
                          Other:
                      </span>
                  </v-col>
                  <v-col cols="12" sm="8">
                      <v-text-field
                         placeholder="Please Specify"
                         :disabled="false"
                         maxlength="50"
                         v-model="bookingForm.other"
                      >
                      </v-text-field>
                  </v-col>
              </v-row>
          </v-col>
          <v-col sm="12" class="pa-0">
               <v-divider style="background-color: #c3af42"/>
          </v-col>
      </v-row>

      <!-- Funeral Director -->
      <v-row align="center">
          <v-col cols="12" sm="2">
            <span>
                Funeral Director
            </span>
          </v-col>
          <v-col cols="12" sm="4">
            <v-row>
                <v-col cols="6" sm="10">
                       <v-select
                          :loading="false"
                          :disabled="false"
                          v-model="bookingForm.funeralDirectorSelected"
                          :items="bookingForm.funeralDirectorsList"
                          item-text="name"
                          item-value="id"
                          placeholder="start typing to access lookup"
                          required
                          clearable
                          :rules="[]"
                        ></v-select>
                </v-col>
                <v-col cols="6" sm="2">
                     <v-btn>
                         <v-icon>
                            fas fa-edit
                        </v-icon>
                      </v-btn>
                </v-col>
            </v-row>
          </v-col>
          <v-col sm="12" class="pa-0">
               <v-divider style="background-color: #c3af42"/>
          </v-col>
      </v-row>


       <!-- Grave -->
      <v-row align="center">
        <v-col cols="12" sm="2">
            <span>
                Grave
            </span>
        </v-col>
        <v-row align="center">
            <v-col cols="12" sm="5">
                <v-row align="center">
                    <v-col sm="4">
                        <v-text-field
                            maxlength="50"
                            v-model="bookingForm.graveNew"
                            placeholder="New"
                        >
                        </v-text-field>
                    </v-col>
                    <v-col sm="8">
                        <a class="link-to" :href="newLinkToMap">
                            open map
                        </a>
                    </v-col>
                </v-row>
            </v-col>
            <v-col cols="12" sm="5">
                <v-row align="center">
                    <v-col sm="4">
                        <v-text-field
                            maxlength="50"
                            v-model="bookingForm.graveExist"
                            placeholder="Existing"
                        >
                        </v-text-field>
                    </v-col>
                    <v-col sm="8">
                        <a class="link-to" :href="existingLinkToMap">
                            search records
                        </a>
                    </v-col>
                </v-row>
            </v-col>
        </v-row>
          <v-col sm="12" class="pa-0">
             <v-divider style="background-color: #c3af42"/>
         </v-col>
     </v-row>


       <!-- Burial Details-->
      <v-row align="center">
                <v-col cols="12" sm="2">
                    <span>Burial Details</span>
                </v-col>
                <v-col cols="12" sm="10">
                    <v-row>
                        <v-col cols="12" sm="1">
                            <p>Coffin Size:</p>
                            <v-select
                              :items="size"
                              item-text="name"
                              item-value="id"
                              v-model="bookingForm.burialCoffinSize" 
                            >
                              
                            </v-select>
                        </v-col>
                        <v-col cols="12" sm="2">
                            <v-row align="center">
                                <v-col cols="12" sm="4">
                                    Length:
                                </v-col>
                                <v-col cols="12" sm="8">
                                      <v-text-field
                                         :disabled="false"
                                         maxlength="50"
                                         v-model="bookingForm.burialLength"
                                      >
                                      </v-text-field>
                                </v-col>
                            </v-row>
                        </v-col>
                         <v-col cols="12" sm="3">
                            <v-row align="center">
                                <v-col cols="12" sm="4">
                                    Width:
                                </v-col>
                                <v-col cols="12" sm="8">
                                    <v-text-field
                                         :disabled="false"
                                         maxlength="50"
                                         v-model="bookingForm.burialWidth"
                                        >
                                      </v-text-field>
                                </v-col>
                            </v-row>
                        </v-col>
                         <v-col cols="12" sm="3">
                            <v-row align="center">
                                <v-col cols="12" sm="4">
                                    Height:
                                </v-col>
                                <v-col cols="12" sm="8">
                                    <v-text-field
                                         :disabled="false"
                                         maxlength="50"
                                         v-model="bookingForm.burialHeight"
                                        >
                                    </v-text-field>
                                </v-col>
                            </v-row>
                        </v-col>
                         <v-col cols="12" sm="3">
                            <v-row align="center">
                                <v-col cols="12" sm="4">
                                    Depth:
                                </v-col>
                                <v-col cols="12" sm="8">
                                        <v-text-field
                                         :disabled="false"
                                         maxlength="50"
                                         v-model="bookingForm.burialDepth"
                                        >
                                      </v-text-field>
                                </v-col>
                            </v-row>
                        </v-col>
                    </v-row>
                </v-col>
          <v-col sm="12" class="pa-0">
               <v-divider style="background-color: #c3af42"/>
           </v-col>
            </v-row>

        <!-- Meeting Location -->
        <v-row>
            <v-col cols="12" sm="2">
                <span>Meeting Location</span>
            </v-col>
              <v-col cols="12" sm="10">
                  <v-row>
                      <v-col sm="10">
                          <v-text-field
                           placeholder="Enter details"
                           :disabled="false"
                           maxlength="50"
                           v-model="bookingForm.meetingLocation"
                          >
                          </v-text-field>
                      </v-col>
                      <v-col sm="2">
                          <v-btn>
                             <v-icon>
                                fas fa-edit
                            </v-icon>
                          </v-btn>
                      </v-col>
                  </v-row>
              </v-col>
            <v-col sm="12" class="pa-0">
               <v-divider style="background-color: #c3af42"/>
           </v-col>
        </v-row>

      <!-- Next of Kin-->
      <v-row align="center">
           <v-col cols="12" sm="2">
            Next of Kin
           </v-col>
           <v-col cols="12" sm="3">
                      <v-row align="center">
                          <v-col cols="6" sm="4">
                              Title:
                          </v-col>
                           <v-col cols="6" sm="8">
                              <v-select
                                  :loading="false"
                                  :disabled="false"
                                  :items="titles"
                                  item-text="name"
                                  item-value="id"
                                  required
                                  clearable
                                  :rules="[]"
                                  v-model="bookingForm.nextOfKinTitle"
                                ></v-select>
                          </v-col>
                      </v-row>
                  </v-col>
                   <v-col cols="12" sm="3">
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
                                  v-model="bookingForm.nextOfKinForename">
                                </v-text-field>
                           </v-col>
                       </v-row>
                   </v-col>
                   <v-col cols="12" sm="3">
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
                                  :rules="[() => bookingForm.nextOfKinSurname.length > 0 || 'This field is required']"
                                 v-model="bookingForm.nextOfKinSurname">
                                </v-text-field>
                           </v-col>
                       </v-row>
                   </v-col>
          <v-col cols="12" sm="1">
              <v-btn @click="openNKModal">
                  <v-icon>
                      fas fa-edit
                  </v-icon>
              </v-btn>
          </v-col>
           <v-col sm="12" class="pa-0">
               <v-divider style="background-color: #c3af42"/>
           </v-col>
      </v-row>


      <!-- Authority for interment-->
      <v-row align="center">
            <v-col cols="12" sm="2">
                Authority for interment
            </v-col>
           <v-col cols="12" sm="3">
                      <v-row align="center">
                          <v-col cols="6" sm="4">
                              Title:
                          </v-col>
                           <v-col cols="6" sm="8">
                              <v-select
                                  :loading="false"
                                  :disabled="false"
                                  :items="titles"
                                  item-text="name"
                                  item-value="id"
                                  required
                                  clearable
                                  :rules="[]"
                                  v-model="bookingForm.authorityForIntermentTitle"
                                ></v-select>
                          </v-col>
                      </v-row>
                  </v-col>
                   <v-col cols="12" sm="3">
                       <v-row align="center">
                           <v-col cols="6" sm="4">
                             <span>
                                Forename(s):
                            </span>
                           </v-col>
                           <v-col cols="6" sm="8">
                                <v-text-field
                                  placeholder="Forename(s)"
                                  :disabled="false"
                                  maxlength="50"
                                  v-model="bookingForm.authorityForIntermentForename">
                                </v-text-field>
                           </v-col>
                       </v-row>
                   </v-col>
                   <v-col cols="12" sm="3">
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
                                  :rules="[() => bookingForm.authorityForIntermentSurname.length > 0 || 'This field is required']"
                                  v-model="bookingForm.authorityForIntermentSurname"
                                 >
                                </v-text-field>
                           </v-col>
                       </v-row>
                   </v-col>
          <v-col cols="12" sm="1">
              <v-btn>
                  <v-icon>
                      fas fa-edit
                  </v-icon>
              </v-btn>
          </v-col>
          <v-col sm="12" class="pa-0">
               <v-divider style="background-color: #c3af42"/>
          </v-col>
      </v-row>


      <!-- Comments -->

      <v-row align="center">
            <v-col cols="12" sm="2">
                <span>Comments</span>
            </v-col>
            <v-col cols="12" sm="10">
                <v-text-field
                        placeholder="Additional details"
                        :disabled="false"
                        maxlength="50"
                        v-model="bookingForm.comments"
                >
                </v-text-field>
            </v-col>
            <v-col sm="12" class="pa-0">
               <v-divider style="background-color: #c3af42"/>
           </v-col>
        </v-row>

      <!-- Booking Status -->


      <v-row align="center">
            <v-col cols="12" sm="2">
                <span>Booking Status</span>
            </v-col>
              <v-col cols="12" sm="10">
                  <v-row align="center">
                      <v-col sm="4">
                          <v-select
                                  :loading="false"
                                  :disabled="false"
                                  :items="[ {name: 'Reservation', id: '1'}]"
                                  item-text="name"
                                  item-value="id"
                                  required
                                  clearable
                                  :rules="[]"
                                  v-model="bookingForm.bookingStatus"
                          ></v-select>
                      </v-col>
                      <v-col sm="2">
                          <v-btn>
                             <v-icon>
                                fas fa-edit
                            </v-icon>
                          </v-btn>
                      </v-col>
                  </v-row>
              </v-col>
        </v-row>
          <v-col sm="12" class="pa-0">
               <v-divider style="background-color: #c3af42"/>
          </v-col>
      </div>
            <v-content>
              <router-view></router-view>
            </v-content>
        </div>
      </v-form>

    <BaseModal
      title="Add New Next of Kin"
      :open="displayNextOfKinModal"
      v-on:close="() => displayNextOfKinModal = false"
    >
      <v-form ref="next-of-kin-form" v-model="newNextOfKinFormValid">
        <div class="next-of-kin-form">
          <legend>Enter Next of Kin Address:</legend>
          <div class="field">
            <label for="add-details">Relationship to deceased</label>
            <v-text-field
              class="input"
              placeholder=""
              :disabled="false"
              maxlength="50"
              name="add-details"
              height="20"
              v-model="nextOfKinForm.addDetails"
            >
            </v-text-field>
          </div>
          <div class="field">
            <label for="title">Title:</label>
            <v-select
              :loading="false"
              :disabled="false"
              :items="titles"
              item-text="name"
              item-value="id"
              required
              clearable
              :rules="[]"
              v-model="nextOfKinForm.title"
            ></v-select>
          </div>
          <div class="field">
            <label for="first-name">First Name(s):</label>
            <v-text-field
              class="input"
              placeholder=""
              :disabled="false"
              maxlength="50"
              name="first-name"
              v-model="nextOfKinForm.forename"
            >
            </v-text-field>
          </div>
          <div class="field">
            <label for="last-name">Surname:</label>
            <v-text-field
              class="input"
              placeholder=""
              :disabled="false"
              maxlength="50"
              name="last-name"
              :rules="[() => nextOfKinForm.surname.length > 0 || 'This field is required']"
              v-model="nextOfKinForm.surname"
            >
            </v-text-field>
          </div>
          <div class="field">
            <label for="email">Email</label>
            <v-text-field
              class="input"
              placeholder=""
              :disabled="false"
              maxlength="50"
              name="email"
              v-model="nextOfKinForm.email"
            >
            </v-text-field>
          </div>
          <div class="field">
            <label for="phone-1">Phone 1:</label>
            <v-text-field
              class="input"
              placeholder=""
              :disabled="false"
              maxlength="50"
              name="phone-1"
              v-model="nextOfKinForm.phone1"
            >
            </v-text-field>
          </div>
          <div class="field">
            <label for="phone-2">Phone 2:</label>
            <v-text-field
              class="input"
              placeholder=""
              :disabled="false"
              maxlength="50"
              name="phone-2"
              v-model="nextOfKinForm.phone2"
            >
            </v-text-field>
          </div>
          <div class="field">
            <label for="postcode">Postcode:</label>
            <v-text-field
              class="input"
              placeholder=""
              :disabled="false"
              maxlength="50"
              name="postcode"
              v-model="nextOfKinForm.postcode"
            >
            </v-text-field>
          </div>
          <div class="field">
            <label for="address-1">Address line 1:</label>
            <v-text-field
              class="input"
              placeholder=""
              :disabled="false"
              maxlength="50"
              name="address-1"
            >
            </v-text-field>
          </div>
          <div class="field">
            <label for="address-2">Address line 1:</label>
            <v-text-field
              class="input"
              placeholder=""
              :disabled="false"
              maxlength="50"
              name="address-2"
            >
            </v-text-field>
          </div>
          <div class="field">
            <label for="city">Town/City:</label>
            <v-text-field
              class="input"
              placeholder=""
              :disabled="false"
              maxlength="50"
              name="city"
            >
            </v-text-field>
          </div>
          <div class="field">
            <label for="country">Country:</label>
            <v-text-field
              class="input"
              placeholder=""
              :disabled="false"
              maxlength="50"
              name="country"
            >
            </v-text-field>
          </div>
          <div class="field j-left">
            <button
              class="add-next-of-kin"
              :disabled="!newNextOfKinFormValid"
              @click="createNextOfKin"
            >
              Add
            </button>
          </div>
        </div>
      </v-form>
    </BaseModal>
  </div>



</template>

<script lang='ts'>
import Vue from 'vue';
import Component, {mixins} from 'vue-class-component';
import BurialType from "@/main-booking/components/Forms/BurialType.vue";
import ScheduledBooking from "@/main-booking/components/Forms/ScheduledBooking.vue";
import Deceased from "@/main-booking/components/Forms/Deceased.vue";
import BaseModal from "@/main-booking/components/Modal/ModalBase.vue";
import moment from "moment";
import axios from "axios";

@Component({
  components: {
    Deceased,
    BurialType,
    ScheduledBooking,
    BaseModal,
  }
})
export default class BookingMenu extends Vue  {
  bookingForm = {
    burialType: 0,
    bookingDate: "",
    bookingTime: "13:00",
    bookingDuration: 30,
    deceasedTitle: 1,
    deceasedForename: "",
    deceasedSurname: "",
    deceasedAge: "",
    dateOfDeath: "",
    address: "",
    placeOfDeath: "",
    other: "",
    burialLength: "",
    burialWidth: "",
    burialDepth: "",
    burialHeight: "",
    meetingLocation: "",
    nextOfKinTitle: "",
    nextOfKinForename: "",
    nextOfKinSurname: "",
    graveNew: "",
    graveExist: "",
    authorityForIntermentTitle: "",
    authorityForIntermentForename: "",
    authorityForIntermentSurname: "",
    bookingStatus: "",
    comments: "",
    burialCoffinSize:"",
    funeralDirectorSelected: null,
    titles: [{name: 'Mr', id: '1'}, {name: 'Mrs', id: '2'}, {name: 'Miss', id: '3'}, {name: 'Ms', id: '4'}],
    adminURL: '',
    siteSelected: '',
    reference:0

  }

  nextOfKinForm = {
    addDetails: "",
    title: "",
    forename: "",
    surname: "",
    email: "",
    phone1: "",
    phone2: ""
  }

  displayNextOfKinModal = false;
  newNextOfKinFormValid = false;
  valid = false
  burialType = 0;
  bookingDate = ""
  bookingTime = "13:00"
  bookingDuration = 30
  deceasedTitle = 1
  deceasedForename = ""
  deceasedSurname = ""
  deceasedAge = ""
  dateOfDeath = ""
  address = ""
  placeOfDeath = ""
  other = ""
  burialLength = ""
  burialWidth = ""
  burialDepth = ""
  burialHeight = ""
  meetingLocation = ""
  nextOfKinTitle = ""
  nextOfKinForename = ""
  nextOfKinSurname = ""
  graveNew = ""
  graveExist = ""
  authorityForIntermentTitle = ""
  authorityForIntermentForename = ""
  authorityForIntermentSurname = ""
  bookingStatus = ""
  comments = ""
  funeralDirectorSelected = null
  titles = [{name: 'Mr', id: '1'}, {name: 'Mrs', id: '2'}, {name: 'Miss', id: '3'}, {name: 'Ms', id: '4'}]
  size= [{name:'mtrs' , id:'mtrs'},{name:'ft/in' , id:'ft/in'}]
  STANDARD_NOTIFICATION_PROPERTIES = {
      addClass: "stack-bottomright",
      stack: {
          "dir1": "up",
          "dir2": "left",
          "firstpos1": 25,
          "firstpos2": 25
      },
      icons: 'fontawesome5',
      width: '300px'
    }

  get site() {
    let currentSiteId = this.$store.state.Booking.selectedSiteId
    this.bookingForm.siteSelected = currentSiteId

    return this.$store.getters.getSiteFromId(parseInt(currentSiteId)) || {}
  }



  get funeralDirectorsList() {
    return this.$store.state.Booking.funeralDirectors
  }


  get isLinkToMapAvailable()
  {
      return this.site && this.site.domain_url
  }

  get linkToMap() {
    const pathToMap = 'mapmanagement/#/'
    let mapURL = `#${this.$route.fullPath}`

    if(this.isLinkToMapAvailable) {
        this.bookingForm.adminURL = window.location.origin;

        const subdomain = this.site.domain_url
        const path = `${pathToMap}?${this.encodingForm()}`

        mapURL = `${subdomain}/${path}`
    }

    return mapURL
  }

  get existingLinkToMap() {
    let mapURL = this.linkToMap

    if(this.isLinkToMapAvailable) {
        mapURL += `&openSearch=true`
    }

    return mapURL
  }

  get newLinkToMap() {
    let mapURL = this.linkToMap

    if(this.isLinkToMapAvailable) {
        mapURL += `&filterAvailablePlots=true`
    }

    return mapURL
  }

  mounted() {
    this.graveExist = this.$router.currentRoute.query['gravenum'] as string
    const bookingQuery = this.$router.currentRoute.query['bookingForm'] as string

    if(bookingQuery) {
      const parsedForm = JSON.parse(decodeURIComponent(bookingQuery))
      const fields = Object.keys(parsedForm)

      fields.forEach((field) => {
        this.bookingForm[field] = parsedForm[field]
      })

      if(this.bookingForm.siteSelected) {
        this.$store.commit('selectSiteId', this.bookingForm.siteSelected)
        this.$store.dispatch('getFuneralDirectors', this.bookingForm.siteSelected)
      }
    }
  }

  openNKModal() {
    this.displayNextOfKinModal = true;
  }

  createNextOfKin(event) {
    event.preventDefault();

    if(this.site) {
      axios({
        method: 'post',
        url:  this.site.domain_url + "/api/person/",
        data: this.nextOfKinForm
      })
      .then(({ data }) => {
        this.bookingForm.nextOfKinTitle = data.title;
        this.bookingForm.nextOfKinForename = data.first_names;
        this.bookingForm.nextOfKinSurname = data.last_name;
        this.displayNextOfKinModal = false;
      })
      .catch(error => {
        console.error("Event could not be saved", error);
        this.displayNextOfKinModal = false;
      });
    }
  }
 
  encodingForm() {
      const encodeForm = encodeURIComponent(JSON.stringify(this.bookingForm))
      const encodedFormQuery = `bookingForm=${encodeForm}`

      return encodedFormQuery;
  }

  changeBurialType(burialType) {
    this.burialType = burialType;
  }

  createBookingEvent() {
      const deathDate = new Date(this.dateOfDeath)
      const deceased_day = deathDate.getDay()
      const deceased_month = deathDate.getMonth()
      const deceased_year = deathDate.getFullYear()
      const event = {
          "calendar_event" : {
              "event_type_id": 1,
              "bookingDate": this.bookingForm.bookingDate,
              "bookingTime": this.bookingForm.bookingTime,
              "duration": this.bookingForm.bookingDuration,
              "start" : moment(this.bookingForm.bookingDate + "T" + this.bookingForm.bookingTime).format('YYYY-MM-DDTHH:mm'),
              "end": moment(this.bookingForm.bookingDate + "T" + this.bookingForm.bookingTime).add(this.bookingForm.bookingDuration, 'm').format('YYYY-MM-DDTHH:mm'),
          },
          "person" : {
              "death" : {
                  "impossible_date_day": deceased_day,
                  "impossible_date_month": deceased_month,
                  "impossible_date_year": deceased_year
              },
              "residence_address": {
                  "postcode": this.bookingForm.address,
              },
              "title": this.bookingForm.deceasedTitle,
              "first_names": this.bookingForm.deceasedForename,
              "last_name": this.bookingForm.deceasedSurname
          },
          "authority_for_interment": {
            "title": this.bookingForm.authorityForIntermentTitle,
            "first_names": this.bookingForm.authorityForIntermentForename,
            "last_name": this.bookingForm.authorityForIntermentSurname
         },
         "funeral_director_id": this.bookingForm.funeralDirectorSelected,
          "burial": {
            "coffin_units": this.bookingForm.burialCoffinSize,
            "coffin_width": this.bookingForm.burialWidth.length > 0 ? this.bookingForm.burialWidth: null,
            "coffin_height": this.bookingForm.burialHeight.length > 0 ? this.bookingForm.burialHeight: null,
            "cremated": this.bookingForm.burialType === 0,
            "burial_remarks": this.bookingForm.comments,
            "impossible_date_year": deceased_year,
            "impossible_date_month": deceased_month,
            "impossible_date_day": deceased_day
         },
          "next_of_kin_person": {
            "first_names": this.bookingForm.nextOfKinForename,
            "last_name": this.bookingForm.nextOfKinSurname,
            "title": this.bookingForm.nextOfKinTitle,
            "current_addresses": [],
            "postcode": "",
            "city": "",
         },
          "grave": {
            "existing": this.bookingForm.graveExist,
            "new_grave": this.bookingForm.graveNew,
          },
      }
    let _this = this
    axios({
      method: 'post',
      url:  this.site.domain_url + "/cemeteryadmin/funeralEvent/",
      data: event
    })
    .then(response => {
      let reference = response.data.calendar_event.reference
      _this.bookingForm.reference = reference
      console.log("Event saved successfully")
    })
    .catch(error => {
         console.log("Event could not be saved")
    })

  }
}
</script>


<style>
    .fixed-menu {
        top: 0;
        padding-top: 50px;
        width: 100%;
        position: fixed;
        background-color: green;
        z-index: 1000;
    }

    .mt-64 {
        margin-top: 128px;
        width: 100%;
    }

    .link-to, .link-to:hover {
        text-decoration: underline;
    }

    .next-of-kin-form {
        padding: 12px 32px;
    }

    .next-of-kin-form legend {
        text-align: left;
        font-size: 16px;
        margin: 0;
    }

    .next-of-kin-form .field {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .next-of-kin-form .field.j-left {
      justify-content: flex-start;
    }

    .next-of-kin-form .add-next-of-kin {
      padding: 8px 20px;
      border-radius: 5px;
      color: white;
      background-color: orangered;
      opacity: 0.8;
    }

    .next-of-kin-form .add-next-of-kin[disabled] {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .next-of-kin-form .field label {
        width: 30%;
    }

    .next-of-kin-form .v-input__control > .v-input__slot > .v-text-field__slot {
      background: antiquewhite;
    }

    .next-of-kin-form .field .input {
        width: 20%;
        margin-top: 0px;
        padding-top: 0px;
    }

    .next-of-kin-form .field .input .v-text-field input,
    .next-of-kin-form .field .input .v-select__slot {
        background-color: rgba(195,143,66, 0.5);
    }

</style>
