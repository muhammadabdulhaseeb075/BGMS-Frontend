<template>
  <div>
    <form class="form-horizontal form-box-inside management-tool-form" @submit.prevent.stop="onSubmit">
      <div class="row field-row">
        <label :class="labelColumnClasses" for="first-names">First Names:</label>
        <div id="first-names" :class="fieldColumnClasses">
          <input type="text" class="form-control" placeholder="First Names" v-model="personFirstNames">
        </div>
      </div>
      <div class="row field-row">
        <label :class="labelColumnClasses" for="last-name">Last Name:</label>
        <div id="last-name" :class="fieldColumnClasses">
          <input type="text" class="form-control" placeholder="Last Name" v-model="personLastName">
        </div>
      </div>
      <div class="row field-row" v-if="!personOnly">
        <label :class="labelColumnClasses" for="company-name">Company Name:</label>
        <div id="company-name" :class="fieldColumnClasses">
          <input type="text" class="form-control" placeholder="Company Name" v-model="companyName">
        </div>
      </div>
      <button class="bgms-button btn" type="submit" value="Submit" @mousedown.prevent :readonly="!fieldChanged" title="Save">
        <i v-if="searchingFlag" class="fa fa-spinner fa-spin"/><span v-if="!searchingFlag">Search</span>
      </button>
    </form>
    <div id="personSearchResults" ref="personSearchResults" v-if="results">
      <label class="col-xs-12 control-label">Results:</label>
      <table class="table table-condensed">
        <thead>
          <tr>
            <th>Name</th>
            <th>Address</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in sortedResults" :key="result.id">
            <td>{{ result.name }}</td>
            <td>{{ formatAddress(result.addresses__first_line, result.addresses__town, result.addresses__postcode) }}</td>
            <td><a href="" @click="$emit('result-selected', { id: result.id, name: result.name, type: result.type });" :title="'Select this ' + result.type"><i class="fa fa-arrow-circle-right"></i></a></td>
          </tr>
          <tr v-if="!results.length">
            <td colspan="3">No results</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component from 'vue-class-component';
import { Watch, Prop } from 'vue-property-decorator'
import axios from 'axios';
import constants from '@/mapmanagement/static/constants.ts';
import { formatAddress } from '@/global-static/dataFormattingAndValidation.ts';

/**
 * Class representing PersonCompanySearch component
 */
@Component
export default class PersonCompanySearch extends Vue {

  formatAddress = formatAddress;

  @Prop() personOnly;

  labelColumnClasses = constants.LABEL_COLUMN_CLASSES;
  fieldColumnClasses = constants.FIELD_COLUMN_CLASSES;
  
  personFirstNames = null;
  personLastName = null;
  companyName = null;

  results = null;

  searchingFlag: boolean = false;

  get fieldChanged() {
    return this.personFirstNames || this.personLastName || this.companyName;
  }

  get sortedResults() {
    if (this.results) {

      let sortedResults = this.results;

      if (sortedResults && sortedResults.length > 1)
        return sortedResults.sort((a, b) => {
          // get values to sort by
          let aSort = a.name;
          let bSort = b.name;

          // use last name if person
          if (a.last_name)
            aSort = a.last_name
          if (b.last_name)
            bSort = b.last_name + ' ' + b.first_names
          
          if (aSort > bSort)
            return 1;
          else if (aSort < bSort)
            return -1;
          else
            return 0;
        });
      else
      return sortedResults;
    }
    else
      return [];
  }

  @Watch('personFirstNames')
  onPersonFirstNamesChanged(val: any, oldVal: any) {
    this.$emit('person-first-names-changed', val);
  }

  @Watch('personLastName')
  onPersonLastNameChanged(val: any, oldVal: any) {
    this.$emit('person-last-name-changed', val);
  }

  @Watch('companyName')
  onCompanyNameChanged(val: any, oldVal: any) {
    this.$emit('company-name-changed', val);
  }

  onSubmit(e) {
    let v = this;
    
    v.searchingFlag = true;

    v.results = null;

    let params = {};

    if (v.personFirstNames)
      params['first_names'] = v.personFirstNames;
    if (v.personLastName)
      params['last_name'] = v.personLastName;
    if (v.companyName)
      params['name'] = v.companyName;
    
    axios.get('/mapmanagement/searchPublicPersonCompany/', { params: params })
      .then((response) => {
        console.log(response);
        v.results = response.data;
        Vue.nextTick(() => { 
          (v.$refs.personSearchResults as HTMLElement).focus(); 
        });
      })
      .catch((error) => {
        console.warn(error);
      })
      .finally(() => {
        v.searchingFlag = false;
      });
  }
}
</script>