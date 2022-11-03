<template>
  <v-app id="MapManagementVueApp">

    <Analytics></Analytics>

    <NavBar></NavBar>

    <Map v-if="permissionsLoaded" @map-loaded="mapLoadComplete"></Map>

    <div v-if="!loadingAngularTemplate">
      <AtlanticGeomaticsInfo/>
      <Search :openSearch="openSearch" />
      <Offline v-if="showOffline && authenticatedSession"/>
      <div class="angular-entry burial-options map-tools map-layer" v-html="renderedHTML"></div>
    </div>
  </v-app>
</template>

<script lang='ts'>
import Vue from 'vue';
import axios from 'axios';
import Component, { mixins } from 'vue-class-component';
import View from 'ol/View';
import Map from '@/mapmanagement/components/Map/Map.vue'
import NavBar from '@/mapmanagement/components/NavBar.vue'
import Analytics from '@/main/components/Analytics.vue'
import SecurityMixin from '@/mixins/securityMixin'
import NotificationMixin from '@/mixins/notificationMixin'
import FeatureTools from '@/mapmanagement/mixins/featureTools'
import GraveLocation from "@/mixins/graveLocation";
//import { mapGetters } from '../../node_modules/vuex/types';
//import { useStore } from '../../node_modules/vuex/types';
declare var angular: any;

@Component({
  components: {
    Map,
    NavBar,
    Analytics,
    AtlanticGeomaticsInfo: () => import('@/mapmanagement/components/AtlanticGeomaticsInfo.vue'),
    Search: () => import('@/mapmanagement/components/Search/SearchButton.vue'),
    Offline: () => import('@/mapmanagement/components/Offline/OfflineToolsAccordion.vue')
  }
})
export default class MapManagementVueApp extends mixins(SecurityMixin, NotificationMixin, FeatureTools, GraveLocation) {

  openSearch = false
  filterPlots = false
  zoomIn = false;
  renderedHTML = null;
  showOffline: boolean = false;
  loadingAngularTemplate: boolean = true;
  permissionsLoaded: boolean = false;
  notice2 = undefined;
  notice3;
  zoomToSection = false;
  section_id = null;
  //coords1 = null;
  //coords2 = null;
/*
  computed: {
    // mix the getters into computed with object spread operator
    ...mapGetters(['getSectionById']);
  }
*/
  //Return true if site is using BACAS API integration
  get isBacasEnabled(): boolean {
    return this.$store.state.isBacasEnabled;
  }

  getSectionById(section_id) {
    debugger; // eslint-disable-line no-debugger
    let sections_all = this.$store.state.allSections;
    let section = sections_all.find(section =>section.id === section_id );
    debugger; // eslint-disable-line no-debugger
    return section;
  }

  get authenticatedSession(): boolean {
    return this.$store.state.authenticatedSession;
  }

  created() {
    let subdomain = location.hostname.split('.').shift();
    //console.log('subdomain is ' + subdomain);
    if(subdomain === "western"){
      console.log("subdomain is matched " + subdomain);
      this.$store.state.isBacasEnabled = true;
    }

    const queries = this.$router.currentRoute.query;
    const bookingFormQuery = queries['bookingForm'] as string
    const siteId = queries['siteId'] as string;
    const adminDomain = queries['adminDomain'] as string;
    // Open the search panel when it's redirected from Booking
    const openSearchQuery = queries['openSearch'] as string
    const filterPlotsQuery = queries['filterAvailablePlots'] as string
    const zoomToSectionQuery = queries['zoomToMapSection'] as string
    const zoomInQuery = queries['zoomIn'] as string
    const searchQuery = queries['search'] as string
    let isSearchSet = (searchQuery === 'true');
    const searchFormQuery = queries['searchForm'] as string;
    //debugger; // eslint-disable-line no-debugger


    this.section_id = parseInt(queries['section_id'] as string);
    //let section_full = this.getSectionById(this.section_id);
    debugger; // eslint-disable-line no-debugger

    if(isSearchSet){
      const searchForm = JSON.parse(atob(searchFormQuery));
      this.$store.commit('setBookingForm', searchForm);
      this.$store.commit('setRedirectMetadata', {siteId, adminDomain});

      const originURL = adminDomain
          ? decodeURIComponent(adminDomain)
          : window.location.origin;
      const parseForm = btoa(JSON.stringify(searchForm));
      const bookingURL = `${originURL}/main/#/booking/search-event?searchForm=${parseForm}&siteId=${siteId}`;
      this.$store.commit('setReturnLink', bookingURL);


    }


    if(bookingFormQuery) {
     this.$store.watch(
       (state)=>{
         return this.$store.state.StepNumber;
       },
       (stepNum)=>{
         if(stepNum == 1){
           if(typeof this.notice2 === 'undefined'){         
                  this.notice2 = this.createPermanentInfoNotification("Type name in search and click the search button.",
                false, () => {
                  this.$emit('close-tool');
                });
            }
           else{
               this.notice2.update({title: "Type name in search and click the search button."});              
            }        

         }else if(stepNum == 2){           
          if(typeof this.notice2 === 'undefined'){
             this.notice2 = this.createPermanentInfoNotification("Select an option from the results.",
            false, () => {
              this.$emit('close-tool');
            });
           }else{
              this.notice2.update({title: "Select an option from the results."});           
          }          

         }else if(stepNum == 3){
            if(typeof this.notice2 === 'undefined'){
              this.notice2 = this.createPermanentInfoNotification("Once map zooms to grave click the 'Link to booking' link in the hover menu. \n Click yes in the confirmation pop up.",
            false, () => {
              this.$emit('close-tool');
            });
             }else{
             this.notice2.update({title: "Once map zooms to grave click the 'Link to booking' link in the hover menu. \n Click yes in the confirmation pop up."});
           }
         }
       }
    )

      const bookingForm = JSON.parse(atob(bookingFormQuery));
      this.$store.commit('setBookingForm', bookingForm);
      this.$store.commit('setRedirectMetadata', {siteId, adminDomain}); 
      
      const originURL = adminDomain
                ? decodeURIComponent(adminDomain)
                : window.location.origin;
      const parseForm = btoa(JSON.stringify(bookingForm));
      const bookingURL = `${originURL}/main/#/booking/add-event?bookingForm=${parseForm}&siteId=${siteId}`;
      this.$store.commit('setReturnLink', bookingURL);    



    }    
    if(zoomToSectionQuery){
      this.zoomToSection = true;
    }
    
    if(openSearchQuery) {
      this.$store.commit('setStepNumber', 1);
      this.openSearch = true;
    }

    if(filterPlotsQuery) {
          // show notice
      this.notice3 = this.createPermanentInfoNotification("1. Select an available plot. \n 2. Click Yes in the confirmation pop up.",
      false, () => {
       this.$emit('close-tool');
      });
      this.filterPlots = true
    }

    if(zoomInQuery) {
      this.zoomIn = true
    }

    // get permissions from server. SiteAdmin > SiteWarden > MemorialPhotographer
    this.getGroups()
    .then(result => {
      if (result) {
        // if not authenticated then it must be a public access session
        this.$store.commit('setAuthenticatedSession');
        if ((result as any).includes("Superuser") || (result as any).includes("SiteAdmin"))
          this.$store.commit('setSiteAdminAccess');
        else if ((result as any).includes("SiteWarden"))
          this.$store.commit('setSiteAdminOrSiteWardenAccess');
        else {
          if ((result as any).includes("MemorialPhotographer"))
            this.$store.commit('setMemorialPhotographyAccess');
          if ((result as any).includes("DataEntry"))
            this.$store.commit('setDataEntry');
          if ((result as any).includes("DataMatcher"))
            this.$store.commit('setDataMatcher');
        }
        if((result as any).includes("Superuser") || (result as any).includes("AG_staff")){
          this.$store.commit("setAgStaffAccess");
        }
      }

      this.permissionsLoaded = true;
    });
  }
  
  mapLoadComplete() {
    axios.get('/mapmanagement/getRenderedMapManagementIndex')
    .then(response => {       
      this.renderedHTML = response.data;
      this.loadingAngularTemplate = false;
      const returnLink = this.$store.state.returnLink;
      if(returnLink != "" && returnLink !== undefined){
        const zoomDiv = document.querySelector<HTMLElement>(".ol-zoom");
        zoomDiv.style.cssText +=  "top: 33px !important;";
        const scaleDiv = document.querySelector<HTMLElement>(".ol-scale-line");
        scaleDiv.style.cssText += "top: 56px !important;";
        const mousePosDiv = document.querySelector<HTMLElement>(".olex-mouse-position");
        mousePosDiv.style.cssText += "top: 35px !important;";        
       
      }else{
        const zoomDiv = document.querySelector<HTMLElement>(".ol-zoom");
        if(zoomDiv.style.cssText.includes("top: 33px !important;")){
          zoomDiv.style.cssText.replace("top: 32px !important;", "") ;
        }        
        const mousePosDiv = document.querySelector<HTMLElement>(".olex-mouse-position");
        if(mousePosDiv.style.cssText.includes("top: 35px !important;")){
          mousePosDiv.style.cssText.replace("top: 35px !important;", "");
        }        
        const scaleDiv = document.querySelector<HTMLElement>(".ol-scale-line");
        if(scaleDiv.style.cssText.includes("top: 56px !important;")){
          scaleDiv.style.cssText.replace("top: 56px !important;", "");
        }  

        
      }



      if(this.zoomToSection){ //section id passed as param from booking so zoom to map section
        debugger; // eslint-disable-line no-debugger
        if(this.section_id){
          //let section_id = this.section_id;
          /*
          try {
            let sections = this.allSections;
            console.log("Sections: " + sections.length());
          }catch (e) {
            console.log("Section Error: " + e);
          }*/
          let section = this.getSectionById(this.section_id);
          if(section) {
            //let section_poly = section?.topopolygon;
            // this.SetExtentSection(section_poly);
          }

        }

        //const coordsArr = [this.coords1, this.coords2];
        //let current_sections = this.$store.allSections;
        //let sect = 25;
        //let current_section = this.$store.allSections.find(x => x.id === this.sect_id);
        //this.SetExtentSection(current_section);
      }
      window.setTimeout(() => {
        // begin angular app
        angular.bootstrap(document.getElementById('map-angular-wrapper'), ['bgmsApp']);
        this.$store.commit('commitAngularMapController', angular.element(document.querySelector("[ng-controller='MapCtrl as map']")));

        // Timeout to give openlayers a headstart before installing SW
        window.setTimeout(() => {
          this.showOffline = true;
        }, 1000);
      });
    })
    .catch(response => {
      console.warn('Couldn\'t get data from server: ' + response);
    });
  }

  nodeScriptReplace(node) {
    if (this.nodeScriptIs(node) === true) {
      node.parentNode.replaceChild(this.nodeScriptClone(node), node);
    }
    else {
      let i = 0;
      let children = node.childNodes;
      while (i < children.length) {
        this.nodeScriptReplace(children[i++]);
      }
    }

    return node;
  }
  nodeScriptIs(node) {
    return node.tagName === 'SCRIPT';
  }
  nodeScriptClone(node){
    let script  = document.createElement("script");
    script.text = node.innerHTML;
    for(let i = node.attributes.length-1; i >= 0; i--) {
      script.setAttribute(node.attributes[i].name, node.attributes[i].value);
    }
    return script;
  }
}
</script>