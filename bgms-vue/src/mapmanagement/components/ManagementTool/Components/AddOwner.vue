<template>
  <div id="addOwner" class="add-container">
    <div class="wizard-navigation">
      <div v-if="!savingFlag">
        <a class="col-xs-3" @click="close()">Cancel</a>
        <div v-if="selectedPage === addOwnerPagesEnum.add">
          <div class="col-xs-6"></div>
          <a class="col-xs-3" @click="leavePersonCompanyDetails(addOwnerPagesEnum.ownership)">Next <i class='fa fa-arrow-right'/></a>
        </div>
        <div v-else-if="selectedPage === addOwnerPagesEnum.ownership">
          <div class="col-xs-3"></div>
          <a class="col-xs-3" @click="createNew ? selectedPage=addOwnerPagesEnum.add : selectedPage=addOwnerPagesEnum.search"><i class='fa fa-arrow-left'/> Back</a>
          <a class="col-xs-3" @click="saveNewOwner">Save</a>
        </div>
      </div>
      <div v-else>  
          <div class="col-xs-11"></div>
          <div class="col-xs-1"><i class="fa fa-spinner fa-spin"></i></div>
      </div>
    </div>
    <div class="wizard-content">
      <ScrollButtons :heightChangedFlag="heightChangedFlag" :parentScroll="true">

        <div v-show="selectedPage === addOwnerPagesEnum.search" class="create-person">
          <PersonCompanySearch @result-selected="resultSelected=$event; leavePersonCompanyDetails(addOwnerPagesEnum.ownership)" @person-first-names-changed="firstNamesFromSearch=$event" @person-last-name-changed="lastNameFromSearch=$event" @company-name-changed="companyNameFromSearch=$event"/>
          <div>
            <button class="bgms-button btn" type="button" title="Create New" @click="selectedPage = addOwnerPagesEnum.add; createNew=true;">
              Create New Person or Company
            </button>
          </div>
        </div>

        <div v-show="selectedPage === addOwnerPagesEnum.add" class="create-person">
          <div class="row field-row no-margin">
            <label for="typeChoice" class="col-xs-4 control-label">Owner Type:</label>
            <div if="typeChoice" class="col-xs-8 no-padding">
              <input id="personType" class="col-xs-2" type="radio" name="ownerTypeRadios" :value="ownerTypesEnum.person" v-model="ownerTypeRadios">
              <label for="personType" class="col-xs-4 control-label">Person</label>
              <input id="companyTyle" class="col-xs-2" type="radio" name="ownerTypeRadios" :value="ownerTypesEnum.company" v-model="ownerTypeRadios">
              <label for="companyTyle" class="col-xs-4 control-label">Company</label>
            </div>
          </div>
          <div class="wizard-page">
            <h1>{{ ownerTypeRadios.charAt(0).toUpperCase() + ownerTypeRadios.slice(1) }} Details</h1>
            <PersonDetails v-show="ownerTypeRadios===ownerTypesEnum.person" ref="personDetails" :createNew="true" :firstNames="firstNamesFromSearch" :lastName="lastNameFromSearch" @height-changed="heightChangedFlag+=1"/>
            <CompanyDetails v-show="ownerTypeRadios===ownerTypesEnum.company" ref="companyDetails" :createNew="true" :companyName="companyNameFromSearch" @height-changed="heightChangedFlag+=1"/>
            <h1>Address</h1>
            <Address :createNew="true" :hideButtons="true" @height-changed="heightChangedFlag+=1"/>
          </div>
        </div>

        <div v-show="selectedPage === addOwnerPagesEnum.ownership" class="wizard-page">
          <h1>Owner Details</h1>
          <GraveOwner :newOwner="true" @height-changed="heightChangedFlag+=1" :startDay="startDay" :startMonth="startMonth" :startYear="startYear" :firstOwner="firstOwner"/>
        </div>

      </ScrollButtons>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator';
import axios from 'axios'
import constants from '@/global-static/constants.ts';
import { makeUndefinedNumbersNull } from '@/global-static/dataFormattingAndValidation.ts';
import Address from '@/mapmanagement/components/ManagementTool/Components/Address.vue';
import GraveOwner from '@/mapmanagement/components/ManagementTool/Components/GraveOwner.vue';
import PersonDetails from '@/mapmanagement/components/ManagementTool/Components/PersonDetails.vue';
import CompanyDetails from '@/mapmanagement/components/ManagementTool/Components/CompanyDetails.vue';
import PersonCompanySearch from '@/mapmanagement/components/ManagementTool/Components/PersonCompanySearch.vue';
import ScrollButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ScrollButtons.vue';
import FeatureTools from '@/mapmanagement/mixins/featureTools';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';

enum ADD_OWNER_PAGES { search, add, ownership }
enum OWNER_TYPES { 
  person = 'person', 
  company = 'company'
}

/**
 * Class representing addOwner component
 */
@Component({
  components: {
    PersonDetails,
    CompanyDetails,
    PersonCompanySearch,
    GraveOwner,
    Address,
    ScrollButtons
  }
})
export default class addOwner extends mixins(FeatureTools, ManagementToolsMixin) {

  @Prop()  id;
  @Prop() startDay;
  @Prop() startMonth;
  @Prop() startYear;
  @Prop() firstOwner;
  
  addOwnerPagesEnum = ADD_OWNER_PAGES;
  selectedPage: ADD_OWNER_PAGES = this.addOwnerPagesEnum.search;
  
  ownerTypesEnum = OWNER_TYPES;

  notificationHelper = this.$store.getters.notificationHelper;

  savingFlag: boolean = false;

  createNew: boolean = false;
  ownerTypeRadios = OWNER_TYPES.person;
  resultSelected = null;
  
  firstNamesFromSearch: string  = null;
  lastNameFromSearch: string  = null;
  companyNameFromSearch: string  = null;

  /*** Watchers ***/

  /**
   * Used to update scrolling
   */
  @Watch('selectedPage', { immediate: true }) 
  onSelectedPageChanged(val: any, oldVal: any) {
    this.heightChangedFlag += 1;
  }

  /**
   * Used to update scrolling
   */
  @Watch('ownerTypeRadios', { immediate: true }) 
  onOwnerTypeChanged(val: any, oldVal: any) {
    this.heightChangedFlag += 1;
  }

  /**
   * Save new ownership data
   */
  saveNewOwner() {
    let v = this;

    v.savingFlag = true;

    // get data
    let data = {
      deed_id: v.$route.params.deedID,
      transfer: v.$route.params.transfer,
      grave_owner: makeUndefinedNumbersNull(v.$store.state.ManagementTool.currentInformation.grave_owner) };

    if (v.createNew) {
      if (v.ownerTypeRadios === OWNER_TYPES.person)
        data['person_details'] = makeUndefinedNumbersNull(v.$store.state.ManagementTool.currentInformation.person_details);
      else if (v.ownerTypeRadios === OWNER_TYPES.company)
        data['company_details'] = makeUndefinedNumbersNull(v.$store.state.ManagementTool.currentInformation.company_details);

      if (v.$store.state.ManagementTool.currentInformation.address && v.$store.state.ManagementTool.currentInformation.address.unsavedChanges)
        data['address'] = v.$store.state.ManagementTool.currentInformation.address;
    }
    else if (v.resultSelected.type==='person')
      data['person_id'] = v.resultSelected.id;
    else if (v.resultSelected.type==='company')
      data['company_id'] = v.resultSelected.id;

    axios.post('/mapmanagement/createNewOwner/', data)
    .then(function(response) {
      v.savingFlag = false;
      v.notificationHelper.createSuccessNotification('New owner saved successfully');

      v.$store.commit('removeComponentData', 'grave_owner');
      v.$store.commit('removeComponentData', 'person_details');
      v.$store.commit('removeComponentData', 'company_details');
      v.$store.commit('removeComponentData', 'address');

      // close new burial page and refresh data to show new burial
      v.close(true);
    })
    .catch(function(response) {
      v.savingFlag = false;
      console.warn('Couldn\'t save new owner:', response.response.data);
      v.notificationHelper.createErrorNotification("Couldn't save new owner");
    });
  }

  leavePersonCompanyDetails(nextPage) {
    if (this.createNew) {
      // only move forward if validation in child component passes
      if (this.ownerTypeRadios===OWNER_TYPES.person && (this.$refs.personDetails as any).validateData())
        this.selectedPage=nextPage;
      else if (this.ownerTypeRadios===OWNER_TYPES.company && (this.$refs.companyDetails as any).validateData())
        this.selectedPage=nextPage;
    }
    else {
      if (!this.resultSelected)
        this.notificationHelper.createErrorNotification("Please select a search result.");
      else
        this.selectedPage=nextPage;
    }
  }

  /**
   * Closes this page and refreshes list of owners
   */
  close(refresh=false) {
    const query = refresh ? { 'refreshowners': 'true' } : null;
    this.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.graveOwnership, params: this.$route.params, query: query});
  }
}
</script>