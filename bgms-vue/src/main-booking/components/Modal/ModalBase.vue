<template>
  <div class="modal-wrapper" v-if="open">
    <div class="modal-panel">
      <div class="modal-head">
        <div class="modal-title">{{title}}</div>
        <span class="close-icon fa fa-times" @click="close"></span>
      </div>
      <div class="modal-content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';

@Component
export default class ModalBase extends Vue {
  @Prop() open: boolean;
  @Prop() title: string = '';

  close() {
    this.$emit("close");
  }
}
</script>

<style scoped>
.modal-wrapper {
  top: 0;
  position: fixed;
  background: rgba(0, 0, 0, 0.2);
  justify-content: center;
  align-items: center;
  z-index: 9999;
  height: 100vh;
  width: calc(100vw - 230px);
  display: none;
}

.modal-wrapper {
  display: flex;
}

.modal-wrapper .modal-head {
  position: relative;
  display: flex;
}

.modal-wrapper .modal-head {
  cursor: pointer;
  color: black;
  background-color: #c3af42;
  width: 100%;
  text-align: center;
  color: white;
  padding: 5px;
  font-weight: 500;
}

.modal-wrapper .modal-head .modal-title {
  width: 97%;
}

.modal-wrapper .modal-head .close-icon {
  display: block;
  padding: 5px;
  background: white;
  color: black;
}

.modal-panel {
  background-color: white;
  width: 500px;
}

</style>