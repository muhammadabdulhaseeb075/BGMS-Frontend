<template>
  <modal-panel :show="show" >
    <div class="site-select-modal">
      <div class="modal-header flex justify-between px-3 py-2">
        <div class="title">{{title}}</div>
        <div class="close-button cursor-pointer" @click="onClose">
          <i class="fa fa-times p-1"></i>
        </div>
      </div>
      <div class="modal-body p-7">
          <p>{{ message }}</p>
      </div>
      <div class="flex justify-end pt-2">
          <button class="fill-button px-4  p-3 rounded-lg" @click="onYesContinue">YES Continue booking</button>
          <button class="fill-button px-4  p-3 rounded-lg" @click="onYesCancel">YES Cancel booking</button>
          <button class="fill-button modal-close px-4 p-3 rounded-lg" @click="onNoStay">NO Stay on booking </button>
        </div>
    </div>
  </modal-panel>
</template>

<style scoped src="./site-select-modal.css"></style>
<script src="./site-select-modal.js"></script> 
