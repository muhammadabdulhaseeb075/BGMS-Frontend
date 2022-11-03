<template>
  <div id = "graveLinkSidebar" class="sidebar">
    <div id="sidebar-header">
      <span class="sidebar-title-span"><h1 class="sidebar-title">Grave Link</h1></span>
      <span v-show="!closeInitiated" id="sidebar-close" class="sidebar-navigation sidebar-close" @click="initiateCloseSidebar" title="Close"><i class="fa fa-times sidebar-navigation-icon"></i></span>
      <span v-show="closeInitiated" id="sidebar-close-initiated" class="sidebar-navigation"><i class="fa fa-times sidebar-navigation-icon"></i></span>
    </div>
    <div id="sidebar-body">
      <div class="sidebar-message" v-if="!isOnline">
        <div class="sidebar-message-contents">
          <h1>You are offline</h1>
          <div>This feature is not available while offline.</div>
        </div>
      </div>
      <div class="sidebar-message" v-if="!isMemorialSelected && isOnline">
        <div class="sidebar-message-contents">
          <h1>Click a memorial to link to a grave</h1>
          <div><span class="fa fa-times"/> indicates a memorial which is not linked to a grave.</div>
        </div>
      </div>
      <div v-if="isMemorialSelected" v-show="isOnline">
        <GraveLinkComponent :id="memorial.getId()" class="panel"/>
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component';
import Sidebar from '@/mapmanagement/mixins/memorialSidebar.ts';
import GraveLinkComponent from '@/mapmanagement/components/MapTools/GraveLinkComponent.vue';

/**
 * Class representing GraveLinkSidebar component
 * @extends Sidebar mixin
 */
@Component({
  components: {
    GraveLinkComponent
  }
})
export default class GraveLinkSidebar extends mixins(Sidebar){

  /**
   * Vue mounted lifecycle hook
   */
  created() {
    this.$store.commit('updateSidebarType', this.$store.state.MemorialSidebar.sideBarTypeEnum.graveLink);
  }

  /**
   * Vue mounted lifecycle hook
   * - registers jQuery event to listen for memorial changes
   */
  mounted() {
    let v= this;

    (window as any).jQuery(document).off('memorialSelectedForGraveLink').on('memorialSelectedForGraveLink', v.memorialSelectedForGraveLink);
  }

  /*** Computed ***/

  /**
   * Computed property: Is app online or has service worker installed and active
   * @returns {boolean}
   */
  get isOnline(): boolean {
    return this.$store.state.Offline.online;
  }

  /**
   * Computed property: Get the selected memorial
   * @returns {any} memorial
   */
  get memorial() {
    return this.$store.state.MemorialSidebar.memorial;
  }

  /*** Methods ***/

  /**
   * Called when the user selects a memorial
   * @param {any} e
   * @param {any} memorial - The selected memorial
   */
  memorialSelectedForGraveLink(e:any, memorial:any) {
    this.memorialSelected(memorial);
  }
}
</script>
