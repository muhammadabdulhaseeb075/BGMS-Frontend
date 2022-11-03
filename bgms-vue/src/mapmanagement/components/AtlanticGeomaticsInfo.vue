<template>
  <div id="atlanticGeomaticsInfo" :class="[{ 'collapsed': hideFullLogo }, 'btn']" data-html2canvas-ignore="true">
    <button class='btn' title="Atlantic Geomatics" @click="collapsed = !collapsed">
      <img :src="require('@/mapmanagement/static/images/ag-logo.png')" crossorigin="anonymous" />
    </button>

    <div :class="[{ 'collapsed': collapsed }, 'ag-info-panel']">
      <address class="ag-info-panel-body">
        <b>ATLANTIC GEOMATICS (INT'L) LIMITED</b><br>
        Unit M, Skirsgill Business Park,<br>
        Penrith, Cumbria, CA11 0FA<br>

        <span>Tel: </span>+44 (0) 17684 83310<br>
        <span>Email: </span><a href="mailto:bgms@atlanticgeomatics.co.uk">bgms@atlanticgeomatics.co.uk</a><br>
        <span>Website: </span> <a href="https://www.atlanticgeomatics.co.uk" target="_blank">www.atlanticgeomatics.co.uk</a>
      </address>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import { Watch } from 'vue-property-decorator'

/**
 * Class representing AtlanticGeomaticsInfo component
 * @extends Vue
 */
@Component
export default class AtlanticGeomaticsInfo extends Vue {

  collapsed: boolean = true;

  /*** Computed ***/

  get hideFullLogo(): boolean {
    const hide = this.$store.state.authenticatedSession && this.collapsed;

    let attributions = document.getElementsByClassName('ol-attribution');

    if (attributions.length) {
      if (hide)
        attributions[0].classList.remove('full-logo');
      else
        attributions[0].classList.add('full-logo');
    }
      

    return hide;
  }

  /*** Watchers ***/

  /*** Methods ***/
}
</script>
