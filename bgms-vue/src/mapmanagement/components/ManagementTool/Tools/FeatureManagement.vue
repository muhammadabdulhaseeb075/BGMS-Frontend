<template>
  <div id="featureManagementComponent" class="management-tool-buttons-container">
    <ul class="management-tool-buttons" v-if="$route.params.id && subbuttons && subbuttonNames">
      <router-link tag="li" class="top-border" :to="openOrCloseChildRoute(managementToolRoute, featureManagementChildRoutesEnum.attributes)">
        <a :class="{ active: isRouteActive(featureManagementChildRoutesEnum.attributes) }">Attributes</a>
      </router-link>
      <SurveyButtons :key="surveyKey" :managementToolRoute="managementToolRoute" :surveysRoute="featureManagementChildRoutesEnum.surveys" :showSurveySubbuttons="subbuttons[subbuttonNames.SURVEYSUBBUTTONS].show" @toggle_survey_subbuttons="toggleSubbuttons"/>
    </ul>
    <div v-else class="loading-placeholder-contents">
      <i class="fa fa-spinner fa-spin"/>
    </div>
    <div id="management-tool-contentbar-container">
      <router-view id="management-tool-contentbar"/>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import axios from 'axios'
import Component, { mixins } from 'vue-class-component'
import { Watch, Prop } from 'vue-property-decorator'
import constants from '@/global-static/constants.ts';
import SurveyButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/SurveyButtons.vue';
import FeatureTools from '@/mapmanagement/mixins/featureTools.ts';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin.ts';
import SubbuttonsMixin from '@/mapmanagement/mixins/subbuttonsMixin.ts';

Vue.use(Vuex);

/**
 * Class representing FeatureManagement
 * @extends ManagementToolsMixin mixin
 * @extends FeatureTools mixin
 * @extends SubbuttonsMixin mixin
 */
@Component({
  components: {
    SurveyButtons
  }
})
export default class FeatureManagement extends mixins(ManagementToolsMixin, FeatureTools, SubbuttonsMixin) {

  @Prop() id;
  @Prop() layer;

  roles = null;

  featureManagementChildRoutesEnum = constants.FEATURE_MANAGEMENT_CHILD_ROUTES;
  
  featureHelperService = this.$store.getters.featureHelperService;

  surveyKey: number = 0;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    this.componentName = "featuremanagement";
    this.$store.commit('setTitle', "Feature");

    this.managementToolRoute = constants.FEATURE_MANAGEMENT_PATH;

    this.$set(this.subbuttons, this.subbuttonNames.SURVEYSUBBUTTONS, { show: false, route: this.featureManagementChildRoutesEnum.surveys });
    
    this.newFeatureSelected();

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
      // refreshes the survey data
      this.surveyKey++;

      // removes refresh in query
      this.appendToOrModifyItemInQuery('refresh', null);
    }
  }
  
  /*** Methods ***/
  
  newFeatureSelected() {
    // highlight and pan to (if needed) the selected feature
    this.highlightFeatures('hightlighted-features', 'hightlighted-features-' + this.id, [{ featureID: this.id, layerName: this.layer }], this.$store.state.MapLayers.layerStyles.selectedStyleWithMarkerFunction, this.layer);
    this.panToFeature(this.id, this.layer);
  }
}
</script>
