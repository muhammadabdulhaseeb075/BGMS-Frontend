<template>
  <div class="data-matching-history">
    <div class="loading-overlay" v-if="loading">
      <i class="fa fa-spinner fa-spin"></i>
      <p>Loading</p>
    </div>
    <div class="row">
      <div class="col-xs-3">
        <h2>Memorial Status</h2>
      </div>
      <div class="col-xs-9">
        <h4>Number of memorials unmatched: {{unmatchedMemorialCount}}</h4>
      </div>
    </div>
    <vue-good-table v-if="rows"
      :columns="columns"
      :rows="rows"
      styleClass="vgt-table striped"
      @on-row-click="onRowClick"
      :sort-options="{
        enabled: true,
        initialSortBy: {field: 'feature_id', type: 'asc'}
      }"/>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component from 'vue-class-component'
import { Watch } from 'vue-property-decorator'
import axios from 'axios'
import 'vue-good-table/dist/vue-good-table.css';
import { VueGoodTable } from 'vue-good-table';

/**
 * Class representing MemorialStatus component
 * @extends Vue
 */
@Component({ components: { VueGoodTable } })
export default class MemorialStatus extends Vue{

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
      label: 'Status',
      field: 'state',
      filterOptions: {
        enabled: true,
        placeholder: 'All states',
        filterDropdownItems: ['Processed', 'Processing', 'Unprocessed'],
      }
    }
  ];

  rows = null;

  unmatchedMemorialCount = null;
  loading = true;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    
    let v = this;

    v.loading = true;

    axios.get('/datamatching/getMemorialState/')
      .then(function(response) {
        v.rows = response.data;
        v.loading = false;
      })
      .catch(function(response) {
        console.warn('Couldn\'t get memorial state:', response);
      });
    
    this.getUnmatchedMemorialCount();
  }

  /*** Watchers ***/

  /*** Computed ***/

  /*** Methods ***/

  getUnmatchedMemorialCount() {

    let v = this;

    axios.get('/datamatching/unmatchedMemorialsCount/')
      .then(function(response) {
        v.unmatchedMemorialCount = response.data.memorials_left;
      })
      .catch(function(response) {
        console.warn('Couldn\'t get unmatched memorials count:', response);
      });
  }

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