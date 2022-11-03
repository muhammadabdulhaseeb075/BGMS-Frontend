<template>
  <modal-panel :show="show" >
    <div class="confirm-modal">
      <div class="modal-header flex justify-between px-3 py-2">
        <div class="title">{{title}}</div>
        <div class="close-button cursor-pointer" @click="onClose">
          <i class="fa fa-times p-1"></i>
        </div>
      </div>
      <div class="modal-body p-7">
          <p>{{message}}</p>
      </div>
      <div class="flex justify-end pt-2">
          <button class="px-4  p-3 rounded-lg" @click="onRemoveEvent">YES</button>
          <button class="modal-close px-4 p-3 rounded-lg" @click="onClose">NO</button>
        </div>
    </div>
  </modal-panel>
</template>

<style scoped src="./confirm-modal.css"></style>
<script src="./confirm-modal.js"></script> 
