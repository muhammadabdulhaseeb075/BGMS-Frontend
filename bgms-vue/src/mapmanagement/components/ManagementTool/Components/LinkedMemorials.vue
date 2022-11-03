<template>
  <div style="width: 100%;">
    <label v-if="showLabel" class="col-xs-12 control-label">Memorials linked to this grave:</label>
    
    <table class="table">
      <thead v-if="selectFlag">
        <tr>
          <th>Select</th>
          <th>Type</th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody id="linked-memorials-list" v-if="componentData && componentData.linkedMemorials && componentData.linkedMemorials.length > 0">
        <tr class="images" v-for="linkedMemorial in sortedLinkedMemorials" :key="linkedMemorial.id" 
            v-viewer.rebuild="{title: 0, rebuild: true, toolbar: { zoomIn:4,zoomOut:4,oneToOne:4,reset:4,prev:4,next:4,rotateLeft:4,rotateRight:4 }, 
            url: (image) => {return image.getAttribute('data-image-url')}}">             
          <td v-if="selectFlag">
            <input type="checkbox" :value="linkedMemorial.id" v-model="selectedMemorials"/>
          </td>
          <td class="thumbnail-td" style="vertical-align: middle">{{ linkedMemorial.layer_display_name }}</td>

          <!-- Only show first 2 images and 'More'. -->
          <td class="thumbnail-td" v-show="index<=2" v-for="(image, index) in linkedMemorial.images" :key="'a'+index">
            <a style="position: relative" href="javascript:void(0)">

              <!-- Show 'More' instead of thumbnail for image 3. -->
              <div v-if="linkedMemorial.images.length>2 && index===2" class="image-count" @click="$el.querySelector('.images').$viewer.show();">More Images
                <img style="display: none" class="image-thumbnail" :data-image-url="image.image_url" :src="image.thumbnail_url"/>
              </div>

              <div v-else>
                <div class="image-loading-spinner">
                  <i class="fa fa-spinner fa-spin"/>
                </div>
                <img class="image-thumbnail" :data-image-url="image.image_url" :src="image.thumbnail_url"/>
              </div>

            </a>
          </td>
          <!-- filler if less than three images -->
          <td v-for="(n, index) in (getNumberOfEmptyColumns(linkedMemorial.images))" :key="'b'+index"></td>
          <!-- don't show link button if it's to the memorial that is already selected -->
          <td v-if="!selectFlag" style="vertical-align: middle"><a v-if="$route.params.id!==linkedMemorial.id" href="" @click="goToMemorialManagementTool(linkedMemorial.id, linkedMemorial.layer_name)" title="Go to Memorial Management"><i class="fa fa-arrow-circle-right"></i></a></td>
        </tr>
      </tbody>
      <tbody id="linked-memorials-list" v-if="!componentData || !componentData.linkedMemorials || componentData.linkedMemorials.length === 0">
        <tr>
          <td colspan="5" v-if="loadingDataFlag"><span class="fa fa-spinner fa-spin"></span></td>
          <td colspan="5" v-else>No memorials have been linked to this {{linkedType}}.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import Component, { mixins } from 'vue-class-component';
import { Watch, Prop } from 'vue-property-decorator';
import VueRouter from 'vue-router'
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';
import constants from '@/global-static/constants.ts';
import 'viewerjs/dist/viewer.css';
import Viewer from 'v-viewer';
import watermark from 'watermarkjs';

Vue.use(Vuex);
Vue.use(VueRouter);
Vue.use(Viewer)

/**
 * Class representing LinkedMemorials component
 * @extends Vue
 */
@Component
export default class LinkedMemorials extends mixins(ManagementToolsMixin) {

  @Prop() id;
  @Prop() linkedType;
  @Prop() selectFlagProp;
  @Prop() showLabel;

  selectedMemorials = [];
  sortedMemorialsPreLoaded = [];

  selectFlag: boolean = false;
  preLoaded: boolean = false;


  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    //debugger; // eslint-disable-line no-debugger
    this.componentName = "linked_memorials";
    this._id = this.id;
    this.selectFlag = this.selectFlagProp === true;

    // load data
    if (this.linkedType === 'person')
      this.loadData('/mapmanagement/relatedMemorials/?person_id=', this._id);
    else
      this.loadData('/mapmanagement/relatedMemorials/?graveplot_uuid=', this._id);
    
      /*this.preload(this.selectedMemorials, (completed, count) => {
        if (completed === true) {
          this.preLoaded = true;
        }
      })*/

  }

  /*** Computed ***/

  /**
   * Computed property:
   * @returns {any} 
   */
  get sortedLinkedMemorials() {
    //debugger; // eslint-disable-line no-debugger
    if (this.componentData && this.componentData.linkedMemorials) {
      const memorials = this.componentData.linkedMemorials;
      //console.log(typeof images[this.spriteCostumeCount])
      //let watermark = require('@/mapmanagement/static/images/ag_watermark.png');
      /*
      //try to preload the full sized images for all linked memorials
      this.preload(this.componentData.linkedMemorials[0].images, (completed, count) => { 
        if (completed === true) {
          this.preLoaded = true;
        }
      })
      */
      if (memorials && memorials.length > 1)
        return memorials.sort((a, b) => a.feature_id > b.feature_id);
      else
      return memorials;
    }
    else
      return [];
  }

  /*** Watchers ***/

  /**
   * Update store when a memorial has been un/selected
   */
  @Watch('selectedMemorials')
  onSelectedMemorialChanged(val: any, oldVal: any) {
    this.$store.commit('appendToComponentData', { componentName: this.componentName, fieldName: 'selectedMemorials', value: val });
  }

  // used to tell parent that data has just been loaded
  @Watch('loadingDataFlag')
  onLoadingDataFlagChanged(val: any, oldVal: any) {
    if (!val)
      this.$emit('loading-data-flag', val)
  }

  /*** Methods ***/

  watermark(imageSource){
    //debugger; //eslint-disable-line no-debugger
    console.log(imageSource);
    let new_watermark=imageSource;
    return new_watermark;
  }
  
  async addWatermark(originalImageSrc) {
    //debugger; //eslint-disable-line no-debugger    
    console.log('ImageURL: ' + originalImageSrc);  
    
    /*
    var options = {
      init: function (img) {
        img.crossOrigin = '*';
      }
    };
    
    await watermark([originalImageSrc])
      .image(watermark.text.lowerRight('AGResearch', '48px Arial', '#fff', 0.5))
      .render();    
    */
    //return watermarkedimage;
    
    let ag_watermark = "https://adlington.bgms.com:8000" + require('@/mapmanagement/static/images/ag_watermark_4x.png');
    //let ag_watermark = new Image();
    //ag_watermark.src = ag_watermark_path;
    
    var options = {
      init: function (img) {
        img.crossOrigin = '*';
      }
    };
    //console.log(typeof images[this.spriteCostumeCount])
    let watermarkedImage = await watermark([originalImageSrc, ag_watermark], options)      
      //.image(watermark.text.lowerRight('AGResearch', '75px Arial', '#fff', 0.75))
      //.render()    
      .image(watermark.image.upperLeft(0.35))
      .load([ag_watermark])
      .image(watermark.image.lowerRight(0.35))
      //.image(watermark.text.lowerRight('AGResearch', '75px Arial', '#fff', 0.75))
      .then(function (img) {
        document.getElementById('linked-memorials').appendChild(img);
      });
      
    /*
    return watermarkedImage = await watermark([originalImageSrc])      
      .image(watermark.text.lowerRight('AGResearch', '48px Arial', '#fff', 0.5))
      .render()
      .then(img => img);
    */
    return watermarkedImage;    
  }


load_img(resource, callback) { //utility methd to load images
  //debugger; //eslint-disable-line no-debugger 
  var img = new Image()
  img.crossOrigin = "*";  
  img.onload = function() {
    callback(img)
  }
  img.src = resource
}

preload(images, callback) { //loop through a list/array of images and preload each one 
  //debugger; //eslint-disable-line no-debugger   
  var l = images.length
  var n = 0
  var completed = false
  if (images.length) {
    for (let i = 0; i < images.length; i++) {
      var resource = images[i].image_url //load the full image, not the thumbnail
      this.load_img(resource, img => {
        n++
        if (typeof callback === 'function') {
          callback(completed, n / l)
          if (n >= l) {
            completed = true
            callback(completed, 1)
          }
        }
      })
    }
  } else {
    if (typeof callback === 'function') {
      completed = true
      callback(completed, 1)
    }
  }
}


  goToMemorialManagementTool(id, layerName) {    
    this.$router.replace({ name: constants.MEMORIAL_MANAGEMENT_PATH, params: { id: id, layer: layerName }})
  }

  /**
   * If less than three images, this will return number of empty columns
   */
  getNumberOfEmptyColumns(images): number {    
    const columnsForImages = 3;

    let imageCount = images ? images.length : 0;

    if (imageCount > columnsForImages)
      return 0;
    else
      return columnsForImages-imageCount;
  }

}
</script>
