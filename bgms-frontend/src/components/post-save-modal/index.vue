<template>
  <modal-panel :show="show" >
    <div class="post-save-modal">
      <div class="modal-header flex justify-between px-3 py-2">
        <div class="title">{{ title }}</div>
        <div class="close-button cursor-pointer" @click="onClose">
          <i class="fa fa-times p-1"></i>
        </div>
      </div>
      <div class="modal-body p-7">
          <p>{{ message }}</p>
          <!--<p>{{ //query }}</p>-->
      </div>
      <div class="flex justify-end pt-2">
        <button class="fill-button px-4  p-3 rounded-lg" @click="goToCalendar">Go To Calendar</button>
        <button class="fill-button px-4  p-3 rounded-lg" @click="goToStatus">Go To Status</button>
        <button class="fill-button modal-close px-4 p-3 rounded-lg" @click="onClose">Stay On Booking</button>
      </div>
    </div>
  </modal-panel>
</template>

<style scoped src="./post-save-modal.css"></style>
<script src="./post-save-modal.js"></script>
