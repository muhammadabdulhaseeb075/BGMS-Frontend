<template>
  <div class="site-list">
    <v-row align="center">
      <v-col cols="12" sm="12">
        <strong>
          Burial Grounds (//TMN):
        </strong>
        <div class="select-list">
          <v-radio-group v-model="selectedSiteId" :column="true" @change="updateSelectedSiteId" >
              <v-radio
                class="site-radio"
                v-for="item in SiteList"                    
                :label="item.name"
                :value="item.id"
                :key="item.id"
                :rules="[() => !!selectedSiteId  || 'Field required']"
                hide-details
              ></v-radio>
          </v-radio-group>
        </div>
      </v-col>
      <v-col sm="12" class="pa-0">
        <v-divider style="background-color: #c3af42"/>
      </v-col>
    </v-row>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop, Watch } from 'vue-property-decorator';

@Component
export default class SiteList extends Vue {
  
  get SiteList() {
    return this.$store.getters.getBereavementStaffAccessSites;          
  }

  get selectedSiteId() {
    return this.$store.state.Booking.selectedSiteId;
  }

  set selectedSiteId(selected){
    this.$store.commit('selectSiteId', selected);
  }

  get selectedSitesIds() {
    return this.$store.state.Booking.selectedSitesIds;
  }

  updateSelectedSiteId(selected) {
    this.selectedSiteId = selected;    
    this.$store.dispatch('getFuneralDirectors', this.selectedSiteId)
    this.selectedSitesIds.length = 0;
    this.selectedSitesIds.push(selected);  
  }    
}
</script>

<style scoped>
  .site-list {
    padding-left: 24px;
  }

  .select-list {
    height: 500px;
    margin-bottom: 50px;
    overflow-y: scroll;
    overflow-x: hidden;
    padding-bottom: 100px;
  }

  .site-radio {
    margin: 15px 0;
  }
</style>
