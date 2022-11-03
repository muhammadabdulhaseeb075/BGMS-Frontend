<template>
  <div v-if="showEdit || editFlag" :class="['form-buttons', { 'bottom-buttons': !showEdit }]">

    <a v-if="showBack" href="javascript:void(0)" class="form-icon" v-show="!editFlag" @click="$emit('toggle-back',true)" @keyup.enter="$emit('toggle-back',true)" title="Back">
      <i class="fa fa-arrow-left"></i>
    </a>

    <a v-if="siteAdminOrSiteWarden" href="javascript:void(0)" class="form-icon" v-show="!editFlag" @click="$emit('toggle-edit',true)" @keyup.enter="$emit('toggle-edit',true)" title="Edit">
      <i class="far fa-edit"></i>
    </a>

    <button class="form-icon" type="submit" value="Submit" v-if="!saving && fieldChanged" v-show="editFlag" title="Save" @mousedown.prevent>
      <i class="far fa-save"></i>
    </button>
    <button  class="form-icon-disabled" v-else v-show="editFlag">
      <i :class="[saving ? 'fa fa-spinner fa-spin' : 'far fa-save']"></i>
    </button>
    
    <a href="javascript:void(0)" class="form-icon" v-show="editFlag && !saving" @click="$emit('toggle-edit',null)" @keyup.enter="$emit('toggle-edit',null)" title="Cancel">
      <i class="fa fa-times"></i>
    </a>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component from 'vue-class-component'
import { Watch, Prop } from 'vue-property-decorator';

/**
 * Class representing FormButtons component
 */
@Component
export default class FormButtons extends Vue {

  @Prop() editFlag;
  @Prop() saving;
  @Prop() fieldChanged;
  @Prop() showEdit;
  @Prop() showBack;

  siteAdminOrSiteWarden: boolean = this.$store.state.siteAdminOrSiteWarden;
}

</script>