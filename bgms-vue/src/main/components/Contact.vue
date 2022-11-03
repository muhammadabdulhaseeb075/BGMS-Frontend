<template>
  <v-container id="contactUs">
    <h1 class="text-center pb-4">Contact Us</h1>
    <address>
      <v-row>
        <v-col cols="2">
          <v-icon class="pr-4">fas fa-envelope</v-icon>
        </v-col>
        <v-col cols="10">
          <a href="mailto:bgms@atlanticgeomatics.co.uk">bgms@atlanticgeomatics.co.uk</a>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="2">
          <v-icon class="pr-4">fas fa-phone</v-icon>
        </v-col>
        <v-col cols="10">
          +44 (0) 17684 83310
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="2">
          <v-icon class="pr-4">fas fa-map-marker-alt</v-icon>
        </v-col>
        <v-col cols="10">
          Atlantic Geomatics<br>
          Unit M<br>
          Skirsgill Business Park<br>
          Penrith<br>
          Cumbria<br>
          CA11 0FA
        </v-col>
      </v-row>
    </address>
  </v-container>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import axios from 'axios'

/**
 * Component for displaying table of funeral events
 */
@Component
export default class FuneralBookings extends Vue {

  /*** Lifecycle hooks ***/

  /*** Getters and setters ***/

  /*** Watchers ***/

  /*** Methods ***/
}
</script>

<style scoped>
#contactUs {
  max-width: 400px;
}

address {
  font-style: normal;
  font-size: 1.3em;
}
</style>