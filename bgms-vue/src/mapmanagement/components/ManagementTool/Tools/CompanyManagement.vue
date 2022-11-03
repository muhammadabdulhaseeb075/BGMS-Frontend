<template>
  <div id="companyManagementComponent" class="management-tool-buttons-container">
    <ul class="management-tool-buttons" v-if="$route.params.id">
      <router-link tag="li" class="top-border" :to="openOrCloseChildRoute(companyManagementPath, companyManagementChildRoutesEnum.companydetails)">
        <a :class="{ active: isRouteActive(companyManagementChildRoutesEnum.companydetails) }">Details</a>
      </router-link>
      <router-link tag="li" v-if="roles && roles.owner" class="top-border" :to="openOrCloseChildRoute(companyManagementPath, companyManagementChildRoutesEnum.companyownership)">
        <a :class="{ active: isRouteActive(companyManagementChildRoutesEnum.companyownership) }">Ownership</a>
      </router-link>
    </ul>
    <div v-else class="loading-placeholder-contents">
      <i class="fa fa-spinner fa-spin"/>
    </div>
    <div id="management-tool-contentbar-container">
      <router-view id="management-tool-contentbar" :class="{ 'component-container': isRouteActive(companyManagementChildRoutesEnum.companyownership) }"></router-view>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import axios from 'axios'
import Component, { mixins } from 'vue-class-component'
import { Watch } from 'vue-property-decorator'
import constants from '@/global-static/constants.ts';
import FeatureTools from '@/mapmanagement/mixins/featureTools';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';

Vue.use(Vuex);

/**
 * Class representing CompanyManagement
 * @extends ManagementToolsMixin mixin
 * @extends FeatureTools mixin
 */
@Component
export default class CompanyManagement extends mixins(ManagementToolsMixin, FeatureTools) {

  roles = null;

  companyManagementPath = constants.COMPANY_MANAGEMENT_PATH;
  companyManagementChildRoutesEnum = constants.COMPANY_MANAGEMENT_CHILD_ROUTES;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    this.componentName = "companymanagement";
    this.$store.commit('setTitle', "Company");

    this.newCompanySelected();

    this.openTool();
  }
  
  /*** Computed ***/

  /*** Watchers ***/

  /**
   * Watcher: When refresh in router query is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('$route.query.refresh')
  onRefreshChanged(val: any, oldVal: any) {
    if (val) {
      // refreshes the grave data
      this.newCompanySelected();

      // removes refresh in query
      this.appendToOrModifyItemInQuery('refresh', null);
    }
  }
  
  /*** Methods ***/

  /**
   * Called when a new company is selected.
   */
  newCompanySelected() {

    let v = this;

    axios.get('/mapmanagement/companyroles/?id=' + v.$route.params.id)
      .then(function(response) {
        v.roles = response.data;
      })
      .catch(function(response) {
        console.warn('Couldn\'t get data from server: ' + response);
        v.roles = false;
      });
  }
}
</script>
