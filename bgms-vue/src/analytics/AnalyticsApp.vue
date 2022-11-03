<template>
  <v-app class="app-wrapper">
    <div id="AnalyticsApp">
      <vertical-menu />
      <div class="analytics-content">
        <router-view/>
      </div>
    </div>
  </v-app>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import VerticalMenu from './components/VerticalMenu/index.vue';

@Component({
    components: {
        VerticalMenu
    }
})
export default class Reports extends Vue {
  name: 'AnalyticsApp'
}

</script>

<style>
  #AnalyticsApp {
    background-color: white;
    display: flex;
    height: calc(100vh - 50px);
  }

  /** This class is setting the full viewport height to the component by default */
  .v-application--wrap {
    min-height: 0vh !important;
  }

  .analytics-content {
    overflow: auto;
    width: 100%;
  }
</style>
