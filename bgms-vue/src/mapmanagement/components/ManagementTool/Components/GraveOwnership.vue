<template>
  <div :id="componentName" v-if="componentData" style="width: 100%">
    <ScrollButtons :heightChangedFlag="heightChangedFlag" v-show="$route.name===graveManagementChildRoutesEnum.graveOwnership">

      <ValidationBox :errors="componentData.errors"/>

      <form class="form-horizontal form-box-inside management-tool-form" @submit.prevent="onSubmit">

        <FormButtons v-if="siteAdminOrSiteWarden" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="true" @toggle-edit="toggleEditCancelButtonsInCreateMode($event, _id, graveManagementPath);"/>

        <div v-if="!editFlag && noData && (!componentData.current_grave_owners || componentData.current_grave_owners.length===0) && (componentData.previous_grave_owners || componentData.previous_grave_owners.length===0 || componentData.image_1 || componentData.image_2)" class="blank-form-placeholder">No deed details recorded.</div>
        <div v-else>
          <StandardInputRow :label="'Register'" :placeholder="'Ownership Register'" v-model="componentData.ownership_register" :inputType="'text'" :attributes="{ maxlength:35 }" :editFlag="editFlag" :readonlyOption="true"/>

          <StandardInputRow :label="'Reference'" :placeholder="'Deed/Ownership Ref'" v-model="componentData.deed_reference" :inputType="'text'" :attributes="{ maxlength:35 }" :editFlag="editFlag" :readonlyOption="true"/>

          <div class="row field-row" v-if="editFlag || componentData.deed_url">
            <label :class="labelColumnClasses" for="deed-url">Document:</label>
            <div :class="fieldColumnClasses" class="form-buttons">
              <div v-if="componentData.deed_url" id="deed-url" class="no-padding">
                <label v-if="fileToUpload">{{ componentData.deed_url }}</label>
                <div v-else class="in-form-button">
                  <a class="btn bgms-button" type="button" target="_blank" :href="componentData.deed_url">
                    <span>Download</span>
                  </a>
                </div>
              </div>

              <div :style="componentData.deed_url ? {} : {'margin-left': '5px'}">
                <label for="fileUploaderInput" class="form-icon-small">
                  <i v-if="componentData.deed_url" v-show="editFlag && !saving" class="far fa-edit" title="Replace Document"></i>
                  <i v-else class="fa fa-plus" title="Add Document"></i>
                </label>
                <input id="fileUploaderInput" ref="fileUploaderInput" type="file" @change="handleFileUpload()">
                <label v-if="componentData.deed_url"  href="javascript:void(0)" class="form-icon-small" v-show="editFlag && !saving" @click="handleFileDelete()" title="Remove Document" style="padding-left: 4px;">
                  <i class="fa fa-times"></i>
                </label>
              </div>
            </div>
          </div>

          <ImageInputRow :label="'Image 1'" v-model="componentData.image_1" :editFlag="editFlag"/>

          <ImageInputRow :label="'Image 2'" v-model="componentData.image_2" :editFlag="editFlag"/>

          <div v-if="editFlag || componentData.cost_unit || componentData.cost_subunit || componentData.cost_subunit2 || componentData.purchase_date_day || componentData.purchase_date_month || componentData.purchase_date_year || componentData.tenure">
            <h2 v-if="editFlag">Purchase Details</h2>
            <section>
              <div class="row field-row" v-if="editFlag">
                <label :class="labelColumnClasses" for="cost-currency">Currency:</label>
                <div id="cost-currency" :class="fieldColumnClasses">
                  <select :disabled="!editFlag" class="form-control" v-model="componentData.cost_currency">
                    <option v-for="currency in $store.state.ManagementTool.currencyList" :value="currency.id" :key="currency.id">
                      {{ currency.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="row field-row" v-if="editFlag || componentData.cost_unit || componentData.cost_subunit || componentData.cost_subunit2">
                <label :class="labelColumnClasses" for="cost">Cost:</label>
                <div v-if="!editFlag && selectedCurrencyDetail" id="cost" :class="fieldColumnClasses">
                  <input readonly type="text" class="form-control" :value="displayCost">
                </div>
                <div v-if="editFlag && componentData.cost_currency && selectedCurrencyDetail" id="cost" :class="fieldColumnClasses">
                  <div class="multi-input">
                    <span class="multi-input_divider">{{ selectedCurrencyDetail.symbol }}</span>
                    <input type="number" min="0" class="form-control multi-input_input multi-input_input--cost-unit no-spinner" v-model.number="componentData.cost_unit" placeholder="0">
                    <span class="multi-input_divider">{{ selectedCurrencyDetail.subunit2_name ? '-' : '.' }}</span>
                    <input type="number" min="0" max="99" class="form-control multi-input_input multi-input_input--cost-subunit no-spinner" onKeyPress="if(this.value.toString().length==2) return false;" v-model.number="componentData.cost_subunit" placeholder="00">
                    <span class="multi-input_divider multi-input_input--cost-unit">{{ selectedCurrencyDetail.subunit1_symbol }}</span>
                    <span class="multi-input_divider">{{ selectedCurrencyDetail.subunit2_name ? '-' : '' }}</span>
                    <input v-if="selectedCurrencyDetail.subunit2_name" type="number" min="0" max="99" class="form-control multi-input_input multi-input_input--cost-subunit no-spinner" onKeyPress="if(this.value.toString().length==2) return false;" v-model.number="componentData.cost_subunit2" placeholder="00">
                    <span class="multi-input_divider">{{ selectedCurrencyDetail.subunit2_name ? selectedCurrencyDetail.subunit2_symbol : '' }}</span>
                  </div>
                </div>
              </div>
              
              <DateInputRow :label="'Start Date'" :editFlag="editFlag" :day="componentData.purchase_date_day" @day-input="componentData.purchase_date_day=$event" :month="componentData.purchase_date_month" @month-input="componentData.purchase_date_month=$event" :year="componentData.purchase_date_year" @year-input="componentData.purchase_date_year=$event"/>

              <SelectInputRow label="Tenure" v-model="componentData.tenure" :editFlag="editFlag" :options="TENUREOPTIONS" :optionValueName="'id'" :optionKeyName="'id'" :optionLabelName="'label'"/>

              <div class="row field-row" v-if="componentData.tenure === 'FIXED' && (editFlag || componentData.tenure_years)">
                <label :class="labelColumnClasses" for="tenure">Tenure Length:</label>
                <div v-if="!editFlag" id="tenure" :class="fieldColumnClasses">
                  <div class="form-control field-text">{{ componentData.tenure_years + ' Years' }}</div>
                </div>
                <div v-if="editFlag" id="tenure" class="col-xs-5 no-padding">
                  <input type="number" class="form-control" placeholder="Tenure" step='1' min='0' v-model.number="componentData.tenure_years">
                </div>
                <div v-if="editFlag" id="years" class="col-xs-3 no-padding"> Years</div>
              </div>

            </section>
          </div>

          <StandardInputRow :label="'Remarks'" v-model="componentData.remarks" :inputType="'textarea'" :attributes="{ maxlength:400 }" :editFlag="editFlag"/>

          <FormButtons v-if="siteAdminOrSiteWarden" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="false" @toggle-edit="toggleEditCancelButtonsInCreateMode($event, _id, graveManagementPath)"/>

          <section v-if="!editFlag">
            <label class="col-xs-12 control-label">Current owners:</label>
            <table class="table table-condensed">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>From Date</th>
                  <th v-if="siteAdminOrSiteWarden"></th>
                  <th></th>
                </tr>
              </thead>
              <tbody v-if="currentOwnersPresent">
                <tr v-for="owner in componentData.current_grave_owners" :key="owner.id">
                  <td>{{ owner.display_name }}</td>
                  <td>{{ individualDateFieldsToSingleDate(owner.owner_from_date_day, owner.owner_from_date_month, owner.owner_from_date_year) }}</td>
                  <td v-if="siteAdminOrSiteWarden"><a href="" @click="editGraveOwner(owner.id)" title="Grave Owner Information"><i class="fa fa-info"></i></a></td>
                  <td><a href="" @click="goToPersonCompanyManagement(owner.owner_id, owner.owner_type)" :title="'Go to ' + (owner.owner_type ? owner.owner_type.charAt(0).toUpperCase() + owner.owner_type.slice(1).toLowerCase() : 'Person') + ' Management'"><i class="fa fa-arrow-circle-right"></i></a></td>
                </tr>
              </tbody>
              <tbody v-else>
                <tr>
                  <td colspan="4" v-if="loadingDataFlag"><span class="fa fa-spinner fa-spin"></span></td>
                  <td colspan="4" v-else>No current owners recorded.</td>
                </tr>
              </tbody>
            </table>
            <button type="button" class="bgms-button btn" @click="addGraveOwner(false)" v-if="siteAdminOrSiteWarden">{{ currentOwnersPresent ? 'Add Additional Owner' : 'Add Owner' }}</button>
            <button type="button" class="bgms-button btn" @click="addGraveOwner(true)" v-if="siteAdminOrSiteWarden && currentOwnersPresent">Transfer Ownership</button>
          </section>
          
          <section v-if="!editFlag && previousOwnersPresent">
            <label class="col-xs-12 control-label">Past owners:</label>
            <table class="table table-condensed">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>From Date</th>
                  <th v-if="siteAdminOrSiteWarden"></th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="owner in componentData.previous_grave_owners" :key="owner.id">
                  <td>{{ owner.display_name }}</td>
                  <td>{{ individualDateFieldsToSingleDate(owner.owner_from_date_day, owner.owner_from_date_month, owner.owner_from_date_year) }}</td>
                  <td v-if="siteAdminOrSiteWarden"><a href="" @click="editGraveOwner(owner.id)" title="Grave Owner Information"><i class="fa fa-info"></i></a></td>
                  <td><a href="" @click="goToPersonCompanyManagement(owner.owner_id, owner.owner_type)" :title="'Go to ' + (owner.owner_type ? owner.owner_type.charAt(0).toUpperCase() + owner.owner_type.slice(1).toLowerCase() : 'Person') + ' Management'"><i class="fa fa-arrow-circle-right"></i></a></td>
                </tr>
              </tbody>
            </table>
          </section>
        </div>
      </form>
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
import Component, { mixins } from 'vue-class-component';
import { Prop, Watch } from 'vue-property-decorator';
import axios from 'axios';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';
import FeatureTools from '@/mapmanagement/mixins/featureTools';
import constants from '@/global-static/constants.ts';
import { individualDateFieldsToSingleDate } from '@/global-static/dataFormattingAndValidation.ts';
import FormButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/FormButtons.vue';
import StandardInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/StandardInputRow.vue';
import DateInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/DateInputRow.vue';
import ScrollButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ScrollButtons.vue';
import SelectInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/SelectInputRow.vue';

/**
 * Class representing GraveOwnership component
 * @extends mixins: ManagementToolsMixin
 */
@Component({
  components: {
    FormButtons,
    StandardInputRow,
    DateInputRow,
    SelectInputRow,
    ScrollButtons,
    ValidationBox: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/ValidationBox.vue'),
    ImageInputRow: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/ImageInputRow.vue'),
  }
})
export default class GraveOwnership extends mixins(ManagementToolsMixin, FeatureTools){
  
  individualDateFieldsToSingleDate = individualDateFieldsToSingleDate;

  @Prop() deedID;

  saving: boolean = false;

  fileToUpload = null;

  graveManagementChildRoutesEnum = constants.GRAVE_MANAGEMENT_CHILD_ROUTES;
  graveManagementPath = constants.GRAVE_MANAGEMENT_PATH;

  TENUREOPTIONS = [
    { id: 'PERPETUAL', label: 'Perpetual' },
    { id: 'FIXED', label: 'Fixed' }
  ]

  /**
   * Vue mounted lifecycle hook
   * - Loads currencies if not already loaded
   */
  mounted() {
    this.componentName = "grave_deed";

    this.editableFields = ['cost_currency', 'cost_unit', 'cost_subunit', 'cost_subunit2', 'purchase_date_day', 'purchase_date_month', 'purchase_date_year', 'tenure', 'tenure_years', 'remarks', 'deed_reference', 'deed_url', 'image_1', 'image_2', 'ownership_register'];

    this.initData();

    // if lists have not yet been loaded into vuex, load them
    if (!this.$store.state.ManagementTool.currencyList) {

      axios.get('/mapmanagement/allOwnershipOptions')
      .then(response => {
        this.$store.commit('setOwnershipLists', response.data);
      })
      .catch(function(response) {
        console.warn('Couldn\'t get ownership lists (currency):', response.response.data);
      });
    }
  }

  /**
   * Get data from server
   */
  initData() {

    if (this.deedID) {
      this._id = this.deedID;
      this.editFlag = this.$route.query.edit==='true';
    }
    else {
      this._id = '';
      this.editFlag = true;
    }

    // load data
    this.loadData('/mapmanagement/graveDeed/?deed_id=', this._id);
  }

  /*** Computed ***/

  /**
   * Computed property:
   * @returns {boolean} Details about the selected currency
   */
  get selectedCurrencyDetail() {
    if (this.$store.state.ManagementTool.currencyList) {
      return this.$store.state.ManagementTool.currencyList.find(currency =>
      currency.id === this.componentData.cost_currency
      );
    }

    return undefined;
  }

  /**
   * @returns cost as a formatted string
   */
  get displayCost() {
    let delimiter = this.selectedCurrencyDetail.subunit2_name ? '-' : '.';

    let returnCost = this.selectedCurrencyDetail.symbol + (this.componentData.cost_unit ? this.componentData.cost_unit : 0);

    if (this.componentData.cost_subunit) {
      // add leading 0 if required
      let subunit = (this.componentData.cost_subunit.toString().length === 1 ? '0' : '') + this.componentData.cost_subunit;
      returnCost += delimiter + subunit;
    }

    // e.g. post decimalisation
    if (this.selectedCurrencyDetail.subunit2_name) {
      if (!this.componentData.cost_subunit)
        returnCost += delimiter + '00';
      
      if (!this.componentData.cost_subunit2)
        returnCost += delimiter + '00';
      else {
        // add leading 0 if required
        let subunit2 = (this.componentData.cost_subunit2.toString().length === 1 ? '0' : '') + this.componentData.cost_subunit2;
        returnCost += delimiter + subunit2;
      }
    }

    return returnCost;
  }

  get currentOwnersPresent() :boolean {
    return this.componentData && this.componentData.current_grave_owners && this.componentData.current_grave_owners.length > 0;
  }

  get previousOwnersPresent() :boolean {
    return this.componentData && this.componentData.previous_grave_owners && this.componentData.previous_grave_owners.length > 0;
  }

  /*** Watchers ***/

  /**
   * Watcher: When editFlag is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('editFlag')
  onEditFlagChanged(val: any, oldVal: any) {
    this.fileToUpload = null;
  }

  /**
   * Watcher: When list of owners needs refreshed is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('$route.query.refreshowners')
  onRefreshChanged(val: any, oldVal: any) {
    if (val) {
      // refreshes the owner data
      this.loadData('/mapmanagement/graveDeed/?deed_id=', this._id);
    }

    // remove refresh in query
    this.appendToOrModifyItemInQuery('refreshowners', null);
  }

  /**
   * Watcher: When deedID is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('$route.params.deedID')
  onDeedIDChanged(val: any, oldVal: any) {
    if (this._id !== val)
      this.initData();
  }

  /**
   * Watcher: When $route.query.refreshOwnership is changed
   * Refreshes to show updated data.
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('$route.query.refreshOwnership')
  onRefreshOwnership(val: any, oldVal: any) {
    if (val) {
      this.initData();

      // removes refresh in query
      this.appendToOrModifyItemInQuery('refreshOwnership', null);
    }
  }

  /*** Methods ***/

  /**
   * Validates data. Displays message if errors present.
   * @returns true if validation passes
   */
  validateData(): boolean {
    let errors = [];
    let returnValue = true;

    if (!this.componentData.purchase_date_day)
      errors.push("A start date day value is required.");
    if (!this.componentData.purchase_date_month)
      errors.push("A start date month value is required.");
    if (!this.componentData.purchase_date_year)
      errors.push("A start date year value is required.");

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

    // if a cost is included, make uncompleted cost fields 0
    if (this.componentData.cost_unit || this.componentData.cost_subunit || (this.selectedCurrencyDetail && this.selectedCurrencyDetail.subunit2_name && this.componentData.cost_subunit2)) {
      if (!this.componentData.cost_unit)
        this.componentData.cost_unit = '00';
        
      if (!this.componentData.cost_subunit)
        this.componentData.cost_subunit = '00';
        
      if (this.selectedCurrencyDetail && this.selectedCurrencyDetail.subunit2_name && !this.componentData.cost_subunit2)
        this.componentData.cost_subunit2 = '00';
    }

    // if currency has been changed to decimal, make sure subunit2_name is undefined
    if (this.selectedCurrencyDetail && !this.selectedCurrencyDetail.subunit2_name && this.componentData.cost_subunit2)
      this.componentData.cost_subunit2 = undefined;
    
    // if tenure is perpetual, make sure years is null
    if (this.componentData.tenure === 'PERPETUAL')
      this.componentData.tenure_years = null;

    let data = this.getChangedData();

    // If a cost value has changed, include the currency in this save.
    // The Currency may have been set by default and isn't actually saved in db.
    if ((data.hasOwnProperty('cost_unit') || data.hasOwnProperty('cost_subunit') || data.hasOwnProperty('cost_subunit2')) && data.hasOwnProperty('cost_currency'))
      data['cost_currency'] = this.componentData['cost_currency'];

    if (this.fileToUpload)
      data['deed_url'] = this.fileToUpload;
    
    // if image has changed, include original's id, if it exists, so we know what to remove from db
    if (data.hasOwnProperty('image_1')) {
      const original = this.componentDataSaved['image_1'];

      if (original) {
        if (!data['image_1'])
          data['image_1'] = {};

        data['image_1']['original_id'] = original.id;
      }

      data['image_1'] = JSON.stringify(data['image_1']);
    }
    if (data.hasOwnProperty('image_2')) {
      const original = this.componentDataSaved['image_2'];

      if (original) {
        if (!data['image_2'])
          data['image_2'] = {};

        data['image_2']['original_id'] = original.id;
      }

      data['image_2'] = JSON.stringify(data['image_2']);
    }

    // put data in FormData. This is needed for file upload.
    let formData = new FormData();

    for ( var key in data ) {
      formData.append(key, data[key]);
    }

    if (this._id) {
      axios.patch('/mapmanagement/graveDeed/', formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        if (this.fileToUpload) {
          this.componentData.deed_url = response.data.deed_url;
          this.fileToUpload = null;
        }

        // updated saved version
        this.updateSavedVersion();
        this.saving = false;
        this.notificationHelper.createSuccessNotification('Grave ownership saved successfully');
        
        // refresh list of ownerships
        this.appendToOrModifyItemInQuery('refresh', 'true')

        window.setTimeout(() => {
          this.appendToOrModifyItemInQuery('edit', null);
        })
      })
      .catch(response => {
        this.saving = false;

        if (response.response.data.deed_reference_taken) {
          this.notificationHelper.createErrorNotification("Deed reference already in use");
        }
        else {
          console.warn('Couldn\'t save grave details:', response.response.data);
          this.notificationHelper.createErrorNotification("Couldn't save grave ownership");
        }
      });
    }
    else {
      formData.append('graveplot_id', this.$route.params.id);

      // new record
      axios.post('/mapmanagement/graveDeed/', formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        if (this.fileToUpload) {
          this.componentData.deed_url = response.data.deed_url;
          this.fileToUpload = null;
        }

        // updated saved version
        this.updateSavedVersion();

        this._id = response.data.id;

        let currentLayer = this.$route.params.layer;

        if(currentLayer==='available_plot') {
          currentLayer = 'reserved_plot';
          // change current available_plot to a reserved_plot as it is now owned
          this.changeFeatureLayer('available_plot', currentLayer, this.$route.params.ownershipavailablePlotID, this.$route.params.id)
          .then(() => {
            this.$router.replace({ name: this.graveManagementChildRoutesEnum.graveOwnership, params: { deedID: this._id, layer: currentLayer }, query: { refresh: 'true' }});
          });
        }
        else
          this.$router.replace({ name: this.graveManagementChildRoutesEnum.graveOwnership, params: { deedID: this._id }, query: { refresh: 'true' }});

        this.saving = false;
        this.notificationHelper.createSuccessNotification('Grave ownership created successfully');
      })
      .catch(response => {
        this.saving = false;

        if (response.response.data.deed_reference_taken) {
          this.notificationHelper.createErrorNotification("Deed reference already in use");
        }
        else {
          console.warn('Couldn\'t save grave details:', response.response.data);
          this.notificationHelper.createErrorNotification("Couldn't create grave ownership");
        }
      });
    }
  }

  handleFileUpload() {
    const file = (this.$refs.fileUploaderInput as any).files[0];
    this.componentData.deed_url = file.name;
    this.fileToUpload = file;
  }

  handleFileDelete() {
    let v = this;
    // this stops the file input being invoked when trying to delete
    window.setTimeout(() => {
      v.fileToUpload = null;
      v.componentData.deed_url = null;
    });
  }

  editGraveOwner(id) {
    this.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.graveowner, params: { deedID: this._id, ownerID: id, startDay: this.componentData.purchase_date_day, startMonth: this.componentData.purchase_date_month, startYear: this.componentData.purchase_date_year }});
  }

  /**
   * Add a person or company as an owner
   */
  addGraveOwner(transfer) {
    let params = { deedID: this._id, transfer: transfer, startDay: this.componentData.purchase_date_day, startMonth: this.componentData.purchase_date_month, startYear: this.componentData.purchase_date_year };

    if (!this.currentOwnersPresent && !this.previousOwnersPresent)
      params['firstOwner'] = 'true';

    this.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.newGraveOwner, params: params})
  }

  goToPersonCompanyManagement(ownerID, ownerType) {
    if (ownerType==='person')
      this.$router.replace({ name: constants.PERSON_MANAGEMENT_CHILD_ROUTES.persondetails, params: { id: ownerID }});
    else
      this.$router.replace({ name: constants.COMPANY_MANAGEMENT_CHILD_ROUTES.companydetails, params: { id: ownerID }});
  }
}
</script>
