<template>
  <div>  
    <router-view :componentProp="componentProp"></router-view>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'
import constants from '@/mapmanagement/static/constants.ts';
import globalConstants from '@/global-static/constants.ts';

// Register the router hooks with their names
Component.registerHooks([
  'beforeRouteUpdate',
  'beforeRouteLeave',
  'beforeRouteEnter'
])

/**
 * Class representing ContentContainer component
 * This is component is a container for components to be displayed in the management tool.
 */
@Component
export default class ContentContainer extends Vue {

  @Prop() componentProp: any;
  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    // While transitioning, contentbar should be at back so it appears behind the tool bar.
    // After transition, contentbar should be at the from so overlays work (i.e. highest z-index)
    let element = document.getElementById("management-tool-contentbar");
    element.addEventListener("transitionend", this.putElementAtFront);
    
    window.setTimeout(() => {
      // set right
      document.getElementById('management-tool-contentbar').style.right = "0px";
    });
  }

  /**
   * Vue router beforeRouteEnter in-component guard
   */
  beforeRouteEnter (to, from, next) {
    let narrowTool = to.name===globalConstants.BURIAL_PERSON_MANAGEMENT_PATH || to.path.indexOf('/' + globalConstants.BURIAL_PERSON_MANAGEMENT_PATH + '/') !== -1;
    
    let toolWidth = narrowTool ? constants.TOOL_WIDTH_NARROW : constants.TOOL_WIDTH;
    
    // set layers accordion position
    let layersAccordion = document.getElementById('layersAccordion');
    if (layersAccordion) layersAccordion.style.right = toolWidth + constants.TOOL_CONTENT_WIDTH + constants.TOOL_BORDER_WIDTH + 10 + "px";

    next();
  }

  /**
   * Puts contentbar 1 z-index in front of the tool bar
   */
  putElementAtFront() {
    let element = document.getElementById("management-tool-contentbar-container");
    element.style.zIndex = '1031';
  }

  /**
   * Vue router beforeRouteUpdate in-component guard
   */
  beforeRouteUpdate (to, from, next) {

    this.checkUnsavedChanges(to, from)
    .then((cont) => {
      next(cont);
    })
    .catch(() => {
      next(false);
    });
  }

  /**
   * Vue router beforeRouteLeave in-component guard
   */
  beforeRouteLeave(to, from, next) {

    this.checkUnsavedChanges(to, from)
    .then((cont) => {
      if (cont) {
        // put contentbar to back ready for next opening
        let element = document.getElementById('management-tool-contentbar-container');
        if (element)
          element.style.zIndex = '-1';

        element = document.getElementById("management-tool-contentbar");
        if (element)
          element.removeEventListener("transitionend", this.putElementAtFront);
        
        this.closeToolContent();

        // allow time for animation to finish before leaving
        window.setTimeout(() => {
          next();
        }, 300);
      }
      else
        next(false);
    })
    .catch(() => {
      next(false);
    });
  }

  /**
   * Closes contents page of the management tool.
   */
  closeToolContent() {
    // Don't do this if tool has been closed. Vue-router will then take care of this.
    if (this.$route.name && document.getElementById('management-tool-contentbar-container') && document.getElementById('management-tool-contentbar')) {
      // set layers accordion position
      let layersAccordion = document.getElementById('layersAccordion');
      if (layersAccordion) layersAccordion.style.right = constants.TOOL_WIDTH + 10 + "px";

      // set right
      document.getElementById('management-tool-contentbar').style.right = - constants.TOOL_CONTENT_WIDTH - constants.TOOL_BORDER_WIDTH + "px";
      document.getElementById('management-tool-contentbar').style.maxHeight = "0px"
    }
  }

  /**
   * If applicable, checks for unsaved data.
   * If unsaved data, askes user for permission to continue.
   */
  checkUnsavedChanges(to, from): Promise<boolean> {

    return new Promise<boolean>((resolve) => {
      // true if a new management tool has been selected (i.e. grave management or memorial management) 
      const managementToolChanged = to.params.id !== from.params.id;
      // true if a different section has been selected
      const sectionChanged = !managementToolChanged && to.name !== from.name;
      // true a form is toggling between edit and view mode

      const editViewModeToggle = !managementToolChanged && !sectionChanged && to.query.edit !== from.query.edit;

      let movingToEditForm = null;
      let movingToViewForm = null;

      // if a form is toggling between edit and view mode
      if (editViewModeToggle) {
        movingToEditForm = to.query.edit === true;
        movingToViewForm = from.query.edit === true;
      }

      let unsavedChangesResult = null;

      if (!movingToEditForm && from.path != '/') {

        unsavedChangesResult = this.unsavedChanges();

        if (unsavedChangesResult != null) {
          const notificationHelper = this.$store.getters.notificationHelper;

          // ask user for confirmation that they want to discard changes
          notificationHelper.createConfirmation("Unsaved Changes", "You have unsaved changes that will be lost if you move away from this screen.\n\nDo you want to continue?", 
          () => { 
            // user responded positively
            if (movingToViewForm || (!managementToolChanged && !sectionChanged)) {
              // set flag for the component to restore it's data from saved (only needed if returning to viewmode)
              this.$store.commit('commitRestoreSavedDataFlag', unsavedChangesResult);
            }

            resolve(true); 
          }, 
          () => { 
            // user responded negatively
            
             // reset navigation flags
            this.$store.commit('goBackFlag', false);
            this.$store.commit('goForwardFlag', false);
            this.$store.commit('closeFlag', false);

            resolve(false);
          });
        }
      }
      
      if (unsavedChangesResult == null) 
        resolve(true);
    });
  }

  /**
   * Checks is there are unsaved changes in current screen.
   * @returns {string} Component containing unsaved changes (or null if no unsaved changes)
   */
  unsavedChanges() {

    const currentInformation = this.$store.state.ManagementTool.currentInformation;

    // Each component will have an object containing its data in currentInformationSaved.
    // Iterate through these objects.
    for (let component in currentInformation) {
      if (currentInformation[component] && typeof currentInformation[component] === 'object') {
        // check if this component has unsavedChanges
        if (currentInformation[component].unsavedChanges)
          return component;
      }
    }

    return null;
  }
}
</script>
