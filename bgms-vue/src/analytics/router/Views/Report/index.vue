<template>
   <div>
      <data-table>
      </data-table>
   </div>
</template>

<script lang='ts'>

import Vue from 'vue';
import Component from 'vue-class-component';
import DataTable from '@/analytics/components/DataTable/index.vue';


@Component({ components: {
   DataTable
}})
export default class Report extends Vue {
   
}

</script>
