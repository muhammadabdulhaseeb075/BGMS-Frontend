<template>
  <div id="site_selection" v-if="bereavementStaffAccessSites !== null">
    <v-select 
      class="py-2 pt-4"
      :value="selectedSiteId"
      @change="updateSelectedSiteId"
      :items="bereavementStaffAccessSites"
      item-text="name"
      item-value="id"
      label="Sites*"
      chips
      on
      :rules="[() => !!selectedSiteId  || 'Field required']"
      hide-details>

      <template slot="selection" slot-scope="data">
        <v-chip v-if="data.index <= 10"
          dark
          :close="true"
          :color="data.item.preferences.site_color"
          @click:close="data.parent.selectItem(undefined)"
        >
          <strong>{{ data.item.name }}</strong>
        </v-chip>
      </template>
    </v-select>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop, Watch } from 'vue-property-decorator';

/**
 * Allows the user to select what sites they want to CRUD events from.
 * Selection is persists in vuex.
 */
@Component
export default class SiteSelector extends Vue {

  loadedSites: boolean = false;
  /**
   * Get sites user has bereavement staff access to
   */
  get bereavementStaffAccessSites() {
    return this.$store.getters.getBereavementStaffAccessSites;
  }

  get selectedSiteId() {
    return this.$store.state.Booking.selectedSiteId;
  }

  set selectedSiteId(selected){
    this.$store.commit('selectSiteId', selected)
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