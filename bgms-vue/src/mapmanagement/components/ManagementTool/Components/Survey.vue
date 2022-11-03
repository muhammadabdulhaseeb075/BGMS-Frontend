<template>
  <div :id="componentName" v-if="componentData">
    <ScrollButtons :heightChangedFlag="heightChangedFlag">

      <ValidationBox v-if="componentData" :errors="componentData.errors"/>

      <form class="form-horizontal form-box-inside management-tool-form" @submit.prevent="onSubmit">

        <FormButtons v-if="siteAdminOrSiteWarden" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="true" @toggle-edit="toggleEditCancelButtonsInCreateMode($event, surveyID, managementToolRoute);"/>
      
        <div v-if="!surveyID">
          <select @change="templateSelected($event)" v-model="selectedTemplateInSelect">
            <option v-for="template in surveyTemplates" :value="template.survey_template_id" :key="template.survey_template_id">
              {{ template.name }}
            </option>
          </select>
        </div>
        <div v-else>
          <h2 style="margin-top:0px;">{{ componentData.name }}</h2>
        </div>

        <div v-for="field in componentData.fields" :key="field.label">

          <SelectInputRow v-if="field.field_name==='select'" :label="field.label" v-model="field.value" :editFlag="editFlag" :options="field.select_options" :allowNull="true"/>
          
          <StandardInputRow v-else-if="field.field_name==='boolean'" :label="field.label" v-model="field.value" :inputType="'checkbox'" :readonlyOption="true" :editFlag="editFlag"/>
          
          <StandardInputRow v-else-if="field.field_name==='char'" :label="field.label" v-model="field.value" :inputType="'text'" :attributes="{ maxlength:255 }" :readonlyOption="true" :editFlag="editFlag"/>

          <DateInputRow v-else-if="field.field_name==='date'" :label="field.label" :editFlag="editFlag" :day="field.day" @day-input="field.day=$event; field.value=dateFieldsToStringForSaving(field)" :month="field.month" @month-input="field.month=$event; field.value=dateFieldsToStringForSaving(field)" :year="field.year" @year-input="field.year=$event; field.value=dateFieldsToStringForSaving(field)"/>

          <StandardInputRow v-else-if="field.field_name==='float'" :label="field.label" :editFlag="editFlag" :readonlyOption="true" v-model.number="field.value" :inputType="'number'" :attributes="{ step:0.01 }"/>

          <StandardInputRow v-else-if="field.field_name==='integer'" :label="field.label" :editFlag="editFlag" :readonlyOption="true" v-model.number="field.value" :inputType="'number'" :attributes="{ step:1 }"/>

          <StandardInputRow v-else-if="field.field_name==='textarea'" :label="field.label" v-model="field.value" :inputType="'textarea'" :attributes="{ maxlength:400 }" :editFlag="editFlag"/>

          <ImageInputRow v-else-if="field.field_name==='image'" :label="field.label" v-model="field.value" :editFlag="editFlag"/>

        </div>
      </form>
      <button v-if="siteAdminOrSiteWarden && surveyID" v-show="!editFlag" type="button" class="bgms-button btn" @click="deleteSurvey()">Delete Survey</button>
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
import { Prop, Watch } from 'vue-property-decorator';
import axios from 'axios';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';
import FeatureTools from '@/mapmanagement/mixins/featureTools';
import FormButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/FormButtons.vue';
import StandardInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/StandardInputRow.vue';
import ScrollButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ScrollButtons.vue';
import constants from '@/global-static/constants.ts';
import { dateFieldsToStringForSaving } from '@/global-static/dataFormattingAndValidation.ts';

/**
 * Class representing Survey component
 * @extends mixins: ManagementToolsMixin
 */
@Component({
  components: {
    FormButtons,
    StandardInputRow,
    DateInputRow: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/DateInputRow.vue'),
    ImageInputRow: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/ImageInputRow.vue'),
    ValidationBox: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/ValidationBox.vue'),
    SelectInputRow: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/SelectInputRow.vue'),
    ScrollButtons
  }
})
export default class Survey extends mixins(ManagementToolsMixin, FeatureTools){

  dateFieldsToStringForSaving = dateFieldsToStringForSaving;

  @Prop() id;
  @Prop() availablePlotID;
  @Prop() layer;
  @Prop() surveyID;

  featureID = null; // this is not feature_id! It is the id from feature model

  saving: boolean = false;

  selectedTemplate = null;
  selectedTemplateInSelect = null;
  surveyTemplates = null;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    this.componentName = "surveys";
    this._id = this.id;
    
    this.editableFields = ['fields'];

    this.initData();
  }

  /*** Computed ***/

  /**
   * @returns {string} The name of the management tool this component belongs to
   */
  get managementToolRoute(): string {
    if (this.isRouteActive(constants.MEMORIAL_MANAGEMENT_PATH))
      return constants.MEMORIAL_MANAGEMENT_PATH;
    else if (this.isRouteActive(constants.GRAVE_MANAGEMENT_PATH))
      return constants.GRAVE_MANAGEMENT_PATH;
    else if (this.isRouteActive(constants.FEATURE_MANAGEMENT_PATH))
      return constants.FEATURE_MANAGEMENT_PATH;
    else
      return null;
  }

  /*** Watchers ***/

  /**
   * Watcher: When surveyID is changed, reload the survey
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('surveyID')
  onSurveyIDChanged(val: any, oldVal: any) {
    this.initData();
  }

  /*** Methods ***/

  /**
   * Loads data needed for this survey/new survey
   */
  initData() {
    // if this is a new survey
    if (!this.surveyID) {

      this.editFlag = true;
      
      //retrieve list of available survey templates
      if (!this.surveyTemplates) {
        this.loadDataWithoutStoring('/survey/layerSurveyTemplates/?layer=', this.layer)
        .then(response => {
          this.surveyTemplates = response;

          if (this.surveyTemplates[0])
            this.selectNewTemplate(this.surveyTemplates[0].survey_template_id);
        });
      }
      else if (this.surveyTemplates[0]) {
        this.selectNewTemplate(this.surveyTemplates[0].survey_template_id);
      }

      // if this is a memorial or grave, we need to find the feature id, i.e. not memorial id or graveplot id
      if (this.managementToolRoute===constants.MEMORIAL_MANAGEMENT_PATH || this.managementToolRoute===constants.GRAVE_MANAGEMENT_PATH) {

        if (this.layer==="available_plot" && this.availablePlotID)
          // we already know the topopolygon id (same as feature id) for available plots
          this.featureID = this.availablePlotID;
        else {
          this.getMemorialPlotFeatureID(this.layer, this.id)
          .then(featureID => {
            this.featureID = featureID;
          });
        }
      }
      else
        this.featureID = this.id;
    }
    else {
      this.editFlag = false;
      this.loadData('/survey/?survey_id=', this.surveyID);
    }
  }

  /**
   * Validates data. Displays message if errors present.
   * @returns true if validation passes
   */
  validateData(): boolean {
    let errors = [];
    let returnValue = true;

    // Either a whole date or no date. Survey Date is compulsory.
    this.componentData.fields.forEach(field => {
      if (field.field_type === 'date' && !field.value && (field.label==='Survey Date' || (field.day || field.month || field.year))) {
        if (!field.day)
          errors.push(`A day value is required for ${field.label}.`);
        if (!field.month)
          errors.push(`A month value is required for ${field.label}.`);
        if (!field.year)
          errors.push(`A year value is required for ${field.label}.`);
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
   * Saves an edit or creates a new survey
   */
  onSubmit() {

    if (!this.validateData()) { return; }

    this.saving = true;

    let data = this.getChangedSurveyData();

    // method depends on whether this is a new or existing survey
    const httpMethod = this.surveyID ? 'patch' : 'post';

    axios({
      method: httpMethod,
      url: '/survey/',
      data: data
    })
      .then(response => {
        // updated saved version
        this.updateSavedVersion();
        this.appendToOrModifyItemInQuery('edit', null);
        this.saving = false;
        this.notificationHelper.createSuccessNotification('Survey saved successfully');

        if (!this.surveyID) {
          this.$router.replace({ name: this.$route.name, params: { 'surveyID': response.data.survey_id }, query: { refresh: 'true' }});
        }
      })
      .catch(response => {
        this.saving = false;
        console.warn('Couldn\'t save survey:', response.response ? response.response.data : response.message);
        this.notificationHelper.createErrorNotification("Couldn't save survey");
      });
  }

  /**
   * Checks each field to find if it has changed. If it has, add it to data object.
   */
  getChangedSurveyData() {
    
    let data = { 
      feature_id: this.featureID, // only needed for new surveys
      survey_template_id: this.selectedTemplate,
      fields: [] };

    // include modified fields
    for (let i in this.componentData.fields) {
      // make undefined numbers null
      if ((this.componentData.fields[i].field_type==='integer' || this.componentData.fields[i].field_type==='float') && !this.componentData.fields[i].value)
        this.componentData.fields[i].value = null;

      if (this.componentData.fields[i].value !== this.componentDataSaved.fields[i].value)
        data.fields.push(this.componentData.fields[i]);
    }

    return data;
  }

  /**
   * Called when a template is selected in select input.
   */
  templateSelected(event) {
    if (this.fieldChanged) {
      // ask for user's confirmation if form contains data
      this.notificationHelper.createConfirmation('Change Survey Template', 'This will overwrite existing data. Do you want to continue?', 
      () => {
        this.selectNewTemplate(event.target.value);
      }, 
      () => {
        // revert select value
        this.selectedTemplateInSelect = this.selectedTemplate;
      });
    }
    else
      this.selectNewTemplate(event.target.value);
  }

  /**
   * Selects a new template and updates fields to match
   */
  selectNewTemplate(selectedTemplate) {
    this.selectedTemplate = selectedTemplate;
    this.selectedTemplateInSelect = selectedTemplate;

    let fields = this.surveyTemplates.find(template => 
        template.survey_template_id === this.selectedTemplate
      ).fields;
  
    this.storeData({ fields: JSON.parse(JSON.stringify(fields)) });

    // Survey Date defaults to today
    this.componentData.fields.forEach(field => {
      if (field.field_type === 'date' && field.label==='Survey Date') {
        const today = new Date();
        field.day = today.getDate();
        field.month = today.getMonth() + 1;
        field.year = today.getFullYear();
        field.value = dateFieldsToStringForSaving(field);
      }
    });
  }

  /**
   * Delete a survey
   */
  deleteSurvey() {
    // ask for user's confirmation
    this.notificationHelper.createConfirmation('Delete Survey', 'Are you sure you want to delete this survey?', 
    () => {
      this.saving = true;

      axios.delete('/survey/?survey_id=' + this.surveyID)
      .then(() => {
        this.saving = false;
        this.notificationHelper.createSuccessNotification('Survey deleted successfully');

        this.$router.replace({ name: this.managementToolRoute, query: { refresh: 'true' } });
      })
      .catch(response => {
        this.saving = false;
        console.warn('Couldn\'t save survey:', response.response ? response.response.data : response.message);
        this.notificationHelper.createErrorNotification("Couldn't delete survey");
      });
    });
  }
}
</script>
