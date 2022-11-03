<template>
  <div id="popup" class="ol-popup">

  <div v-for="person in scope.personsPage" :key="person.id">
    <a style="cursor: pointer;"><strong>{{person.first_names}} {{person.last_name}}</strong><span v-show='person.has_age()'>, {{person.get_rounded_age_shortened().age}} {{person.get_rounded_age_shortened().units}}</span><span v-show='person.has_burial_date()'>, {{get_display_date(person)}}</span></a>
  </div>

  <div v-show='scope.persons.length <= (scope.currentPage * scope.itemsPerPage)'>
    <div v-show='scope.noOfUnmarkedGraves>1'>
      <div>{{scope.noOfUnmarkedGraves}} unknown graves</div>
    </div>
    
    <div v-show='scope.noOfUnmarkedGraves==1 && scope.persons.length===0 && scope.personsReservedPage.length===0'>
      <div><a style="cursor: pointer;">Unknown grave</a></div>
    </div>
  </div>

  <!-- people who reserved plot -->
  <div v-for="person in scope.personsReservedPage" :key="person.person_id">
    <a style="cursor: pointer;color: #ca4f4f;"><strong>{{person.person__first_names}} {{person.person__last_name}} (reserved)</strong>
    </a>
  </div>
  <!-- FIN: people who reserved plot -->

  <!--<pagination v-show="scope.totalItems>scope.itemsPerPage" total-items="scope.totalItems" v-model="scope.currentPage" max-size="scope.maxSize" items-per-page="scope.itemsPerPage" class="pagination-sm" boundary-links="false" @change="pageChanged()" direction-links="false" rotate="false"></pagination>-->

</div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import { getDisplayDate } from '@/global-static/dataFormattingAndValidation.ts';

@Component
export default class ClusterDetailsMarker extends Vue {

  getDisplayDate = getDisplayDate;

  @Prop() scope;

  pageChanged() {
    /*console.log('pageChanged');
    var begin = (this.currentPage - 1) * this.itemsPerPage;
    var end = begin + this.itemsPerPage;
    this.personsPage = this.persons.slice(begin, end);
    console.log('begin:'+begin);
    console.log('end:'+end);
    if (begin !== 0)
      this.personsReservedPage = this.personsReserved.slice(begin, end);*/
  }

  get_display_date(person) {
    let person_date = person.burial_date+"";
    if(person_date.length>4){
      return getDisplayDate(person.burial_date, false);
    }
    return person.burial_date;
  }
}
</script>