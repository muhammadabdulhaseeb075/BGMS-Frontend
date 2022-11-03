<template>
  <div id = "management-tool">
    <div id="management-tool-title-vertical"><p>{{ $store.state.ManagementTool.title }} Management</p></div>
    <div id="management-tool-header">
      <div id="management-tool-header-buttons">
        <div v-if="!narrowTool">
          <div class="col-xs-3 no-padding">
            <a v-show="showLocator" href="javascript:void(0)" id="management-tool-locate" class="management-tool-navigation" @click="locateCurrentFeature" title="Locate feature on map"><i class="fa fa-location-arrow management-tool-navigation-icon"></i></a>
          </div>

          <div class="col-xs-3 no-padding">
            <a href="javascript:void(0)" id="management-tool-left" class="management-tool-navigation" @click="goBack" v-if="history.length>1" title="Go back"><i class="fa fa-arrow-left management-tool-navigation-icon"></i></a>
            <a id="management-tool-left-disabled" class="management-tool-navigation-disabled" v-else><i class="fa fa-arrow-left"></i></a>
          </div>

          <div class="col-xs-3 no-padding">
            <a href="javascript:void(0)" id="management-tool-right" class="management-tool-navigation" @click="goForward" v-if="future.length>0" title="Go forward"><i class="fa fa-arrow-right management-tool-navigation-icon"></i></a>
            <a id="management-tool-right-disabled" class="management-tool-navigation-disabled" v-else><i class="fa fa-arrow-right"></i></a>
          </div>
        </div>

        <div :class="narrowTool ?  'col-xs-12' : 'col-xs-3'" class="no-padding">
          <a href="javascript:void(0)" id="management-tool-close" class="management-tool-navigation management-tool-close" @click="closeTool" title="Close"><i class="fa fa-times management-tool-navigation-icon"></i></a>
        </div>
      </div>
    </div>
    <div id="management-tool-body">
      <div class="management-tool-message" v-if="!isOnline && !narrowTool">
        <div class="management-tool-message-contents">
          <h1>You are offline</h1>
          <div>This tool is unavailable while offline.</div>
        </div>
      </div>
      <router-view :key="$route.params.id" v-else-if="isOnline && !loading"></router-view>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import VueRouter from 'vue-router'
import Component, { mixins } from 'vue-class-component'
import { Prop } from 'vue-property-decorator'
import FeatureTools from '@/mapmanagement/mixins/featureTools'
import constants from '@/global-static/constants.ts';
import { messages } from '@/global-static/messages.js';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';

Vue.use(VueRouter);

/**
 * Class representing ManagementTool component
 * @extends Vue
 */
@Component
export default class ManagementTool extends mixins(FeatureTools, ManagementToolsMixin) {
  
  loading = true;

  notificationHelper: any = this.$store.getters.notificationHelper;

  /**
   * Vue mounted lifecycle hook
   * - registers jQuery event to listen for feature being selected
   */
  mounted() {
    (window as any).jQuery(document).off('featureSelected').on('featureSelected', this.featureSelectedInAngularJS);

    if(!this.$store.state.authenticatedSession){ //Disable right-click if in a public session
      document.addEventListener('contextmenu', event => event.preventDefault());
    }    
    this.loading = false;
  }

  /*** Watchers ***/

  /*** Computed ***/

  /**
   * Computed property: Is app online or has service worker installed and active
   * @returns {boolean}
   */
  get isOnline(): boolean {
    return this.$store.state.Offline.online;
  }

  /**
   * Computed property: History of URLs
   * @returns {[]}
   */
  get history() {
    return this.$store.state.ManagementTool.history;
  }

  /**
   * Computed property: 
   * @returns {[]}
   */
  get future() {
    return this.$store.state.ManagementTool.future;
  }

  /**
   * Computed property: 
   * @returns True if locator button should be shown for this feature
   */
  get showLocator() {
    if (this.isRouteActive(constants.GRAVE_MANAGEMENT_PATH) || this.isRouteActive(constants.MEMORIAL_MANAGEMENT_PATH) || this.isRouteActive(constants.FEATURE_MANAGEMENT_PATH))
      return true;
    else
      return false;
  }

  /**
   * Computed property:
   * @returns {boolean} True if narrow tool
   */
  get narrowTool(): boolean {
    return this.$route.name===constants.BURIAL_PERSON_MANAGEMENT_PATH || this.$route.path.indexOf('/' + constants.BURIAL_PERSON_MANAGEMENT_PATH + '/') !== -1;
  }
  
  /*** Methods ***/
  
  /**
   * Called when a different feature is selected in openlayers
   * @param e
   * @param featureInfo Object containing feature id, layerName and memorialGroup
   */
  featureSelectedInAngularJS(e:any, featureInfo:any) {
    this.featureSelected(featureInfo);
  }

  /**
   * Closes the tool
   */
  closeTool() {
    this.$store.commit('closeFlag', true);
    this.$router.replace('/');
  }

  /**
   * Go back to previous url
   */
  goBack() {
    this.$store.commit('goBackFlag', true);
    this.$router.replace({ path: this.history[this.history.length-2].path });
  }

  /**
   * Go forward to previous url
   */
  goForward() {
    this.$store.commit('goForwardFlag', true);
    this.$router.replace({ path: this.future[this.future.length-1].path });
  }

  /**
   * Locate current feature on map
   */
  locateCurrentFeature() {
    if (!this.showLocator) {
      this.notificationHelper.createErrorNotification(messages.search.unknowLocation.title);
    }
    else if (this.isRouteActive(constants.GRAVE_MANAGEMENT_PATH)) {
      let layer = 'plot';

      if (this.$route.params.layer)
        layer = this.$route.params.layer as string;
      
      if (layer === "available_plot")
        this.panToFeature(this.$route.params.availablePlotID, layer, false);
      else
        this.panToFeature(this.$route.params.id, layer, false);
    }
    else if (this.isRouteActive(constants.MEMORIAL_MANAGEMENT_PATH) || this.isRouteActive(constants.FEATURE_MANAGEMENT_PATH))
      this.panToFeature(this.$route.params.id, this.$route.params.layer, false);
  }
}
</script>
