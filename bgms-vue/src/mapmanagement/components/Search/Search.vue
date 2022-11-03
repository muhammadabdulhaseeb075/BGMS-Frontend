<template>
  <div v-show="!exportMapOpen" id="search-panel">
    <div id="container-left-menu" class="collapse-menu">
      <div class="offline-message" v-if="!online">
        <h1>You are offline</h1>
        <h2>Search is not available while offline.</h2>
      </div>
      <div id="search" v-else>

        <ul id="search-tabs" class="row" v-if="authenticatedSession">
          <li :style="includeGravesInSearch ? { 'width': '22%' } : { 'width': '33%' }" :readonly="searchInProgressFlag" @click="toggleTabs(searchTypeEnum.burial)" v-if="!isBacasEnabled">
            <a :class="{ active: currentSearchType===searchTypeEnum.burial }">Burials</a>
          </li>
          <li style="width: 34%" :readonly="searchInProgressFlag" @click="toggleTabs(searchTypeEnum.reservation)"  v-if="!isBacasEnabled">
            <a :class="{ active: currentSearchType===searchTypeEnum.reservation }">Reservations</a>
          </li>
          <li :style="includeGravesInSearch ? { 'width': '22%' } : { 'width': '33%' }" :readonly="searchInProgressFlag" @click="toggleTabs(searchTypeEnum.owner)" v-if="!isBacasEnabled">
            <a :class="{ active: currentSearchType===searchTypeEnum.owner }">Owners</a>
          </li>
          <li v-if="includeGravesInSearch && !isBacasEnabled" style="width: 22%" :readonly="searchInProgressFlag" @click="toggleTabs(searchTypeEnum.grave)">
            <a :class="{ active: currentSearchType===searchTypeEnum.grave }">Graves</a>
          </li>
        </ul>

        <v-col cols="12" class="py-0">
          <div class="sidebar-form sidebar-offcanvas input-group">
            <form class="search-form" id="search-form" @submit.prevent="beginSearch" autocomplete="off">
              <div v-if="currentSearchType!==searchTypeEnum.grave">
                <v-row>
                  <v-col cols="12" class="fieldWrapper form-group floating-label-form-group px-4 py-0">
                    <label for="first-names-field">First name(s)</label>
                    <input id="first-names-field" type="text" class="form-control form-field" placeholder="First name(s)" maxlength="200" v-model="firstNames" autofocus>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" class="fieldWrapper form-group floating-label-form-group px-4 py-0">
                    <label for="last-name-field">Last name</label>
                    <input id="last-names-field" type="text" class="form-control form-field" placeholder="Last name" maxlength="35" v-model="lastName">
                  </v-col>
                </v-row>
                <v-row v-show="currentSearchType===searchTypeEnum.owner">
                  <v-col cols="12" class="fieldWrapper form-group floating-label-form-group px-4 py-0">
                    <label for="company-name-field">Company name</label>
                    <input id="company-name-field" type="text" class="form-control form-field" placeholder="Company name" maxlength="200" v-model="companyName">
                  </v-col>
                </v-row>
                <v-row class="pr-4 pt-1">
                  <v-spacer></v-spacer>
                  <label id='advanced-search-button' class="btn btn-bgms btn-form advanced-search-expand" title="Advance search" @click="showOrHideAdvancedSearch()">
                    <span>{{ showAdvanceSearch ? 'Less ' : 'More ' }}</span>
                    <span :class="[ 'glyphicon', showAdvanceSearch ? 'glyphicon-chevron-up' : 'glyphicon-chevron-down' ]"/>
                  </label>
                </v-row>
              </div>

              <div id="advanced-search-section" v-show="showAdvanceSearch || currentSearchType===searchTypeEnum.grave">
                
                <v-row v-show="currentSearchType===searchTypeEnum.owner">
                  <v-col cols="12" class="fieldWrapper form-group floating-label-form-group px-4 py-0">
                    <label for="email-field">Email</label>
                    <input id="email-field" type="text" class="form-control form-field" placeholder="Email" maxlength="254" v-model="email">
                  </v-col>
                </v-row>

                <section v-show="currentSearchType===searchTypeEnum.burial">
                  <div class="row">
                    <div class="fieldWrapper form-group col-xs-6 floating-label-form-group">
                      <label for="age-from-field">Age (from)</label>
                      <input id="age-from-field" type="number" class="form-control form-field" placeholder="Age (from)" min="0" max="150" step="1" v-model="ageFrom">
                    </div>
                    <div class="fieldWrapper form-group col-xs-6 floating-label-form-group">
                      <label for="age-to-field">Age (to)</label>
                      <input id="age-to-field" type="number" class="form-control form-field" placeholder="Age (to)" min="0" max="150" step="1" v-model="ageTo">
                    </div>
                  </div>
                  <div id="year_burial_date_range" class="row" v-if="!specificBurialDate">
                    <div class="fieldWrapper form-group col-xs-6 floating-label-form-group">
                      <label for="burial-year-from-field">Burial year (from)</label>
                      <input id="burial-year-from-field" type="number" class="form-control form-field" placeholder="Burial year (from)" min="0001" max="9999" step="1" v-model="burialYearFrom">
                    </div>
                    <div class="fieldWrapper form-group col-xs-6 floating-label-form-group">
                      <label for="burial-year-to-field">Burial year (to)</label>
                      <input id="burial-year-to-field" type="number" class="form-control form-field" placeholder="Burial year (to)" min="0001" max="9999" step="1" v-model="burialYearTo">
                    </div>
                  </div>
                  <div id="burial_date_range" class="row" v-if="specificBurialDate">
                    <div class="fieldWrapper form-group col-xs-6 floating-label-form-group">
                      <label for="burial-date-from-field">Date of burial (from)</label>
                      <input id="burial-date-from-field" type="text" onfocus="(this.type='date')" class="form-control form-field" placeholder="Date of burial (from)" v-model="burialDateFrom">
                    </div>
                    <div class="fieldWrapper form-group col-xs-6 floating-label-form-group">
                      <label for="burial-date-to-field">Date of burial (to)</label>
                      <input id="burial-date-to-field" type="text" onfocus="(this.type='date')" class="form-control form-field" placeholder="Date of burial (to)" v-model="burialDateTo">
                    </div>
                  </div>
                  <div class="specific-date row" >
                    <div class="col-xs-12" >
                      <div class="checkbox">
                        <label>
                          <span>
                            <input id="specific-date-check" class="simple" type="checkbox" v-model="specificBurialDate">
                            Specific date of burial?
                          </span>
                        </label>
                      </div>
                    </div>
                  </div>
                  <v-row v-if="authenticatedSession && memorialLayers">
                    <v-col cols="12" :class="[{'floating-label-form-group-with-value': graveLayer}, 'fieldWrapper', 'form-group', 'px-4', 'py-0', 'floating-label-form-group model-list-select']">
                      <label class="control-label" for="memorial-layer">Memorial type:</label>

                      <div id="memorial-layer" class="model-list-select-div model-list-select-div-12" @keyup.delete="memorialLayer=''">
                        <model-list-select :list="memorialLayers"
                          v-model="memorialLayer"
                          option-value="layer_id"
                          option-text="display_name"
                          placeholder="All Memorial Types">
                        </model-list-select>
                      </div>
                    </v-col>
                  </v-row>
                </section>

                <section v-if="authenticatedSession" v-show="currentSearchType===searchTypeEnum.burial || currentSearchType===searchTypeEnum.reservation || currentSearchType===searchTypeEnum.grave">
                  
                  <v-row class="row" v-show="currentSearchType===searchTypeEnum.grave">
                    <v-col cols="12" :class="[{'floating-label-form-group-with-value': graveLayer}, 'fieldWrapper', 'form-group', 'px-4', 'py-0', 'floating-label-form-group model-list-select']" v-show="!isBacasEnabled">
                      <label class="control-label" for="memorial-layer">Grave type:</label>
                      <div id="grave-layer" class="model-list-select-div model-list-select-div-12" @keyup.delete="graveLayer=''">
                        <model-list-select :list="graveLayers"
                          v-model="graveLayer"
                          option-value="key"
                          option-text="text"
                          placeholder="All Grave Types">
                        </model-list-select>
                      </div>
                    </v-col>
                  </v-row>

                  <div class="loadingGraveID" v-show="loadingSections || loadingSubsections">
                    <i class="fa fa-spinner fa-spin"></i>
                    <p>Loading grave sections</p>
                  </div>

                  <div class="row">
                    <div :class="[{'floating-label-form-group-with-value': selectedSection}, 'fieldWrapper', 'form-group', 'col-xs-6', 'floating-label-form-group model-list-select']" v-if="allSections && allSections.length > 0">
                      <label for="section">Section:</label>
                      <div id="section" class="model-list-select-div" @keyup.delete="selectedSection=''">
                        <model-list-select :list="allSections"
                          v-model="selectedSection"
                          option-value="id"
                          option-text="section_name"
                          placeholder="Section">
                        </model-list-select>
                      </div>
                    </div>
                    <div :class="[{'floating-label-form-group-with-value': selectedSubsection}, 'fieldWrapper', 'form-group', 'col-xs-6', 'floating-label-form-group model-list-select']" v-if="allSubsections && allSubsections.length > 0">
                      <label for="subsection">Subsection:</label>
                      <div id="subsection" class="model-list-select-div" @keyup.delete="selectedSubsection=''">
                        <model-list-select :list="allSubsectionsFiltered"
                          v-model="selectedSubsection"
                          option-value="id"
                          option-text="subsection_name"
                          placeholder="Subsection"
                          :isDisabled="allSubsectionsFiltered.length === 0">
                        </model-list-select>
                      </div>
                    </div>

                    <div class="floating-label-form-group fieldWrapper form-group col-xs-6 model-list-select">
                      <label for="grave-numbers">Grave number:</label>
                      <div id="grave-numbers" class="model-list-select-div">
                        <input type="text" class="col-xs-7 form-control form-field" placeholder="Grave number" v-model="enteredGraveNumber">
                      </div>
                    </div>
                  </div>
                </section>
              </div>

              <div class="row">
                <div class="fieldWrapper form-group col-xs-2 floating-label-form-group search-button">
                  <button title="Clear" type="button" class="btn sidebar-normal-button btn-bgms btn-form" aria-label="Left Align" style="float: left;" @click="clearSearhForm">
                  <span class="icon-Clear-02-Filled" aria-hidden="true"></span>
                </button>
                </div>
                <div class="fieldWrapper form-group col-xs-8 fuzzy-container">
                  <input id="id_fuzzy_value" type="range" min="75" max="100" step="5" v-model="fuzzyValue" class="input-range"/>
                  <span>Broad</span>
                  <span style="float: right;">Exact</span>
                </div>
                <div class="fieldWrapper form-group col-xs-2 floating-label-form-group search-button">
                  <button type="submit" title="Search" class="btn sidebar-normal-button btn-bgms btn-form ladda-button" data-style="slide-right" aria-label="Left Align" style="float: right;">
                    <span class="ladda-label icon-Search-Filled" aria-hidden="true"></span>
                  </button>
                </div>
              </div>
            </form>

          </div>
        </v-col>

        <SearchResults ref="resultsComponent" v-if="loadResultsComponent" v-show="searchConducted" :results="results" :currentSearchType="currentSearchType" :searchConducted="searchConducted" :resultsCount="resultsCount" :showAdvanceSearch="showAdvanceSearch"></SearchResults>
        
      </div>
    </div>
  </div>
</template>

<script lang='ts'>

import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import axios from 'axios';
import * as Ladda from 'ladda';
require('ladda/dist/ladda.min.css');
import GraveLocation from '@/mixins/graveLocation.ts';
import FeatureTools from '@/mapmanagement/mixins/featureTools.ts';
import PersonMixin from '@/mapmanagement/mixins/personMixin.ts';
import { FEATURES_DATA } from '@/global-static/constants.ts';
import { formatName, formatAgeYears, getRoundedAge, formatAddress } from '@/global-static/dataFormattingAndValidation.ts';
import { messages } from '@/global-static/messages.js';
import { SEARCH_TYPE_ENUM } from '@/mapmanagement/static/constants.ts';

enum searchType { burial = 'burial', reservation = 'reservation', owner = 'owner' }
enum columnType { name, date, age, address }

/**
 * Class representing Search component
 */
@Component({
  components: {
    SearchResults: () => import('@/mapmanagement/components/Search/SearchResults.vue'),
  }
})
export default class Search extends mixins(GraveLocation, PersonMixin, FeatureTools){

  formatAgeYears = formatAgeYears;
  formatAddress = formatAddress;

  showAdvanceSearch: boolean = false;
  specificBurialDate: boolean = false;
  loadResultsComponent: boolean = false;

  searchTypeEnum = SEARCH_TYPE_ENUM;
  currentSearchType: SEARCH_TYPE_ENUM = SEARCH_TYPE_ENUM.burial;

  personService = this.$store.getters.personService;
  notificationHelper: any = this.$store.getters.notificationHelper;
  markerService: any = this.$store.getters.markerService;

  searchInProgressFlag: boolean = false;

  /**
   * Form fields
   */
  firstNames: string = "";
  lastName: string = "";
  companyName: string = "";
  email: string = "";
  ageFrom: number = null;
  ageTo: number = null;
  burialYearFrom: number = null;
  burialYearTo: number = null;
  burialDateFrom: Date = null;
  burialDateTo: Date = null;
  memorialLayer: number = null;
  graveLayer: number = null;
  fuzzyValue: number = 100;

  burialSearchConducted: boolean = false;
  reservationSearchConducted: boolean = false;
  ownerSearchConducted: boolean = false;
  graveSearchConducted: boolean = false;

  burialResultsCount: number = 0;
  reservationResultsCount: number = 0;
  ownerResultsCount: number = 0;
  graveResultsCount: number = 0;

  burialResults = [];
  reservationResults = [];
  ownerResults = [];
  graveResults = [];

  graveLayers = [
    {
      key: 'available_plot',
      text: 'Available'
    },
    {
      key: 'plot',
      text: 'Burial'
    },
    {
      key: 'reserved_plot',
      text: 'Reserved'
    }
  ]

   /**
    * Vue mounted lifecycle hook
    * - loads memorial layers if needed
    * - listens for screen resize
    */
  mounted() {
    //currentSearchType: SEARCH_TYPE_ENUM = SEARCH_TYPE_ENUM.burial;
    if(this.isBacasEnabled){
      this.currentSearchType = SEARCH_TYPE_ENUM.grave;
    }

    // this will load results component so we don't have to wait for it later on
    this.loadResultsComponent = true;
    const returnLink = this.$store.state.returnLink;
    if(returnLink != "" && returnLink !== undefined){
      const SearchMenuDiv = document.getElementById("container-left-menu");
      SearchMenuDiv.style.cssText += "top: 30px !important;"; 
    }else{
       const SearchMenuDiv = document.getElementById("container-left-menu");
        if(SearchMenuDiv.style.cssText.includes("top: 30px !important;")){
          SearchMenuDiv.style.cssText.replace("top: 30px !important;", ""); 
        }
    }
  }

   /**
    * Vue destroyed lifecycle hook
    * - removes grave highlights on close
    */
  destroyed() {
    this.clearSearhForm();
  }

  /*** Computed ***/

  get includeGravesInSearch() {
    return this.$store.state.includeGravesInSearch;
  }

  get searchConducted(): boolean {
    if (this.currentSearchType===SEARCH_TYPE_ENUM.burial)
      return this.burialSearchConducted;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.reservation)
      return this.reservationSearchConducted;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.owner)
      return this.ownerSearchConducted;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.grave)
      return this.graveSearchConducted;
    
    return null;
  }
  set searchConducted(value: boolean) {
    if (this.currentSearchType===SEARCH_TYPE_ENUM.burial)
      this.burialSearchConducted = value;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.reservation)
      this.reservationSearchConducted = value;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.owner)
      this.ownerSearchConducted = value;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.grave)
      this.graveSearchConducted = value;
  }

  /**
   * Computed property:
   * @returns {number} Number of results for the selected tab
   */
  get resultsCount(): number {
    if (this.currentSearchType===SEARCH_TYPE_ENUM.burial)
      return this.burialResultsCount;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.reservation)
      return this.reservationResultsCount;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.owner)
      return this.ownerResultsCount;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.grave)
      return this.graveResultsCount;
    
    return 0;
  }
  set resultsCount(value: number) {
    if (this.currentSearchType===SEARCH_TYPE_ENUM.burial)
      this.burialResultsCount = value;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.reservation)
      this.reservationResultsCount = value;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.owner)
      this.ownerResultsCount = value;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.grave)
      this.graveResultsCount = value;
  }

  /**
   * Computed property:
   * @returns Results for the selected tab
   */
  get results() {
    if (this.currentSearchType===SEARCH_TYPE_ENUM.burial)
      return this.burialResults;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.reservation)
      return this.reservationResults;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.owner)
      return this.ownerResults;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.grave)
      return this.graveResults;
    
    return null;
  }
  set results(value) {
    if (this.currentSearchType===SEARCH_TYPE_ENUM.burial)
      this.burialResults = value;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.reservation)
      this.reservationResults = value;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.owner)
      this.ownerResults = value;
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.grave)
      this.graveResults = value;
  }

  /**
   * Computed property: Get online status
   * @returns {boolean} True if online
   */
  get online(): boolean {
    return this.$store.state.Offline.online;
  }

  /**
   * Computed property
   * @returns {boolean} True if export map is open
   */
  get exportMapOpen(): boolean {
    return this.$store.state.exportMapOpen;
  }

  /**
   * Computed property: Get the available memorial layers
   * @returns {any} memorial layers
   */
  get memorialLayers() {
    return this.$store.state.memorialLayers;
  }

  //Return true if site is using BACAS API integration
  get isBacasEnabled(): boolean {
    return this.$store.state.isBacasEnabled;
  } 

  get authenticatedSession(): boolean {
    return this.$store.state.authenticatedSession;
  }

  /*** Methods ***/

  /**
   * Shows/hides advanced search fields
   */
  showOrHideAdvancedSearch() {
    this.showAdvanceSearch = !this.showAdvanceSearch;
    this.changeResultsComponent(false);
  }
  
  /**
   * Clear the search form
   */
  clearSearhForm() {
    this.firstNames = "";
    this.lastName = "";
    this.companyName = "";
    this.email = "";
    this.ageFrom = null;
    this.ageTo = null;
    this.burialYearFrom = null;
    this.burialYearTo = null;
    this.burialDateFrom = null;
    this.burialDateTo = null;
    this.memorialLayer = null;
    this.graveLayer = null;
    this.enteredGraveNumber = "";
    this.selectedSection = "";
    this.selectedSubsection = "";
    
    this.burialSearchConducted = false;
    this.reservationSearchConducted = false;
    this.ownerSearchConducted = false;
    this.graveSearchConducted = false;

    this.burialResultsCount = 0;
    this.reservationResultsCount = 0;
    this.ownerResultsCount = 0;
    this.graveResultsCount = 0;

    this.burialResults = [];
    this.reservationResults = [];
    this.ownerResults = [];
    this.graveResults = [];

    // removes grave highlights
    this.clearHighlight();
    this.closeClickDetails();
    this.markerService.removeMarkersByGroup('person-hover');
  }

  /**
   * Send search request to server and display results
   */
  beginSearch() {
    this.searchConducted = false;

    this.searchInProgressFlag = true;
    let l = Ladda.create( document.querySelector( '.ladda-button' ) );
    l.start();

    let params = {};

    params['search_type'] = this.currentSearchType;
    
    if (this.currentSearchType!==SEARCH_TYPE_ENUM.grave) {
      if (this.firstNames)
        params["first_names"] = "'" + this.firstNames + "'";
      if (this.lastName)
        params["last_name"] = "'" + this.lastName + "'";

      if (this.currentSearchType===SEARCH_TYPE_ENUM.owner) {
        if (this.companyName)
          params["company_name"] = "'" + this.companyName + "'";
        if (this.email)
          params["email"] = this.email;
      }

      if (this.currentSearchType===SEARCH_TYPE_ENUM.burial) {
        if (this.ageFrom)
          params["age"] = this.ageFrom;
        if (this.ageTo)
          params["age_to"] = this.ageTo;
        
        if (this.specificBurialDate) {
          if (this.burialDateFrom)
            params["burial_date"] = this.burialDateFrom;
          if (this.burialDateTo)
            params["burial_date_to"] = this.burialDateTo;
        }
        else {
          if (this.burialYearFrom)
            params["burial_date"] = (new Date(this.burialYearFrom,1,1)).toISOString().substring(0, 10);
          if (this.burialYearTo)
            params["burial_date_to"] = (new Date(this.burialYearTo,12,31)).toISOString().substring(0, 10);
        }

        if (this.memorialLayer)
          params["memorial_types"] = this.memorialLayer;
      }
    }
    
    if (this.currentSearchType===SEARCH_TYPE_ENUM.burial || this.currentSearchType===SEARCH_TYPE_ENUM.reservation || this.currentSearchType===SEARCH_TYPE_ENUM.grave) {

      if (this.currentSearchType===SEARCH_TYPE_ENUM.grave && this.graveLayer)
        params["graveplot_layer"] = this.graveLayer;

      // get the grave ref details if entered
      if (this.enteredGraveNumber)
        params["graveplot_grave_number"] = this.enteredGraveNumber;
      if (this.selectedSection)
        params["section_id"] = this.selectedSection;
      if (this.selectedSubsection)
        params["subsection_id"] = this.selectedSubsection;
    }

    if (params == {}) {
      this.notificationHelper.createWarningNotification("Please enter search criteria.");
      return;
    }
    
    params["fuzzy_value"] = this.fuzzyValue;

    axios.get('/mapmanagement/mapSearch/', { params: params })
      .then(response => {
        console.log(response);

        this.results = response.data;
        this.resultsCount = this.results.length;

        //show results in table
        this.searchConducted = true;
        //debugger; // eslint-disable-line no-debugger
        this.$store.commit('setStepNumber', 2);
        this.changeResultsComponent();
      })
      .catch(error => {
        console.warn(error);
      })
      .finally(() => {
        l.stop();
        l.remove();
        this.searchInProgressFlag = false;
      });
  }

  /**
   * Toggles search tab and resizes results window accordingly
   */
  toggleTabs(newTab: SEARCH_TYPE_ENUM) {
    if (newTab!==this.currentSearchType) {
      this.currentSearchType = newTab;
      this.markerService.removeMarkersByGroup('person-hover');

      this.changeResultsComponent();
    }
  }

  /**
   * Resizes the results component if it is open
   * @param showResultsOnMap Highlight results on map if true
   */
  changeResultsComponent(showResultsOnMap = true) {
    if (this.loadResultsComponent && this.searchConducted)
      Vue.nextTick(() => {
        (this.$refs.resultsComponent as any).resizeResults();

        if (showResultsOnMap)
          // show results on map
          (this.$refs.resultsComponent as any).highlightMemorialsAndGraveplots();
      });
  }

  /**
   * Clear results highlights on the map
   */
  clearHighlight() {
    this.highlightFeatures('hightlighted-results', 'hightlighted-results');
  }
}
</script>
