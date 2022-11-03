<template>
  <div id="popup" class="ol-popup">

  <div v-for="person in scope.personsPage" :key="person.id">
    <a style="cursor: pointer;"><strong>{{person.last_name}} </strong></a>

  </div>

</div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';

@Component
export default class DisplayNameMarker extends Vue {


  @Prop() scope;


}
</script>
