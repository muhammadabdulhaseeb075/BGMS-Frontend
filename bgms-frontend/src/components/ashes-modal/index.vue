<template>
  <modal-panel :show="show" >
    <div class="ashes-modal">
      <div class="modal-header flex justify-between px-3 py-2">
        <div class="title">{{ title }}</div>
        <div class="close-button cursor-pointer" @click="onClose">
          <i class="fa fa-times p-1"></i>
        </div>
      </div>
      <div class="modal-body p-7">
        <p>
          <!--Create Event on Date: <br/>-->
          <strong>{{ message }}</strong>
        </p>
          <!--<p>{{query}}</p>-->
          <p>
            <br>
            <input type="radio" id="ashes" value="ashes" v-model="ashes" @change="valueChanged($event)">
            <label for="ashes">Ashes</label>
            <br>
            <input type="radio" id="burial" value="burial" v-model="ashes" @change="valueChanged($event)">
            <label for="burial">Burial</label>
          </p>
      </div>
      <div class="flex justify-end pt-5">
          <button class="fill-button" v-show="showConfirmButton" @click="onContinue">Confirm</button>
          <button class="empty-button" v-show="!showConfirmButton">&nbsp;&nbsp;</button>
          <button class="fill-button" @click="onClose">Cancel</button>
        </div>
    </div>
  </modal-panel>
</template>

<style scoped src="./ashes-modal.css"></style>
<script src="./ashes-modal.js"></script> 
