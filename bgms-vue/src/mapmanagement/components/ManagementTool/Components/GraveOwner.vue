<template>
  <div :id="componentName" v-if="componentData">
    <ScrollButtons :heightChangedFlag="heightChangedFlag">

      <ValidationBox :errors="componentData.errors"/>

      <form class="form-horizontal form-box-inside management-tool-form no-margin" @submit.prevent="onSubmit">

        <FormButtons v-if="siteAdminOrSiteWarden && !newOwner" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)" :showEdit="true" :showBack="true" @toggle-back="close(true)"/>

        <div v-if="_id" class="row field-row name-field">{{ componentData.display_name }}</div>

        <section>
          <StandardInputRow :label="'Current'" v-model="componentData.active_owner" :inputType="'checkbox'" :readonlyOption="true" :editFlag="editFlag && !expiredToDate" :readonly="toDateIncluded"/>

          <DateInputRow :label="'Owner From'" :editFlag="editFlag" :day="componentData.owner_from_date_day" @day-input="componentData.owner_from_date_day=$event" :month="componentData.owner_from_date_month" @month-input="componentData.owner_from_date_month=$event" :year="componentData.owner_from_date_year" @year-input="componentData.owner_from_date_year=$event"/>

          <DateInputRow :label="'Owner To'" :editFlag="editFlag" :day="componentData.owner_to_date_day" @day-input="componentData.owner_to_date_day=$event" :month="componentData.owner_to_date_month" @month-input="componentData.owner_to_date_month=$event" :year="componentData.owner_to_date_year" @year-input="componentData.owner_to_date_year=$event"/>

          <div class="row field-row" v-if="!editFlag && componentData.owner_status.length">
            <label :class="labelColumnClasses" for="owner-status">Status:</label>
            <div id="owner-status" :class="fieldColumnClasses">
              <div class="form-control field-text">{{ statusFormatted }}</div>
            </div>
          </div>
          <div id="owner-status-select" v-else-if="editFlag && ownerStatusList">
            <div class="col-xs-11 no-padding">
              <h2>Status</h2>
            </div>
            <button class="btn sidebar-normal-button add-button col-xs-1" style="margin-top:7px;" type="button" @click="$modal.show('add-status')" v-show="editFlag"><i class="fa fa-plus"></i></button>
            <div class="col-xs-12 no-padding">
              <multiselect :disabled="!editFlag" :value='componentData.owner_status' placeholder="Add a status" label='status' track-by="id" :options="ownerStatusList" :multiple="true" :close-on-select="true" @select="addStatus" @remove="removeStatus" :searchable="false" :taggable="true"></multiselect>
            </div>
          </div>

          <StandardInputRow :label="'Remarks'" v-model="componentData.remarks" :inputType="'textarea'" :attributes="{ maxlength:400 }" :editFlag="editFlag"/>

        </section>

        <FormButtons v-if="siteAdminOrSiteWarden && !newOwner" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="false" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)"/>
      </form>

      <!-- Status modal form -->
      <AddModel url="/mapmanagement/allOwnershipOptions/" fieldName="status" storeCommit="appendStatusList" @new-data-added="addOwnerStatus($event)" maxlength='200'></AddModel>
  
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
import Component, { mixins } from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import axios from 'axios';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';
import FormButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/FormButtons.vue';
import StandardInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/StandardInputRow.vue';
import DateInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/DateInputRow.vue';
import constants from '@/mapmanagement/static/constants.ts';
import globalConstants from '@/global-static/constants.ts';
import { individualDateFieldsToSingleDate } from '@/global-static/dataFormattingAndValidation.ts';
import ScrollButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ScrollButtons.vue';

const hash = require('object-hash');

/**
 * Class representing GraveOwner component
 * @extends mixins: ManagementToolsMixin
 */
@Component({
  components: {
    Multiselect: () => import('vue-multiselect'),
    FormButtons,
    StandardInputRow,
    DateInputRow,
    ScrollButtons,
    ValidationBox: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/ValidationBox.vue'),
    AddModel: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/AddModal.vue')
  }
})
export default class GraveOwner extends mixins(ManagementToolsMixin){

  @Prop() newOwner;
  @Prop() ownerID;
  @Prop() startDay;
  @Prop() startMonth;
  @Prop() startYear;
  @Prop() firstOwner;

  saving: boolean = false;

  labelColumnClasses = constants.LABEL_COLUMN_CLASSES;
  fieldColumnClasses = constants.FIELD_COLUMN_CLASSES;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    this.componentName = "grave_owner";
    this._id = this.newOwner ? '' : this.ownerID;
    if (this.newOwner) this.editFlag = true;

    this.editableFields = ['active_owner', 'owner_from_date_day', 'owner_from_date_month', 'owner_from_date_year', 'owner_to_date_day', 'owner_to_date_month', 'owner_to_date_year', 'owner_status', 'remarks'];

    // load data
    this.loadDataWithoutStoring('/mapmanagement/graveOwner/?id=', this._id)
    .then((result) => {
      this.storeData(result);
      
      if (this.firstOwner) {
        // this is the first owner register for this deed. So give it the deed's start date.
        this.componentData.owner_from_date_day = this.startDay;
        this.componentData.owner_from_date_month = this.startMonth;
        this.componentData.owner_from_date_year = this.startYear;
      }

      // if lists have not yet been loaded into vuex, load them (they should have by this stage anyway)
      if (!this.$store.state.ManagementTool.currencyList) {
        axios.get('/mapmanagement/allOwnershipOptions')
        .then(response => {
          this.$store.commit('setOwnershipLists', response.data);
        })
        .catch(response => {
          console.warn('Couldn\'t get ownership lists:', response);
        });
      }
    })
    .catch(() => {});
  }

  /*** Computed ***/

  /**
   * @returns true if to date is in the past
   */
  get expiredToDate() {

    let returnValue = false;

    if (this.toDateIncluded) {
      let today = new Date();
      if (this.componentData.owner_to_date_year < today.getFullYear())
        returnValue = true;
      else if (this.componentData.owner_to_date_year === today.getFullYear()) {
        if (this.componentData.owner_to_date_month < (today.getMonth()+1))
          returnValue = true;
        else if (this.componentData.owner_to_date_month == (today.getMonth()+1)) {
          if (this.componentData.owner_to_date_day < today.getDate())
            returnValue = true;
        }
      }

      if (returnValue)
        this.componentData.active_owner = false;
      else if (this.toDateIncluded)
        this.componentData.active_owner = true;
    }

    return returnValue;
  }

  get toDateIncluded() {
    return this.componentData.owner_to_date_day && this.componentData.owner_to_date_month && this.componentData.owner_to_date_year;
  }

  /**
   * Computed property:
   * @returns {boolean} Details about the selected currency
   */
  get ownerStatusList() {
    return this.$store.state.ManagementTool.ownerStatusList;
  }

  /**
   * @returns {string} Owner status/es in viewable format
   */
  get statusFormatted() {
    let value = '';

    const ownerStatus = this.componentData.owner_status;

    if (ownerStatus && ownerStatus.length) {
      ownerStatus.forEach(element => {
        if (value)
          value += ', ';
        value += element.status;
      });
    }

    return value;
  }

  /*** Watchers ***/

  /*** Methods ***/

  /**
   * Validates data. Displays message if errors present.
   * @returns true if validation passes
   */
  validateData(): boolean {
    let errors = [];
    let returnValue = true;

    if ((this.componentData.owner_from_date_year < this.startYear) ||
    (this.componentData.owner_from_date_year===this.startYear && this.componentData.owner_from_date_month < this.startMonth) ||
    (this.componentData.owner_from_date_year===this.startYear && this.componentData.owner_from_date_month===this.startMonth && this.componentData.owner_from_date_day < this.startDay))
      errors.push("The 'Owner From' date must be on or after the ownership start date (" + individualDateFieldsToSingleDate(this.startDay, this.startMonth, this.startYear) + ").");

    if (errors.length > 0) {
      returnValue = false;

      // scroll to top so user can see validation message
      Vue.nextTick(() => { (document.getElementById('verticalScroll') as HTMLElement).scrollTop = 0; });
    }
    
    // Add errors to componentData. Doing this means errors are removed when form is cancelled or saved.
    Vue.set( this.componentData, 'errors', errors )

    return returnValue;
  }

  /**
   * Saves an edit
   */
  onSubmit() {
    if (!this.validateData()) { return; }

    this.saving = true;

    let data = this.getChangedData();

    // get the entire object if it has been modified at all
    if (hash(this.componentData.owner_status) != hash(this.componentDataSaved.owner_status))
      data['owner_status'] = this.componentData.owner_status;

    axios.patch('/mapmanagement/graveOwner/', data)
      .then(response => {
        // updated saved version
        this.updateSavedVersion();
        this.appendToOrModifyItemInQuery('refreshowners', true);
        this.appendToOrModifyItemInQuery('edit', null);
        this.notificationHelper.createSuccessNotification('Grave owner saved successfully');
      })
      .catch(response => {
        console.warn('Couldn\'t save grave details:', response);
        this.notificationHelper.createErrorNotification("Couldn't save grave owner");
      })
      .finally(() => {
        this.saving = false;
      });
  }

  close(refresh: boolean = false) {
    let query = this.$route.query ? this.$route.query : {};

    if (refresh)
      query['refreshOwnership'] = 'true';

    this.$router.replace({ name: globalConstants.GRAVE_MANAGEMENT_CHILD_ROUTES.graveOwnership, params: this.$route.params, query: query });
  }

  /** 
   * Add status
   */ 
  addStatus(selectedOption, id=null) {
    this.componentData.owner_status.push({
      id: selectedOption.id,
      status: selectedOption.status
    });
  }

  /** 
   * Remove status
   */ 
  removeStatus(removedOption, id) {
    this.componentData.owner_status.forEach((stat, index) => {
      // if can't be found in select)
      if (stat.id === removedOption.id) {
        this.componentData.owner_status.splice(index, 1);  
      }
    });
  }

  addOwnerStatus(statusID) {

    const status = this.ownerStatusList.find(status => status.id===statusID);
    this.addStatus(status);
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
