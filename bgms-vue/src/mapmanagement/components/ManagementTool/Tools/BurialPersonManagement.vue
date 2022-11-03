<template>
  <div id="burialPersonManagementComponent" class="management-tool-buttons-container">
    <div id="management-tool-contentbar-container">
      <router-view id="management-tool-contentbar"></router-view>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import Component, { mixins } from 'vue-class-component'
import { Watch } from 'vue-property-decorator'
import FeatureTools from '@/mapmanagement/mixins/featureTools.ts'
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin.ts';

Vue.use(Vuex);

/**
 * Class representing BurialPersonManagement
 * @extends ManagementToolsMixin mixin
 * @extends FeatureTools mixin
 */
@Component({
  components: {
    ContentContainer: () => import('@/mapmanagement/components/ManagementTool/FormHelperComponents/ContentContainer.vue')
  }
})
export default class BurialPersonManagement extends mixins(ManagementToolsMixin, FeatureTools) {

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    this.componentName = "burialpersonmanagement";
    this.$store.commit('setTitle', "Person");

    this.openTool(true);
  }
  
  /*** Computed ***/

  /*** Watchers ***/
  
  /*** Methods ***/
}
</script>
