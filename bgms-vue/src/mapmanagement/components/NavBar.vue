<template>
  <div id="top-nav" class="top-nav" data-html2canvas-ignore="true">
    <v-toolbar class="navbar navbar-expand-lg navbar-light" flat role="navigation">
      <v-toolbar-title>
        <a :href="authenticatedSession ? (siteDetails.homepage ? siteDetails.homepage : '/') : 'https://www.atlanticgeomatics.co.uk/burial-ground-management-system'" :target="authenticatedSession ? '' : '_blank'">          
          <img class="logo" :src="require('@/mapmanagement/static/images/BGMS_logo_header.png')" crossorigin="anonymous" />
        </a>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-toolbar-items>
        <v-menu v-if="authenticatedSession" 
          bottom 
          left 
          content-class="menu-dropdown">
          <template v-slot:activator="{ on, value }">
            <v-btn
              dark
              text
              class="d-none d-sm-flex"
              :class="{ active: value }"
              v-on="on">
              <span>User Guide</span>
              <i class="fas" :class="value ? 'fa-caret-up' : 'fa-caret-down'"/>
            </v-btn>
          </template>
          <v-list>
            <v-list-item tag="a" target="_blank" :href="siteDetails.user_guide" nav>
              <v-list-item-title>View user guide</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

        <v-menu v-if="siteAdmin || dataEntryAccess || dataMatcherAccess" 
          bottom 
          left 
          content-class="menu-dropdown">
          <template v-slot:activator="{ on, value }">
            <v-btn
              dark
              text
              :class="{ active: value }"
              v-on="on">
              <span>Actions</span>
              <i class="fas" :class="value ? 'fa-caret-up' : 'fa-caret-down'"/>
            </v-btn>
          </template>
          <v-list>
            <v-list-item v-if="dataEntryAccess" tag="a" href="/dataentry/" nav>
              <v-list-item-title>Burial Record Entry Portal</v-list-item-title>
            </v-list-item>
            <v-list-item v-if="dataMatcherAccess" tag="a" href="/datamatching/" nav>
              <v-list-item-title>Image Matching Portal</v-list-item-title>
            </v-list-item>
            <v-list-item v-if="siteAdmin" tag="a" href="/siteadminportal/" nav>
              <v-list-item-title>Admin Portal</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

        <v-menu bottom left 
          content-class="menu-dropdown site-details" 
          v-if="siteDetails">
          <template v-slot:activator="{ on, value }">
            <v-btn
              dark
              text
              class="d-none d-sm-flex"
              :class="{ active: value }"
              v-on="on">
              <span>About</span>
              <i class="fas" :class="value ? 'fa-caret-up' : 'fa-caret-down'"/>
            </v-btn>
          </template>
          <v-row>
            <v-col cols="4" class="font-weight-bold white--text">
              Address: 
            </v-col>
            <v-col cols="8" class="grey--text text--darken-3">
              {{ siteDetails.address.first_line }} <br>
              {{ siteDetails.address.second_line }}
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="4" class="font-weight-bold white--text">
              Town: 
            </v-col>
            <v-col cols="8" class="grey--text text--darken-3">
              {{ siteDetails.address.town }} 
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="4" class="font-weight-bold white--text">
              County: 
            </v-col>
            <v-col cols="8" class="grey--text text--darken-3">
              {{ siteDetails.address.county }} 
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="4" class="font-weight-bold white--text">
              Postcode: 
            </v-col>
            <v-col cols="8" class="grey--text text--darken-3">
              {{ siteDetails.address.postcode }} 
            </v-col>
          </v-row>
          <v-row class="pt-4">
            <v-col cols="6">
              <a :href="siteDetails.terms_conditions" target="_blank">Terms of Use</a>
            </v-col>
            <v-col cols="6">
              <a :href="siteDetails.privacy_notice" target="_blank">Privacy Policy</a>
            </v-col>
          </v-row>
        </v-menu>
        
        <v-menu v-if="!authenticatedSession" 
          bottom 
          left 
          content-class="menu-dropdown">
          <template v-slot:activator="{ on, value }">
            <v-btn
              dark
              text
              class="d-none d-sm-flex"
              :class="{ active: value }"
              v-on="on">
              <span>Help</span>
              <i class="fas" :class="value ? 'fa-caret-up' : 'fa-caret-down'"/>
            </v-btn>
          </template>
          <v-list>
            <v-list-item 
              tag="a"
              :href="siteDetails.public_user_guide"
              target="_blank"
              nav>
              <v-list-item-title>View user guide</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        
        <v-menu v-if="authenticatedSession" bottom left content-class="menu-dropdown">
          <template v-slot:activator="{ on, value }">
            <v-btn
              dark
              text
              :class="{ active: value }"
              v-on="on">
              <i class="fas fa-user"/>
              <span><i class="user-menu-user">{{ username }}</i></span>
              <i class="fas" :class="value ? 'fa-caret-up' : 'fa-caret-down'"/>
            </v-btn>
          </template>
          <v-list>
            <v-list-item tag="a" href="/logout/" nav>
              <v-list-item-title>Log Out</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

        <v-btn
          v-if="!authenticatedSession"
          dark
          text
          href="https://www.atlanticgeomatics.co.uk/contact"
          target="_blank">
          <span>Feedback</span>
        </v-btn>
        
        <v-menu v-if="!authenticatedSession" 
          bottom left 
          content-class="menu-legend menu-dropdown">
          <template v-slot:activator="{ on, value }">
            <v-btn
              dark
              text
              class="d-none d-sm-flex"
              :class="{ active: value }"
              v-on="on">
              <span>Legend</span>
              <i class="fas" :class="value ? 'fa-caret-up' : 'fa-caret-down'"/>
            </v-btn>
          </template>

          <v-list v-for="displayGroup in filteredAndSortedLayerGroups" :key="displayGroup.layerGroup.name" class="pt-0 pb-4">
            <h4 class="my-0 px-3 font-weight-bold">{{ displayGroup.layerGroup.display_name }}</h4>
            <v-list-item v-for="displayLayer in displayGroup.layerGroup.layers" :key="displayLayer.name"
              class="px-0">
              <v-col cols="4" class="py-1">
                <div :class="'key '+displayLayer.name+'_key'"></div>
              </v-col>
              <v-col cols="8" class="py-1">
                {{displayLayer.display_name}}
              </v-col>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar-items>

    </v-toolbar>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import axios from 'axios';
import Component, { mixins } from 'vue-class-component';
import { Watch } from 'vue-property-decorator'

@Component
export default class NavBar extends Vue {

  siteDetails = false;
  filteredAndSortedLayerGroups = [];

  created() {
    axios.get('/bgsite/sitedetails/')
    .then(response => {
      this.siteDetails = response.data;
    })
  }
  
  get username() {
    return (window as any).document.user.username;
  }

  get siteAdmin(): boolean {
    return this.$store.state.siteAdmin;
  }

  get dataEntryAccess(): boolean {
    return this.$store.state.dataEntryAccess;
  }

  get dataMatcherAccess(): boolean {
    return this.$store.state.dataMatcherAccess;
  }

  get authenticatedSession(): boolean {
    return this.$store.state.authenticatedSession;
  }

  get displayGroups() {
    return this.$store.state.MapLayers.displayGroups;
  }
  
  /*** Watchers ***/
  /**
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('displayGroups', { immediate: true, deep: true })
  onDisplayGroupsChanged(val: any, oldVal: any) {
    let result = [];
  
    Object.keys(val).forEach(key => {
      if (val[key].isPanelDisplayed && key != 'base') {
        result.push(val[key]);
      }
    });

    this.filteredAndSortedLayerGroups = result.sort((a, b) => b.layerGroup.hierarchy - a.layerGroup.hierarchy);
  }
}
</script>