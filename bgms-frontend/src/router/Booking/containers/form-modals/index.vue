<template>
  <modal-panel :show="show">
    <div class="form-modals">
      <div class="modal-header flex justify-between px-3 py-2">
        <div class="title">{{ title }}</div>
        <div class="close-button cursor-pointer" @click="onClose">
            <i class="fa fa-times p-1"></i>
        </div>
      </div>
      <div class="modal-body p-7">
        <component
            :is="modalName"
            :data_id="data_id"
            v-bind="{form: formData}"
            @add="onSendData"
            @close="onClose"
            @push-data="onSendData">
        </component>
      </div>
    </div>
  </modal-panel>
</template>

<style scoped src="./form-modals.css"></style>

<script src="./form-modals.js"></script>
