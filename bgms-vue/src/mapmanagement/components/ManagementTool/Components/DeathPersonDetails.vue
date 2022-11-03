<template>
  <div id="deathPersonDetailsElement" v-if="componentData">
    <ScrollButtons :heightChangedFlag="heightChangedFlag" v-show="$route.name!==graveManagementChildRoutesEnum.convertReservation && $route.name!==graveManagementChildRoutesEnum.deleteReservation">

      <ValidationBox :errors="componentData.errors"/>

      <form class="form-horizontal form-box-inside management-tool-form no-margin" @submit.prevent="onSubmit">

        <FormButtons v-if="siteAdminOrSiteWarden && (!createMode || reservationFlag)" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="true" @toggle-edit="toggleEdit($event)"/>

        <section>

          <StandardInputRow :label="'Date of Burial'" v-if="componentData.most_recent_burial_date" v-show="!editFlag" :value="showYearIfImpossibleMonthIsNotDefined(componentData)" :inputType="'text'" :readonlyOption="true" :editFlag="false"/>
          <StandardInputRow v-if="reservationFlag || componentData.reservation_reference" :label="'Reservation Reference'" :placeholder="'Reservation Reference'" v-model="componentData.reservation_reference" :inputType="'text'" :attributes="{ maxlength:35 }" :editFlag="reservationFlag && editFlag" :readonlyOption="true"/>

          <!-- In display mode, show name fields together -->
          <div class="row field-row" v-if="!editFlag && (componentData.title || componentData.first_names || componentData.last_name)">
            <label :class="labelColumnClasses" for="full-name">Name:</label>
            <div id="full-name" :class="fieldColumnClasses">
              <div class="form-control field-text">{{ getJoinedText([componentData.title, componentData.first_names, componentData.last_name], ' ') }}</div>
            </div>
          </div>
          <div v-else-if="editFlag">

            <StandardInputRow :label="'Title'" v-model="componentData.title" :inputType="'text'" :attributes="{ maxlength:30 }"/>
            <StandardInputRow :label="'First Names'" v-model="componentData.first_names" :inputType="'text'" :attributes="{ maxlength:200 }"/>
            <StandardInputRow :label="'Last Name'" v-model="componentData.last_name" :inputType="'text'" :attributes="{ maxlength:35,  class:'uppercase-text' }"/>

          </div>
          
          <StandardInputRow :label="'Birth Name'" v-model="componentData.birth_name" :inputType="'text'" :attributes="{ maxlength:200 }" :readonlyOption="true" :editFlag="editFlag"/>
          <StandardInputRow :label="'Nickname'" v-model="componentData.other_names" :inputType="'text'" :attributes="{ maxlength:100 }" :readonlyOption="true" :editFlag="editFlag"/>
          <StandardInputRow :label="'Gender'" v-model="componentData.gender" :inputType="'text'" :attributes="{ maxlength:10 }" :readonlyOption="true" :editFlag="editFlag"/>

          <!--profession_field-->
          <StandardInputRow
            :key="componentData.profession_field.name" :label="componentData.profession_field.name"
            v-model="componentData[componentData.profession_field.content]"
            :inputType="componentData.profession_field.type"
            :attributes="{ maxlength:10 }" :readonlyOption="true" :editFlag="editFlag"
            :options_select="select_fields(componentData.profession_field.options)"
            :placeholder="componentData.profession_field.name"/>
          <!--religion_field-->
          <StandardInputRow
            :key="componentData.religion_field.name" :label="componentData.religion_field.name"
            v-model="componentData['death'][componentData.religion_field.content]" :inputType="componentData.religion_field.type"
            :attributes="{ maxlength:10 }" :readonlyOption="true" :editFlag="editFlag"
            :options_select="select_fields(componentData.religion_field.options)"
            :placeholder="componentData.religion_field.name"/>
          <!--parish_field-->
          <StandardInputRow
            :key="componentData.parish_field.name" :label="componentData.parish_field.name"
            v-model="componentData['death'][componentData.parish_field.content]" :inputType="componentData.parish_field.type"
            :attributes="{ maxlength:10 }" :readonlyOption="true" :editFlag="editFlag"
            :options_select="select_fields(componentData.parish_field.options)"
            :placeholder="componentData.parish_field.name"/>

          <div class="row field-row form-buttons" v-if="editFlag || componentData.next_of_kin">
            <label :class="labelColumnClasses" for="next-of-kin">Next of Kin:</label>
            <div v-if="componentData.next_of_kin && componentData.next_of_kin_display_name" id="next-of-kin" class="col-xs-7" style="padding-left:12px">
              {{ componentData.next_of_kin_display_name }}
            </div>
            <a v-if="!editFlag && componentData.next_of_kin.id" href="" @click="goToPersonManagement(componentData.next_of_kin.id)" title="Go to Person Management" class="col-xs-1"><i class="fa fa-arrow-circle-right"/></a>
            <a v-if="editFlag && componentData.next_of_kin" href="" title="Remove Next of Kin" @click="componentData.next_of_kin=null;componentData.next_of_kin_relationship=null;" class="form-icon-small col-xs-1"><i class="fa fa-times"/></a>
            <a v-else-if="editFlag" href="" class="form-icon-small col-xs-1" title="Add Next of Kin" @click="$modal.show('add-next-of-kin')">
              <i class="fa fa-plus"></i>
            </a>
          </div>

          <StandardInputRow :label="'Next of Kin Relationship'" v-model="componentData.next_of_kin_relationship" :inputType="'text'" :attributes="{ maxlength:50 }" :readonlyOption="true" :editFlag="editFlag"/>

        </section>

        <h2 v-if="editFlag">Age</h2>
        <section>
          <DateInputRow :label="'Date of Birth'" :editFlag="editFlag" :day="componentData.impossible_date_day" @day-input="componentData.impossible_date_day=$event" :month="componentData.impossible_date_month" @month-input="componentData.impossible_date_month=$event" :year="componentData.impossible_date_year" @year-input="componentData.impossible_date_year=$event"/>

          <div class="row field-row" v-if="!reservationFlag && (editFlag || componentData.death.impossible_date_day || componentData.death.impossible_date_month || componentData.death.impossible_date_year)">
            <label :class="labelColumnClasses" for="death-date">Date of Death:</label>
            <div v-if="!editFlag" id="death-date" :class="fieldColumnClasses">
              <input readonly type="text" class="form-control" :value="individualDateFieldsToSingleDate(componentData.death.impossible_date_day, componentData.death.impossible_date_month, componentData.death.impossible_date_year)">
            </div>
            <div v-if="editFlag" id="death-date" :class="fieldColumnClasses">
              <div class="multi-input">
                <input class="form-control multi-input_input multi-input_input--day no-spinner" type="number" step="1" min="0" max="31" placeholder="dd" v-model.number="componentData.death.impossible_date_day" onKeyPress="if(this.value.toString().length==2) return false;">
                <span class="multi-input_divider">/</span>
                <input class="form-control multi-input_input multi-input_input--month no-spinner" type="number" step="1" min="0" max="12" placeholder="mm" v-model.number="componentData.death.impossible_date_month" onKeyPress="if(this.value.toString().length==2) return false;">
                <span class="multi-input_divider">/</span>
                <input class="form-control multi-input_input multi-input_input--year no-spinner" type="number" step="1" min="0" :max="(new Date()).getFullYear()" placeholder="yyyy" v-model.number="componentData.death.impossible_date_year" onKeyPress="if(this.value.length==4) return false;">
              </div>
            </div>
          </div>
          <div class="row field-row" v-if="!reservationFlag && !editFlag && hasAtLeastOneNumericTimeExpression(componentData.death.age_years, componentData.death.age_months, componentData.death.age_weeks, componentData.death.age_days, componentData.death.age_hours, componentData.death.age_minutes)">
            <label :class="labelColumnClasses" for="age">Age:</label>
            <div id="age" :class="fieldColumnClasses">
              <div class="form-control field-text">{{ getFullAge(componentData.death.age_years, componentData.death.age_months, componentData.death.age_weeks, componentData.death.age_days, componentData.death.age_hours, componentData.death.age_minutes) }}</div>
            </div>
          </div>
          <div v-else-if="!reservationFlag && editFlag">
            
            <StandardInputRow :label="'Years'" v-model.number="componentData.death.age_years" :inputType="'number'" :attributes="{ step:1, min:0, max:125 }"/>
            <StandardInputRow :label="'Months'" v-model.number="componentData.death.age_months" :inputType="'number'" :attributes="{ step:1, min:0 }"/>
            <StandardInputRow :label="'Weeks'" v-model.number="componentData.death.age_weeks" :inputType="'number'" :attributes="{ step:1, min:0 }"/>
            <StandardInputRow :label="'Days'" v-model.number="componentData.death.age_days" :inputType="'number'" :attributes="{ step:1, min:0 }"/>
            <StandardInputRow :label="'Hours'" v-model.number="componentData.death.age_hours" :inputType="'number'" :attributes="{ step:1, min:0 }"/>
            <StandardInputRow :label="'Minutes'" v-model.number="componentData.death.age_minutes" :inputType="'number'" :attributes="{ step:1, min:0 }"/>

          </div>
        </section>
        
        <StandardInputRow :label="'Description'" v-model="componentData.description" :inputType="'textarea'" :attributes="{ maxlength:200 }" :editFlag="editFlag"/>

        <div class="row field-row" v-if="!editFlag && (componentData.residence_address && (componentData.residence_address.first_line || componentData.residence_address.second_line || componentData.residence_address.town || componentData.residence_address.county || componentData.residence_address.postcode || componentData.residence_address.country))">
          <!-- In display mode, display address without individual labels -->
          <label :class="labelColumnClasses" for="full-address">Address:</label>
          <div id="full-address" :class="fieldColumnClasses">
            <div class="form-control field-text">{{ getJoinedText([componentData.residence_address.first_line, componentData.residence_address.second_line, componentData.residence_address.town, componentData.residence_address.county, componentData.residence_address.postcode, componentData.residence_address.country], '\n') }}</div>
          </div>
        </div>
        <div v-else-if="editFlag">
          <h2>Address</h2>
          <section :class="{'smaller-line-height': !editFlag }">
            
            <StandardInputRow :label="'First Line'" v-model="componentData.residence_address.first_line" :inputType="'text'" :attributes="{ maxlength:200 }"/>
            <StandardInputRow :label="'Second Line'" v-model="componentData.residence_address.second_line" :inputType="'text'" :attributes="{ maxlength:200 }"/>
            <StandardInputRow :label="'Town'" v-model="componentData.residence_address.town" :inputType="'text'" :attributes="{ maxlength:50 }"/>
            <StandardInputRow :label="'County'" v-model="componentData.residence_address.county" :inputType="'text'" :attributes="{ maxlength:50 }"/>
            <StandardInputRow :label="'Postcode'" v-model="componentData.residence_address.postcode" :inputType="'text'" :attributes="{ maxlength:10,  class:'uppercase-text' }"/>
            <StandardInputRow :label="'Country'" v-model="componentData.residence_address.country" :inputType="'text'" :attributes="{ maxlength:50 }"/>
            
          </section>
        </div>
        <section v-if="!reservationFlag && (editFlag || componentData.death.death_cause || componentData.death.event)">

          <StandardInputRow :label="'Cause of Death'" v-model="componentData.death.death_cause" :inputType="'textarea'" :attributes="{ maxlength:250 }" :editFlag="editFlag"/>
           <!-- pdf upload -->
           <div>        
            <label  for='file_upload_id' v-if="pdfToUpload==null"> Add a File: {{ componentData.file }}
              <input type="file" @change="selectFile" id='file_upload_id'>
              <i class="fas fa-file-pdf pointer">
              <span v-if="fileName">  {{fileName.name}}  </span>
              <span v-else>  No file selected  </span>
              </i>      
            </label>                       
           </div>
           
          <!--event_field-->
          <StandardInputRow
            :key="componentData.event_field.name" :label="componentData.event_field.name"
            v-model="componentData['death'][componentData.event_field.content]" :inputType="componentData.event_field.type"
            :attributes="{ maxlength:10 }" :readonlyOption="true" :editFlag="editFlag"
            :options_select="select_fields(componentData.event_field.options)"
            :placeholder="componentData.event_field.name"/>
        </section>

        <FormButtons v-if="siteAdminOrSiteWarden && (!createMode || reservationFlag)" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="false" @toggle-edit="toggleEdit($event)"/>

      </form>

      <div v-if="reservationFlag && siteAdminOrSiteWarden && !editFlag && !createMode">
        <button type="button" class="bgms-button btn" @click="$router.replace({ name: graveManagementChildRoutesEnum.convertReservation, params: { personID: personID } })">Convert to Burial</button>
        <button type="button" class="bgms-button btn" @click="$router.replace({ name: graveManagementChildRoutesEnum.deleteReservation, params: { personID: personID } })">Delete Reservation</button>
      </div>

      <form v-if="!reservationFlag && !createMode" class="form-horizontal form-box-inside management-tool-form" action="" v-show="!editFlag">
        <div class="row field-row">
          <label class="col-xs-12 control-label" for="linked-memorials">Memorials:</label>
        </div>
        <section id="linked-memorials" class="row no-margin">
          <LinkedMemorials class="col-xs-12" :id="id" :linkedType="'person'" @loading-data-flag="heightChangedFlag += 1"/>
        </section>
      </form>

      <!-- Profession modal form -->
      <AddModel url="/mapmanagement/allPersonOptions/" fieldName="profession" storeCommit="appendProfessionList" @new-data-added="componentData.profession=$event" maxlength='200'></AddModel>

      <!-- Religion modal form -->
      <AddModel url="/mapmanagement/allPersonOptions/" fieldName="death.religion" storeCommit="appendReligionList" @new-data-added="componentData.death.religion=$event" maxlength='200'></AddModel>
      
      <!-- Parish modal form -->
      <AddModel url="/mapmanagement/allPersonOptions/" fieldName="death.parish" storeCommit="appendParishList" @new-data-added="componentData.death.parish=$event" maxlength='200'></AddModel>
      
      <!-- Event modal form -->
      <AddModel url="/mapmanagement/allPersonOptions/" fieldName="death.event" storeCommit="appendEventList" @new-data-added="componentData.death.event=$event" maxlength='35' includeDescription='true'></AddModel>
      
      <!-- Next of kin modal form -->
      <AddNextOfKin @update-next-of-kin="componentData.next_of_kin=$event; componentData.next_of_kin_display_name=componentData.next_of_kin.display_name;"></AddNextOfKin>

    </ScrollButtons>
    <router-view></router-view>
  </div>
  <div v-else class="loading-placeholder">
    <div class="loading-placeholder-contents">
      <i class="fa fa-spinner fa-spin"/>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator';
import axios from 'axios'
import { _ } from 'core-js';
import constants from '@/global-static/constants.ts';
import { formatDate, individualDateFieldsToSingleDate } from '@/global-static/dataFormattingAndValidation.ts';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin.ts';
import FeatureTools from '@/mapmanagement/mixins/featureTools.ts';
import ScrollButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ScrollButtons.vue';
import FormButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/FormButtons.vue';
import StandardInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/StandardInputRow.vue';
import DateInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/DateInputRow.vue';
import LinkedMemorials from '@/mapmanagement/components/ManagementTool/Components/LinkedMemorials.vue';
import {isNumeric} from "rxjs/internal-compatibility";

/**
 * Class representing DeathPersonDetails component
 * @extends mixins: ManagementToolsMixin
 */
@Component({
  components: {
    LinkedMemorials,
    FormButtons,
    StandardInputRow,
    DateInputRow,
    ScrollButtons,
    ValidationBox: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/ValidationBox.vue'),
    AddNextOfKin: () => import('@/mapmanagement/components/ManagementTool/Components/AddNextOfKinModal.vue'),
    AddModel: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/AddModal.vue')
  }
})
export default class DeathPersonDetails extends mixins(ManagementToolsMixin, FeatureTools){

  formatDate = formatDate;
  individualDateFieldsToSingleDate = individualDateFieldsToSingleDate;

  @Prop() id;
  @Prop() showComponent;
  @Prop() personID;

  saving: boolean = false;

  createMode: boolean = false;

  newProfession: string = '';
  newReligion: string = '';
  newParish: string = '';
  newEventName: string = '';
  newEventDescription: string = '';
  fileName: string = '';
  pdfToUpload = null;


  // true if this is a reservation
  reservationFlag: boolean = false;

  graveManagementChildRoutesEnum = constants.GRAVE_MANAGEMENT_CHILD_ROUTES;

  reservedPersonService = this.$store.getters.reservedPersonService;

  /**
   * Vue mounted lifecycle hook
   * - Load options for select elements
   */
  mounted() {
    //debugger; //eslint-disable-line no-debugger 
    let v = this;

    v.reservationFlag = v.isRouteActive(constants.GRAVE_MANAGEMENT_CHILD_ROUTES.reservations);

    v.componentName = "death_person_details";

    v.editableFields = ['title', 'first_names', 'last_name', 'birth_name', 'other_names', 'impossible_date_day', 'impossible_date_month', 'impossible_date_year', 'gender', 'description', 'profession','parish','religion','event','residence_address', 'next_of_kin', 'next_of_kin_relationship', 'reservation_reference'];

    // death fields do not apply to reservations
    if (!v.reservationFlag)
      v.editableFields.push('death');

    v.initData();

    // if lists have not yet been loaded into vuex, load them
    if (!this.$store.state.ManagementTool.professionList && !this.$store.state.ManagementTool.eventList && !this.$store.state.ManagementTool.religionList && !this.$store.state.ManagementTool.parishList) {

      axios.get('/mapmanagement/allPersonOptions')
      .then(function(response) {
        v.$store.commit('setPersonDetailLists', response.data);
      })
      .catch(function(response) {
        console.warn('Couldn\'t get person details lists:', response.response.data);
      });
    }
  }
  
  initData() {
    let v = this;

    // this is needed in ManagementToolsMixin
    // if this is a reservation, use personID prop
    v._id = v.reservationFlag ? 
      v.personID ? v.personID : ''
      : v.id;

    if (v._id === '') {
      v.createMode = true;
      v.editFlag = true;
    }
    else {
      v.createMode = false;
      v.editFlag = false;
    }

    v.loadDataWithoutStoring('/mapmanagement/personDetail/?person_id=', v._id)
    .then((result) => {
      // Before storing: add address object if it is null
      if (!result['residence_address']) {
        result['residence_address'] = { 
          first_line: undefined,
          second_line: undefined,
          town: undefined,
          county: undefined,
          postcode: undefined,
          country: undefined
        };
      }

      v.storeData(result);
    })
    .catch(() => {});
  }


  /*** Watchers ***/

  /**
   * Used to update scrolling in 'Add Burial' and tabs
   */
  @Watch('showComponent', { immediate: true }) 
  onShowComponentChanged(val: any, oldVal: any) {
    if (val)
      this.heightChangedFlag += 1;
  }

  /**
   * Watcher: When deedID is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('$route.params.personID')
  onDeedIDChanged(val: any, oldVal: any) {
    if (this._id !== val)
      this.initData();
  }
  /**
   * Watcher: When pdfFlag is changed
   * @param {any} val
   * @param {any} oldVal
   */
   @Watch('pdfFlag')
  onEditFlagChanged(val: any, oldVal: any) {
    this.pdfToUpload = null;
  }

  /*** Methods ***/

  /**
   * Validates data. Displays message if errors present.
   * @returns true if validation passes
   */
  validateData(): boolean {
    let errors = [];
    let returnValue = true;

    if (!this.componentData.first_names && !this.componentData.last_name) {
      errors.push("A first name and/or last name is required.");
      returnValue = false;

      // scroll to top so user can see validation message
      Vue.nextTick(() => { (document.getElementById('verticalScroll') as HTMLElement).scrollTop = 0; });
    }
    
    // Add errors to componentData. Doing this means errors are removed when form is cancelled or saved.
    Vue.set( this.componentData, 'errors', errors )

    return returnValue;
  }
// file upload icon 
  selectFile(event){
  this.fileName=event.target.files[0]
  console.log(event.target.files)
  }

  /**
   * Saves an edit
   */
  onSubmit() {

    let v = this;

    if (v.validateData()) {
      v.saving = true;

      let data = v.getChangedData();
      let formData = {};

    for ( var key in data ) {
      if(typeof data[key] === 'object'){
        let dir = {};
        for ( var objKey in data[key] ){
          dir[objKey] = data[key][objKey];
        }
        formData[key] = dir;
      }
      else{
        formData[key] = data[key];
      }
    }

      if (v._id) {
        // update existing record 
        axios.patch('/mapmanagement/personDetail/', formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      )
        .then(function(response) {
          v.updateNextOfKinAfterSave(response.data.next_of_kin)
          // updated saved version
          v.updateSavedVersion();
          v.appendToOrModifyItemInQuery('edit', null);
          v.saving = false;
          v.notificationHelper.createSuccessNotification('Person details saved successfully');
        })
        .catch(function(response) {
          v.saving = false;
          const result = JSON.parse(JSON.stringify(response.response.data));
          if (result.reservation_reference_taken) {
            v.notificationHelper.createErrorNotification("Reservation reference already in use");
          }
          else {
            console.warn('Couldn\'t save person details:', response.response.data);
            v.notificationHelper.createErrorNotification("Couldn't save person details");
          }
        });
      }
      else {
        if (v.reservationFlag) {
          data['reservation'] = true;
          data['graveplot_id'] = v.id;
          data['layer'] = v.$route.params.layer;
        }

        // create new record
        axios.post('/mapmanagement/personDetail/', data,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then(function(response) {
          v.updateNextOfKinAfterSave(response.data.next_of_kin)
          // updated saved version
          v.updateSavedVersion();
          v.saving = false;

          if (v.reservationFlag) {

            // refreshes list of reserved persons
            v.reservedPersonService.loadReservedPersonsFromGeoJson();

            let currentLayer = v.$route.params.layer;

            if(currentLayer==='available_plot') {
              currentLayer = 'reserved_plot';
              // change current available_plot to a reserved_plot as it now has a reservation
              v.changeFeatureLayer('available_plot', currentLayer, v.$route.params.reservationavailablePlotID, v.$route.params.id)
              .then(() => {
                v.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.reservations, params: { personID: response.data.person_id, layer: currentLayer }, query: { refresh: 'true' }});
              });
            }
            else
              v.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.reservations, params: { personID: response.data.person_id }, query: { refresh: 'true' }});

            v.notificationHelper.createSuccessNotification('Reservation created successfully');
          }
          else
            v.notificationHelper.createSuccessNotification('Person created successfully');
        })
        .catch(function(response) {
          v.saving = false;
          if (v.reservationFlag) {
            
            if (response.response.data.reservation_reference_taken) {
              v.notificationHelper.createErrorNotification("Reservation reference already in use");
            }
            else {
              console.warn('Couldn\'t create reservation:', response.response.data);
              v.notificationHelper.createErrorNotification("Couldn't create reservation");
            }
          }
          else {
            console.warn('Couldn\'t create person:', response.response.data);
            v.notificationHelper.createErrorNotification("Couldn't create person");
          }
        });
      }
    }
  }

  hasAtLeastOneNumericTimeExpression(years, months, weeks, days, hours, minutes){
    return isNumeric(years) || isNumeric(months)
            || isNumeric(weeks) || isNumeric(days)
            || isNumeric(hours) || isNumeric(minutes);
  }

  getFullAge(years, months, weeks, days, hours, minutes): string {

    let fullAge = "";

    if (isNumeric(years))
      fullAge = years + " " + (years===1 ? 'year' : 'years')
    
    if (isNumeric(months)) {
      if (fullAge)
        fullAge += " ";
      
      fullAge += months + " " + (months===1 ? 'month' : 'months')
    }
    
    if (isNumeric(weeks)) {
      if (fullAge)
        fullAge += " ";
      
      fullAge += weeks + " " + (weeks===1 ? 'week' : 'weeks')
    }
    
    if (isNumeric(days)) {
      if (fullAge)
        fullAge += " ";
      
      fullAge += days + " " + (days===1 ? 'day' : 'days')
    }
    
    if (isNumeric(hours)) {
      if (fullAge)
        fullAge += " ";
      
      fullAge += hours + " " + (hours===1 ? 'hour' : 'hours')
    }
    
    if (isNumeric(minutes)) {
      if (fullAge)
        fullAge += " ";
      
      fullAge += minutes + " " + (minutes===1 ? 'minute' : 'minutes')
    }

    return fullAge;
  }

  /**
   * Open person management for next of kin
   */
  goToPersonManagement(id) {
    debugger; //eslint-disable-line no-debugger 
    this.$router.replace({ name: constants.PERSON_MANAGEMENT_CHILD_ROUTES.persondetails, params: { id: id }});
  }

  updateNextOfKinAfterSave(nextOfKinData) {
    this.componentData.next_of_kin = nextOfKinData;
  }

  /**
   * Toggles edit.
   * Or, when creating a reservation, closes when 'Cancel' is clicked
   */
  toggleEdit(event) {
    debugger; //eslint-disable-line no-debugger 
    if (this.reservationFlag && !this._id && !event)
      this.$router.replace({ name: constants.GRAVE_MANAGEMENT_PATH });
    else
      this.appendToOrModifyItemInQuery('edit', event);
  }

  showYearIfImpossibleMonthIsNotDefined(person){
    if(person.burials[0] && !person.burials[0].impossible_date_month && person.most_recent_burial_date){
      return person.most_recent_burial_date.split("-")[0]
    }
    return formatDate(person.most_recent_burial_date);
  }

  select_fields(value){
    if (value != null){
      let options = value.split(/\n/ig);
      return options;
    }
    else {
      return [];
    }
  }
}
</script>

<style scoped>
input[type="file"] {
    display: none;
};
</style>