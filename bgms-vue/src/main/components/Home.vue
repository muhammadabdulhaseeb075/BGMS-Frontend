<template>
  <div id="home" style="height: 100%" ref="home">
    <div id="welcome">{{ welcomeMessage }}</div>
    <br>
    <v-card
      max-width="400"
      class="mx-auto">
      
      <v-progress-linear
        :active="loading || mapmanagementAccessSites===null"
        :indeterminate="loading || mapmanagementAccessSites===null"
        absolute
        top
        color="light-blue darken-1"
      ></v-progress-linear>

      <v-list class="grow">
        <div v-if="mapmanagementAccessSites">
          <h2>Burial Grounds</h2>
          <div v-for="site in mapmanagementAccessSites" :key="site.id">

            <v-list-group
              v-if="site.data_entry || site.data_matcher || site.site_admin"
              no-action
              :key="site.id"
            >
              <template v-slot:activator>
                <v-list-item-content>
                  <v-list-item-title><h4>{{ site.name }}</h4></v-list-item-title>
                </v-list-item-content>
              </template>

              <v-list-item
                link
                :href="site.domain_url"
                @click.stop="loading=true"
              >
                <v-list-item-title>Map Management</v-list-item-title>
                <v-list-item-icon>
                  <v-icon>fas fa-map</v-icon>
                </v-list-item-icon>
              </v-list-item>

              <v-list-item
                link
                v-if="site.data_entry"
                :href="site.domain_url + '/dataentry/'"
                @click.stop="loading=true"
              >
                <v-list-item-title>Burial Record Entry Portal</v-list-item-title>
                <v-list-item-icon>
                  <v-icon>fas fa-book</v-icon>
                </v-list-item-icon>
              </v-list-item>

              <v-list-item
                link
                v-if="site.data_matcher"
                :href="site.domain_url + '/datamatching/'"
                @click.stop="loading=true"
              >
                <v-list-item-title>Image Matching Portal</v-list-item-title>
                <v-list-item-icon>
                  <v-icon>fas fa-image</v-icon>
                </v-list-item-icon>
              </v-list-item>

              <v-list-item
                link
                v-if="site.site_admin"
                :href="site.domain_url + '/siteadminportal/'"
                @click.stop="loading=true"
              >
                <v-list-item-title>Admin Portal</v-list-item-title>
                <v-list-item-icon>
                  <v-icon>fas fa-cog</v-icon>
                </v-list-item-icon>
              </v-list-item>

            </v-list-group>

            <v-list-item
              v-else
              link
              :href="site.domain_url"
              @click.stop="loading=true"
            >
              <v-list-item-title class="font-weight-bold">{{ site.name }}</v-list-item-title>
              <v-list-item-icon>
                <v-icon>fas fa-map</v-icon>
              </v-list-item-icon>
            </v-list-item>

          </div>
        </div>

        <div v-if="bereavementStaffAccessSites && bereavementStaffAccessSites.length > 0">
          <h2 class="">Bereavement Services</h2>
            <v-list-item 
              :href= "'https://' + strippedHost + '/main/#/booking/calendar'"
              @click.stop="loading=true">
              <h4 :href="'https://' + strippedHost + '/main/#/booking/calendar'">Booking Management</h4>
            </v-list-item>
            <v-list-item link href="/" disabled><h4>Grave Ownership</h4></v-list-item>
            <v-list-item link href="/" disabled><h4>Invoicing</h4></v-list-item>
        </div>

        <v-list-item
          link
          v-if="sitemanagementAccess"
          href="/sitemanagement"
          @click.stop="loading=true">
          <h2>Site Management</h2></v-list-item>
      </v-list>
    </v-card>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import axios from 'axios';
import Component from 'vue-class-component';

@Component
export default class Home extends Vue {

  loading: boolean = false;

  /**
   * Get sites user has mapmanagement access to
   */
  get mapmanagementAccessSites() {
    return this.$store.state.mapmanagementAccessSites;
  }

  /**
   * Get sites user has bereavement staff access to
   */
  get bereavementStaffAccessSites() {
    return this.$store.getters.getBereavementStaffAccessSites;
  }

  /**
   * True if user has sitemanagement access
   */
  get sitemanagementAccess() {
    return this.$store.state.sitemanagementAccess;
  }

  get shortName() {
    return (window as any).document.user.short_name;
  }

  get welcomeMessage() {
    const now = new Date();
    const hours = now.getHours();

    let message = "Good ";

    if (hours >= 17)
      message += "evening";
    else if (hours >= 12)
      message += "afternoon";
    else
      message += "morning";
    
    if (this.shortName)
      message += ', ' + this.shortName;
    
    return message;
  }

  get strippedHost(){
    return location.host.replace('www.','')
  }
}
</script>