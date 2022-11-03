<template>
  <p class="validation-box" v-if="errors && errors.length">
    <b>Please correct the following error{{ errors.length>1 ? 's' : '' }}:</b>
    <ul>
      <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
    </ul>
  </p>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator';

/**
 * Class representing ValidationBox component
 */
@Component
export default class ValidationBox extends Vue {

  @Prop() errors;
}

</script>