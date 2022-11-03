<template>
  <div>
    <!-- textarea input -->
    <div v-if="inputType==='textarea'">
      <div class="row field-row" v-if="!editFlag && (value || showFalsyValue)">
        <label :class="labelColumnClasses" :for="id">{{label}}:</label>
        <div :id="id" :class="fieldColumnClasses">
            <div class="form-control field-text">{{ value }}</div>
        </div>
      </div>
      <div v-else-if="editFlag">
        <h2>{{label}}</h2>
        <div :id="id" class="col-xs-12 no-padding">
          <textarea rows="3" class="form-control" :placeholder="placeholder ? placeholder : label"  v-bind="attributes" :value="value" @input="$emit('input', $event.target.value)"/>
        </div>
      </div>
    </div>

    <div class="row field-row" v-else-if="!readonlyOption || (editFlag || (value || showFalsyValue) || readonly)">

      <label :class="labelColumnClasses" :for="id">{{label}}:</label>

      <!-- Checkbox input -->
      <div v-if="inputType==='checkbox'" :class="fieldColumnClasses">
        <div v-if="!editFlag || readonly" :id="id">
          <input readonly type="text" class="form-control" :value="value ? 'Yes' : 'No'">
        </div>
        <div v-else :id="id">
          <input :readonly="readonlyOption && !editFlag" :type="inputType" class="form-control" v-bind="attributes" :checked="value" @input="$emit('input', $event.target.checked)">
        </div>
      </div>

      <!-- Select input -->
      <div v-if="inputType==='select'" :id="id" :class="[fieldColumnClasses, { 'unit-field': (editFlag && unit)}]">
        <select  v-if="!(readonlyOption && !editFlag) && !notAnOption(options_select, value)" :readonly="readonlyOption && !editFlag" list="select_options"
               :type="'text'" class="form-control" :placeholder="placeholder ? placeholder : label" v-bind="attributes"
               :value="(!editFlag && unit) ? value + unit : value" @input="$emit('input', $event.target.value)"
        >
          <option v-for="option in options_select" :key="option" v-bind:value="option">
             {{ option }}
          </option>
        </select>
        <input v-if="(readonlyOption && !editFlag) || notAnOption(options_select, value)" :readonly="readonlyOption && !editFlag"
               :type="'text'" class="form-control" :placeholder="placeholder ? placeholder : label" v-bind="attributes"
               :value="(!editFlag && unit) ? value + unit : value" @input="$emit('input', $event.target.value)"
        >
        <span v-if="editFlag && unit">{{unit.trim()}}</span>
      </div>

      <!-- Other input types -->
      <div v-else-if="inputType!=='checkbox' && inputType!=='select'" :id="id" :class="[fieldColumnClasses, { 'unit-field': (editFlag && unit)}]">
        <input :readonly="readonlyOption && !editFlag" :type="(!editFlag && unit) ? 'text' : inputType"
               class="form-control" :placeholder="placeholder ? placeholder : label" v-bind="attributes"
               :value="(!editFlag && unit) ? value + unit : value" @input="$emit('input', $event.target.value)"

        >
        <span v-if="editFlag && unit">{{unit.trim()}}</span>
      </div>

    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator';
import constants from '@/mapmanagement/static/constants.ts';

/**
 * Class representing StandardInputRow component
 */
@Component
export default class StandardInputRow extends Vue {

  @Prop() label;
  /**
   * If this is blank then the label will be used by default
   */
  @Prop() placeholder;
  @Prop() value;
  @Prop() inputType;
  @Prop() editFlag;
  @Prop() readonly;
  @Prop() showFalsyValue;
  @Prop() unit;
  @Prop() options_select;

  /**
   * True if field should be readonly when editFlag is false and value is empty
   */
  @Prop() readonlyOption;

  /**
   * Object containing any additional attributes
   */
  @Prop() attributes;

  labelColumnClasses = constants.LABEL_COLUMN_CLASSES;
  fieldColumnClasses = constants.FIELD_COLUMN_CLASSES;

  /**
   * Returns the label in kebab case
   */
  get id() {
    return this.label.replace(/\s+/g, '-').toLowerCase();
  }

  notAnOption(options, value){
    if (!value)
      return false
    for(let option of options){
      if (option == value){
        return false
      }
    }
    return true
  }
}

</script>