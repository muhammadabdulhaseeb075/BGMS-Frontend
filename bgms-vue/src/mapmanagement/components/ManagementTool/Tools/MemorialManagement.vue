<template>
  <div id="memorialManagementComponent" class="management-tool-buttons-container">
    <ul class="management-tool-buttons" v-if="$route.params.id && subbuttons && subbuttonNames">
      <div v-if="graveplot_list != undefined && graveplot_list.length > 0">
        <li v-for="item in graveplot_list" v-bind:key="item" class="management-tool-buttons-identifier"
          style="line-height: 20px; background-color: #f1e7b1;">
          <div class="burial-official-type">{{item}}</div>
        </li>
      </div>
      <li class="top-border" @click="toggleSubbuttons(subbuttonNames.PERSONSUBBUTTONS)">
        <a href="javascript:void(0)" :class="{ active: subbuttons[this.subbuttonNames.PERSONSUBBUTTONS].show }"><span>Persons</span></a>
      </li>
      <div class="management-tool-subbuttons">
        <transition name="list">
          <ul v-show="subbuttons[this.subbuttonNames.PERSONSUBBUTTONS].show && !loadingPersons">
            <li v-if="siteAdminOrSiteWarden" @click="openCloseAddPerson()">
              <a href="javascript:void(0)" class="add-new" :class="{ active: ($route.name===memorialManagementChildRoutesEnum.addPerson) }"><i class="fas fa-plus"/> Add New</a>
            </li>

            <li v-for="person in componentData" :key="person.person_id" :class="{ active: $route.params.person_id === person.person_id }">
              <a href="javascript:void(0)" @click="openClosePerson(person.person_id)">{{person.display_name}}</a>
            </li>

          </ul>
        </transition>
        <ul v-show="subbuttons[this.subbuttonNames.PERSONSUBBUTTONS].show && loadingPersons" class="loading-placeholder-contents">
          <li><i class="fa fa-spinner fa-spin"/></li>
        </ul>
      </div>
      
      <router-link v-if="authenticatedSession" tag="li" class="top-border" :to="openOrCloseChildRoute(managementToolRoute, memorialManagementChildRoutesEnum.memorialDetails)">
        <a :class="{ active: isRouteActive(memorialManagementChildRoutesEnum.memorialDetails) }">Details</a>
      </router-link>

      <!-- <router-link v-if="authenticatedSession && featureExistsOnMap" tag="li" class="top-border" :to="openOrCloseChildRoute(managementToolRoute, memorialManagementChildRoutesEnum.memorialGeometry)">
        <a :class="{ active: isRouteActive(memorialManagementChildRoutesEnum.memorialGeometry) }">Geometry</a>
      </router-link> -->
      
      <router-link tag="li" class="top-border" :to="openOrCloseChildRoute(managementToolRoute, memorialManagementChildRoutesEnum.photos)">
        <a :class="{ active: isRouteActive(memorialManagementChildRoutesEnum.photos) }">Photos</a>
      </router-link>
      
      <router-link v-if="authenticatedSession" tag="li" class="top-border" :to="openOrCloseChildRoute(managementToolRoute, memorialManagementChildRoutesEnum.linkedGraves, [{ name: 'linkToGraveProp', value: true }, { name: 'showLabelProp', value: true }, { name: 'selectFlagProp', value: false }])">
        <a :class="{ active: isRouteActive(memorialManagementChildRoutesEnum.linkedGraves) }">Graves</a>
      </router-link>

      <router-link v-if="authenticatedSession && attributesExist" tag="li" class="top-border" :to="openOrCloseChildRoute(managementToolRoute, memorialManagementChildRoutesEnum.attributes)">
        <a :class="{ active: isRouteActive(memorialManagementChildRoutesEnum.attributes) }">Attributes</a>
      </router-link>

      <SurveyButtons v-if="authenticatedSession" :key="surveyKey" :managementToolRoute="managementToolRoute" :surveysRoute="memorialManagementChildRoutesEnum.surveys" :showSurveySubbuttons="subbuttons[subbuttonNames.SURVEYSUBBUTTONS].show" @toggle_survey_subbuttons="toggleSubbuttons"/>

    </ul>
    <div id="management-tool-contentbar-container">
      <router-view id="management-tool-contentbar" :class="{ 'component-container': (isRouteActive(memorialManagementChildRoutesEnum.photos) || isRouteActive(memorialManagementChildRoutesEnum.linkedGraves)), 'photosComponent': isRouteActive(memorialManagementChildRoutesEnum.photos) }"></router-view>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import Component, { mixins } from 'vue-class-component'
import axios from 'axios'
import { Watch } from 'vue-property-decorator'
import constants from '@/global-static/constants.ts';
import SurveyButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/SurveyButtons.vue';
import FeatureTools from '@/mapmanagement/mixins/featureTools.ts'
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin.ts';
import SubbuttonsMixin from '@/mapmanagement/mixins/subbuttonsMixin.ts';
import View from "ol/View";

Vue.use(Vuex);

/**
 * Class representing MemorialManagement
 * @extends ManagementToolsMixin mixin
 * @extends FeatureTools mixin
 * @extends SubbuttonsMixin mixin
 */
@Component({
  components: {
    ContentContainer: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/ContentContainer.vue'),
    SurveyButtons
  }
})
export default class MemorialManagement extends mixins(ManagementToolsMixin, FeatureTools, SubbuttonsMixin) {
  
  memorialManagementChildRoutesEnum = constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES;

  loadingPersons = false;
  attributesExist: boolean = false;
  featureExistsOnMap: boolean = false;

  surveyKey: number = 0;

  authenticatedSession: boolean = this.$store.state.authenticatedSession;
  graveplot_list = []
  zoomIn: string | string[];

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    let v = this;

    this.zoomIn = v.$route.query['zoomIn'];
    this.componentName = "memorialmanagement";
    this.$store.commit('setTitle', "Memorial");

    this.managementToolRoute = constants.MEMORIAL_MANAGEMENT_PATH;

    this.$set(this.subbuttons, this.subbuttonNames.PERSONSUBBUTTONS, { show: false, route: this.memorialManagementChildRoutesEnum.persons });
    this.$set(this.subbuttons, this.subbuttonNames.SURVEYSUBBUTTONS, { show: false, route: this.memorialManagementChildRoutesEnum.surveys });

    this.newMemorialSelected(this.$route.params.id);

     if (this.zoomIn) {
        const dataExtent = this.$store.state.ExportMap.mapDataExtend;
        if (dataExtent) {
          (window as any).OLMap.setView(new View({
            center: [(dataExtent[0] + dataExtent[2]) / 2, (dataExtent[1] + dataExtent[3]) / 2],
            zoom: 7,
            extent: dataExtent,
            constrainOnlyCenter: true,
            resolutions: [6.999999999999999, 2.8, 1.4, 0.7, 0.28, 0.14, 0.07, 0.028, 0.014, 0.007, 0.0028],
          }))
        }
      this.newMemorialSelected(this.$route.params.id);
    }

    if (this.authenticatedSession) {
      axios.get('/mapmanagement/featureAttributesExist/?memorial_id=' + v.$route.params.id)
      .then((response) => {
        if (response.data.attributesFound)
          this.attributesExist = true;
      });
    }

    axios.get('/mapmanagement/graveLinks/?memorial_uuid=' + v.$route.params.id)
      .then(response => {
        if(response.data && response.data.graveplot_memorials) {
          for (const graveplot of response.data.graveplot_memorials) {
            let lable = ""
            if (graveplot.section)
              lable += graveplot.section + " ";
            if (graveplot.subsection)
              lable += graveplot.subsection + " ";
            if (graveplot.grave_number)
              lable += graveplot.grave_number;
            v.graveplot_list.push(lable)
          }
        }
      })
      .catch(response => {
        console.warn('[GraveLinkSidebar] Couldn\'t get grave links:', response);
      });

    this.openTool();

    if (this.$route.name===constants.MEMORIAL_MANAGEMENT_PATH)
      this.subbuttons[this.subbuttonNames.PERSONSUBBUTTONS].show = true;
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
      this.newMemorialSelected(this.$route.params.id);
      
      // refreshes the survey data
      this.surveyKey++;

      // removes refresh in query
      this.appendToOrModifyItemInQuery('refresh', null);
    }
  }
  
  /*** Methods ***/

  newMemorialSelected(memorialID) {

    let v = this;

    let layer = this.$route.params.layer;

    if (layer === 'bench' || layer === 'lych_gate')
      layer = 'memorials_' + layer;

    this.loadMemorialInformation(memorialID, layer);

    this.loadingPersons = true;

    this.loadData('/mapmanagement/relatedPersons/?memorial_uuid=', memorialID)
    .then(() => {
      Vue.nextTick(() => {
        v.loadingPersons = false;
      });
    })
    .catch(() => {
      v.loadingPersons = false;
    });
    
    this.highlightFeatures('hightlighted-features', 'hightlighted-features-' + memorialID, [{ featureID: memorialID, layerName: layer }], this.$store.state.Styles.highlightedMemorialStyle);
    this.panToFeature(memorialID, layer);
  }

  loadMemorialInformation(featureID, layer) {
    // this is needed for the photo and geometry components
    this.getFeatureFromLayer(featureID, layer)
    .then(feature => {
      this.$store.commit('updateMemorial', feature);
      this.featureExistsOnMap = !!feature;
    });
  }

  openClosePerson(person_id) {
    if (this.$route.name!==this.memorialManagementChildRoutesEnum.persons || this.$route.params.person_id!==person_id) {
      // we're opening a person
      this.$router.push({ name: this.memorialManagementChildRoutesEnum.persons, params: { burial_id: this.getFieldFromObjectItem('person_id', person_id, 'most_recent_burial_id'), person_id: person_id }});
    }
    else
      this.$router.push({ name: this.managementToolRoute });
  }

  openCloseAddPerson() {
    if (this.$route.name!==this.memorialManagementChildRoutesEnum.addPerson) {
      this.$router.push({ name: this.memorialManagementChildRoutesEnum.addPerson, params: { memorialLinkFlagProp: 'false' }});
    }
    else
      this.$router.push({ name: this.managementToolRoute });
  }
}
</script>
