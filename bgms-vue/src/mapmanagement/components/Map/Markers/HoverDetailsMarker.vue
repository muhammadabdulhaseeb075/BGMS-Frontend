<template>
<div id="popup" class="ol-popup z-index">
	<div >{{ scope.message }}</div>
</div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';

@Component
export default class HoverDetailsMarker extends Vue {

  @Prop() scope;
}
</script>