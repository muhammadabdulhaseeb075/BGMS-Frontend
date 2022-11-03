<template>
  <div id="burialDetailsComponent" v-if="componentData">
    <ScrollButtons :heightChangedFlag="heightChangedFlag">
      <p class="validation-box" v-if="noBurialFlag && !editFlag">
        <b>This person does not have a burial record.</b>
        <button class="bgms-button btn" @click="appendToOrModifyItemInQuery('edit', true)" v-if="siteAdminOrSiteWarden">Add Burial Record</button>
      </p>
      <form class="form-horizontal form-box-inside management-tool-form" @submit.prevent="onSubmit" v-else>

        <FormButtons v-if="siteAdminOrSiteWarden && !createMode" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="true" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)"/>
        <div v-else-if="createMode && fieldChanged"/>
        
        <section>

          <ImageInputRow :label="'Burial Record Image'" v-model="componentData.burial_record_image" :editFlag="editFlag"/>

          <StandardInputRow :label="'Transcribed Grave No.'" v-show="!editFlag" v-model="componentData.transcribed_grave_number" :inputType="'text'" :readonlyOption="true" :editFlag="false"/>

          <div v-if="componentData.register" class="row field-row">
            <label for="register" class="col-xs-4 control-label">Register:</label>
            <div id="register" class="col-xs-8 no-padding">
              <input readonly="readonly" type="text" placeholder="Register" class="form-control" :value="componentData.register">
            </div>
          </div>      

          <StandardInputRow :label="'Burial No.'" v-model="componentData.burial_number" :inputType="'text'" :attributes="{ maxlength:10 }" :readonlyOption="true" :editFlag="editFlag" :placeholder="'Burial Number'"/>

          <DateInputRow :label="'Date of Burial'" :editFlag="editFlag" :day="componentData.impossible_date_day" @day-input="componentData.impossible_date_day=$event" :month="componentData.impossible_date_month" @month-input="componentData.impossible_date_month=$event" :year="componentData.impossible_date_year" @year-input="componentData.impossible_date_year=$event"/>
          
          <StandardInputRow :label="'Interred'" v-model="componentData.interred" :inputType="'checkbox'" :readonlyOption="true" :editFlag="editFlag"/>
          <StandardInputRow :label="'Consecrated'" v-model="componentData.consecrated" :inputType="'checkbox'" :readonlyOption="true" :editFlag="editFlag"/>
          <StandardInputRow :label="'Requires Investigation'" v-model="componentData.requires_investigation" :inputType="'checkbox'" :readonlyOption="true" :editFlag="editFlag"/>

        </section>
        <div v-if="editFlag || componentData.cremated || componentData.impossible_cremation_date_day || componentData.impossible_cremation_date_month || componentData.impossible_cremation_date_year || componentData.cremation_certificate_no">
          <h2 class="flag-min-height" v-if="editFlag"></h2>
          <section>

            <StandardInputRow :label="'Cremated'" v-model="componentData.cremated" :inputType="'checkbox'" :readonlyOption="true" :editFlag="editFlag"/>

            <!-- only show if cremated is null or true -->
            <div class="row field-row input_form_spaces" v-if="(editFlag && componentData.cremated !== false) || componentData.impossible_cremation_date_day || componentData.impossible_cremation_date_month || componentData.impossible_cremation_date_year">
              <label :class="labelColumnClasses" for="cremation-date">Date of Cremation:</label>
              <div v-if="!editFlag" id="cremation-date" :class="fieldColumnClasses">
                <input readonly type="text" class="form-control" :value="individualDateFieldsToSingleDate(componentData.impossible_cremation_date_day, componentData.impossible_cremation_date_month, componentData.impossible_cremation_date_year)">
              </div>
              <div v-if="editFlag" id="cremation-date" :class="fieldColumnClasses">
                <div class="multi-input">
                  <input class="form-control multi-input_input multi-input_input--day no-spinner" type="number" step="1" min="0" max="31" placeholder="dd" v-model.number="componentData.impossible_cremation_date_day" onKeyPress="if(this.value.toString().length==2) return false;">
                  <span class="multi-input_divider">/</span>
                  <input class="form-control multi-input_input multi-input_input--month no-spinner" type="number" step="1" min="0" max="12" placeholder="mm" v-model.number="componentData.impossible_cremation_date_month" onKeyPress="if(this.value.toString().length==2) return false;">
                  <span class="multi-input_divider">/</span>
                  <input class="form-control multi-input_input multi-input_input--year no-spinner" type="number" step="1" min="0" :max="(new Date()).getFullYear()" placeholder="yyyy" v-model.number="componentData.impossible_cremation_date_year" onKeyPress="if(this.value.length==4) return false;">
                </div>
              </div>
            </div>
            
            <!-- only show if cremated is null or true -->
            <div class="input_form_spaces">
              <StandardInputRow v-if="(editFlag && componentData.cremated !== false) || componentData.cremation_certificate_no" :label="'Certificate'" v-model="componentData.cremation_certificate_no" :inputType="'text'" :attributes="{ maxlength:35 }" :readonlyOption="true" :editFlag="editFlag" :placeholder="'Certificate No.'"/>
            </div>

          </section>
        </div>

        <StandardInputRow :label="'Coffin height'" v-model="componentData.coffin_height" :inputType="'number'" :attributes="{ maxlength:10 }" :readonlyOption="true" :editFlag="editFlag" :placeholder="'Coffin height'"/>
        <StandardInputRow :label="'Coffin width'" v-model="componentData.coffin_width" :inputType="'number'" :attributes="{ maxlength:10 }" :readonlyOption="true" :editFlag="editFlag" :placeholder="'Coffin width'"/>

        <StandardInputRow
            v-for=" field in componentData.form_fields" :key="field.name"
            :label="field.name" v-model="componentData[field.content]" :inputType="field.type"
            :attributes="{ maxlength:10 }" :readonlyOption="true" :editFlag="editFlag"
            :options_select="select_fields(field.options)"
            :placeholder="field.name"/>

        <StandardInputRow :label="'Burial Remarks'" v-model="componentData.burial_remarks" :inputType="'textarea'" :attributes="{ maxlength:200 }" :editFlag="editFlag"/>
        <StandardInputRow :label="'User Remarks'" v-model="componentData.user_remarks" :inputType="'textarea'" :attributes="{ maxlength:200 }" :editFlag="editFlag"/>

        <div v-if="this.$store.state.ManagementTool.burialOfficialList && (editFlag || (componentData.burial_officials && componentData.burial_officials.length > 0))">
          <h2 class="flag-min-height" v-if="editFlag">Burial Official</h2>
          <section class="row no-margin">
            <label v-show="!editFlag" class="col-xs-12 control-label">Burial Officials:</label>
            <table v-show="!editFlag" class="table table-condensed">
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Name</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="official in componentData.burial_officials" :key="official.official_id">
                  <td>{{ getOfficialType(official.burial_official_type_id) }}</td>
                  <td>{{ getJoinedText([official.official_title, official.official_first_names, official.official_last_name], ' ') }}</td>
                </tr>
              </tbody>
            </table>
            <div id="burial-official-select" v-if="editFlag">
              <div id="burial-official" class="col-xs-12 no-padding">
                <multiselect :disabled="!editFlag" :value='componentData.burial_officials' label='label' :options="sortedBurialOfficialList" :multiple="true" :close-on-select="true" @select="addOfficial" @remove="removeOfficial" group-values="list" group-label="group" :group-select="false" :internal-search="false" @search-change="burialOfficialsSearch" :hide-selected="true"></multiselect>
              </div>
            </div>
            <carousel id="burial-official-carousel" :per-page="1" navigationEnabled loop paginationColor="#a5a5a5" paginationActiveColor="#41b883" class="col-xs-12" v-if="editFlag && componentData.burial_officials.length > 0">
              <slide :class="[{ active: index===0}, 'item']" v-for="(official, index) in componentData.burial_officials" :key="official.official_id">
                <div class="row field-row-carousel">
                  <label class="control-label col-xs-3" for="official-title">Name:</label>
                  <div id="official-title" class="col-xs-9 no-padding">
                    <div class="form-control field-text">{{ getJoinedText([official.official_title, official.official_first_names, official.official_last_name], ' ') }}</div>
                  </div>
                </div>
                <div class="row field-row-carousel" v-if="editFlag || official.burial_official_type_id">
                  <label class="control-label col-xs-3" for="type">Type:</label>
                  <div id="type" class="col-xs-9 no-padding" style="padding-right: 1px!important;">
                    <select :readonly="!editFlag" :disabled="!editFlag" class="form-control" v-model="official.burial_official_type_id">
                      <option v-for="type in $store.state.ManagementTool.burialOfficialType" :value="type.id" :key="type.id">
                        {{ type.official_type }}
                      </option>
                    </select>
                  </div>
                </div>
              </slide>
            </carousel>
          </section>
        </div>
        <FormButtons v-if="siteAdminOrSiteWarden && !createMode" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="false" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)"/>
        
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
import Multiselect from 'vue-multiselect'
import { Carousel, Slide } from 'vue-carousel';
import Component, { mixins } from 'vue-class-component'
import { Watch, Prop } from 'vue-property-decorator';
import axios from 'axios'
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin.ts';
import FormButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/FormButtons.vue';
import StandardInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/StandardInputRow.vue';
import DateInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/DateInputRow.vue';
import ImageInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ImageInputRow.vue';
import ScrollButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ScrollButtons.vue';
import constants from '@/global-static/constants.ts';
import { messages } from '@/global-static/messages.js';
import { individualDateFieldsToSingleDate } from '@/global-static/dataFormattingAndValidation.ts';

/**
 * Class representing BurialDetails component
 * @extends mixins: ManagementToolsMixin
 */
@Component({
  components: {
    Multiselect,
    Carousel,
    Slide,
    FormButtons,
    StandardInputRow,
    DateInputRow,
    ImageInputRow,
    ScrollButtons
  }
})
export default class BurialDetails extends mixins(ManagementToolsMixin){
  
  individualDateFieldsToSingleDate = individualDateFieldsToSingleDate;

  @Prop() id;
  @Prop() person_id;
  @Prop() createMode;
  @Prop() showComponent;

  saving: boolean = false;
  processingImage: boolean = false;

  searchQuery: string = '';

  noBurialFlag: boolean = false;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    let v = this;

    this.componentName = "burial_details";
    this._id = this.id ? this.id : '';

    v.editableFields = ['burial_number', 'impossible_date_day', 'impossible_date_month', 'impossible_date_year', 'impossible_order_date_day', 'impossible_order_date_month', 'impossible_order_date_year', 'consecrated', 'cremated', 'impossible_cremation_date_day', 'impossible_cremation_date_month', 'impossible_cremation_date_year', 'cremation_certificate_no', 'interred', 'depth', 'depth_units', 'depth_position', 'burial_remarks', 'requires_investigation', 'user_remarks', 'place_from_which_brought', 'register', 'register_page', 'registration_number', 'burial_officials', 'burial_record_image', 'transcribed_grave_number', 'coffin_height', 'coffin_width', 'coffin_units'];

    // Load data. Creates new (unsaved) if id is blank.
    v.loadData('/mapmanagement/burialDetails/?burial_id=', v._id);

    if (v.createMode)
      v.editFlag = true;
    else if (!v.id) {
      v.noBurialFlag = true;
    }

    // if lists have not yet been loaded into vuex, load them
    if (!v.$store.state.ManagementTool.burialOfficialList 
      && !v.$store.state.ManagementTool.burialOfficialType) {

      axios.get('/mapmanagement/allBurialOptions')
      .then(function(response) {
        v.$store.commit('setBurialDetailLists', response.data);
      })
      .catch(function(response) {
        console.warn('Couldn\'t get burial details lists:', response);
      });
    }
}


  /*** Computed ***/

  /**
   * @returns list of burial officials with search query applied (if it exists)
   */
  get sortedBurialOfficialList() {
    let v = this;

    if (!v.searchQuery)
      return v.$store.state.ManagementTool.burialOfficialList;
    else {
      let sortedBurialOfficialList = [];

      v.$store.state.ManagementTool.burialOfficialList.forEach((groupList) => {
        let list = groupList.list.filter((burialOfficial) => {
          return burialOfficial.last_name &&
            burialOfficial.last_name.toUpperCase().lastIndexOf(v.searchQuery.toUpperCase(), 0) === 0;
        });

        sortedBurialOfficialList.push({ group: groupList.group, list: list });
      });

      return sortedBurialOfficialList;
    }
  }

  /*** Watchers ***/

  /**
   * Used to update scrolling in 'Add Burial' and tabs
   */
  @Watch('showComponent') 
  onShowComponentChanged(val: any, oldVal: any) {
    if (val)
      this.heightChangedFlag += 1;
  }

  /*** Methods ***/

  /** 
   * Add official
   * (I tried doing this in setter but it wouldn't work properly)
   */ 
  addOfficial(selectedOption, id) {
    this.componentData.burial_officials.push({
      official_id: selectedOption.id,
      burial_official_type_id: null,
      official_title: selectedOption.title,
      official_first_names: selectedOption.first_names,
      official_last_name: selectedOption.last_name,
      label: selectedOption.label
    });
  }

  /** 
   * Remove deleted official
   * (I tried doing this in setter but it wouldn't work properly)
   */ 
  removeOfficial(removedOption, id) {
    this.componentData.burial_officials.forEach((selectedOfficial, index) => {
      // if can't be found in select)
      if (selectedOfficial.official_id === removedOption.official_id) {
        this.componentData.burial_officials.splice(index, 1);  
      }
    });
  }

  /**
   * Saves an edit
   */
  onSubmit() {

let v = this;

    v.saving = true;

    //if cremated is false, ensure other cremated fields are null
    if (this.componentData.cremated === false) {
      this.componentData.cremation_certificate_no = null;
      this.componentData.impossible_cremation_date_day = null;
      this.componentData.impossible_cremation_date_month = null;
      this.componentData.impossible_cremation_date_year = null;
    }

    if (v.noBurialFlag)
      v._id = v.componentData.id;

    let data = v.getChangedData();

    // if creating a new burial
    if (v.noBurialFlag) {

      let newData = { 'burial_details': data };

      if (v.$route.name === constants.GRAVE_MANAGEMENT_PATH)
        newData['graveplot_id'] = v.$route.params.id;

      if (v.person_id)
        newData['person_details'] = { id: v.person_id };

      axios.post('/mapmanagement/createNewBurial/', newData)
        .then(function(response) {
          // updated saved version
          v.updateSavedVersion();
          v.appendToOrModifyItemInQuery('edit', null);
          v.saving = false;
          v.notificationHelper.createSuccessNotification('Burial successfully created');
          v.noBurialFlag = false;
          // refresh tool to load burial id
          v.appendToOrModifyItemInQuery('refresh', true);
        })
        .catch(function(response) {
          v.saving = false;
          console.warn('Couldn\'t create new burial:', response.response.data);
          v.notificationHelper.createErrorNotification("Couldn't create new burial");
        });
    }
    // if updating an existing burial
    else {
      axios.patch('/mapmanagement/burialDetails/', data)
        .then(function(response) {
          // updated saved version
          v.updateSavedVersion();
          v.appendToOrModifyItemInQuery('edit', null);



          v.saving = false;
          v.notificationHelper.createSuccessNotification('Burial details saved successfully');
        })
        .catch(function(response) {
          v.saving = false;
          console.warn('Couldn\'t save burial details:', response);
          v.notificationHelper.createErrorNotification("Couldn't save burial details");
        });
    }
  }

  /**
   * Sets the search query for burial officials
   */
  burialOfficialsSearch(query) {
    this.searchQuery = query;
  }

  /**
   * Get the official type from the official type id
   */
  getOfficialType(id) {
    if (id)
      return this.$store.state.ManagementTool.burialOfficialType.find(type => type.id === id ).official_type;
    else
      return null;
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

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>