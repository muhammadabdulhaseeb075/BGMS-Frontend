<template>
  <modal name="add-next-of-kin" 
        height="auto" 
        width="310px" 
        :clickToClose="false"
        draggable
        @before-close="closeAddNextOfKin">
    <div id="addNextOfKin" class="add-container">
      <div class="wizard-navigation">
        <div v-if="!savingFlag">
          <a class="col-xs-3" @click="close(false)">Cancel</a>
          <div v-if="createNew">
            <div class="col-xs-3"></div>
            <a class="col-xs-6" @click="close(true)">Add Next of Kin</a>
          </div>
        </div>
        <div v-else>  
            <div class="col-xs-11"></div>
            <div class="col-xs-1"><i class="fa fa-spinner fa-spin"></i></div>
        </div>
      </div>
      <div class="wizard-content">
        <div v-show="!createNew" class="create-person">
          <PersonCompanySearch id="personCompanySearch" :personOnly='true' @result-selected="resultSelected=$event; close(true);" @person-first-names-changed="firstNamesFromSearch=$event" @person-last-name-changed="lastNameFromSearch=$event"/>
          <div>
            <button class="bgms-button btn" type="button" title="Create New" @click="createNew=true;">
              Create New Person
            </button>
          </div>
        </div>

        <div v-if="createNew" class="create-person">
          <div class="wizard-page">
            <h1>Person Details</h1>
            <PersonDetails ref="personDetails" :createNew="true" :firstNames="firstNamesFromSearch" :lastName="lastNameFromSearch" @height-changed="heightChangedFlag+=1"/>
            <h1>Address</h1>
            <Address :createNew="true" :hideButtons="true" @height-changed="heightChangedFlag+=1"/>
          </div>
        </div>
      </div>
    </div>
  </modal>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator';
import axios from 'axios'
import constants from '@/global-static/constants.ts';
import Address from '@/mapmanagement/components/ManagementTool/Components/Address.vue';
import PersonCompanySearch from '@/mapmanagement/components/ManagementTool/Components/PersonCompanySearch.vue';
import FeatureTools from '@/mapmanagement/mixins/featureTools';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';
import { makeUndefinedNumbersNull } from '@/global-static/dataFormattingAndValidation.ts';
import VModal from 'vue-js-modal'

Vue.use(VModal, { dynamic: true, injectModalsContainer: true })

/**
 * Class representing addOwner component
 */
@Component({
  components: {
    PersonDetails: () => import('@/mapmanagement/components/ManagementTool/Components/PersonDetails.vue'),
    PersonCompanySearch,
    Address
  }
})
export default class addOwner extends mixins(FeatureTools, ManagementToolsMixin) {

  @Prop()  id;

  notificationHelper = this.$store.getters.notificationHelper;

  savingFlag: boolean = false;

  createNew: boolean = false;
  resultSelected = null;
  
  firstNamesFromSearch: string  = null;
  lastNameFromSearch: string  = null;

  /*** Watchers ***/

  /**
   * Used to update scrolling
   */
  @Watch('selectedPage', { immediate: true }) 
  onSelectedPageChanged(val: any, oldVal: any) {
    this.heightChangedFlag += 1;
  }
  
  /**
   * Close the modal screen
   * @param {boolean} save True if we are returning data. (I.e. will be false for cancel.)
   */
  close(save: boolean) {
    let data = null;

    if (save) {
      // if creating a new person
      if (this.createNew) {
        if ((this.$refs.personDetails as any).validateData()) {
          const personDetails = this.$store.state.ManagementTool.currentInformation.person_details;
          const personName = personDetails.first_names + (personDetails.first_names ? ' ' : '') + personDetails.last_name;
          data = { 
            new_create_details: makeUndefinedNumbersNull(personDetails),
            display_name: personName
          };
        }
        else
          return;
      }
      // if using an existing person
      else {
        if (!this.resultSelected) {
          this.notificationHelper.createErrorNotification("Please select a search result.");
          return;
        }
        else
          data = { 
            new_id: this.resultSelected.id,
            display_name: this.resultSelected.name };
      }
    }
        
    this.$modal.hide('add-next-of-kin', data);
  }
  
  /**
   * Called when next of kin modal is closed
   */
  closeAddNextOfKin(event) {
    
    // event.params will contain either the id of a person that is to be added as a next of kin (new_id),
    // or the data to create a new person that is to be added as a next of kin (new_create_detail), 
    // plus a display name
    if (event.params) {
      this.$emit('update-next-of-kin', event.params);
    }
  }
}
</script>