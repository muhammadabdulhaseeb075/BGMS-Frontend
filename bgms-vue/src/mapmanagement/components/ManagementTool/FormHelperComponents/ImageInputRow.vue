<template>
  <div class="row field-row" v-if="editFlag || value">
    <label :class="labelColumnClasses" :for="id">{{label}}:</label>

    <div :id="id" :class="[fieldColumnClasses, 'included-table']">
      <div v-if="processingImage" class="saving-spinner">
        <i class="fa fa-spinner fa-spin"/>
      </div>
      <div v-else-if="!processingImage" class="field-row">
        <div v-if="imageIncluded">
          <a href="javascript:void(0)" style="position: relative" v-viewer="{navbar: 0, title: 0, toolbar: { zoomIn:4,zoomOut:4,oneToOne:4,reset:4 }, url: (image) => {return image.getAttribute('data-image-url')}}">
            <div class="image-loading-spinner">
              <i class="fa fa-spinner fa-spin"/>
            </div>
            <img class="image-thumbnail" :data-image-url="value.image_url" :src="value.thumbnail_url"/>
          </a>
        </div>
        <span class="photo-buttons form-buttons" v-if="siteAdminOrSiteWarden && editFlag">
          <label v-if="imageIncluded" :for="id + '-input'" class="form-icon-small"><i class="far fa-edit" title="Replace Image"></i></label>
          <label v-else :for="id + '-input'" class="form-icon-small"><i class="fa fa-plus" title="Add Image"></i></label>
          <input :id="id + '-input'" :ref="id + '-input'" class="fileUploaderInput" type="file" accept="image/jpg,image/jpeg" @change="processImage">
          <div v-if="imageIncluded" class="form-icon-small" title="Remove Image" @click="$emit('input', null)">
            <i class="fa fa-times"></i>
          </div>
        </span>
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import { Prop } from 'vue-property-decorator';
import constants from '@/mapmanagement/static/constants.ts';
import { messages } from '@/global-static/messages.js';
import Compressor from 'compressorjs';
import 'viewerjs/dist/viewer.css'
import Viewer from 'v-viewer'

Vue.use(Viewer)

/**
 * Class representing DateInputRow component
 */
@Component
export default class DateInputRow extends Vue {

  @Prop() label;
  @Prop() value;
  @Prop() editFlag;

  labelColumnClasses = constants.LABEL_COLUMN_CLASSES;
  fieldColumnClasses = constants.FIELD_COLUMN_CLASSES;

  processingImage: boolean = false;

  siteAdminOrSiteWarden: boolean = this.$store.state.siteAdminOrSiteWarden;

  /**
   * Returns the label in kebab case
   */
  get id() {
    return this.label.replace(/\s+/g, '-').toLowerCase();
  }

  /**
   * @returns {boolean} True if this field contains an image
   */
  get imageIncluded(): boolean {
    return this.value != null && this.value.thumbnail_url && this.value.thumbnail_url != '';
  }

  /**
   * Uploads image selected by user and compresses
   */
  processImage(e) {
    let v = this;

    if (e) {
      v.processingImage = true;

      let files = e.target.files || e.dataTransfer.files;

      if (!files.length)
        return;

      new Compressor(files[0], { quality: .95, checkOrientation: true,
        success(result) {
          let reader = new FileReader();

          // Handle the compressed image file
          reader.onload = function(e) {
            v.$emit('input', { thumbnail_url: reader.result, image_name: files[0].name })
          };
          reader.readAsDataURL(result);
          v.processingImage = false;
        },
        error(err) {
          console.log(err);
          let notificationHelper = this.$store.getters.notificationHelper;
          notificationHelper.createErrorNotification(messages.memorialImages.upload.fail.title);
          v.processingImage = false;
        }
      });
    }
    else
      v.$emit('input', null);
  }
}

</script>