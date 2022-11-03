<template>
  <table id="table-search" :class="[ includeSubsections ? 'grave-table-3' : includeSections ? 'grave-table-2': 'grave-table-1' ]" class='table basic-search-results table-fixed borderless table-hover'>
    <thead ref="resultTHead">
      <tr>

        <th v-if="includeSections" @click="sortResults(columnTypeEnum.section)" class="section-column">Section</th>
        <th v-if="includeSubsections" @click="sortResults(columnTypeEnum.subsection)" class="subsection-column">Subsection</th>
        <th @click="sortResults(columnTypeEnum.graveNumber)" class="gravenumber-column">Grave No.</th>
        <th @click="sortResults(columnTypeEnum.layer)" class="layer-column">Layer</th>
        <th class="link-column"/>

      </tr>
    </thead>
    <tbody v-if="searchConducted" ref="resultTBody" :style="{ 'max-height': resultsHeight }">
      <tr role="row" v-for="result in resultsSorted" :key="result.graveplot_uuid" @click="showGrave(result)">

        <td v-if="includeSections" class="section-column">{{ result.section_name ? result.section_name : '-' }}</td>
        <td v-if="includeSubsections" class="subsection-column">{{ result.subsection_name ? result.subsection_name : '-' }}</td>
        <td class="gravenumber-column">{{ result.graveref__grave_number ? result.graveref__grave_number : '-' }}</td>
        <td class="layer-column">{{ !result.graveplot_layer ? '-' : '' }}<div v-if="result.graveplot_layer" :class="result.graveplot_layer + '_key'"/></td>
        <td><a class="link-column burial-record" href="javascript:void(0)" @click.stop="openGraveManagement(result)" title="Grave Management"><i class="icon-View-Burial-Record-Filled"></i></a></td>

      </tr>
    </tbody>
  </table>
</template>

<script lang='ts'>

import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import { Watch, Prop } from 'vue-property-decorator'
import constants from '@/global-static/constants.ts';
import { FEATURES_DATA } from '@/global-static/constants.ts';
import { messages } from '@/global-static/messages.js';
import FeatureTools from '@/mapmanagement/mixins/featureTools.ts';
import PersonMixin from '@/mapmanagement/mixins/personMixin.ts';

enum columnType { 
  section = "section_name",
  subsection = "subsection_name",
  graveNumber = "grave_number",
  layer = "graveplot_layer" }

/**
 * Class representing SearchResults_Graves component
 */
@Component
export default class SearchResults_Graves extends mixins(FeatureTools, PersonMixin) {

  @Prop() results;
  @Prop() currentSearchType;
  @Prop() searchConducted;
  @Prop() resultsHeight;

  columnTypeEnum = columnType;
  currentSort: columnType = this.columnTypeEnum.section;
  currentSortDir: string = "asc";

  /*** Computed ***/

  /**
   * Computed property
   * @returns {any} Returns angularjs person controller
   */
  get personController(): any {
    return (window as any).angular.element(document.querySelector("[ng-controller='personController as person']")).controller();
  }
  
  /**
   * Computed property: Sorts the results to users requirements
   * @returns Sorted results
   */
  get resultsSorted() {
    if (!this.results)
      return [];

    const modifier = this.currentSortDir === 'desc' ? -1 : 1;

    return this.results.sort((a,b) => {
      if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
      if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
      return 0;
    });
  }

  /**
   * @returns {boolean} True if including sections in results table
   */
  get includeSections(): boolean {
    const allSections = this.$store.state.allSections
    return allSections && allSections.length > 0;
  }

  /**
   * @returns {boolean} True if including subsections in results table
   */
  get includeSubsections(): boolean {
    const allSubsections = this.$store.state.allSubsections
    return allSubsections && allSubsections.length > 0;
  }
  

  /*** Watchers ***/


  /*** Methods ***/

  /**
   * @returns Array of centre coordinates for result's graveplots and memorials
   */
  getResultCentreCoordinates(result) {
    const memorials = result.memorials.map(y => y.memorial_uuid);
    const graves = result.graveplots.map(y => y.graveplot_uuid/*{
      if (y.graveplot_layer==='reserved_plot')
        return y.topopolygon_id;
      else
        y.graveplot_uuid;
    }*/);
    const features = memorials.concat(graves);
    return this.getFeaturesCentreCoordinate(features);
  }

  /**
   * Resets sort to default
   */
  resetSort() {
    this.currentSort = this.columnTypeEnum.section;
    this.currentSortDir = "asc";
  }

  /**
   * Changes results sorting depending on column clicked
   * @param {columnType}
   */
  sortResults(column: columnType){
    if (column === this.currentSort) {
      this.currentSortDir = this.currentSortDir==='asc'?'desc':'asc';
    }
    this.currentSort = column;
  }

  /**
   * Open management tool using router to display details for grave
   * @param result
   */
  openGraveManagement(result) {

    let params = { id: result.graveplot_uuid, layer: result.graveplot_layer };

    if (result.graveplot_layer==='available_plot') 
      params['availablePlotID'] = result.topopolygon_id;
  
    this.$router.replace({ name: constants.GRAVE_MANAGEMENT_PATH, params: params });
  }

  /**
   * Show person on map when click on result row
   * @param result
   */
  showGrave(result) {

    if (result.topopolygon_id) {
      const graves = [
        {
          'featureID': result.graveplot_uuid, 
          'layerName': result.graveplot_layer
        },
        {
          'featureID': result.topopolygon_id, 
          'layerName': result.graveplot_layer
        }
      ];

      const features = graves as [FEATURES_DATA];
      this.highlightFeaturesAndSetExtent('hightlighted-results', 'hightlighted-results', features, this.$store.state.MapLayers.layerStyles.selectedStyleFunction);
      //debugger; // eslint-disable-line no-debugger
      this.$store.commit('setStepNumber', 3);
    }
    else
      // if no topopolygon id, the grave does not have a topo, hence not on map
      this.$store.getters.notificationHelper.createErrorNotification(messages.search.unknowLocation.title);
  }

  /**
   * highlights the results on the map
   */
  highlightGraveplots(results = null) {

    if (!results)
      results = this.results;

    let graves = results.map(x => {
      let featureID = x.graveplot_uuid;

      if (x.graveplot_layer==='available_plot')
        featureID = x.topopolygon_id;

      return {
        'featureID': featureID, 
        'layerName': x.graveplot_layer
      }
    });
    
    graves = [].concat.apply([], graves);

    const features = graves as [FEATURES_DATA];
    this.highlightFeatures('hightlighted-results', 'hightlighted-results', features, this.$store.state.MapLayers.layerStyles.selectedStyleFunction);
  }

}
</script>
