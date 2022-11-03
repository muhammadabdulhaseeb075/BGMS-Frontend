<template>
  <div v-if="componentData">

    <StandardInputRow v-if="componentData.section_id" :label="'Section'" v-model="componentData.section_name" :inputType="'text'" :readonlyOption="true" :editFlag="false"/>
    <StandardInputRow v-if="componentData.subsection_id" :label="'Subsection'" v-model="componentData.subsection_name" :inputType="'text'" :readonlyOption="true" :editFlag="false"/>

    <div v-if="editFlagProp || componentData.grave_number" class="row field-row">
      <label class="control-label col-xs-4" for="grave-number">Grave Number:</label>
      <div id="grave-number" class="col-xs-5 no-padding">
        <input :readonly="!editFlagProp" type="text" class="form-control" :placeholder="editFlagProp ? 'Grave Number' : 'None'" maxlength="20" :value="value" @input="$emit('input', $event.target.value)" @keyup.enter="validateGraveNumber">
      </div>
      <div class="col-xs-3 no-padding in-form-button row" v-show="editFlagProp">
        <button class="btn bgms-button col-xs-8" type="button" @click="() => {
          validateGraveNumber()
        }" :disabled="saving || (checkedGraveNumber && checkedGraveNumber === componentData.grave_number)">
          <span v-show="validationStatus === validationStatusEnum.validating" class="fa fa-spinner fa-spin"></span>
          <span v-show="validationStatus !== validationStatusEnum.validating">Verify</span></button>
        <span v-show="validationStatus === validationStatusEnum.available && checkedGraveNumber && checkedGraveNumber === componentData.grave_number" class="fa fa-check-circle col-xs-4"></span>
        <span v-show="validationStatus === validationStatusEnum.unavailable && checkedGraveNumber && checkedGraveNumber === componentData.grave_number" class="fa fa-times-circle col-xs-4"></span>
      </div>
    </div>
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
import Vuex from 'vuex';
import Component, { mixins } from 'vue-class-component'
import { Watch, Prop } from 'vue-property-decorator';
import axios from 'axios'
import StandardInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/StandardInputRow.vue';
import { messages } from '@/global-static/messages';
import boolean from "vue-good-table/src/components/types/boolean";

Vue.use(Vuex);

// used to define the current validation status
enum validationStatusType { none, validating, available, unavailable }

/**
 * Class representing GraveRef component
 * @extends Vue
 */
@Component({
  components: {
    StandardInputRow
  }
})
export default class GraveRef extends Vue {

  @Prop() editFlagProp;
  @Prop() componentData;
  @Prop() componentDataSaved;
  @Prop() value;
  @Prop() saving: boolean;

  validationStatusEnum = validationStatusType;
  validationStatus: validationStatusType = this.validationStatusEnum.none;
  checkedGraveNumber: string = null;

  notificationHelper: any = this.$store.getters.notificationHelper;


  /*** Computed ***/

  /**
   * Computed property:
   * @returns {boolean} True if the grave number has been changed
   */
  get graveNumberChanged(): boolean {
    return this.componentData.grave_number !== this.componentDataSaved.grave_number;
  }

  /*** Watchers ***/

  @Watch('editFlagProp', {immediate: true})
  onEditChanged(val, oldVal) {
    if (!val) {
      this.validationStatus = this.validationStatusEnum.none;
      this.checkedGraveNumber = null;
    }
  }


  /*** Methods ***/

  /**
   * Validated the grave number
   * (combination of grave number, section and subsection must be unique)
   */
  validateGraveNumber() {
    let v = this;

    // this prevents enter key press
    if (v.saving)
      return;

    v.validationStatus = v.validationStatusEnum.validating;

    axios.get('/mapmanagement/newGraveNumberCheck', {
      params: {
        graveNumber: v.componentData.grave_number,
        sectionID: v.componentData.section_id,
        subsectionID: v.componentData.subsection_id
      }
    })
      .then(function(response) {
        if( typeof response.data == "boolean") {
          if (response.data) {
             v.notificationHelper.createConfirmation(messages.toolbar.plot.linkGraveRef.confirmation.title, messages.toolbar.plot.linkGraveRef.confirmation.text, function () {
             const compentDataKeys = Object.keys(v.componentData);
             let newEmptyComponentState = {}

             for (const key of compentDataKeys) {
               if (key !== 'grave_number') {
                 newEmptyComponentState[key] = undefined;
               } else {
                 newEmptyComponentState[key] = v.componentData[key];
               }
             }
             v.notificationHelper.createSuccessNotification(messages.graveLinks.save.success.title);
             v.validationStatus = v.validationStatusEnum.available;
             v.$emit('onLoadData', newEmptyComponentState);
           }, () => {
                v.validationStatus = v.validationStatusEnum.none;
                v.checkedGraveNumber = undefined;
            });
          } else {
            v.validationStatus = v.validationStatusEnum.unavailable;
               v.$emit('onVerify');
            v.notificationHelper.createErrorNotification(messages.graveLinks.save.fail.title);
          }
        } else {
            v.notificationHelper.createConfirmation(messages.toolbar.plot.linkGraveRef.confirmation.title, messages.toolbar.plot.linkGraveRef.confirmation.text, function () {
            const componentState = v.$store.state.ManagementTool.currentInformationSaved['grave_details'];
            const currentState = {
              ...response.data,
              id: componentState.id,
              feature_id: componentState.feature
            }
              v.validationStatus = v.validationStatusEnum.none;
              v.$emit('onLoadData', currentState)
            }, () => {
                v.validationStatus = v.validationStatusEnum.none;
               v.checkedGraveNumber = undefined;
            });
        }
          v.checkedGraveNumber = v.componentData.grave_number;
      })
      .catch(function(response) {

        v.validationStatus = v.validationStatusEnum.none;
        v.checkedGraveNumber = undefined;
        console.warn('Couldn\'t validate grave number:', response.data);
      });
  }

}
</script>
