<template>
  <div id="companyDetailsElement" v-if="componentData">
    <ScrollButtons :heightChangedFlag="heightChangedFlag" :noChangeParentHeight="$route.name===graveManagementChildRoutesEnum.newGraveOwner">

      <ValidationBox :errors="componentData.errors"/>

      <form id="company_details_form" class="form-horizontal form-box-inside management-tool-form no-margin" @submit.prevent="onSubmit" v-show="$route.name!==companyManagementChildRoutesEnum.companydetailsaddress">

        <FormButtons v-if="siteAdminOrSiteWarden && !createMode" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="true" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)"/>
        <div v-else-if="createMode && fieldChanged"/>

        <section>
          <StandardInputRow :label="'Name'" v-model="componentData.name" :inputType="'text'" :attributes="{ maxlength:200 }" :readonlyOption="true" :editFlag="editFlag"/>
          <StandardInputRow :label="'Email'" v-model="componentData.email" :inputType="'email'" :readonlyOption="true" :editFlag="editFlag"/>
          <PhoneInputRow :label="'Phone Number'" v-model="componentData.phone_number" :readonlyOption="true" :editFlag="editFlag" @phone-validation="phoneNumberValid=$event"/>
          <PhoneInputRow :label="'Phone Number 2'" v-model="componentData.phone_number_2" :readonlyOption="true" :editFlag="editFlag" @phone-validation="phoneNumberValid2=$event"/>
          <StandardInputRow :label="'Remarks'" v-model="componentData.remarks" :inputType="'textarea'" :attributes="{ maxlength:200 }" :editFlag="editFlag"/>
        </section>

        <FormButtons v-if="siteAdminOrSiteWarden && !createMode" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="false" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)"/>

      </form>

      <section v-if="!editFlag" v-show="$route.name===companyManagementChildRoutesEnum.companydetails">
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
                <router-link tag="a" href="" :to="openOrCloseChildRoute(companyManagementChildRoutesEnum.companydetails, companyManagementChildRoutesEnum.companydetailsaddress, [{ name: 'addressID', value: address.id }])" title="Edit address"><i class="far fa-edit"></i></router-link>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="3" v-if="loadingDataFlag"><span class="fa fa-spinner fa-spin"></span></td>
              <td colspan="3" v-else>No addresses recorded.</td>
            </tr>
          </tbody>
        </table>
        <router-link v-if="siteAdminOrSiteWarden" tag="button" id="add-new-grave-link-btn" class="bgms-button btn" :to="openOrCloseChildRoute(companyManagementChildRoutesEnum.companydetails, companyManagementChildRoutesEnum.companydetailsaddress, [{ name: 'createNew', value: true }])">Add New Address</router-link>
      </section>

      <section v-if="!editFlag && previousAddressesPresent" v-show="$route.name===companyManagementChildRoutesEnum.companydetails">
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
                <router-link tag="a" href="" :to="openOrCloseChildRoute(companyManagementChildRoutesEnum.companydetails, companyManagementChildRoutesEnum.companydetailsaddress, [{ name: 'addressID', value: address.id }])" title="Edit address"><i class="far fa-edit"></i></router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <router-view :companyId="_id"></router-view>

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

/**
 * Class representing CompanyDetails component
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
export default class CompanyDetails extends mixins(ManagementToolsMixin){

  @Prop() id;
  @Prop() createNew;
  @Prop() companyName;

  saving: boolean = false;

  createMode: boolean = false;
  
  phoneNumberValid: boolean = true;
  phoneNumberValid2: boolean = true;

  companyManagementChildRoutesEnum = constants.COMPANY_MANAGEMENT_CHILD_ROUTES;
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

    v.componentName = "company_details";

    v.editableFields = ['name', 'email', 'phone_number', 'remarks', 'addresses'];
    
    v.loadDataWithoutStoring('/api/company/?id=', v._id)
    .then((result) => {
      v.storeData(result);
      
      if (v.createNew) {
        // if company name has been given for creating a new company
        if (v.companyName)
          v.componentData.name = v.companyName;
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
  
  /**
   * Watcher: updates name field when it has been changed by parent
   */
  @Watch('companyName')
  onLastNamePropChanged(val: any, oldVal: any) {
    this.componentData.name = val;
  }

  /*** Watchers ***/

  /**
   * Watcher: When refresh in router query is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('$route.query.refreshaddress')
  onRefreshChanged(val: any, oldVal: any) {
    if (val) {
      // refreshes the company data
      this.loadData('/api/company/?id=', this._id);
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

      axios.patch('/api/company/', data)
      .then(function(response) {
        // updated saved version
        v.updateSavedVersion();
        v.appendToOrModifyItemInQuery('edit', null);
        v.saving = false;
        v.notificationHelper.createSuccessNotification('Company details saved successfully');
      })
      .catch(function(response) {
        v.saving = false;
        console.warn('Couldn\'t save company details:', response);
        v.notificationHelper.createErrorNotification("Couldn't save company details");
      });
    }
  }

  /**
   * Validates data. Displays message if errors present.
   * @returns true if validation passes
   */
  validateData(): boolean {
    let errors = [];

    if (!this.componentData.name)
      errors.push("A name is required.");

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
      Vue.nextTick(() => { ((document.getElementById('verticalScroll')) as HTMLElement).scrollTop = 0; });

      this.heightChangedFlag += 1;
    }
    
    // Add errors to componentData. Doing this means errors are removed when form is cancelled or saved.
    Vue.set( this.componentData, 'errors', errors )

    return errors.length === 0;
  }
}
</script>
