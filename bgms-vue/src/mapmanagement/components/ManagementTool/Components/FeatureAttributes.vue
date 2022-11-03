<template>
  <div :id="componentName" v-if="componentData">
    <ScrollButtons :heightChangedFlag="heightChangedFlag">

      <ValidationBox :errors="componentData.errors"/>

      <form class="form-horizontal form-box-inside management-tool-form" @submit.prevent="onSubmit">

        <div class="blank-form-placeholder" v-if="!(componentData.attributes && componentData.attributes.length>0)">No attributes are linked to this feature type.</div>
        <div v-else>

          <FormButtons v-if="siteAdminOrSiteWarden" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="true" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)"/>
        
          <div class="blank-form-placeholder" v-if="!(editFlag || attributesRecorded)">No attributes recorded.</div>

          <div v-for="attribute in componentData.attributes" :key="attribute.feature_attribute_id">

            <SelectInputRow v-if="attribute.field_name==='select'" :label="attribute.label" v-model="attribute.value" :editFlag="editFlag" :options="attribute.select_options" :allowNull="true"/>
            
            <StandardInputRow v-else-if="attribute.field_name==='boolean'" :label="attribute.label" v-model="attribute.value" :inputType="'checkbox'" :readonlyOption="true" :editFlag="editFlag"/>
            
            <StandardInputRow v-else-if="attribute.field_name==='char'" :label="attribute.label" v-model="attribute.value" :inputType="'text'" :attributes="{ maxlength:255 }" :readonlyOption="true" :editFlag="editFlag"/>

            <DateInputRow v-else-if="attribute.field_name==='date'" :label="attribute.label" :editFlag="editFlag" :day="attribute.day" @day-input="attribute.day=$event; attribute.value=dateFieldsToStringForSaving(attribute)" :month="attribute.month" @month-input="attribute.month=$event; attribute.value=dateFieldsToStringForSaving(attribute)" :year="attribute.year" @year-input="attribute.year=$event; attribute.value=dateFieldsToStringForSaving(attribute)"/>

            <StandardInputRow v-else-if="attribute.field_name==='float'" :label="attribute.label" :editFlag="editFlag" :readonlyOption="true" v-model.number="attribute.value" :inputType="'number'" :attributes="{ step:0.01 }"/>

            <StandardInputRow v-else-if="attribute.field_name==='integer'" :label="attribute.label" :editFlag="editFlag" :readonlyOption="true" v-model.number="attribute.value" :inputType="'number'" :attributes="{ step:1 }"/>

            <StandardInputRow v-else-if="attribute.field_name==='textarea'" :label="attribute.label" v-model="attribute.value" :inputType="'textarea'" :attributes="{ maxlength:400 }" :editFlag="editFlag"/>

          </div>

        </div>
      </form>
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
import ScrollButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ScrollButtons.vue';
import constants from '@/global-static/constants.ts';
import { dateFieldsToStringForSaving } from '@/global-static/dataFormattingAndValidation.ts';

/**
 * Class representing FeatureAttributes component
 * @extends mixins: ManagementToolsMixin
 */
@Component({
  components: {
    FormButtons,
    StandardInputRow,
    DateInputRow: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/DateInputRow.vue'),
    ValidationBox: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/ValidationBox.vue'),
    SelectInputRow: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/SelectInputRow.vue'),
    ScrollButtons
  }
})
export default class FeatureAttributes extends mixins(ManagementToolsMixin){

  dateFieldsToStringForSaving = dateFieldsToStringForSaving;

  @Prop() id;

  saving: boolean = false;

  iDName: string = null;

  /**
   * Vue mounted lifecycle hook
   * - Loads option for select boxes
   */
  mounted() {
    let v = this;

    v.componentName = "feature_attributes";
    v._id = v.id;
    
    v.editableFields = ['attributes'];

    if (v.isRouteActive(constants.MEMORIAL_MANAGEMENT_PATH))
      v.iDName = "memorial_id";
    else if (v.isRouteActive(constants.GRAVE_MANAGEMENT_PATH))
      v.iDName = "graveplot_id";
    else
      v.iDName = "feature_id";

    // load data
    v.loadData(`/mapmanagement/featureAttributes/?${v.iDName}=`, v._id);
  }

  /*** Computed ***/
  
  /**
   * @returns {boolean} true if at least one attribute has data recorded
   */
  get attributesRecorded(): boolean {
    if (this.componentData.attributes && this.componentData.attributes.length>0) {
      for (let attribute of this.componentData.attributes) {
        if (attribute.value)
          return true;
      }
    }

    return false;
  }

  /*** Methods ***/

  /**
   * Validates data. Displays message if errors present.
   * @returns true if validation passes
   */
  validateData(): boolean {
    let errors = [];
    let returnValue = true;

    // either a whole date or no date
    this.componentData.attributes.forEach(attribute => {
      if (attribute.field_name === 'date' && !attribute.value && (attribute.day || attribute.month || attribute.year)) {
        if (!attribute.day)
          errors.push(`A day value is required for ${attribute.label}.`);
        if (!attribute.month)
          errors.push(`A month value is required for ${attribute.label}.`);
        if (!attribute.year)
          errors.push(`A year value is required for ${attribute.label}.`);
      }
    });

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

    let v = this;

    if (!v.validateData()) { return; }

    v.saving = true;

    let data = this.getChangedAttributeData();

    axios.patch('/mapmanagement/featureAttributes/', data)
      .then(function(response) {
        // updated saved version
        v.updateSavedVersion();
        v.appendToOrModifyItemInQuery('edit', null);
        v.saving = false;
        v.notificationHelper.createSuccessNotification('Attributes saved successfully');
      })
      .catch(function(response) {
        v.saving = false;
        console.warn('Couldn\'t save attributes:', response.response ? response.response.data : response.message);
        v.notificationHelper.createErrorNotification("Couldn't save attributes");
      });
  }

  /**
   * Checks each attribute to find if it has changed. If it has, add it to data object.
   */
  getChangedAttributeData() {
    
    let data = { attributes: [] };
    data[this.iDName] = this._id;

    // include modified attributes
    for (let i in this.componentData.attributes) {
      // make undefined numbers null
      if ((this.componentData.attributes[i].type==='integer' || this.componentData.attributes[i].type==='float') && !this.componentData.attributes[i].value)
        this.componentData.attributes[i].value = null;

      if (this.componentData.attributes[i].value !== this.componentDataSaved.attributes[i].value)
        data.attributes.push(this.componentData.attributes[i]);
    }

    return data;
  }
}
</script>
