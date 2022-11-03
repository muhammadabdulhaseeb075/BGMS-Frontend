<template>
  <div id="v-SearchController" data-html2canvas-ignore="true">
     <button v-if="returnLink" @click="bookingReturn" title="BackBooking" class="bookReturn btn sidebar-normal-button" aria-label="Left Align" >
       <i class="fas fa-backward"/><span>&nbsp;&nbsp;Return to Booking</span>
    </button>
    <button @click="toggleOpenSearch" title="Search" :style="{ left: buttonLeft + 'px'}" class="btn sidebar-normal-button btn-bgms btn-left-toolbar" aria-label="Left Align" >
      <span class="icon-Search-Filled" aria-hidden="true"></span>
    </button>
    <div v-if="loadSearch" v-show="openSearch">
      <SearchComponent :key="searchKey"/>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop, Watch } from 'vue-property-decorator'

/**
 * Class representing SearchButton component
 * @extends Vue
 */
@Component({
  components: {
    // async loading for code splitting
    SearchComponent: () => import('./Search.vue')
  }
})
export default class SearchButton extends Vue {
  @Prop() openSearch: boolean = false;

  loadSearch: boolean = false;
  // refreshes the search component when search is closed
  searchKey: number = 0;



  mounted() {
    window.setTimeout(() => {
      if (this.online)
        // delay loading data needed for search component so map gets loaded first
        this.loadRequiredData();
    }, 1500);
  }
  
  /*** Computed ***/

  /**
   * Computed property: Get online status
   * @returns {boolean} True if online
   */
  get online(): boolean {
    return this.$store.state.Offline.online;
  }

   /** Gets the link for returning to booking if redirected from booking page.*/
   get returnLink(){
    return this.$store.state.returnLink;
  }

  /**
   * Computed property:
   * @returns {number} The left position of button
   */
  get buttonLeft(): number {
    if (this.openSearch)
      return 300;
    else
      return 0;
  }

  bookingReturn(){
    const bookingURLs = this.returnLink;
    //redirect to booking pages
    window.location.assign(bookingURLs);
  }

  /*** Watchers ***/

  /**
   * Watcher: When online is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('online')
  onOnlineChanged(val: any, oldVal: any) {
    if (val) {
      this.loadRequiredData();
    }
  }
  
  /*** Methods ***/

  /**
   * Load data required for search to work
   */
  loadRequiredData() {
    if (this.$store.state.includeGravesInSearch==null) {
      // Get the memorial layers from server
      this.$store.dispatch('getIncludeGravesInSearchValue');
    }

    if (!this.$store.state.memorialLayers) {
      // Get the memorial layers from server
      this.$store.dispatch('populateMemorialLayers');
    }

    this.loadSearch = true;
  }

  /**
   * Open/close the search panel
   */
  toggleOpenSearch() {
    if (!this.openSearch && !this.online) {
      let notificationHelper = this.$store.getters.notificationHelper;
      notificationHelper.createWarningNotification("Search functionality is not available while offline.");
    }
    else if (this.openSearch) {
      this.searchKey += 1;
      this.openSearch = false;
    }
    else
      this.openSearch = true;
  }
}
</script>
