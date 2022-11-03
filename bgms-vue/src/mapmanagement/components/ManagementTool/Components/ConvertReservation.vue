<template>
  <div id="convertReservation" class="add-container">
    <div class="wizard-navigation">
      <div v-if="!savingFlag">
        <a class="col-xs-3" @click="$router.push({ name: graveManagementChildRoutesEnum.reservations, params: { personID: personID }})">Cancel</a>
        <div class="col-xs-6"></div>
        <a class="col-xs-3" @click="convertToBurial">Convert</a>
      </div>
      <div v-else>  
        <div class="col-xs-11"></div>
        <div class="col-xs-1"><i class="fa fa-spinner fa-spin"></i></div>
      </div>
    </div>
    <div class="wizard-content">
      <div class="wizard-page">
        
        <ScrollButtons :heightChangedFlag="heightChangedFlag">

          <ValidationBox v-if="errors" :errors="errors"/>

          <form class="form-horizontal form-box-inside management-tool-form">
            <DateInputRow :label="'Date of Burial'" :editFlag="true" :day="burialDay" @day-input="burialDay=$event" :month="burialMonth" @month-input="burialMonth=$event" :year="burialYear" @year-input="burialYear=$event"/>

            <div v-show="showLinkedMemorials">
              <h3 class="no-padding">The following memorial/s are linked to this grave. Select any that you would like to link to this new burial.</h3>
              <LinkedMemorials :id="id" :linkedType:="'grave'" :selectFlagProp="true" @loading-data-flag="memorialsLoaded=true; heightChangedFlag += 1"/>
            </div>
          </form>

        </ScrollButtons>
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator';
import axios from 'axios'
import constants from '@/global-static/constants.ts';
import LinkedMemorials from '@/mapmanagement/components/ManagementTool/Components/LinkedMemorials.vue';
import FeatureTools from '@/mapmanagement/mixins/featureTools';
import DateInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/DateInputRow.vue';
import ScrollButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ScrollButtons.vue';

/**
 * Class representing ConvertRegistration component
 */
@Component({
  components: {
    LinkedMemorials,
    DateInputRow,
    ScrollButtons,
    ValidationBox: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/ValidationBox.vue'),
  }
})
export default class ConvertRegistration extends mixins(FeatureTools) {

  @Prop()  id;
  @Prop() personID;
  @Prop() layer;

  notificationHelper = this.$store.getters.notificationHelper;
  reservedPersonService = this.$store.getters.reservedPersonService;

  savingFlag: boolean = false;
  memorialLinkFlag: boolean = false;

  memorialsLoaded: boolean = false;
  selectedMemorials = [];

  burialDay: number = null;
  burialMonth: number = null;
  burialYear: number = null;

  errors = null;

  graveManagementChildRoutesEnum = constants.GRAVE_MANAGEMENT_CHILD_ROUTES;

  heightChangedFlag: number = 0;

  mounted() {
    const today = new Date();
    this.burialDay = today.getDate();
    this.burialMonth = today.getMonth() + 1;
    this.burialYear = today.getFullYear();
  }

  /**
   * @returns true if there are memorials to display
   */
  get showLinkedMemorials() {
    if (this.memorialsLoaded)
      return this.$store.state.ManagementTool.currentInformation.linked_memorials &&this.$store.state.ManagementTool.currentInformation.linked_memorials.linkedMemorials && this.$store.state.ManagementTool.currentInformation.linked_memorials.linkedMemorials.length > 0;
    else
      return false;
  }

  /**
   * Validates data. Displays message if errors present.
   * @returns true if validation passes
   */
  validateData(): boolean {
    let errors = [];
    let returnValue = true;

    if (!this.burialDay)
      errors.push("A burial date day value is required.");
    if (!this.burialMonth)
      errors.push("A burial date month value is required.");
    if (!this.burialYear)
      errors.push("A burial date year value is required.");

    if (errors.length > 0) {
      returnValue = false;

      // scroll to top so user can see validation message
      Vue.nextTick(() => { ((document.getElementById('verticalScroll') as HTMLElement).scrollTop) = 0; });
    }
    
    this.errors = errors;

    return returnValue;
  }

  /**
   * Convert reservation to burial
   */
  convertToBurial() {
    let v = this;
    
    if (!v.validateData())
      return;

    v.savingFlag = true;

    // get data
    let data = {
      graveplot_id: v.id,
      person_id: v.personID,
      layer: v.layer,
      burial_day: v.burialDay,
      burial_month: v.burialMonth,
      burial_year: v.burialYear };
    
    if (this.showLinkedMemorials)
      data['selected_memorials'] = v.$store.state.ManagementTool.currentInformation.linked_memorials.selectedMemorials;

    axios.post('/mapmanagement/convertReservation/', data)
    .then(function(response) {

      if(v.layer==='reserved_plot') {
        // change current plot to a plot as it now has a burial
        v.changeFeatureLayer('reserved_plot', 'plot', v.$route.params.id, v.$route.params.id)
        .then(() => {
          v.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.burials, params: { person_id: response.data.person_id, burial_id: response.data.burial_id, layer: 'plot' }, query: { refresh: 'true' }});
        })
      }
      else
        v.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.burials, params: { person_id: response.data.person_id, burial_id: response.data.burial_id }, query: { refresh: 'true' }});

      // remove person from list of reserved persons
      v.reservedPersonService.removeReservedPerson(v.personID);

      v.savingFlag = false;
      v.notificationHelper.createSuccessNotification('Reservation successfully converted to a burial');
    })
    .catch(function(response) {
      v.savingFlag = false;
      console.warn('Failed to convert reservation to a burial:', response.response.data);
      v.notificationHelper.createErrorNotification("Failed to convert reservation to a burial");
    });
  }
}
</script>