<template>
   <div class="reports-home">
      <report-list />
   </div> 
</template>

<script lang='ts'>

import Vue from 'vue';
import Component from 'vue-class-component';
import ReportList from '@/analytics/components/ReportList/index.vue';

@Component({ components: {
   ReportList
}})
export default class Index extends Vue {

}

</script>
