<template>
  <div id="scroll-buttons">
    <div class="scroll-button" v-show="scrollBarShown">
      <a class="form-icon" @mouseenter="scrollEvent(-0.5)" @mouseleave="stopScrollFlag=true" :class="{ active: canScrollUp }">
        <i class="fa fa-angle-up"></i>
      </a>
    </div>
    <div id="verticalScroll" ref="verticalScroll" class="vertical-scroll" :class="{ 'parent-scroll': parentScroll }" :style="{ 'width': componentWidth }">
      <slot/>
    </div>
    <div class="scroll-button" v-show="scrollBarShown">
      <a class="form-icon" @mouseenter="scrollEvent(1)" @mouseleave="stopScrollFlag=true" :class="{ active: canScrollDown }">
        <i class="fa fa-angle-down"></i>
      </a>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator'
import constants from '@/mapmanagement/static/constants.ts';

/**
 * Class representing ScrollButtons component
 */
@Component
export default class ScrollButtons extends Vue {

  @Prop() heightChangedFlag;
  @Prop() noChangeParentHeight;
  @Prop() parentScroll;

  scrollBarShown: boolean = false;
  stopScrollFlag: boolean = true;
  canScrollUp: boolean = false;
  canScrollDown: boolean = false;

  componentWidth = constants.TOOL_CONTENT_WIDTH + 'px';

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    let v = this;

    if (!this.noChangeParentHeight)
      // set parent component's width
      (this.$parent.$el as HTMLElement).style.height = '100%';
  }

  /*** Watchers ***/

  /**
   * Watcher: When the height of the div has changed, determine if we need the scroll buttons or not
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('heightChangedFlag', { immediate: true })
  onHeightChanged(val: any, oldVal: any) {
    if (val) {
      Vue.nextTick(() => {
        let scrollBarShown = false;
        let element = this.$refs.verticalScroll as HTMLElement;
        
        if (element) {
          scrollBarShown = element.scrollHeight > element.clientHeight;

          if (scrollBarShown) {
            // increase width or element so scroll bar can't be seen
            let scrollBarWidth = element.offsetWidth - element.clientWidth;
            this.componentWidth = constants.TOOL_CONTENT_WIDTH + scrollBarWidth + 'px';
          }
          else
            this.componentWidth = constants.TOOL_CONTENT_WIDTH + 'px';
        }
      
        this.scrollBarShown = scrollBarShown;

      });
    }
  }

  /**
   * Begin scrolling
   */
  scrollEvent(scrollInterval = 1) {
    this.stopScrollFlag = false;
    let element = this.$refs.verticalScroll as HTMLElement;

    //we're wanting to scroll down
    if (scrollInterval > 0) {
      this.canScrollDown = element.scrollTop < element.scrollHeight - element.clientHeight;
    }
    //we're wanting to scroll up
    else if (scrollInterval < 0) {
      this.canScrollUp = element.scrollTop > 0;
    }

    this.scrollUntilStopped(element, scrollInterval);
  }

  /**
   * Recursive function that scrolls until mouse is moved off button
   */
  scrollUntilStopped(element, scrollInterval) {
    let v = this;

    window.setTimeout(() => {
      let originalScrollTop = element.scrollTop;
      element.scrollTop += scrollInterval;

      // if not stopped and more scrolling is possible
      if (!v.stopScrollFlag && originalScrollTop != element.scrollTop) {
        v.scrollUntilStopped(element, scrollInterval);
      }
      else {
        v.canScrollDown = false;
        v.canScrollUp = false;
      }
    }, 5);
  }
}
</script>