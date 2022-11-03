<template>
  <v-app id="MainVueApp">

    <Analytics></Analytics>

		<div class="top-nav">
      <header class="navbar navbar-expand-lg navbar-light" role="navigation">
        <v-row no-gutters>
          <router-link to="/">
            <div class="logo">
              <div class="logo-navigation-bar"></div>
            </div>
          </router-link>

          <div class="flex-grow-1"></div>
          
          <v-menu bottom content-class="user-menu">
            <template v-slot:activator="{ on }">
              <v-btn
                dark
                text
                v-on="on">
                <i class="fas fa-user"/>
                <span><i class="user-menu-user">{{ username }}</i></span>
                <i class="fas fa-caret-down"/>
              </v-btn>
            </template>
            <v-list>
              <v-list-item tag="a" href="/logout/" nav>
                <v-list-item-title>Log Out</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-row>
      </header>
		</div>
    <router-view></router-view>

    <div class="flex-grow-1"></div>

    <v-footer class="page-footer" color="grey lighten-2">
      <v-row>
        <v-col cols="4" class="copyright py-0">
          © {{new Date().getFullYear()}} Atlantic Geomatics (Int'l) Limited
        </v-col>
        <v-col cols="4" class="text-center py-0">
          <a href="https://www.atlanticgeomatics.co.uk" target="_blank">
            <img style="vertical-align: middle" :src="require('@/mapmanagement/static/images/ag-logo.png')" crossorigin="anonymous" />
          </a>
        </v-col>
        <v-col cols="4" class="text-right py-0">
          <v-btn text :to="{ name: 'contact' }">CONTACT</v-btn>
          <!--<v-btn text target="_blank" href="/docs/BGMS_User_Guide.pdf">USER GUIDE</v-btn>-->
        </v-col>
      </v-row>
    </v-footer>

  </v-app>
</template>

<script lang='ts'>
import Vue from 'vue';
import axios from 'axios';
import Component, { mixins } from 'vue-class-component';
import Analytics from '@/main/components/Analytics.vue';

@Component({
  components: {
    Analytics
  }
})
export default class Main extends Vue {
  
  get username() {
    return (window as any).document.user.username;
  }
}
</script>