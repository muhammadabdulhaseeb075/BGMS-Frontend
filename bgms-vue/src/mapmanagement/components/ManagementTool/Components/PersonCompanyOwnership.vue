<template>
  <div v-if="componentData" style="width: 100%;">
    <div v-if="componentData.owned_graves && componentData.owned_graves.length > 0">
      <label class="col-xs-12 control-label">Graves Owned:</label>
      <table class="table table-condensed">
        <thead>
          <tr>
            <th/>
            <th>Grave No.</th>
            <th v-if="includeSection">Section</th>
            <th v-if="includeSubsection">Sub</th>
            <th/>
          </tr>
        </thead>
        <tbody>
          <template v-for="(grave, index) in componentData.owned_graves">
            <tr :key="grave.deed_id">
              <td class="letter-index">{{ indexToLetter(index) }}</td>
              <td class="table-row-bottom">{{ grave.grave_number ? grave.grave_number : 'Unknown' }}</td>
              <td v-if="includeSection" class="table-row-bottom">{{ grave.section_name }}</td>
              <td v-if="includeSubsection" class="table-row-bottom">{{ grave.subsection_name }}</td>
              <td><a href="" @click="goToGraveManagementTool(grave.grave_id, grave.deed_id, grave.site)" title="Go to Grave Management"><i class="fa fa-arrow-circle-right"></i></a></td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <div v-if="componentData.previously_owned_graves && componentData.previously_owned_graves.length > 0">
      <label class="col-xs-12 control-label">Graves Previously Owned:</label>
      <table class="table table-condensed">
        <thead>
          <tr>
            <th/>
            <th>Grave No.</th>
            <th v-if="includeSection">Section</th>
            <th v-if="includeSubsection">Sub</th>
            <th/>
          </tr>
        </thead>
        <tbody>
          <template v-for="(grave, index) in componentData.previously_owned_graves">
            <tr :key="grave.deed_id">
              <td class="letter-index">{{ indexToLetter(index) }}</td>
              <td class="table-row-bottom">{{ grave.grave_number ? grave.grave_number : 'Unknown' }}</td>
              <td v-if="includeSection" class="table-row-bottom">{{ grave.section_name }}</td>
              <td v-if="includeSubsection" class="table-row-bottom">{{ grave.subsection_name }}</td>
              <td><a href="" @click="goToGraveManagementTool(grave.grave_id, grave.deed_id, grave.site)" title="Go to Grave Management"><i class="fa fa-arrow-circle-right"></i></a></td>
            </tr>
          </template>
        </tbody>
      </table>
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
import Component, { mixins } from 'vue-class-component';
import { Watch, Prop } from 'vue-property-decorator';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';
import constants from '@/global-static/constants.ts';

Vue.use(Vuex);

/**
 * Class representing PersonCompanyOwnership component
 * @extends Vue
 */
@Component
export default class PersonCompanyOwnership extends mixins(ManagementToolsMixin) {

  @Prop() id;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    this.componentName = "person_company_ownership";
    this._id = this.id;

    // load data
    if (this.$route.name===constants.PERSON_MANAGEMENT_CHILD_ROUTES.personownership)
      this.loadData('/mapmanagement/personownership/?id=', this._id);
    else if (this.$route.name===constants.COMPANY_MANAGEMENT_CHILD_ROUTES.companyownership)
      this.loadData('/mapmanagement/companyownership/?id=', this._id);
  }

  /*** Computed ***/

  get includeSection(): boolean {
    if (this.componentData)
      return this.componentData.owned_graves.find(grave => grave.section_name) || this.componentData.previously_owned_graves.find(grave => grave.section_name);
    else
      return false
  }

  get includeSubsection(): boolean {
    if (this.componentData)
      return this.componentData.owned_graves.find(grave => grave.subsection_name) || this.componentData.previously_owned_graves.find(grave => grave.subsection_name);
    else
      return false
  }

  /*** Watchers ***/

  /*** Methods ***/

  goToGraveManagementTool(id, deedID, site) {
    if (this.componentData.current_site_name && this.componentData.current_site_name===site)
      this.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.graveOwnership, params: { id: id, deedID: deedID, layer: 'unknown' }});
    else
      this.notificationHelper.createInfoNotification("Go To Grave Management", "This grave exists in a different site: " + site);
  }

  /**
   * Map 0 based index to letter
   */
  indexToLetter(index) {
    let abc = 'abcdefghijklmnopqrstuvwxyz';
    return abc[index];
  }
}
</script>
