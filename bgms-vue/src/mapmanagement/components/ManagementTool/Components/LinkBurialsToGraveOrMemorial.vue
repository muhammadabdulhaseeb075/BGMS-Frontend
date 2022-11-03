<template>
  <form class="form-horizontal form-box-inside" @submit.prevent="linkSelected">
    <div style="width: 100%; padding-left: 0px;" class="management-tool-form">
      <label class="col-xs-12 control-label">{{ message }}</label>
    </div>
    <table class="table table-condensed">
      <thead>
        <tr>
          <th><input type="checkbox" @change="selectAll" checked="true"/></th>
          <th>Name</th>
        </tr>
      </thead>
      <tbody id="linked-memorials-list">
        <tr v-for="personOrBurial in distinctPersonsOrBurials" :key="personOrBurial.burial_id">
          <td><input type="checkbox" :value="personOrBurial.selected" v-model="personOrBurial.selected"/></td>
          <td>{{ personOrBurial.display_name }}</td>
        </tr>
      </tbody>
    </table>
    <div class="form_buttons">
      <button type="submit" class="bgms-button btn">Yes</button>
      <button class="bgms-button btn" type="button" @click="close()">No</button>
    </div>
  </form>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import axios from 'axios';
import NotificationMixin from '@/mixins/notificationMixin.ts';
import FeatureTools from '@/mapmanagement/mixins/featureTools';

/**
 * Class representing LinkBurialsToGraveOrMemorial component
 */
@Component
export default class LinkBurialsToGraveOrMemorial extends mixins(NotificationMixin, FeatureTools) {

  @Prop() linkToGrave: boolean;
  @Prop() linkToMemorial: boolean;
  @Prop() message;
  @Prop() distinctPersonsOrBurials;
  @Prop() memorialUUID;
  @Prop() graveplotUUID;
  @Prop() graveNumber;
  @Prop() addToMemorialsLinkedToGrave;

  /*** Methods ***/

  /**
   * Toggle checkbox for all rows
   */
  selectAll(event) {
    this.distinctPersonsOrBurials.forEach((person) => {
      person.selected = event.target.checked;
    });
  }
  
  close() {
    this.$emit('closeComponent');
  }

   /**
   * This will also link burials to grave or memorial as required
   */
  linkSelected(e) {
    e.preventDefault();

    let toLink = [];

    this.distinctPersonsOrBurials.forEach((personOrBurial) => {
      if (personOrBurial.selected) {
        let newItem = { 'burial_id': personOrBurial.burial_id,
                        'person_id': personOrBurial.person_id };

        if (this.linkToMemorial)
          newItem['add_to_memorial'] = true;

        if (this.linkToGrave)
          newItem['add_to_grave'] = true;
        
        if (this.addToMemorialsLinkedToGrave)
          newItem['add_to_memorials_linked_to_grave'] = true;

        toLink.push(newItem);
      }
    });

    if (toLink.length > 0) {

      let postData = {
        "memorial_uuid": this.memorialUUID,
        "graveplot_uuid": this.graveplotUUID,
        "grave_number": this.graveNumber,
        "burial_list": toLink
      }

      axios.post('/mapmanagement/modifyBurialsLinkedFeatures/', postData)
      .then((response) => {
        this.createSuccessNotification(`Persons successfully linked to ${this.linkToMemorial ? 'memorial' : 'grave'}`);
        this.updateGraveplotLayer(response.data);
        this.$emit('linksMadeSuccessfully', response.data.memorials);
      })
      .catch(response => {
        this.createHTTPErrorNotificationandLog(response, `Persons unsuccessfully linked to ${this.linkToMemorial ? 'memorial' : 'grave'}.`);
      })
      .finally(() => {
        this.$emit('closeComponent');
      });
    }
    else
      this.$emit('closeComponent');
  }

   /**
   * Check if graveplot needs layer updated, and change it if it does
   */
  updateGraveplotLayer(data) {
    if (data.original_graveplot_layer && data.new_graveplot_layer && data.original_graveplot_layer !== data.new_graveplot_layer) {
      // need to change graveplot layer

      // if changed to available layer, need to update layer id with topopolygon id
      const newID = data.new_graveplot_layer === 'available_plot' ? data.graveplot_topopolygon_id : data.graveplot_id;
      this.changeFeatureLayer(data.original_graveplot_layer, data.new_graveplot_layer, this.graveplotUUID, newID);
    }
  }
}
</script>
