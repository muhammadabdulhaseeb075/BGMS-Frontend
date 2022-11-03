<template>
  <modal :name="modalName" 
        height="auto" 
        width="350px" 
        :clickToClose="false"
        @opened="$refs.newTextbox.focus()">
    <form class="form-horizontal form-box-inside management-tool-form container" @submit.prevent="addNewData()">
      
      <div class="row">
        <h1>Add new {{ fieldName }}</h1>
      </div>

      <div class="row">
        <label :class="labelColumnClasses" :for="fieldName">{{ includeDescription ? 'Name' : nameAsTitle }}:</label>
        <div :id="fieldName" class="col-xs-7">
          <input :disabled="savingModal" ref="newTextbox" v-model="newData" type="text" class="form-control" :placeholder="nameAsTitle" :maxlength="maxlength" required>
        </div>

        <label v-if="includeDescription" :class="labelColumnClasses" for="description">Description:</label>
        <div v-if="includeDescription" id="description" class="col-xs-7">
          <input :disabled="savingModal" v-model="newDataDescription" type="text" class="form-control" placeholder="Description" :maxlength="maxlength" required>
        </div>
      </div>

      <div class="row">
        <div v-show="savingModal">
          <i class="fa fa-spinner fa-spin"></i>
        </div>
        <div v-show="!savingModal">
          <button type="submit" class="btn bgms-button">Add</button>
          <button class="btn bgms-button" @click="$modal.hide(modalName)">Close</button>
        </div>
      </div>
    </form>
  </modal>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import axios from 'axios';
import VModal from 'vue-js-modal';
import constants from '@/mapmanagement/static/constants.ts';

Vue.use(VModal)

/**
 * Class representing AddModal component
 */
@Component
export default class AddModal extends Vue {

  @Prop() url;
  @Prop() fieldName;
  @Prop() storeCommit;
  @Prop() maxlength;
  @Prop() includeDescription;

  notificationHelper = this.$store.getters.notificationHelper;

  savingModal: boolean = false;
  
  newData: string = '';
  newDataDescription: string = '';

  labelColumnClasses = constants.LABEL_COLUMN_CLASSES;

  get modalName() {
    return 'add-' + this.fieldName
  }

  get nameAsTitle() {
    return this.fieldName[0].toUpperCase() + this.fieldName.slice(1);
  }

  /**
   * Adds new data to database
   */
  addNewData() {
    this.savingModal = true;

    let data = {};

    // field names are different if includes description
    if (this.includeDescription) {
      data['new_' + this.fieldName + '_name'] = this.newData;
      data['new_' + this.fieldName + '_description'] = this.newDataDescription;
    }
    
    data['new_' + this.fieldName] = this.newData;

    axios.put(this.url, data)
      .then(response => {
        this.$store.commit(this.storeCommit, response.data);
        this.$emit('new-data-added', response.data.id);
        this.$modal.hide('add-' + this.fieldName)
        this.newData = '';
        this.newDataDescription = '';

        this.notificationHelper.createSuccessNotification('New ' + this.fieldName + ' created successfully');
      })
      .catch(response => {
        const msg = 'New ' + this.fieldName + ' could not be created'
        console.warn(msg + ':', response.response.data);
        this.notificationHelper.createErrorNotification(msg);
      })
      .finally(() => {
        this.savingModal = false;
      });
  }
}
</script>