<template>
  <div id="DataMatchingVueApp">

    <Analytics></Analytics>

    <div class="main-sidebar">
      <!-- sidebar: style can be found in sidebar.less -->
      <div class="sidebar" id="scrollspy">

        <!-- sidebar menu: : style can be found in sidebar.less -->
        <ul class="nav sidebar-menu">
          <li class="header"><h3>Memorials</h3></li>
          <li :class="{ active: $route.name === 'Index' }"><a @click="$router.push({ name: 'Index' })"><i class="fa far fa-circle"></i> Image Matching</a></li>
          <!-- This searches for photo filename. Remove as we think it is uneccessary
          <li>
            <form action="" @submit="searchByImage" class="navbar-form navbar-left">
              <div class="form-group">
                <input type="text" class="form-control" placeholder="Search By Image Name" v-model="imageSearchTerm">
              </div>
            </form>
          </li>-->
        </ul>

        <ul v-if="siteAdminOrSiteWarden" class="nav sidebar-menu">
          <li class="header"><h3>History</h3></li>
          <li :class="{ active: $route.name === 'MemorialStatus' }"><a @click="$router.push({ name: 'MemorialStatus' })"><i class="fa far fa-circle"></i> Memorial Status</a></li>
          <li :class="{ active: $route.name === 'UserActivity' }"><a @click="$router.push({ name: 'UserActivity' })"><i class="fa far fa-circle"></i> User Activity</a></li>
        </ul>
      </div>
      <!-- /.sidebar -->
    </div>
    <router-view class="main-contents"/>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import Component, { mixins } from 'vue-class-component'
import axios from 'axios'
import vueRouter from 'vue-router'
import SecurityMixin from '@/mixins/securityMixin'
import Analytics from '@/main/components/Analytics.vue';

Vue.use(Vuex);
Vue.use(vueRouter);

/**
 * Class representing DataMatchingVueApp component
 * @extends Vue
 */
@Component({
  components: {
    Analytics
  }
})
export default class DataMatchingVueApp extends mixins(SecurityMixin) {
  
  siteAdminOrSiteWarden = null;

  //imageSearchTerm = "";

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    
    let v = this;

    v.getGroupRequiredValue(['SiteAdmin', 'SiteWarden'])
    .then((result) => {
      v.siteAdminOrSiteWarden = result;
    })
    .catch(() => {
      v.siteAdminOrSiteWarden = false;
    });
  }

  /*** Watchers ***/

  /*** Computed ***/

  /*** Methods ***/

  /*searchByImage() {

    let v = this;

    axios.get('/datamatching/searchImages/', { params: { image_search: v.imageSearchTerm }})
      .then(function(response) {
        v.imageSearchTerm = "";
        // refresh the memorial data
        v.$router.go(0);
      })
      .catch(function(response) {
        console.warn('Unable to find image using search term:', response);
      });
  }*/
}
</script>