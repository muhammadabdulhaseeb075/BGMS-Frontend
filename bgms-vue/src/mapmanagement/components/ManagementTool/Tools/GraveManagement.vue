<template>
  <div id="graveManagementComponent" class="management-tool-buttons-container">
    <ul class="management-tool-buttons" v-if="$route.params.id && subbuttons && subbuttonNames">
      <li v-if="grave_number != ''" class="management-tool-buttons-identifier"
          style="line-height: 20px; background-color: #f1e7b1;">
          <div class="burial-official-type">{{grave_number}}</div>
      </li>
      <li class="top-border" @click="toggleSubbuttons(subbuttonNames.BURIALSUBBUTTONS)" v-if="loadingBurials || (burials && burials.length>0) || siteAdminOrSiteWarden">
        <a href="javascript:void(0)" :class="{ active: subbuttons[subbuttonNames.BURIALSUBBUTTONS].show }"><span>Burials</span></a>
      </li>
      <div class="management-tool-subbuttons">
        <transition name="list">
          <ul v-show="subbuttons[subbuttonNames.BURIALSUBBUTTONS].show && !loadingBurials">
          
            <li @click="openCloseAddBurial()" v-if="siteAdminOrSiteWarden && !isBacasEnabled">
              <a href="javascript:void(0)" class="add-new" :class="{ active: ($route.name===graveManagementChildRoutesEnum.addBurial) }"><i class="fas fa-plus"/> Add New</a>
            </li>

            <li v-for="burial in burials" :key="burial.id" :class="{ active: $route.params.burial_id === burial.id }">
              <a v-if="!isBacasEnabled" href="javascript:void(0)" @click="openCloseBurial(burial.id)">{{burial.display_name}}</a>
              <a v-if="isBacasEnabled" href="javascript:void(0)" >{{burial.display_name}}</a>
            </li>

          </ul>
        </transition>
        <ul v-show="subbuttons[subbuttonNames.BURIALSUBBUTTONS].show && loadingBurials" class="loading-placeholder-contents">
          <li><i class="fa fa-spinner fa-spin"/></li>
        </ul>
      </div>

      <li class="top-border" @click="toggleSubbuttons(subbuttonNames.RESERVATIONSUBBUTTONS)" v-if="!isBacasEnabled && (loadingReservations || (reservations && reservations.length>0) || siteAdminOrSiteWarden)">
        <a href="javascript:void(0)" :class="{ active: subbuttons[subbuttonNames.RESERVATIONSUBBUTTONS].show }"><span>Reservations</span></a>
      </li>
      <div class="management-tool-subbuttons">
        <transition name="list">
          <ul v-show="subbuttons[subbuttonNames.RESERVATIONSUBBUTTONS].show && !loadingReservations">
            
            <li @click="openCloseReservation(null)" v-if="siteAdminOrSiteWarden">
              <a href="javascript:void(0)" class="add-new" :class="{ active: ($route.name===graveManagementChildRoutesEnum.reservations && !$route.params.personID) }"><i class="fas fa-plus"/> Add New</a>
            </li>

            <li v-for="reservation in reservations" :key="reservation.id" @click="openCloseReservation(reservation.person_id.toString())">
              <a href="javascript:void(0)" :class="{ active: ($route.name===graveManagementChildRoutesEnum.reservations && $route.params.personID===reservation.person_id.toString()) }">{{reservation.display_name}}</a>
            </li>

          </ul>
        </transition>
        <ul v-show="subbuttons[subbuttonNames.RESERVATIONSUBBUTTONS].show && loadingReservations" class="loading-placeholder-contents">
          <li><i class="fa fa-spinner fa-spin"/></li>
        </ul>
      </div>


     <router-link v-if="!isBacasEnabled" tag="li" class="top-border" :to="openOrCloseChildRoute(managementToolRoute, graveManagementChildRoutesEnum.graveDetails)">
        <a :class="{ active: isRouteActive(graveManagementChildRoutesEnum.graveDetails) }">Details</a>
      </router-link>

      <!-- <router-link tag="li" class="top-border" :to="openOrCloseChildRoute(managementToolRoute, graveManagementChildRoutesEnum.graveGeometry)" v-if="featureExistsOnMap">
        <a :class="{ active: isRouteActive(graveManagementChildRoutesEnum.graveGeometry) }">Geometry</a>
      </router-link> -->

      <router-link v-if="!isBacasEnabled" tag="li" class="top-border" :to="openOrCloseChildRoute(managementToolRoute, graveManagementChildRoutesEnum.linkedMemorials, [{ name: 'linkedType', value: 'grave' }, { name: 'showLabel', value: true }])">
        <a :class="{ active: isRouteActive(graveManagementChildRoutesEnum.linkedMemorials) }">Memorials</a>
      </router-link> 

      <li class="top-border" @click="toggleSubbuttons(subbuttonNames.OWNERSHIPSUBBUTTONS)" v-if="!isBacasEnabled && (loadingOwnership || (ownership && ownership.length>0) || siteAdminOrSiteWarden)">
        <a id="ownership-button" href="javascript:void(0)" :class="{ active: showOwnershipButtons }"><span>Ownership</span></a>
      </li>
      <div class="management-tool-subbuttons">
        <transition name="list">
          <ul v-show="showOwnershipButtons && !loadingOwnership">
            
            <li @click="openCloseOwnership(null)" v-if="siteAdminOrSiteWarden">
              <a href="javascript:void(0)" class="add-new" :class="{ active: ($route.name===graveManagementChildRoutesEnum.graveOwnership && !$route.params.deedID) }"><i class="fas fa-plus"/> Add New</a>
            </li>
<!-- 
            <li v-for="deed in ownership" :key="deed.id" @click="openCloseOwnership(deed.id.toString())">
              <a href="javascript:void(0)" :class="{ active: $route.params.deedID === deed.id.toString() }">{{ individualDateFieldsToSingleDate(deed.purchase_date_day, deed.purchase_date_month, deed.purchase_date_year) + (deed.tenure_years ? ' (' + deed.tenure_years + ')' : '') }}</a>
            </li> -->

          </ul>
        </transition>
        <ul v-show="showOwnershipButtons && loadingOwnership" class="loading-placeholder-contents">
          <li><i class="fa fa-spinner fa-spin"/></li>
        </ul>
      </div>

      <router-link v-if="!isBacasEnabled && attributesExist" tag="li" class="top-border" :to="openOrCloseChildRoute(managementToolRoute, graveManagementChildRoutesEnum.attributes)">
        <a :class="{ active: isRouteActive(graveManagementChildRoutesEnum.attributes) }">Attributes</a>
      </router-link>

      <SurveyButtons v-if="$route.params.layer!=='available_plot' || $route.params.availablePlotID" :key="surveyKey" :managementToolRoute="managementToolRoute" :surveysRoute="graveManagementChildRoutesEnum.surveys" :showSurveySubbuttons="subbuttons[subbuttonNames.SURVEYSUBBUTTONS].show" @toggle_survey_subbuttons="toggleSubbuttons"/>

    </ul>
    <div v-else class="loading-placeholder-contents">
      <i class="fa fa-spinner fa-spin"/>
    </div>
    <div id="management-tool-contentbar-container">
      <router-view id="management-tool-contentbar" :class="{ 'component-container': isRouteActive(graveManagementChildRoutesEnum.linkedMemorials) }"></router-view>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import VueRouter from 'vue-router';
import Component, { mixins } from 'vue-class-component'
import { Watch } from 'vue-property-decorator'
import axios from 'axios'
import constants from '@/global-static/constants.ts';
import { individualDateFieldsToSingleDate } from '@/global-static/dataFormattingAndValidation.ts';
import SurveyButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/SurveyButtons.vue';
import FeatureTools from '@/mapmanagement/mixins/featureTools.ts';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin.ts';
import SubbuttonsMixin from '@/mapmanagement/mixins/subbuttonsMixin.ts';
import NotificationMixin from '@/mixins/notificationMixin.ts';
import View from "ol/View";

Vue.use(Vuex);
Vue.use(VueRouter);

/**
 * Class representing GraveManagement
 * @extends ManagementToolsMixin mixin
 * @extends FeatureTools mixin
 * @extends SubbuttonsMixin mixin
 */
@Component({
  components: {
    SurveyButtons
  }
})
export default class GraveManagement extends mixins(ManagementToolsMixin, FeatureTools, SubbuttonsMixin, NotificationMixin) {

  //Computed method. Return true if site is using BACAS API integration.
  get isBacasEnabled(): boolean {
    return this.$store.state.isBacasEnabled;
  }  

  individualDateFieldsToSingleDate = individualDateFieldsToSingleDate;
  
  graveManagementChildRoutesEnum = constants.GRAVE_MANAGEMENT_CHILD_ROUTES;

  loadingBurials: boolean = false;
  burials = null;
  loadingReservations: boolean = false;
  reservations = null;
  loadingOwnership: boolean = false;
  ownership = null;
  attributesExist: boolean = false;
  featureExistsOnMap: boolean = false;
  zoomIn: string | string[];

  searchQuery = null;
  searchFormQuery = null;
  siteId = null;
  adminDomain = null;
  notice_5;

  availablePlotID = null;

  surveyKey: number = 0;
  grave_number: string = '';

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {

    let v = this;

    this.zoomIn = v.$route.query['zoomIn'];
    this.searchQuery = v.$route.query['search'];
    this.searchFormQuery = v.$route.query['searchForm'];
    this.siteId = v.$route.query['siteId'];
    this.adminDomain = v.$route.query['adminDomain'];

    v.componentName = "gravemanagement";
    v.$store.commit('setTitle', "Grave");

    this.managementToolRoute = constants.GRAVE_MANAGEMENT_PATH;

    this.$set(this.subbuttons, this.subbuttonNames.OWNERSHIPSUBBUTTONS, { show: false, route: this.graveManagementChildRoutesEnum.graveOwnership });
    this.$set(this.subbuttons, this.subbuttonNames.RESERVATIONSUBBUTTONS, { show: false, route: this.graveManagementChildRoutesEnum.reservations });
    this.$set(this.subbuttons, this.subbuttonNames.BURIALSUBBUTTONS, { show: false, route: this.graveManagementChildRoutesEnum.burials });
    this.$set(this.subbuttons, this.subbuttonNames.SURVEYSUBBUTTONS, { show: false, route: this.graveManagementChildRoutesEnum.surveys });

    debugger; //eslint-disable-line no-debugger
    if(this.searchQuery){
        let searchForm = "{}";
        if(this.searchFormQuery){
          searchForm = JSON.parse(atob(this.searchFormQuery));
          this.$store.commit('setBookingForm', searchForm);
        }

        let site_id = this.siteId;
        let admin_domain = this.adminDomain;
        this.$store.commit('setRedirectMetadata', {site_id, admin_domain});

        const originURL = admin_domain
            ? decodeURIComponent(admin_domain)
            : window.location.origin;
        //const parseForm = btoa(JSON.stringify(searchForm));
        const parseForm = this.searchFormQuery;
        const bookingURL = `${originURL}/main/#/booking/search-event?searchForm=${parseForm}&siteId=${site_id}`;
        this.$store.commit('setReturnLink', bookingURL);

        let notice_text = "<a href='" + bookingURL + "'>Click to Return to Search.</a>";
        /* Disable the blue box when coming from search results
        this.notice_5 = this.createPermanentInfoNotification('Click Link to Left to Return to Search.',
          false, () => {
              this.$emit('close-tool');
            });
        */
      }

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
    }
    if (!v.$route.params.layer || v.$route.params.layer==='unknown') {
      // We need to get the layer from the server. This is important for locating the graveplot on the map.
      axios.get('/mapmanagement/getGraveplotLayer/?graveplot_id=' + v.$route.params.id)
      .then(function(response) {
        let params = { layer: response.data.layer };

        if (response.data.layer==="available_plot")
          params['availablePlotID'] = response.data.topopolygon_id;

        v.$router.replace({ params: params});
        Vue.nextTick(() => {
          v.newGraveSelected();
        })
      })
      .catch(function(response) {
        console.warn('Couldn\'t get graveplot layer:', response.response.data);
      });
    }
    else
      v.newGraveSelected();
    
    axios.get('/mapmanagement/featureAttributesExist/?graveplot_id=' + v.$route.params.id)
    .then((response) => {
      if (response.data.attributesFound)
        v.attributesExist = true;
    });

    const url_id = '/mapmanagement/graveDetails/?graveplot_uuid=' + v.$route.params.id
    axios.get(url_id)
    .then((response) => {
      debugger; // eslint-disable-line no-debugger
      if(response.data && response.data.section_name){
        v.grave_number += response.data.section_name + " ";
      }
      if(response.data && response.data.subsection_name){
        v.grave_number += response.data.subsection_name + " ";
      }
      if(response.data && response.data.grave_number){
        v.grave_number += response.data.grave_number;
      }
      
      const filterAvailablePlots = this.$router.currentRoute.query.filterAvailablePlots;
      debugger; // eslint-disable-line no-debugger
      if(v.grave_number && filterAvailablePlots) {
        this.createConfirmation(
          "Confirmation needed",
          `Add ${v.grave_number} as Grave number for the booking`, 
          () => {
            debugger; // eslint-disable-line no-debugger
            const queries = this.$router.currentRoute.query;
            // Get the booking form cache
            const bookingFormQuery = queries.bookingForm as string;
            const siteIdQuery = queries.siteId as string;
            const adminDomain = queries.adminDomain as string;
            const bookingForm = JSON.parse(atob(bookingFormQuery));
            // update the new grave number to send to the booking form
            bookingForm.detailsGraveNumber = v.grave_number;
            bookingForm.detailsBurialUUID = v.$route.params.id;

            // generate the booking url with the new information added into
            // the booking form
            const originURL = adminDomain
                ? decodeURIComponent(adminDomain)
                : window.location.origin;
            const parseForm = btoa(JSON.stringify(bookingForm));
            const bookingURL = `${originURL}/main/#/booking/add-event?bookingForm=${parseForm}&siteId=${siteIdQuery}`;
            //redirect to add booking page
            window.location.assign(bookingURL);
          }
        )
      }
    });

    v.openTool();

  }
  /*** Computed ***/

  get showOwnershipButtons() {
    const currentShow = document.getElementById("ownership-button") ? document.getElementById("ownership-button").classList.contains("active") : false;
    const newShow = this.subbuttons[this.subbuttonNames.OWNERSHIPSUBBUTTONS].show;

    // if ownership button is selected, and no components are open, and at least one deed exists
    if (currentShow != newShow && newShow && this.$route.name === constants.GRAVE_MANAGEMENT_PATH && this.ownership && this.ownership.length) {
      // select the first ownership record
      this.openCloseOwnership(this.ownership[0].id.toString())
    }

    if(!this.ownership || this.ownership.length==0){
      return newShow;
    }
    else{
      return false;
    }
    
  }

  /*** Watchers ***/

  /**
   * Watcher: When refresh in router query is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('$route.query.refresh')
  onRefreshChanged(val: any, oldVal: any) {
    debugger; //eslint-disable-line no-debugger
    if (val) {
      // refreshes the grave data
      this.newGraveSelected(true);

       const url_id = '/mapmanagement/graveDetails/?graveplot_uuid=' + this.$route.params.id
        axios.get(url_id)
        .then((response) => {
          this.grave_number = "";
          if(response.data && response.data.section_name){
            this.grave_number += response.data.section_name + " ";
          }
          if(response.data && response.data.subsection_name){
            this.grave_number += response.data.subsection_name + " ";
          }
          if(response.data && response.data.grave_number){
            this.grave_number += response.data.grave_number;
          }
        });
      
      // refreshes the survey data
      this.surveyKey++;

      // removes refresh in query
      this.appendToOrModifyItemInQuery('refresh', null);
    }
  }

  /**
   * Watcher: When availablePlotID param changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('$route.params.availablePlotID', { immediate: true })
  onAvailablePlotIDChanged(val: any, oldVal: any) {
    if (val)
      this.availablePlotID = this.$route.params.availablePlotID;
    else if (oldVal && this.$route.params.layer === 'available_plot')
      // availablePlotID is an optional param. For some reason it disappears when the path changes.
      // This makes sure it is always there if we need it.
      this.$router.replace({ params: { 'availablePlotID': oldVal }});
  }
  
  /*** Methods ***/

  /**
   * Called when a new grave is selected.
   */
  newGraveSelected(refresh: boolean = false) {
    debugger; // eslint-disable-line no-debugger
    this.burials = null;
    this.reservations = null;
    this.ownership = null;

    let id = this.$route.params.id;
    let featureID = id;

    let layer = 'plot';
    if (this.$route.params.layer)
      layer = this.$route.params.layer as string;

    if (layer==='available_plot') {
      this.availablePlotID = this.$route.params.availablePlotID;
      featureID = this.availablePlotID;
    }

      if (this.$route.name===constants.GRAVE_MANAGEMENT_PATH) {
        this.subbuttons[this.subbuttonNames.BURIALSUBBUTTONS].show = false;
        this.subbuttons[this.subbuttonNames.RESERVATIONSUBBUTTONS].show = false;

        if (layer==='plot')
          this.subbuttons[this.subbuttonNames.BURIALSUBBUTTONS].show = true;
        else if (layer==='reserved_plot')
          this.subbuttons[this.subbuttonNames.RESERVATIONSUBBUTTONS].show = true;
      }

      this.loadingBurials = true;

      debugger; // eslint-disable-line no-debugger

      // load list of burials relating to grave
      this.loadDataWithoutStoring('/mapmanagement/relatedBurials/?graveplot_uuid=', id)
      .then((result) => {
        this.burials = result;
        Vue.nextTick(() => {
          this.loadingBurials = false;
        });
      })
      .catch(() => {
        this.loadingBurials = false;
      });

      if(!this.isBacasEnabled){ //bacas api doesn't currently offer reservation data?
        this.loadingReservations = true;
        // load list of burials relating to grave
        this.loadDataWithoutStoring('/mapmanagement/relatedReservations/?graveplot_uuid=', id)
        .then((result) => {
          this.reservations = result;
          Vue.nextTick(() => {
            this.loadingReservations = false;
          });
        })
        .catch(() => {
          this.loadingReservations = false;
        });
      }

      if(!this.isBacasEnabled){ //bacas api doesn't currently provide ownershop data
        this.loadingOwnership = true;
        // load list of deeds relating to grave
        this.loadDataWithoutStoring('/mapmanagement/graveDeedsList/?graveplot_uuid=', id)
        .then((result) => {
          this.ownership = result;
          Vue.nextTick(() => {
            this.loadingOwnership = false;
          });
        })
        .catch(() => {
          this.loadingOwnership = false;
       });
      }

    // only need these if the grave has actually change, i.e. not just a refresh
    if (!refresh) {
      // highlight and pan to (if needed) the selected grave
      this.highlightFeatures('hightlighted-features', 'hightlighted-features-' + featureID, [{ featureID: featureID, layerName: layer }], this.$store.state.Styles.highlightedGraveStyle);
      this.panToFeature(featureID, layer);
    }

    // Look for grave on the map
    this.getFeatureFromLayer(featureID, layer)
    .then(value => {
      this.featureExistsOnMap = !!value;
    });
  }

  openCloseBurial(burial_id) {
    debugger; //eslint-disable-line no-debugger
    let v = this;

    if (v.$route.name!==v.graveManagementChildRoutesEnum.burials || v.$route.params.burial_id!==burial_id) {
      // we're opening an existing burial
      v.$router.push({ name: v.graveManagementChildRoutesEnum.burials, params: { burial_id: burial_id, person_id: v.getFieldFromObjectItem('id', burial_id, 'person_id', v.burials) }});
    }
    else
      v.$router.push({ name: v.managementToolRoute });
  }

  openCloseAddBurial() {
    let v = this;

    if (v.$route.name!==v.graveManagementChildRoutesEnum.addBurial) {
      v.$router.push({ name: v.graveManagementChildRoutesEnum.addBurial, params: { memorialLinkFlagProp: 'true', addburialavailablePlotID: v.availablePlotID }});
    }
    else
      v.$router.push({ name: v.managementToolRoute });
  }

  openCloseReservation( person_id) {
    let v = this;

    if (v.$route.name!==v.graveManagementChildRoutesEnum.reservations || v.$route.params.personID!==person_id) {
      // we're opening a burial
      v.$router.push({ name: v.graveManagementChildRoutesEnum.reservations, params: { personID: person_id, reservationavailablePlotID: v.availablePlotID }});
    }
    else
      v.$router.push({ name: v.managementToolRoute });
  }

  openCloseOwnership(deed_id: string) {
    let v = this;

    const ownerRouteActive: boolean = v.$route.name===v.graveManagementChildRoutesEnum.graveOwnership

    if (!ownerRouteActive || v.$route.params.deedID!==deed_id) {
      // we're opening a burial
      v.$router.push({ name: v.graveManagementChildRoutesEnum.graveOwnership, params: { deedID: deed_id, ownershipavailablePlotID: v.availablePlotID }});
    }
    else
      v.$router.push({ name: v.managementToolRoute });
  }
}
</script>
