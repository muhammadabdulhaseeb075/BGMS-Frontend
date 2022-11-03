<template>
  <div id = "memorialCaptureSidebar" class="sidebar">
    <div id="sidebar-header">
      <span class="sidebar-title-span"><h1 class="sidebar-title">Memorial Capture</h1></span>
      <span v-show="!closeInitiated" id="sidebar-close" class="sidebar-navigation sidebar-close" @click="initiateCloseSidebar" title="Close"><i class="fa fa-times sidebar-navigation-icon"></i></span>
      <span v-show="closeInitiated" id="sidebar-close-initiated" class="sidebar-navigation"><i class="fa fa-times sidebar-navigation-icon"></i></span>
    </div>
    <div id="sidebar-body">
      <div class="sidebar-message" v-if="!isOnlineOrServiceWorkerInControl">
        <div class="sidebar-message-contents">
          <h1>You are offline</h1>
          <div>Offline functionality is not currently available on this device.</div>
        </div>
      </div>
      <div class="sidebar-message" v-if="!isMemorialSelected && isOnlineOrServiceWorkerInControl">
        <div class="sidebar-message-contents">
          <h1>Click a memorial to capture data</h1>
          <div><span class="fa fa-times"/> indicates a memorial which has no image.</div>
        </div>
      </div>
      <div id="mc-sections" v-show="isOnlineOrServiceWorkerInControl && isMemorialSelected">
        
        <div class="panel photosComponent" v-if="memorialPhotographyAccess">
          <div class="panel-header">
            <!--Removed collapsable panel as closing the image viewer also closed the panel.-->
            <button class="sidebar-subheading" type="button" aria-expanded="!collapsed" aria-controls="photoCollapse" disabled>
            Photos
            </button>
          </div>
          <div id="photoCollapse" ref="photoCollapse">
            <div class="panel-body">
              <Photos :takingPhotoSupported='takingPhotoSupported' v-if="isMemorialSelected" :updateMemorialIndicators="true"/>
            </div>
          </div>
        </div>

        <Details v-if="isMemorialSelected && siteAdminOrSiteWarden"/>

        <Inscriptions v-if="isMemorialSelected && siteAdminOrSiteWarden"/>

        <div id="inspectionsComponent" class="panel" v-if="siteAdminOrSiteWarden">
          <div class="panel-header">
            <button :class="{collapsed: inspectionCollapsed}" class="sidebar-subheading" type="button" data-toggle="collapse" data-target="#inspectionCollapse" aria-expanded="!collapsed" aria-controls="inspectionCollapse">
            Inspections
            </button>
          </div>
          <div :class="{in: !inspectionCollapsed}" class="collapse collapseSection" id="inspectionCollapse" ref="inspectionCollapse">
            <div class="panel-body">
              <Inspections :takingPhotoSupported='takingPhotoSupported' v-if="isMemorialSelected"/>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Component, { mixins } from 'vue-class-component'
import { Watch } from 'vue-property-decorator'
import Photos from '@/mapmanagement/components/MapTools/MemorialCaptureSidebar/Photos.vue'
import Inscriptions from '@/mapmanagement/components/MapTools/MemorialCaptureSidebar/Inscriptions.vue'
import Details from '@/mapmanagement/components/MapTools/MemorialCaptureSidebar/Details.vue'
import Inspections from '@/mapmanagement/components/MapTools/MemorialCaptureSidebar/Inspections.vue'
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import Text from 'ol/style/Text';
import Sidebar from '@/mapmanagement/mixins/memorialSidebar'

/**
 * Class representing MemorialCaptureSidebar component
 * @extends Vue
 */
@Component({
  components: {
    Photos,
    Inscriptions,
    Details,
    Inspections
  }
})
export default class MemorialCaptureSidebar extends mixins(Sidebar){

  takingPhotoSupported: boolean = false;
  memorialPhotographyAccess: boolean = this.$store.state.memorialPhotographyAccess;
  siteAdminOrSiteWarden: boolean = this.$store.state.siteAdminOrSiteWarden;

  created() {
    this.$store.commit('updateSidebarType', this.$store.state.MemorialSidebar.sideBarTypeEnum.memorialCapture);
  }

  /**
   * Vue mounted lifecycle hook
   * - registers jQuery event to listen for memorial changes
   * - detects if taking a photo is supported
   */
  mounted() {

    (window as any).jQuery(document).off('memorialSelectedForMemorialCapture').on('memorialSelectedForMemorialCapture', this.memorialSelectedForMemorialCapture);

    // Detect if taking a photo is supported
    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const constraints = {
        audio: false,
        video: {
          facingMode: { exact: "environment" },
          width:  { ideal: 9999 },
          height: { ideal: 9999 },
        }
      };

      // Get the camera stream
      navigator.mediaDevices.getUserMedia(constraints)
      .then(str => {
        this.takingPhotoSupported = true;

        // close the stream
        let stream = str;
        stream.getTracks().forEach(function(track){ track.stop(); });
        stream = null;
      })
      .catch(err => {
        this.takingPhotoSupported = false;
      });
    }

    // used for photos and inspection component
    // (other components has this included, not photos as it is also used in featuresidebar)
    (window as any).jQuery(this.$refs.photoCollapse).on('hidden.bs.collapse', () => {
      this.$store.commit('setPhotoCollapsed', true);
    });

    (window as any).jQuery(this.$refs.photoCollapse).on('shown.bs.collapse', () => {
      this.$store.commit('setPhotoCollapsed', false);
    });

    (window as any).jQuery(this.$refs.inspectionCollapse).on('hidden.bs.collapse', () => {
      this.$store.commit('setInspectionCollapsed', true);
    });

    (window as any).jQuery(this.$refs.inspectionCollapse).on('shown.bs.collapse', () => {
      this.$store.commit('setInspectionCollapsed', false);
    });
  }

  /*** Watchers ***/

  /**
   * Watcher: When the sidebar width needs changed, this fires event
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('narrowSidebar', { immediate: true})
  onNarrowSidebarChanged(val: boolean, oldVal: any) {
    if (oldVal !== undefined && val != oldVal) {
      if (val)
        (window as any).jQuery(document).trigger('narrowSidebar');
      else
        (window as any).jQuery(document).trigger('wideSidebar');
    }
  }

  /*** Computed ***/

  /**
   * Computed property: Is app online or has service worker installed and active
   * @returns {boolean}
   */
  get isOnlineOrServiceWorkerInControl(): boolean {
    return this.$store.state.Offline.online || this.$store.state.Offline.offlineReady;
  }

  /**
   * Computed property: Get photoCollapsed
   * @returns {boolean} True if this section should be collapsed
   */
  get photosCollapsed(): boolean {
    return this.$store.state.MemorialCaptureSidebar.photoCollapsed;
  }

  /**
   * Computed property: Get inspectionCollapsed
   * @returns {boolean} True if this section should be collapsed
   */
  get inspectionCollapsed(): boolean {
    return this.$store.state.MemorialCaptureSidebar.inspectionCollapsed;
  }
  
  /*** Methods ***/

  /**
   * Called when the user selects a memorial
   * @param {any} e
   * @param {any} memorial - The selected memorial
   */
  memorialSelectedForMemorialCapture(e:any, memorial:any) {
    this.memorialSelected(memorial);
  }
}
</script>
