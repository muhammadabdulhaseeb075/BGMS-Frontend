<template>
  <div id="personDetailsElement" v-if="componentData">
    <ScrollButtons :heightChangedFlag="heightChangedFlag" :noChangeParentHeight="$route.name===graveManagementChildRoutesEnum.newGraveOwner">

      <ValidationBox :errors="componentData.errors"/>

      <form id="person_details_form" class="form-horizontal form-box-inside management-tool-form no-margin" @submit.prevent="onSubmit" v-show="$route.name!==personManagementChildRoutesEnum.persondetailsaddress">

        <FormButtons v-if="siteAdminOrSiteWarden && !createMode" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="true" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)"/>
        <div v-else-if="createMode && fieldChanged"/>

        <section>

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
          <StandardInputRow :label="'Email'" v-model="componentData.email" :inputType="'email'" :readonlyOption="true" :editFlag="editFlag"/>
          <PhoneInputRow :label="'Phone Number'" v-model="componentData.phone_number" :readonlyOption="true" :editFlag="editFlag" @phone-validation="phoneNumberValid=$event"/>
          <PhoneInputRow :label="'Phone Number 2'" v-model="componentData.phone_number_2" :readonlyOption="true" :editFlag="editFlag" @phone-validation="phoneNumberValid2=$event"/>
          <StandardInputRow :label="'Gender'" v-model="componentData.gender" :inputType="'text'" :attributes="{ maxlength:10 }" :readonlyOption="true" :editFlag="editFlag"/>

          <div class="row field-row" v-if="editFlag || componentData.birth_date_day || componentData.birth_date_month || componentData.birth_date_year">
            <label :class="labelColumnClasses" for="birth-date">Date of Birth:</label>
            <div v-if="!editFlag" id="birth-date" :class="fieldColumnClasses">
              <input readonly type="text" class="form-control" :value="individualDateFieldsToSingleDate(componentData.birth_date_day, componentData.birth_date_month, componentData.birth_date_year)">
            </div>
            <div v-if="editFlag" id="birth-date" :class="fieldColumnClasses">
              <div class="multi-input">
                <input class="form-control multi-input_input multi-input_input--day no-spinner" type="number" step="1" min="0" max="31" placeholder="dd" v-model.number="componentData.birth_date_day" onKeyPress="if(this.value.toString().length==2) return false;">
                <span class="multi-input_divider">/</span>
                <input class="form-control multi-input_input multi-input_input--month no-spinner" type="number" step="1" min="0" max="12" placeholder="mm" v-model.number="componentData.birth_date_month" onKeyPress="if(this.value.toString().length==2) return false;">
                <span class="multi-input_divider">/</span>
                <input class="form-control multi-input_input multi-input_input--year no-spinner" type="number" step="1" min="0" :max="(new Date()).getFullYear()" placeholder="yyyy" v-model.number="componentData.birth_date_year" onKeyPress="if(this.value.length==4) return false;">
              </div>
            </div>
          </div>
        </section>
        
        <StandardInputRow :label="'Remarks'" v-model="componentData.remarks" :inputType="'textarea'" :attributes="{ maxlength:200 }" :editFlag="editFlag"/>

        <FormButtons v-if="siteAdminOrSiteWarden && !createMode" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="false" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)"/>

      </form>

      <section v-if="!editFlag" v-show="$route.name===personManagementChildRoutesEnum.persondetails">
        <label class="col-xs-12 control-label">Current Addresses:</label>
        <table class="table table-condensed">
          <thead>
            <tr>
              <th>Address</th>
              <th>Current</th>
              <th v-if="siteAdminOrSiteWarden"></th>
            </tr>
          </thead>
          <tbody v-if="currentAddressesPresent">
            <tr v-for="address in componentData.current_addresses" :key="address.id">
              <td>{{ address.display_address }}</td>
              <td>{{ address.current ? 'Yes' : 'No' }}</td>
              <td v-if="siteAdminOrSiteWarden">
                <router-link tag="a" href="" :to="openOrCloseChildRoute(personManagementChildRoutesEnum.persondetails, personManagementChildRoutesEnum.persondetailsaddress, [{ name: 'addressID', value: address.id }])" title="Edit address"><i class="far fa-edit"></i></router-link>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="3" v-if="loadingDataFlag"><span class="fa fa-spinner fa-spin"></span></td>
              <td colspan="3" v-else>No current addresses recorded.</td>
            </tr>
          </tbody>
        </table>
        <router-link v-if="siteAdminOrSiteWarden" tag="button" id="add-new-grave-link-btn" class="bgms-button btn" :to="openOrCloseChildRoute(personManagementChildRoutesEnum.persondetails, personManagementChildRoutesEnum.persondetailsaddress, [{ name: 'createNew', value: true }])">Add New Address</router-link>
      </section>

      <section v-if="!editFlag && previousAddressesPresent" v-show="$route.name===personManagementChildRoutesEnum.persondetails">
        <label class="col-xs-12 control-label">Previous Addresses:</label>
        <table class="table table-condensed">
          <thead>
            <tr>
              <th>Address</th>
              <th>Current</th>
              <th v-if="siteAdminOrSiteWarden"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="address in componentData.previous_addresses" :key="address.id">
              <td>{{ address.display_address }}</td>
              <td>{{ address.current ? 'Yes' : 'No' }}</td>
              <td v-if="siteAdminOrSiteWarden">
                <router-link tag="a" href="" :to="openOrCloseChildRoute(personManagementChildRoutesEnum.persondetails, personManagementChildRoutesEnum.persondetailsaddress, [{ name: 'addressID', value: address.id }])" title="Edit address"><i class="far fa-edit"></i></router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <router-view :personId="_id"></router-view>

    </ScrollButtons>
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
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';
import ScrollButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ScrollButtons.vue';
import FormButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/FormButtons.vue';
import StandardInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/StandardInputRow.vue';
import PhoneInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/PhoneInputRow.vue';
import constants from '@/global-static/constants.ts';
import { individualDateFieldsToSingleDate } from '@/global-static/dataFormattingAndValidation.ts';

/**
 * Class representing PersonDetails component
 * @extends mixins: ManagementToolsMixin
 */
@Component({
  components: {
    FormButtons,
    StandardInputRow,
    PhoneInputRow,
    ScrollButtons,
    ValidationBox: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/ValidationBox.vue')
  }
})
export default class PersonDetails extends mixins(ManagementToolsMixin){
  
  individualDateFieldsToSingleDate = individualDateFieldsToSingleDate;

  @Prop() id;
  @Prop() createNew;
  @Prop() firstNames;
  @Prop() lastName;

  saving: boolean = false;

  createMode: boolean = false;

  phoneNumberValid: boolean = true;
  phoneNumberValid2: boolean = true;

  personManagementChildRoutesEnum = constants.PERSON_MANAGEMENT_CHILD_ROUTES;
  graveManagementChildRoutesEnum = constants.GRAVE_MANAGEMENT_CHILD_ROUTES;

  /**
   * Vue mounted lifecycle hook
   * - Load options for select elements
   */
  mounted() {
    let v = this;

    if (v.createNew) {
      v.createMode = true;
      this.editFlag = true;
    }

    // this is needed in ManagementToolsMixin
    v._id = v.createNew ? '' : v.id;

    v.componentName = "person_details";

    v.editableFields = ['title', 'first_names', 'last_name', 'birth_name', 'other_names', 'birth_date_day', 'birth_date_month', 'birth_date_year', 'gender', 'email', 'phone_number', 'remarks', 'addresses'];

    v.loadDataWithoutStoring('/api/person/?id=', v._id)
    .then((result) => {
      v.storeData(result);
      
      if (v.createNew) {
        // if first names and/or last name has been given for creating a new person
        if (v.firstNames)
          v.componentData.first_names = v.firstNames;
        if (v.lastName)
          v.componentData.last_name = v.lastName;
      }
    })
    .catch(() => {});
  }


  /*** Computed ***/

  get currentAddressesPresent() :boolean {
    return this.componentData && this.componentData.current_addresses && this.componentData.current_addresses.length > 0;
  }

  get previousAddressesPresent() :boolean {
    return this.componentData && this.componentData.previous_addresses && this.componentData.previous_addresses.length > 0;
  }

  /*** Watchers ***/
  
  /**
   * Watcher: updates first names field when it has been changed by parent
   */
  @Watch('firstNames')
  onFirstNamesPropChanged(val: any, oldVal: any) {
    this.componentData.first_names = val;
  }
  
  /**
   * Watcher: updates last name field when it has been changed by parent
   */
  @Watch('lastName')
  onLastNamePropChanged(val: any, oldVal: any) {
    this.componentData.last_name = val;
  }

  /**
   * Watcher: When refresh in router query is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('$route.query.refreshaddress')
  onRefreshChanged(val: any, oldVal: any) {
    if (val) {
      // refreshes the person data
      this.loadData('/api/person/?id=', this._id);
    }

    // removes refresh in query
    this.appendToOrModifyItemInQuery('refreshaddress', null);
  }

  /*** Methods ***/

  /**
   * Saves an edit
   */
  onSubmit() {

    let v = this;

    if (v.validateData()) {
      v.saving = true;

      let data = v.getChangedData();

      axios.patch('/api/person/', data)
      .then(function(response) {
        // updated saved version
        v.updateSavedVersion();
        v.appendToOrModifyItemInQuery('edit', null);
        v.saving = false;
        v.notificationHelper.createSuccessNotification('Person details saved successfully');
      })
      .catch(function(response) {
        v.saving = false;
        console.warn('Couldn\'t save person details:', response);
        v.notificationHelper.createErrorNotification("Couldn't save person details");
      });
    }
  }

  /**
   * Validates data. Displays message if errors present.
   * @returns true if validation passes
   */
  validateData(): boolean {
    let errors = [];

    if (!this.componentData.first_names && !this.componentData.last_name)
      errors.push("A first name and/or last name is required.");

    if (this.componentData.phone_number && !this.phoneNumberValid)
      errors.push("Phone number is not valid.");

    if (this.componentData.phone_number_2 && !this.phoneNumberValid2)
      errors.push("Phone number 2 is not valid.");

    let nodes = document.querySelectorAll(`#${'person_details_form'} :invalid`);

    if (nodes.length > 0) {
      for (let i in nodes) {
        const node = nodes[i] as HTMLInputElement;
        if (node.type) {
          errors.push(node.validationMessage);
        }
      }
    }

    if (errors.length > 0) {
      // scroll to top so user can see validation message
      Vue.nextTick(() => { (document.getElementById('verticalScroll') as HTMLElement).scrollTop = 0; });

      this.heightChangedFlag += 1;
    }
    
    // Add errors to componentData. Doing this means errors are removed when form is cancelled or saved.
    Vue.set( this.componentData, 'errors', errors )

    return errors.length === 0;
  }
}

</script>
