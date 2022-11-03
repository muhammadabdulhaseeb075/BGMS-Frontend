<template>
  <div v-if="componentData" style="width: 100%;">
    <div v-if="componentData.next_of_kin_to && componentData.next_of_kin_to.length > 0">
      <label class="col-xs-12 control-label">Next Of Kin To:</label>
      <table class="table table-condensed">
        <thead>
          <tr>
            <th>Name</th>
            <th/>
          </tr>
        </thead>
        <tbody>
          <template v-for="person in componentData.next_of_kin_to">
            <tr :key="person.id">
              <td class="table-row-bottom">{{ person.display_name }}</td>
              <td><a href="" @click="goToPerson(person)" title="Go to Person"><i class="fa fa-arrow-circle-right"></i></a></td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
  <div v-else class="loading-placeholder">
    <div class="loading-placeholder-contents">
      <i class="fa fa-spinner fa-spin"/>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import Component, { mixins } from 'vue-class-component';
import { Watch, Prop } from 'vue-property-decorator';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';
import constants from '@/global-static/constants.ts';

Vue.use(Vuex);

/**
 * Class representing PersonNextOfKinTo component
 * @extends Vue
 */
@Component
export default class PersonNextOfKinTo extends mixins(ManagementToolsMixin) {

  @Prop() id;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    this.componentName = "person_next_of_kin_to";
    this._id = this.id;

    // load data
    this.loadData('/mapmanagement/personNextOfKinTo/?id=', this._id);
  }

  /*** Computed ***/

  /*** Watchers ***/

  /*** Methods ***/

  goToPerson(person) {
    if (this.componentData.current_site_name && this.componentData.current_site_name===person.site) {
      if (person.reserved_graveplot_uuid) {
        // this is a reserved person
        this.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.reservations, params: { id: person.reserved_graveplot_uuid, personID: person.id, layer: 'unknown' }});
      }
      else if (person.first_memorial && person.most_recent_burial)
        // this person is linked to a memorial
        this.$router.replace({ name: constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.persons, params: { id: person.first_memorial['memorial_uuid'], person_id: person.id, layer: person.first_memorial['layer'], burial_id: person.most_recent_burial.id }});
      else if (person.most_recent_burial && person.most_recent_burial.graveplot_uuid)
        // this person is link to a grave
        this.$router.replace({ name: constants.GRAVE_MANAGEMENT_CHILD_ROUTES.burials, params: { id: person.most_recent_burial.graveplot_uuid, person_id: person.id, layer: 'plot', burial_id: person.most_recent_burial.id }});
      else
        // this person isn't linked to anything
        this.$router.replace({ name: constants.BURIAL_PERSON_MANAGEMENT_CHILD_ROUTES.person, params: { id: person.id, person_id: person.id, burial_id: person.most_recent_burial.id, layer: 'unknown' }});
    }
    else
      this.notificationHelper.createInfoNotification("Go To Person", "This person exists in a different site: " + person.site);
  }
}
</script>
