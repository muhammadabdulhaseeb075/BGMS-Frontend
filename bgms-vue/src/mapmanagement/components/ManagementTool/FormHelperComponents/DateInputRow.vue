<template>
  <div class="row field-row" v-if="editFlag || day || month || year">
    <label :class="labelColumnClasses" for="date-field">{{ label }}:</label>
    <div v-if="!editFlag" id="date-field" :class="fieldColumnClasses">
      <input readonly type="text" class="form-control" :value="individualDateFieldsToSingleDate(day, month, year)">
    </div>
    <div v-if="editFlag" id="date-field" :class="fieldColumnClasses">
      <div class="multi-input">

        <input class="form-control multi-input_input multi-input_input--day no-spinner" type="number" step="1" min="0" max="31" maxlength="2" placeholder="dd" :value="day" @input="keyPress($event); $emit('day-input', parseInt($event.target.value))" @click="$event.target.select()">

        <span class="multi-input_divider">/</span>

        <input class="form-control multi-input_input multi-input_input--month no-spinner" type="number" step="1" min="0" max="12" maxlength="2" placeholder="mm" :value="month" @input="keyPress($event); $emit('month-input', parseInt($event.target.value))" @click="$event.target.select()">

        <span class="multi-input_divider">/</span>

        <input class="form-control multi-input_input multi-input_input--year no-spinner" type="number" step="1" min="0" maxlength="4" :max="(new Date()).getFullYear()" placeholder="yyyy" :value="year" @input="keyPress($event); $emit('year-input', parseInt($event.target.value))" @click="$event.target.select()">
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator';
import constants from '@/mapmanagement/static/constants.ts';
import { individualDateFieldsToSingleDate } from '@/global-static/dataFormattingAndValidation.ts';

/**
 * Class representing DateInputRow component
 */
@Component
export default class DateInputRow extends Vue {
  
  individualDateFieldsToSingleDate = individualDateFieldsToSingleDate;

  @Prop() label;
  @Prop() day;
  @Prop() month;
  @Prop() year;
  @Prop() editFlag;

  labelColumnClasses = constants.LABEL_COLUMN_CLASSES;
  fieldColumnClasses = constants.FIELD_COLUMN_CLASSES;

  /**
   * Returns the label in kebab case
   */
  get id() {
    return this.label.replace(/\s+/g, '-').toLowerCase();
  }

  keyPress(e) {
    if (e.target.value.length > e.target.maxLength) 
      e.target.value = e.target.value.slice(0, e.target.maxLength);
  }
}

</script>