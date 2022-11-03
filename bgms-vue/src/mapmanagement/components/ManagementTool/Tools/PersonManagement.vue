<template>
  <div id="personManagementComponent" class="management-tool-buttons-container">
    <ul class="management-tool-buttons" v-if="$route.params.id">
      <router-link tag="li" class="top-border" :to="openOrCloseChildRoute(personManagementPath, personManagementChildRoutesEnum.persondetails)">
        <a :class="{ active: isRouteActive(personManagementChildRoutesEnum.persondetails) }">Details</a>
      </router-link>
      <router-link tag="li" v-if="roles && roles.owner" class="top-border" :to="openOrCloseChildRoute(personManagementPath, personManagementChildRoutesEnum.personownership)">
        <a :class="{ active: isRouteActive(personManagementChildRoutesEnum.personownership) }">Ownership</a>
      </router-link>
      <router-link tag="li" v-if="roles && roles.next_of_kin" class="top-border" :to="openOrCloseChildRoute(personManagementPath, personManagementChildRoutesEnum.personNextOfKinTo)">
        <a :class="{ active: isRouteActive(personManagementChildRoutesEnum.personNextOfKinTo) }">Next Of Kin To</a>
      </router-link>
    </ul>
    <div v-else class="loading-placeholder-contents">
      <i class="fa fa-spinner fa-spin"/>
    </div>
    <div id="management-tool-contentbar-container">
      <router-view id="management-tool-contentbar" :class="{ 'component-container': isRouteActive(personManagementChildRoutesEnum.personownership) || isRouteActive(personManagementChildRoutesEnum.personNextOfKinTo) }"></router-view>
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
 * Class representing PersonManagement
 * @extends ManagementToolsMixin mixin
 * @extends FeatureTools mixin
 */
@Component
export default class PersonManagement extends mixins(ManagementToolsMixin, FeatureTools) {

  roles = null;

  personManagementPath = constants.PERSON_MANAGEMENT_PATH;
  personManagementChildRoutesEnum = constants.PERSON_MANAGEMENT_CHILD_ROUTES;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    this.componentName = "personmanagement";
    this.$store.commit('setTitle', "Person");

    this.newPersonSelected();

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
      this.newPersonSelected();

      // removes refresh in query
      this.appendToOrModifyItemInQuery('refresh', null);
    }
  }
  
  /*** Methods ***/

  /**
   * Called when a new person is selected.
   */
  newPersonSelected() {

    let v = this;

    axios.get('/mapmanagement/personroles/?id=' + v.$route.params.id)
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
