<template>
  <div class="col-md-12 collapse-menu-results" :style="{ height: resultPanelHeight + 'px' }">
    <div class="search-results-div">
      <div ref="resultInfo" class="result-info">
        <div class="col-xs-6">
          <h5><strong>Total results: {{ resultsCount }}</strong></h5>
        </div>
        <div class="col-xs-6">
            <button title="Reset sort" type="button" class="btn sidebar-normal-button btn-bgms btn-form btn-xs" aria-label="Left Align" style="float: right;" @click="resetSort">
                <span class="fa fa-filter" aria-hidden="true" style="margin-right: 8px;"></span>
                <span class="fa fa-times" aria-hidden="true" style="font-size: 10px;position: absolute;top: 20px;right: 20px;"></span>
            </button>
        </div>
      </div>

      <SearchResultsPersons v-if="currentSearchType!==searchTypeEnum.grave" ref="personResultsComponent" :results="results" :currentSearchType="currentSearchType" :searchConducted="searchConducted" :resultsHeight="resultsHeight"></SearchResultsPersons>

      <SearchResultsGraves v-else ref="graveResultsComponent" :results="results" :currentSearchType="currentSearchType" :searchConducted="searchConducted" :resultsHeight="resultsHeight"></SearchResultsGraves>

    </div>
  </div>
</template>

<script lang='ts'>

import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import { Prop } from 'vue-property-decorator'
import constants from '@/global-static/constants.ts';
import { SEARCH_TYPE_ENUM } from '@/mapmanagement/static/constants.ts';
import { FEATURES_DATA } from '@/global-static/constants.ts';
import { messages } from '@/global-static/messages.js';
import FeatureTools from '@/mapmanagement/mixins/featureTools.ts';
import PersonMixin from '@/mapmanagement/mixins/personMixin.ts';

/**
 * Class representing SearchResults component
 */
@Component({
  components: {
    SearchResultsPersons: () => import('@/mapmanagement/components/Search/SearchResults_Persons.vue'),
    SearchResultsGraves: () => import('@/mapmanagement/components/Search/SearchResults_Graves.vue'),
  }
})
export default class SearchResults extends mixins(FeatureTools, PersonMixin) {

  @Prop() results;
  @Prop() currentSearchType;
  @Prop() searchConducted;
  @Prop() resultsCount;
  @Prop() showAdvanceSearch;

  searchTypeEnum = SEARCH_TYPE_ENUM;

  resultPanelHeight: number = 0;

  mounted() {
    // resizes panel when screen is resized
    (window as any).jQuery(window).on("resize.doResize", this.resizeResults);
  }

  /*** Computed ***/

  get authenticatedSession(): boolean {
    return this.$store.state.authenticatedSession;
  }

  /**
   * Computed property
   * @returns {string} Returns style for height of results
   */
  get resultsHeight(): string {
    if (!this.authenticatedSession)
      return this.showAdvanceSearch ? 'calc(100vh - 389px)' : 'calc(100vh - 284px)';
    
    return this.showAdvanceSearch ? 'calc(100vh - 546px)' : 'calc(100vh - 312px)';
  }

  /*** Methods ***/
  
  /**
   * Resizes the results panel depending on number of results found
   */
  resizeResults() {

    Vue.nextTick(() => {
      const com = (this.currentSearchType===this.searchTypeEnum.grave ? this.$refs.graveResultsComponent : this.$refs.personResultsComponent) as any;

      this.resultPanelHeight = 5 + (this.$refs["resultInfo"] as HTMLElement).clientHeight +
        (com.$refs.resultTHead as HTMLElement).clientHeight + (this.searchConducted ? (com.$refs.resultTBody as HTMLElement).clientHeight : 0);
    });
  }

  resetSort() {
    (this.$refs.personResultsComponent as any).resetSort;
  }

  highlightMemorialsAndGraveplots() {
    if (this.currentSearchType!==this.searchTypeEnum.grave)
      (this.$refs.personResultsComponent as any).highlightMemorialsAndGraveplots();
    else
      (this.$refs.graveResultsComponent as any).highlightGraveplots();
  }
}
</script>
