<template>
  <div id="detailsComponent" class="panel">
    <div class="panel-header">
      <button :class="{collapsed: collapsed}" class="sidebar-subheading" type="button" data-toggle="collapse" data-target="#detailsCollapse" aria-expanded="!collapsed" aria-controls="detailsCollapse">
      Attributes
      </button>
    </div>
    <div :class="{in: !collapsed}" class="collapse collapseSection" id="detailsCollapse" ref="detailsCollapse">
      <div class="panel-body">
        <div class="row">
          <label class="control-label col-xs-5" for="feature-id">Feature ID:</label>
          <div id="feature-id" class="col-xs-7">{{ featureId }}</div>
        </div>
        <form :class="{'form-horizontal': !narrowSidebar}" class="form-box-inside" action="" @submit.prevent="onSubmit" v-show="!loadingDetails">
          <div class="form-group">
            <label :class="{'col-xs-5': !narrowSidebar}" class="control-label" for="memorial-layer">Memorial type:</label>
            <div id="memorial-layer" :class="{'col-xs-7': !narrowSidebar}" class="form-field">
              <select v-model="memorialLayer" :disabled="!siteAdminOrSiteWarden">
                <option v-for="memorialLayer in memorialLayers" :value="memorialLayer.layer_code" :key="memorialLayer.layer_id">
                  {{ memorialLayer.display_name }}
                </option>
              </select>
            </div>
          </div>
          <button type="submit" v-show="layerChanged" class="btn bgms-button sidebar-normal-button">Save</button>
          <button class="btn bgms-button sidebar-normal-button" type="button" @click="memorialLayer = memorial.get('marker_type')" v-show="layerChanged">Cancel</button>
        </form>
        <form :class="{'form-horizontal': !narrowSidebar}" class="form-box-inside" action="" @submit.prevent="onSubmitMaterial" v-show="!loadingDetails">
          <div class="form-group">
            <label :class="{'col-xs-5': !narrowSidebar}" class="control-label" for="memorial-layer">Material:</label>
            <div id="memorial-layer" :class="{'col-xs-7': !narrowSidebar}" class="form-field">
              <select v-model="material" :disabled="!siteAdminOrSiteWarden">
                <option v-for="material in materials" :value="material" :key="material">
                  {{ material }}
                </option>
              </select>
            </div>
          </div>
          <button type="submit" v-show="materialChanged" class="btn bgms-button sidebar-normal-button">Save</button>
          <button class="btn bgms-button sidebar-normal-button" type="button" @click="material = originalMaterial" v-show="materialChanged">Cancel</button>
        </form>

        <div v-show="loadingDetails" class="mc-spinner">
          <i class="fa fa-spinner fa-spin"/>
          <p>Loading details</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import Component from 'vue-class-component'
import { Watch } from 'vue-property-decorator'
import axios from 'axios'
import GeoJSON from 'ol/format/GeoJSON';

import { messages } from '@/global-static/messages.js';
import { VISUALISATIONENUM, showMemorialIndicators, hideMemorialIndicators, createMemorialBenchImageOverlay } from '@/mapmanagement/components/Map/models/Memorial';

Vue.use(Vuex);

/**
 * Class representing Details component
 * @extends Vue
 */
@Component
export default class Details extends Vue{

  loadingDetails: boolean = false;

  notificationHelper: any = this.$store.getters.notificationHelper;
  siteAdminOrSiteWarden: boolean = this.$store.state.siteAdminOrSiteWarden;

  featureId: string = '';
  memorialLayer: any = null;

  material: string = null;
  originalMaterial: string = null;

  /**
   * Vue mounted lifecycle hook
   * - gets notificationHelper from angularjs
   * - gets the memorial layers
   * - Listens for bootstrap events fired when section is collapsed/opened
   */
  mounted() {

    if (!this.$store.state.memorialLayers) {
      this.loadingDetails = true;

      // Get the memorial layers from server
      this.$store.dispatch('populateMemorialLayers')
      .finally(() => {
        this.loadingDetails = false;
      });
    }

    if (!this.$store.state.MemorialCaptureSidebar.materials) {
      this.loadingDetails = true;

      // Get the materials from server
      axios.get('/geometries/featureAttributeMaterials/')
      .then(response => {
        this.$store.commit('populateMaterials', response.data.materials);
      })
      .catch(response => {
        console.warn('Couldn\'t get materials:', response);
      })
      .finally(() => {
        this.loadingDetails = false;
      });
    }

    (window as any).jQuery(this.$refs.detailsCollapse).on('hidden.bs.collapse', () => {
      this.$store.commit('setDetailCollapsed', true);
    });

    (window as any).jQuery(this.$refs.detailsCollapse).on('shown.bs.collapse', () => {
      this.$store.commit('setDetailCollapsed', false);
    });
  }

  /*** Watchers ***/
  /**
   * Watcher: when new memorial is selected
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('memorial', { immediate: true})
  onMemorialChanged(val: any, oldVal: any) {
    if (val === oldVal || !val){
      return;
    }
    this.loadingDetails = true;
    this.featureId = val.get("feature_id");
    this.memorialLayer = val.get("marker_type");
    this.material = this.originalMaterial = val.get("material");
    
    // features in multiple groups including memorials
    if (this.memorialLayer === "memorials_bench" || this.memorialLayer === "memorials_lych_gate" || this.memorialLayer === "memorials_mausoleum")
      this.memorialLayer = this.memorialLayer.replace("memorials_", "");

    this.loadingDetails = false;
  }

  /**
   * Watcher: when new data is entered or unsaved data is saved
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('layerChanged', { immediate: true})
  onLayerChanged(val: any, oldVal: any) {
    this.$store.commit('toggleUnsavedDetails', val);
  }

  /**
   * Watcher: when new data is entered or unsaved data is saved
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('materialChanged', { immediate: true})
  onmaterialChanged(val: any, oldVal: any) {
    this.$store.commit('toggleUnsavedDetails', val);
  }

  /*** Computed ***/

  /**
   * Computed property: Get the selected memorial
   * @returns {any} memorial
   */
  get memorial() {
    return this.$store.state.MemorialSidebar.memorial;
  }

  /**
   * Computed property: Get the memorial's photos
   * @returns {any} photos
   */
  get online() {
    return this.$store.state.Offline.online;
  }

  /**
   * Computed property: Get the available memorial layers
   * @returns {any} memorial layers
   */
  get memorialLayers() {
    return this.$store.state.memorialLayers;
  }

  /**
   * Computed property: Get the available materials
   * @returns {any} materials
   */
  get materials() {
    return this.$store.state.MemorialCaptureSidebar.materials;
  }

  /**
   * Computed property: Returns true when the layer has been changed and not yet saved
   * @returns {boolean} true if layer has changed
   */
  get layerChanged(): boolean {
    let originalValue = this.memorial.get("marker_type");

    // features in multiple groups including memorials
    if (originalValue === "memorials_bench" || originalValue === "memorials_lych_gate" || originalValue === "memorials_mausoleum")
      originalValue = originalValue.replace("memorials_", "");

    return originalValue !== this.memorialLayer;
  }

  /**
   * Computed property: Returns true when the material has been changed and not yet saved
   * @returns {boolean} true if material has changed
   */
  get materialChanged(): boolean {
    const originalValue = this.originalMaterial;
    return originalValue !== this.material;
  }

  /**
   * Computed property: Get detailCollapsed
   * @returns {boolean} True if this section should be collapsed
   */
  get collapsed(): boolean {
    return this.$store.state.MemorialCaptureSidebar.detailCollapsed;
  }

  /**
   * Computed property: Should the sidebar be narrow or wide (depends on which sections are collapsed)
   * @returns {boolean}
   */
  get narrowSidebar(): boolean {
    return this.$store.getters.narrowSidebar;
  }

  /*** Methods ***/

  /**
   * If online: saves change to server.
   * If offline: adds change to service worker queue.
   * Also updates ol feature textValue and style
   */
  onSubmit() {

    let geojsonFormatter = new GeoJSON();
    let geoJSONFeature = geojsonFormatter.writeFeature(this.memorial);
    let jsonObject = JSON.parse(geoJSONFeature);
    let featureHelperService = this.$store.getters.featureHelperService;
    jsonObject.id = featureHelperService.getFeatureId(this.memorial);
    jsonObject.properties.marker_type = this.memorialLayer;
    jsonObject.properties.old_marker_type = this.memorial.get('marker_type');
    
    let memorialService = this.$store.getters.memorialService;

    axios.post('/mapmanagement/updateMemorial/', { 'geojsonFeature': JSON.stringify(jsonObject) })
      .then(response => {
        // update ol feature
        memorialService.moveMemorialToLayer(this.memorial.getId(), this.memorialLayer).then(() => {
          new Promise((resolve, reject) => {
            // update style
            hideMemorialIndicators();
            showMemorialIndicators(VISUALISATIONENUM.image); // TODO: Should be no need to reload the ENTIRE visualisation
            resolve();
          })
          .then(() => {
            //show selected icon again
            if (this.memorial.get("marker_type") === "memorials_bench") {
              this.memorial.setStyle(createMemorialBenchImageOverlay(VISUALISATIONENUM.image, true, this.memorial));
            }
            else {
              let originalMemorialStyle = this.memorial.getStyle()[0];
              let highlightedStyle = originalMemorialStyle.clone();
              highlightedStyle.setText(this.$store.state.Styles.markerText);
              this.memorial.setStyle([highlightedStyle]);
            }

            console.log(response);
            this.notificationHelper.createSuccessNotification(messages.burialDetails.saveChanges.success.title);
          });
        });
      })
      .catch(error => {
        console.log(error);
        this.notificationHelper.createErrorNotification(messages.burialDetails.saveChanges.fail.title);
      });
  }

  /**
   * If online: saves change to server.
   * If offline: adds change to service worker queue.
   */
  onSubmitMaterial() {

    axios.post('/geometries/featureAttributeMaterials/', { 'memorial_id': this.memorial.getId(), 'material': this.material })
      .then(response => {
        this.originalMaterial = this.material;
        this.memorial.set('material',this.material);
        this.notificationHelper.createSuccessNotification(messages.burialDetails.saveChanges.success.title);
      })
      .catch(error => {
        console.log(error);
        this.notificationHelper.createErrorNotification(messages.burialDetails.saveChanges.fail.title);
      });
  }
}
</script>
