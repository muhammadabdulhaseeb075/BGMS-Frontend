<template>
  <div class="row field-row" v-if="!readonlyOption || (editFlag || value || readonly)">

    <label :class="labelColumnClasses" :for="id">{{label}}:</label>

    <!-- Other input types -->
    <div :id="id" :class="fieldColumnClasses" :readonly="readonlyOption && !editFlag">
      <vue-tel-input 
        :placeholder="placeholder ? placeholder : 'Phone Number'"
        :disabled="readonlyOption && !editFlag" 
        :inputClasses="'form-control'" 
        :value="value ? value : ''"
        @input="(num, obj) => { $emit('input', obj.number.e164); $emit('phone-validation', obj.isValid); }"
        :preferredCountries="['gb']"
        defaultCountry="gb"
        :disabledFetchingCountry="true">
      </vue-tel-input>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator';
import { VueTelInput } from 'vue-tel-input';
import constants from '@/mapmanagement/static/constants.ts';

/**
 * Class representing PhoneInputRow component
 */
@Component({
  components: {
    VueTelInput
  }
})
export default class PhoneInputRow extends Vue {

  @Prop() label;
  /**
   * If this is blank then the label will be used by default
   */
  @Prop() placeholder;
  @Prop() value;
  @Prop() inputType;
  @Prop() editFlag;
  @Prop() readonly;

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
  
  number = {};

  mounted() {
    this.number = this.value;
  }

  /**
   * Returns the label in kebab case
   */
  get id() {
    return this.label.replace(/\s+/g, '-').toLowerCase();
  }
}

</script>