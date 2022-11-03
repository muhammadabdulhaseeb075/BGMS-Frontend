<template>
  <div class="data-matching-history">
    <div class="loading-overlay" v-if="loading">
      <i class="fa fa-spinner fa-spin"></i>
      <p>Loading</p>
    </div>
    <h2 class="col-md-4">User Activity Log</h2>
    <vue-good-table v-if="rows"
      :columns="columns"
      :rows="rows"
      styleClass="vgt-table striped"
      @on-row-click="onRowClick"
      :sort-options="{
        enabled: true
      }"/>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component from 'vue-class-component'
import { Watch } from 'vue-property-decorator'
import axios from 'axios'
import { VueGoodTable } from 'vue-good-table';
import 'vue-good-table/dist/vue-good-table.css';

/**
 * Class representing UserActivity component
 * @extends Vue
 */
@Component({ components: { VueGoodTable } })
export default class UserActivity extends Vue{

  columns = [
    {
      label: 'Memorial Feature ID',
      field: 'feature_id',
      filterOptions: {
        enabled: true,
      },
      formatFn: this.removeLeadingZeros,
    },
    {
      label: 'Name',
      field: 'name',
      filterOptions: {
        enabled: true,
      }
    },
    {
      label: 'Date',
      field: 'date'
    },
    {
      label: 'Status',
      field: 'state',
      filterOptions: {
        enabled: true,
        placeholder: 'All states',
        filterDropdownItems: ['In use', 'Skipped', 'Viewed'],
      }
    }
  ];

  rows = null;
  
  loading = true;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    
    let v = this;
    
    v.loading = true;

    axios.get('/datamatching/getUserActivity/')
      .then(function(response) {
        v.rows = response.data;
        v.loading = false;
      })
      .catch(function(response) {
        console.warn('Couldn\'t get user activity:', response);
      });
  }

  /*** Watchers ***/

  /*** Computed ***/

  /*** Methods ***/

  /**
   * Change the 'in use' memorial to selected and go to index page
   */
  onRowClick(params) {
    let v = this;

    axios.post('/datamatching/changeToMemorialById/', { data_matching_memorial_id: params.row.data_matching_memorial_id })
      .then(function(response) {
        v.$router.push({ name: 'Index' });
      })
      .catch(function(response) {
        if (response.response.data.message) {
          console.warn(response.response.data.message);
          (window as any).memorialModule.failNotification(response.response.data.message);
        }
        else
          console.warn('Couldn\'t get memorial data:', response);
      });
  }

  /**
   * Removes leading zeros from column displayed data
   */
  removeLeadingZeros(value) {
    return value.replace(/^0+/, '');
  }
}
</script>