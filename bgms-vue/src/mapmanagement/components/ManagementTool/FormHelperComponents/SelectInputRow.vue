<template>
  <div class="row field-row" v-if="editFlag || value">
    <label :class="labelColumnClasses" :for="id">{{label}}:</label>
    <div :id="id" :class="fieldColumnClasses">
      <select :disabled="!editFlag" class="form-control" :value="value" @input="$emit('input', $event.target.value)">
        <option v-if="allowNull" :value="null" :key="'null'">-</option>
        <option v-for="option in options" :value="optionValueName ? option[optionValueName] : option" :key="optionKeyName ? option[optionKeyName] : option">
          {{ optionLabelName ? option[optionLabelName] : option }}
        </option>
      </select>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import { Prop } from 'vue-property-decorator';
import constants from '@/mapmanagement/static/constants.ts';

/**
 * Class representing SelectInputRow component
 */
@Component
export default class SelectInputRow extends Vue {

  @Prop() label;
  @Prop() options;
  @Prop() value;
  @Prop() editFlag;
  @Prop() allowNull;
  
  // map object property names
  @Prop() optionValueName;
  @Prop() optionKeyName;
  @Prop() optionLabelName;

  labelColumnClasses = constants.LABEL_COLUMN_CLASSES;
  fieldColumnClasses = constants.FIELD_COLUMN_CLASSES;

  /**
   * Returns the label in kebab case
   */
  get id() {
    return this.label.replace(/\s+/g, '-').toLowerCase();
  }
}

</script>