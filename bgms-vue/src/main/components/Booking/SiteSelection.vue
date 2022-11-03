<template>
  <div id="site_selection" v-if="selectedSitesIds !== null">
    <v-select 
      class="py-2"
      :value="selectedSitesIds"
      @change="updateSelectedSitesIds"
      :items="bereavementStaffAccessSites"
      item-text="name"
      item-value="id"
      label="Sites"
      multiple
      chips
      hide-details>

      <template v-slot:prepend-item>
        <v-list-item
          ripple
          @click="toggleSelectedSites">
          <v-list-item-action>
            <v-icon :color="selectedSitesIds.length > 0 ? 'indigo darken-4' : ''">{{ siteSelectIcon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ allSitesSelected ? 'Unselect All' : 'Select All' }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>

      <template slot="selection" slot-scope="data">
        <v-chip v-if="data.index <= 10"
          close
          dark
          :color="data.item.preferences.site_color"
          @click:close="data.parent.selectItem(data.item)">
          <strong>{{ data.item.name }}</strong>
        </v-chip>
        <span v-if="data.index === 10" class="grey--text caption">
          (+{{ selectedSitesIds.length - (data.index + 1) }} others)
        </span>
      </template>
    </v-select>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator'

/**
 * Allows the user to select what sites they want to CRUD events from.
 * Selection is persists in vuex.
 */
@Component
export default class SiteSelection extends Vue {

  loadedSites: boolean = false;

  /**
   * Get sites user has bereavement staff access to
   */
  get bereavementStaffAccessSites() {
    return this.$store.getters.getBereavementStaffAccessSites;
  }

  get selectedSitesIds() {
    let ids = this.$store.state.Booking.selectedSitesIds;

    if (!this.loadedSites && !ids.length && this.bereavementStaffAccessSites && this.bereavementStaffAccessSites.length) {
      // initially display all sites
      const siteIds = this.bereavementStaffAccessSites.map(obj => {
        return obj.id;
      });
      ids.push.apply(ids, siteIds);
      this.loadedSites = true;
    }
    return ids;
  }

  get allSitesSelected() {
    return this.selectedSitesIds.length === this.bereavementStaffAccessSites.length;
  }

  get someSitesSelected() {
    return this.selectedSitesIds.length > 0 && !this.allSitesSelected;
  }

  get siteSelectIcon() {
    if (this.allSitesSelected) return 'fas fa-window-close'
    if (this.someSitesSelected) return 'fas fa-minus-square'
    return 'far fa-square'
  }
  
  /**
   * Select all sites if not all already selected.
   * Unselect all sites if all already selected.
   */
  toggleSelectedSites() {

    const sitesToAdd = this.allSitesSelected ? [] : this.bereavementStaffAccessSites.map(a => a.id);

    // remove existing (while keeping reference)
    this.selectedSitesIds.length = 0;
    this.selectedSitesIds.push.apply(this.selectedSitesIds, sitesToAdd);
  }

  /**
   * Update selected sites array without new reference
   */
  updateSelectedSitesIds(selected) {
    this.selectedSitesIds.length = 0;
    this.selectedSitesIds.push.apply(this.selectedSitesIds, selected);
  }
}
</script>