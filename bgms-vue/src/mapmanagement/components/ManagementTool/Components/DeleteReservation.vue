<template>
  <div id="deleteReservation" class="add-container">
    <div class="wizard-navigation">
      <div v-if="!savingFlag">
        <a class="col-xs-3" @click="$router.push({ name: graveManagementChildRoutesEnum.reservations, params: { personID: personID }})">Cancel</a>
        <div class="col-xs-6"></div>
        <a class="col-xs-3" @click="deleteReservation">Delete</a>
      </div>
      <div v-else>  
        <div class="col-xs-11"></div>
        <div class="col-xs-1"><i class="fa fa-spinner fa-spin"></i></div>
      </div>
    </div>
    <div class="wizard-content">
      <div class="wizard-page">
        
        <ScrollButtons>

          <form class="form-horizontal form-box-inside management-tool-form">
            <StandardInputRow :label="'Remarks'" v-model="remarks" :inputType="'textarea'" :attributes="{ maxlength:200 }" :editFlag="true"/>
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
import FeatureTools from '@/mapmanagement/mixins/featureTools';
import ScrollButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ScrollButtons.vue';
import StandardInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/StandardInputRow.vue';

/**
 * Class representing DeleteReservation component
 */
@Component({
  components: {
    ScrollButtons,
    StandardInputRow
  }
})
export default class DeleteReservation extends mixins(FeatureTools) {

  @Prop() id;
  @Prop() personID;
  @Prop() layer;

  notificationHelper = this.$store.getters.notificationHelper;
  reservedPersonService = this.$store.getters.reservedPersonService;

  savingFlag: boolean = false;

  remarks: string = null;

  graveManagementChildRoutesEnum = constants.GRAVE_MANAGEMENT_CHILD_ROUTES;

  /**
   * Deletes a reservation including deleting the person record
   */
  deleteReservation() {
    let v = this;

    v.notificationHelper.createConfirmation('Delete Reservation', 'Are you sure you want to delete this reservation?',
    () => {
      v.savingFlag = true;

      let data = { params: { person_id: v.personID, graveplot_id: v.$route.params.id, notes: v.remarks }};

      axios.delete('/mapmanagement/personDetail/', data)
      .then(function(response) {

        if(response.data.available_plot) {
          // change current available plot to a plot/reserved_plot if it has no more burials, reservations or ownership
          v.changeFeatureLayer(v.$route.params.layer, 'available_plot', v.$route.params.id, response.data.topopolygon_id)
          .then(() => {
            v.$router.replace({ name: constants.GRAVE_MANAGEMENT_PATH, params: { layer: 'available_plot', availablePlotID: response.data.topopolygon_id }, query: { refresh: 'true' } });
          });
        }
        else
          v.$router.replace({ name: constants.GRAVE_MANAGEMENT_PATH, query: { refresh: 'true' } });

        // remove person from list of reserved persons
        v.reservedPersonService.removeReservedPerson(v.personID);

        v.savingFlag = false;
        v.notificationHelper.createSuccessNotification('Reservation deleted');
      })
      .catch(function(response) {
        v.savingFlag = false;
        console.warn('Couldn\'t delete reservation:', response.response.data);
        v.notificationHelper.createErrorNotification("Couldn't delete reservation");
      });
    });
  }
}
</script>