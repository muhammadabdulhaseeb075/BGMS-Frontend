import Vue from 'vue'
import Vuex from 'vuex'
import Component from 'vue-class-component'
import { VISUALISATIONENUM, showMemorialIndicators, hideMemorialIndicators, createMemorialBenchImageOverlay, showMemorialIndicatorForSingleMemorial } from '@/mapmanagement/components/Map/models/Memorial';

Vue.use(Vuex);

/**
 * Sidebar mixin
 * @extends Vue
 */
@Component
export default class memorialSidebar extends Vue{

  closeInitiated: boolean = false;

  notificationHelper: any = this.$store.getters.notificationHelper;

  /**
   * Vue mounted lifecycle hook
   * - sets sidebar width
   * - stores selected marker styleLayer
   */
  mounted() {
    window.setTimeout(() => {
      if (this.$store.state.MemorialSidebar.sideBarType === this.$store.state.MemorialSidebar.sideBarTypeEnum.memorialCapture && this.narrowSidebar) {
        (window as any).jQuery(document).trigger('narrowSidebar');
      }
      else {
        (window as any).jQuery(document).trigger('wideSidebar');
      }
    });

    // Turns on image visualisation (ticks and crosses)
    showMemorialIndicators(this.$store.state.MemorialSidebar.sideBarType === this.$store.state.MemorialSidebar.sideBarTypeEnum.memorialCapture ? VISUALISATIONENUM.image : VISUALISATIONENUM.graveLink);
  }

  /*** Watchers ***/


  /*** Computed ***/

  /**
   * Computed property: Is a memorial selected?
   * @returns {boolean}
   */
  get isMemorialSelected(): boolean {
    return this.$store.state.MemorialSidebar.memorial !== null && this.$store.state.MemorialSidebar.memorial !== undefined;
  }

  /**
   * Computed property: Should the sidebar be narrow or wide (depends on which sections are collapsed)
   * @returns {boolean}
   */
  get narrowSidebar(): boolean {
    return this.$store.getters.narrowSidebar;
  }  

  /*** Methods ***/

  /**
   * Called when the user selects a memorial
   * @param {any} memorial - The selected memorial
   */
  memorialSelected(memorial:any) {
    let v = this;

    let currentMemorial = this.$store.state.MemorialSidebar.memorial;

    // if changing memorial, first check if there are unsaved changes
    if (v.$store.state.MemorialSidebar.sideBarType === v.$store.state.MemorialSidebar.sideBarTypeEnum.memorialCapture 
      && currentMemorial && memorial.getId() !== currentMemorial.getId()
      && v.$store.getters.unsavedMemorialCaptureChanges) {
        // there are unsaved changes
        v.notificationHelper.createConfirmation(
          "Memorial Capture", "You have unsaved changes which will be lost if you select a new memorial.\n\nDo you want to continue?", function() {
          // user has choosen to lose unsaved changes
          v.selectNewMemorial(currentMemorial, memorial);
        });
    }
    else
      v.selectNewMemorial(currentMemorial, memorial);
  }

  /**
   * Called when currently selected memorial has been closed (if it exists) and we're ready to load the new memorial
   * @param {any} currentMemorial - previously selected memorial (if it exists)
   * @param {any} newMemorial - newly selected memorial
   */
  selectNewMemorial(currentMemorial, newMemorial) {
    let v = this;

    // checks if this is a new or different memorial
    if (!currentMemorial || newMemorial.getId() !== currentMemorial.getId()) {

      v.closeCurrentMemorial(currentMemorial)
      .then(() => {
        //highlight selected memorial
        if (newMemorial.get("marker_type") === "memorials_bench") {
          if (v.$store.state.MemorialSidebar.sideBarType === v.$store.state.MemorialSidebar.sideBarTypeEnum.memorialCapture)
            newMemorial.setStyle(createMemorialBenchImageOverlay(VISUALISATIONENUM.image, true, newMemorial));
          else (v.$store.state.MemorialSidebar.sideBarType === v.$store.state.MemorialSidebar.sideBarTypeEnum.graveLink)
            newMemorial.setStyle(createMemorialBenchImageOverlay(VISUALISATIONENUM.graveLink, true, newMemorial));
        }
        else {
          let originalMemorialStyle = newMemorial.getStyle()[0];
          let highlightedStyle = originalMemorialStyle.clone();
          highlightedStyle.setText(v.$store.state.Styles.markerText);
          highlightedStyle.setZIndex(2000);
          newMemorial.setStyle([highlightedStyle]);
        }

        v.$store.commit('updateMemorial', newMemorial);
      })
      .catch((reason) => {
        console.log('Handle rejected promise ('+reason+') here.');
      });
    }
  }

  /**
   * Closes the current memorial:
   * -removes highlighting
   * -resets the data ready for the next selection
   */
  closeCurrentMemorial(currentMemorial) {
    return new Promise((resolve, reject) => {
      if (currentMemorial) {
        
        if (this.$store.state.MemorialSidebar.sideBarType === this.$store.state.MemorialSidebar.sideBarTypeEnum.memorialCapture) {
          showMemorialIndicatorForSingleMemorial(VISUALISATIONENUM.image, currentMemorial, currentMemorial.get('marker_type'));
          this.$store.commit('resetMemorialCaptureSidebar');
        }
        else if (this.$store.state.MemorialSidebar.sideBarType === this.$store.state.MemorialSidebar.sideBarTypeEnum.graveLink) {
        // resets the icons
          hideMemorialIndicators();
          showMemorialIndicators(VISUALISATIONENUM.graveLink); // TODO: Should be no need to reload the ENTIRE visualisation
        }

        this.$store.commit('resetSidebar');

        resolve();
      }
      else
        resolve();
    });
  }

  /**
   * Closes the sidebar
   */
  initiateCloseSidebar() {
    let v = this;

    v.closeInitiated = true;
    let currentMemorial = this.$store.state.MemorialSidebar.memorial;

    if (v.$store.state.MemorialSidebar.sideBarType === v.$store.state.MemorialSidebar.sideBarTypeEnum.memorialCapture && currentMemorial
      && v.$store.getters.unsavedMemorialCaptureChanges) {
        v.notificationHelper.createConfirmation("Memorial Capture", "You have unsaved changes which will be lost if you close Memorial Capture.\n\nDo you want to continue?", function() {
          v.closeSidebar();
        }, function() {
          v.closeInitiated = false;
        });
    }
    else if (currentMemorial && v.$store.state.MemorialSidebar.stopSidebarClose) {
      v.closeSidebarWait()
    }
    else
      v.closeSidebar();
  }

  closeSidebarWait() {
    if (this.$store.state.MemorialSidebar.stopSidebarClose) {
      setTimeout(this.closeSidebarWait, 500);
    }
    else
      this.closeSidebar();
  }

  /**
   * Closes the sidebar
   */
  closeSidebar() {
    this.closeCurrentMemorial(this.$store.state.MemorialSidebar.memorial)
    .catch((reason) => {
      console.log('Handle rejected promise ('+reason+') here.');
    });
    
    // Turns off image visualisation (ticks and crosses)
    hideMemorialIndicators();

    (window as any).jQuery(document).trigger('closeSidebar');
    this.$store.commit('resetSidebar');

    if (this.$store.state.MemorialSidebar.sideBarType === this.$store.state.MemorialSidebar.sideBarTypeEnum.memorialCapture)
      this.$store.commit('resetMemorialCaptureSidebar');

    this.closeInitiated = false;
  }
}
