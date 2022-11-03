<template>
  <div :id="componentName" v-if="componentData">
    <form class="form-horizontal form-box-inside management-tool-form" @submit.prevent="onSubmit">

      <FormButtons v-if="siteAdminOrSiteWarden && !hideButtons" :editFlag="true" :saving="saving" :fieldChanged="fieldChanged" @toggle-edit="close()" :showEdit="true" :showBack="true" @toggle-back="$emit('close-grave-owner',true)"/>
            
      <StandardInputRow :label="'First Line'" v-model="componentData.first_line" :inputType="'text'" :attributes="{ maxlength:200 }"/>
      <StandardInputRow :label="'Second Line'" v-model="componentData.second_line" :inputType="'text'" :attributes="{ maxlength:200 }"/>
      <StandardInputRow :label="'Town'" v-model="componentData.town" :inputType="'text'" :attributes="{ maxlength:50 }"/>
      <StandardInputRow :label="'County'" v-model="componentData.county" :inputType="'text'" :attributes="{ maxlength:50 }"/>
      <StandardInputRow :label="'Postcode'" v-model="componentData.postcode" :inputType="'text'" :attributes="{ maxlength:10,  class:'uppercase-text' }"/>
      <StandardInputRow :label="'Country'" v-model="componentData.country" :inputType="'text'" :attributes="{ maxlength:50 }"/>

      <section>
        <StandardInputRow :label="'Current'" v-model="componentData.current" :inputType="'checkbox'" :readonlyOption="true" :editFlag="!expiredToDate" :readonly="toDateIncluded"/>

        <DateInputRow :label="'Address From'" :editFlag="true" :day="componentData.from_date_day" @day-input="componentData.from_date_day=$event" :month="componentData.from_date_month" @month-input="componentData.from_date_month=$event" :year="componentData.from_date_year" @year-input="componentData.from_date_year=$event"/>

        <DateInputRow :label="'Address To'" :editFlag="true" :day="componentData.to_date_day" @day-input="componentData.to_date_day=$event" :month="componentData.to_date_month" @month-input="componentData.to_date_month=$event" :year="componentData.to_date_year" @year-input="componentData.to_date_year=$event"/>
      </section>

      <FormButtons v-if="siteAdminOrSiteWarden && !hideButtons" :editFlag="true" :saving="saving" :fieldChanged="fieldChanged" @toggle-edit="close()"/>
    </form>
  </div>
  <div v-else class="loading-placeholder">
    <div class="loading-placeholder-contents">
      <i class="fa fa-spinner fa-spin"/>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script lang='ts'>
import Component, { mixins } from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import axios from 'axios';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin.ts';
import FormButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/FormButtons.vue';
import StandardInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/StandardInputRow.vue';
import DateInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/DateInputRow.vue';
import constants from '@/global-static/constants.ts';

/**
 * Class representing GraveOwner component
 * @extends mixins: ManagementToolsMixin
 */
@Component({
  components: {
    FormButtons,
    StandardInputRow,
    DateInputRow
  }
})
export default class Address extends mixins(ManagementToolsMixin){

  @Prop() personId;
  @Prop() companyId;
  @Prop() addressID;
  @Prop() createNew;
  @Prop() hideButtons;

  saving: boolean = false;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    let v = this;

    v.componentName = "address";

    // this is needed in ManagementToolsMixin
    v._id = v.createNew ? '' : v.addressID;

    v.loadData('/api/address/?id=', v._id);

    v.editableFields = ['first_line', 'second_line', 'town', 'county', 'postcode', 'country', 'current', 'from_date_day', 'from_date_month', 'from_date_year', 'to_date_day', 'to_date_month', 'to_date_year'];
  }

  /*** Computed ***/

  /**
   * @returns true if to date is in the past
   */
  get expiredToDate() {

    let returnValue = false;

    if (this.toDateIncluded) {
      let today = new Date();
      if (this.componentData.to_date_year < today.getFullYear())
        returnValue = true;
      else if (this.componentData.to_date_year === today.getFullYear()) {
        if (this.componentData.to_date_month < (today.getMonth()+1))
          returnValue = true;
        else if (this.componentData.to_date_month == (today.getMonth()+1)) {
          if (this.componentData.to_date_day < today.getDate())
            returnValue = true;
        }
      }

      if (returnValue)
        this.componentData.current = false;
      else if (this.toDateIncluded)
        this.componentData.current = true;
    }

    return returnValue;
  }

  get toDateIncluded(): boolean {
    return this.componentData.to_date_day && this.componentData.to_date_month && this.componentData.to_date_year;
  }

  /*** Watchers ***/

  /*** Methods ***/

  /**
   * Saves an edit
   */
  onSubmit() {

    let v = this;

    v.saving = true;

    let data = this.getChangedData();

    if (v._id) {
      axios.patch('/api/address/', data)
        .then(function(response) {
          // updated saved version
          v.updateSavedVersion();
          v.close(true);
          v.notificationHelper.createSuccessNotification('Address saved successfully');
        })
        .catch(function(response) {
          v.saving = false;
          console.warn('Couldn\'t save address:', response);
          v.notificationHelper.createErrorNotification("Couldn't save address");
        });
    }
    else {
      if (v.personId)
        data['person_id'] = v.personId;

      if (v.companyId)
        data['company_id'] = v.companyId;
      
      axios.post('/api/address/', data)
        .then(function(response) {
          // updated saved version
          v.updateSavedVersion();
          v.close(true);
          v.notificationHelper.createSuccessNotification('New address saved successfully');
        })
        .catch(function(response) {
          v.saving = false;
          console.warn('Couldn\'t save address:', response);
          v.notificationHelper.createErrorNotification("Couldn't save new address");
        });
    }
  }

  close(refresh=false) {
    const query = refresh ? { refreshaddress: 'true'} : null;

    if (this.isRouteActive(constants.PERSON_MANAGEMENT_CHILD_ROUTES.persondetails))
      this.$router.replace({ name: constants.PERSON_MANAGEMENT_CHILD_ROUTES.persondetails, query: query });
    else if (this.isRouteActive(constants.COMPANY_MANAGEMENT_CHILD_ROUTES.companydetails))
      this.$router.replace({ name: constants.COMPANY_MANAGEMENT_CHILD_ROUTES.companydetails, query: query });
  }
}
</script>
