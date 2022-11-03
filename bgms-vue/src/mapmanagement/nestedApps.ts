import Vue from 'vue'
import router from '@/mapmanagement/router/index.js';
import store from './store'
import SecurityMixin from '@/mixins/securityMixin'

/**
 * Class is used to dynamically add Vue components as apps into AngularJS.
 * Once all AngularJS code is migrated we won't need this.
 */
export default class NestedApps {

  constructor() {
    /**
     * Adds a function to window. This is used by Angular.js to launch vue apps.
     * Imports the required component asynchronously (doing it like this allows webpack code splitting)
     * and then creates new app.
     * The new app is returned to Angular.js controller.
     * @returns - promise that resolves the new vue app.
     */
    (window as any).initVue = (id, component) => {
      if (component === 'MemorialCaptureSidebar'){
        return import('@/mapmanagement/components/MapTools/MemorialCaptureSidebar/MemorialCaptureSidebar.vue').then(com => {
          return this.createNewApp(id, com);
        });
      }
      else if (component === 'ManagementTool'){
        return import('@/mapmanagement/components/ManagementTool/ManagementTool.vue').then(com => {
          return this.createNewApp(id, com);
        });
      }
      else if (component === 'ExportMap') {
        return import('@/mapmanagement/components/MapTools/ExportMap.vue').then(com => {
          return this.createNewApp(id, com);
        });
      }
      else if (component === 'DrawingTools') {
        return import('@/mapmanagement/components/MapTools/DrawingToolsAccordion.vue').then(com => {
          return this.createNewApp(id, com);
        });
      }
      else if (component === 'OtherTools') {
        return import('@/mapmanagement/components/MapTools/OtherToolsAccordion.vue').then(com => {
          return this.createNewApp(id, com);
        });
      }
      else if (component === 'GraveLinkSidebar') {
        return import('@/mapmanagement/components/MapTools/GraveLinkSidebar.vue').then(com => {
          return this.createNewApp(id, com);
        });
      }
      else if (component === 'LayersToolbar') {
        return import('@/mapmanagement/components/MapTools/LayersToolbar.vue').then(com => {
          return this.createNewApp(id, com);
        });
      }
    }
  }

  /**
   * Called from AngularJS controllers to create new Vue apps
   * @param id ID for the new app
   * @param component Component to load
   * @returns Returns a new Vue app with the given component loaded.
   */
  createNewApp(id, component) {
    return new Vue({
      el: id,
      store,
      router,
      mixins: [SecurityMixin],
      render: (h) => h(component.default),
    });
  }
}
