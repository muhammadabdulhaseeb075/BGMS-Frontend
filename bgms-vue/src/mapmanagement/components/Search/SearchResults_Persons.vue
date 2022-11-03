<template>
  <table id="table-search" :class="{ 'burial-table': currentSearchType===searchTypeEnum.burial, 'reservation-table': currentSearchType===searchTypeEnum.reservation, 'owner-table': currentSearchType===searchTypeEnum.owner }" class='table basic-search-results table-fixed borderless table-hover'>
    <thead ref="resultTHead">
      <tr>

        <th @click="sortResults(columnTypeEnum.name)" class="name-column">Name</th>
        <th v-show="currentSearchType===searchTypeEnum.burial" class="burial-date-column" @click="sortResults(columnTypeEnum.date)">Burial Date</th>
        <th v-show="currentSearchType===searchTypeEnum.burial" class="age-column string-min" @click="sortResults(columnTypeEnum.age)">Age</th>
        <th v-show="currentSearchType===searchTypeEnum.owner" class="address-column string-min" @click="sortResults(columnTypeEnum.address)">Address</th>
        <th class="link-column"/>

      </tr>
    </thead>
    <tbody v-if="searchConducted" ref="resultTBody" :style="{ 'max-height': resultsHeight }">
      <tr role="row" v-for="result in resultsSorted" :key="result.id" @mouseover="hoverPerson=result" @click="showPerson(result)">

        <td class="name-column">
          {{ formatResultName(result) }}</td>
        <td v-if="currentSearchType===searchTypeEnum.burial" class="burial-date-column">{{ showYearIfImpossibleMonthIsNotDefined(result) }}</td>
        <td v-if="currentSearchType===searchTypeEnum.burial" class="age-column string-min">{{ formatAgeYears(result.age_years, result.age_months, result.age_weeks, result.age_days, result.age_hours, result.age_minutes) }}</td>
        <td v-if="currentSearchType===searchTypeEnum.owner" class="address-column string-min">{{ formatAddress(result.addresses__first_line, result.addresses__town, result.addresses__postcode) }}</td>
        <td><a class="link-column burial-record" href="javascript:void(0)" @click.stop="openManagementTool(result)" title="Burial record"><i class="icon-View-Burial-Record-Filled"></i></a></td>

      </tr>
    </tbody>
  </table>
</template>

<script lang='ts'>

import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import { Watch, Prop } from 'vue-property-decorator'
import constants from '@/global-static/constants.ts';
import { SEARCH_TYPE_ENUM } from '@/mapmanagement/static/constants.ts';
import { FEATURES_DATA } from '@/global-static/constants.ts';
import { messages } from '@/global-static/messages.js';
import FeatureTools from '@/mapmanagement/mixins/featureTools.ts';
import PersonMixin from '@/mapmanagement/mixins/personMixin.ts';
import { formatName, getRoundedAge, formatDate, formatAgeYears, formatAddress } from '@/global-static/dataFormattingAndValidation.ts';

enum columnType { name, date, age, address }

/**
 * Class representing SearchResults_Persons component
 */
@Component
export default class SearchResults_Persons extends mixins(FeatureTools, PersonMixin) {

  @Prop() results;
  @Prop() currentSearchType;
  @Prop() searchConducted;
  @Prop() resultsHeight;

  formatDate = formatDate;
  formatAgeYears = formatAgeYears;
  formatAddress = formatAddress;

  columnTypeEnum = columnType;
  currentSort: columnType = this.columnTypeEnum.name;
  currentSortDir: string = "asc";

  searchTypeEnum = SEARCH_TYPE_ENUM;

  hoverPerson = null;
  showSearchHoverFlag: boolean = true;

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
    
    if (this.currentSort === this.columnTypeEnum.name) {
      return this.results.sort((a,b) => {
        if(a["last_name"] < b["last_name"]) return -1 * modifier;
        if(a["last_name"] > b["last_name"]) return 1 * modifier;
        if(a["first_names"] < b["first_names"]) return -1 * modifier;
        if(a["first_names"] > b["first_names"]) return 1 * modifier;
        if(a["burial_date"] < b["burial_date"]) return -1 * modifier;
        if(a["burial_date"] > b["burial_date"]) return 1 * modifier;
        return 0;
      });
    }
    else if (this.currentSort === this.columnTypeEnum.date) {
      return this.results.sort((a,b) => {
        if(a["burial_date"] < b["burial_date"]) return -1 * modifier;
        if(a["burial_date"] > b["burial_date"]) return 1 * modifier;
        return 0;
      });
    }
    else if (this.currentSort === this.columnTypeEnum.age) {
      return this.results.sort((a,b) => {
        if(a["age_years"] < b["age_years"]) return -1 * modifier;
        if(a["age_years"] > b["age_years"]) return 1 * modifier;
        if(a["age_months"] < b["age_months"]) return -1 * modifier;
        if(a["age_months"] > b["age_months"]) return 1 * modifier;
        if(a["age_weeks"] < b["age_weeks"]) return -1 * modifier;
        if(a["age_weeks"] > b["age_weeks"]) return 1 * modifier;
        if(a["age_days"] < b["age_days"]) return -1 * modifier;
        if(a["age_days"] > b["age_days"]) return 1 * modifier;
        if(a["age_hours"] < b["age_hours"]) return -1 * modifier;
        if(a["age_hours"] > b["age_hours"]) return 1 * modifier;
        if(a["age_minutes"] < b["age_minutes"]) return -1 * modifier;
        if(a["age_minutes"] > b["age_minutes"]) return 1 * modifier;
        return 0;
      });
    }
    else if (this.currentSort === this.columnTypeEnum.address) {
      return this.results.sort((a,b) => {
        if((!a["addresses__first_line"] && b["addresses__first_line"]) || a["addresses__first_line"] < b["addresses__first_line"]) return -1 * modifier;
        if((a["addresses__first_line"] && !b["addresses__first_line"]) || a["addresses__first_line"] > b["addresses__first_line"]) return 1 * modifier;
        if((!a["addresses__town"] && b["addresses__town"]) || a["addresses__town"] < b["addresses__town"]) return -1 * modifier;
        if((a["addresses__town"] && !b["addresses__town"]) || a["addresses__town"] > b["addresses__town"]) return 1 * modifier;
        if((!a["addresses__postcode"] && b["addresses__postcode"]) || a["addresses__postcode"] < b["addresses__postcode"]) return -1 * modifier;
        if((a["addresses__postcode"] !&& b["addresses__postcode"]) || a["addresses__postcode"] > b["addresses__postcode"]) return 1 * modifier;
        return 0;
      });
    }

    return this.results.sort((a,b) => {
      if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
      if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
      return 0;
    });
  }
  

  /*** Watchers ***/

  /**
   * Watcher: When a new person is hover over in results, this updates the map marker
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('hoverPerson')
  onHoverChanged(val: any, oldVal: any) {
    if (this.showSearchHoverFlag && val) {
      // show new hover details
      const centreCoordinates = this.getResultCentreCoordinates(val);
      this.personController.showSearchHover({ first_names: val.first_names, last_name: val.last_name }, centreCoordinates);
    }
  }


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
    this.currentSort = this.columnTypeEnum.name;
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
   * Formats name according to type of result
   */
  formatResultName(result): string {
    if (this.currentSearchType===SEARCH_TYPE_ENUM.owner && result.type==='company')
      return result.name;
    else
      return formatName(result.first_names, result.last_name)
  }

  /**
   * Open management tool using router to display details for person
   * @param result
   */
  openManagementTool(result) {

    // Prioritise memorial, then grave. If result is linked to neither then open memorial without id.
    if (this.currentSearchType===SEARCH_TYPE_ENUM.reservation) {
      // this is a reserved person
      if (result.graveplots[0].graveplot_layer==="reserved_plot" && result.graveplots[0].topopolygon_id)
        // this is a reserved plot
        this.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.reservations, params: { id: result.graveplots[0].graveplot_uuid, layer: 'reserved_plot', availablePlotID: result.graveplots[0].topopolygon_id, personID: result.id }});
      else
        this.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.reservations, params: { id: result.graveplots[0].graveplot_uuid, layer: 'plot', personID: result.id }});
    }
    else if (this.currentSearchType===SEARCH_TYPE_ENUM.owner) {
      if (result.type==='person')
        // this is a person owner
        this.$router.replace({ name: constants.PERSON_MANAGEMENT_CHILD_ROUTES.persondetails, params: { id: result.id }});
      else
        // this is a company owner
        this.$router.replace({ name: constants.COMPANY_MANAGEMENT_CHILD_ROUTES.companydetails, params: { id: result.id }});
    }
    else if (result.memorials.length > 0)
      this.$router.replace({ name: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.persons, params: { id: result.memorials[0].memorial_uuid, person_id: result.id, layer: result.memorials[0].memorial_layer, burial_id: result.first_burial_id }});
    else if (result.graveplots.length > 0)
      this.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.burials, params: { id: result.graveplots[0].graveplot_uuid, person_id: result.id, layer: 'plot', burial_id: result.first_burial_id }});
    else
      this.$router.replace({ name: constants.BURIAL_PERSON_MANAGEMENT_CHILD_ROUTES.person, params: { id: result.id, person_id: result.id, burial_id: result.first_burial_id }});
  }

  /**
   * Show person on map when click on result row
   * @param result
   */
  showPerson(result) {    
    this.showSearchClick(result);

    const memorials = result.memorials.map(y => {
      return {
        'featureID': y.memorial_uuid, 
        'layerName': y.memorial_layer
      }
    });

    const graves = result.graveplots.map(y => {
      return {
        'featureID': y.graveplot_uuid, 
        'layerName': y.graveplot_layer
      }
    });

    const features = memorials.concat(graves) as [FEATURES_DATA];
    this.highlightFeaturesAndSetExtent('hightlighted-results', 'hightlighted-results', features, this.$store.state.MapLayers.layerStyles.selectedStyleFunction);
    this.$store.commit('setStepNumber', 3);
  }

  /**
   * @function
   * @description
   * Pan's to memorial and shows information box.
   */
  showSearchClick(result){
    // only show first available feature
    let featureID = null;
    let centreCoordinate = null;

    if (result.memorials && result.memorials.length > 0) {
      for (let memorial of result.memorials) {
        centreCoordinate = this.getFeatureCentreCoordinate(memorial.memorial_uuid);
        if (centreCoordinate) {
          featureID = memorial.memorial_uuid;
          break;
        }
      }
    }

    if (!featureID && result.graveplots && result.graveplots.length > 0) {
      for (let grave of result.graveplots) {
        centreCoordinate = this.getFeatureCentreCoordinate(grave.graveplot_uuid);
        if (centreCoordinate) {
          featureID = grave.graveplot_uuid;
          break;
        }
      }
    }

    if(featureID){
      let person = {
        first_names: result.first_names,
        last_name: result.last_name,
        burial_date: result.burial_date,
        grave_id: result.graveplots && result.graveplots.length ? result.graveplots[0].graveplot_uuid : '',
        age: getRoundedAge(result.age_years, result.age_months, result.age_weeks, result.age_days, result.age_hours, result.age_minutes)
      };
      let template = this.createSingleFeatureClickTemplate(person);
      this.personInteractionService.featureOverlays['searched-memorials'].removeAllFeatures();
      this.showClickDetails(centreCoordinate, featureID, template, template.scope['closeHandler']);
    }
    else
      this.$store.getters.notificationHelper.createErrorNotification(messages.search.unknowLocation.title);
  }

  /**
   * @returns Template for single feature basic details box
   */
  createSingleFeatureClickTemplate(person) {
    if(person){
      this.showSearchHoverFlag = false;

      person['closeHandler'] = () => {
        this.personInteractionService.hideClickDetails();
        this.highlightMemorialsAndGraveplots();
        this.showSearchHoverFlag = true;
      };
      
      if (this.currentSearchType===SEARCH_TYPE_ENUM.burial)
        person['burial'] = true;

      let template = {
        component: "BasicDetailsMarker",
        scope: person
      }
      return template;
    }
  }

  /**
   * highlights the results on the map
   */
  highlightMemorialsAndGraveplots() {
    // remove any open click details
    this.closeClickDetails();

    let memorials = this.results.map(x => { 
      return x.memorials.map(y => {
        return {
          'featureID': y.memorial_uuid, 
          'layerName': y.memorial_layer
        }
      }) 
    });

    memorials = [].concat.apply([], memorials);

    let graves = this.results.map(x => { 
      return x.graveplots.map(y => {
        return {
          'featureID': y.graveplot_uuid, 
          'layerName': y.graveplot_layer
        }
      }) 
    });
    
    graves = [].concat.apply([], graves);

    const features = memorials.concat(graves) as [FEATURES_DATA];
    this.highlightFeatures('hightlighted-results', 'hightlighted-results', features, this.$store.state.MapLayers.layerStyles.selectedStyleFunction);
  }

  readonly YEAR = 0;
  showYearIfImpossibleMonthIsNotDefined(person) {
    if(!person.has_impossible_month && person.burial_date){
      return person.burial_date.split('-')[this.YEAR];
    } else {
      return formatDate(person.burial_date)
    }
  }

}
</script>
