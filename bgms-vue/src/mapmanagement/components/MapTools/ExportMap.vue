<template>
  <div>
    <!-- panel left -->
    <div class="exportMap left">
      <div
        class="container"
        aria-expanded="true"
        style="
                width: 80%;
                margin-top: 96px;
                background-color: rgba(223, 223, 224, 0.8);
            "
      >
        <div
          class=""
          style="
              border-bottom: 1px solid #EF622D;
              margin-bottom: 15px;
              color: #E9602C;
              text-align: center;
          "
        >
          <h3 class="">Export map tools</h3>
        </div>

        <div class="row animated-radiobutton">
          <div class="col-md-12" style="">
            <form>
              <input
                type="radio"
                name="memorial-id-label"
                id="memorial-id-label"
                value="1"
                v-model="showLabels"
                @change="showOrHideMemorialLabels"
              />
              <label for="memorial-id-label"
                >Show memorial reference number</label
              >
              <!-- burial number start -->
              <input
                type="radio"
                name="burial-number-label"
                id="burial-number-label"
                value="5"
                v-model="showLabels"
                @change="showOrHideBurialNumberLabels"
              />
              <label for="burial-number-label"
                >Show burial number</label
              >
              <!-- burial number end -->
               <!-- show grave number start -->
              <input
                type="radio"
                name="show-grave-number"
                id="show-grave-number"
                value="4"
                v-model="showLabels"
                @change="showOrHideLabel"
              />
              <label for="show-grave-number">Show grave number</label>
               <!-- show grave number end -->
              <input
                type="radio"
                name="memorial-image-check-label"
                id="memorial-image-check-label"
                value="2"
                v-model="showLabels"
                @change="showOrHideMemorialImageCheck"
              />
              <label for="memorial-image-check-label"
                >Show memorial images check</label
              >
              <input
                type="radio"
                name="memorial-no-label"
                id="memorial-no-label"
                value="3"
                v-model="showLabels"
                @change="
                  showOrHideMemorialLabels();
                  showOrHideMemorialImageCheck();
                  showOrHideLabel();
                "
              />
              <label for="memorial-no-label">Show no labels</label>
            </form>
          </div>
        </div>

        <div v-show="showLabels === '1' || showLabels === '4' || showLabels === '5'">
          <div class="row">
            <div class="col-md-12">
              <button
                class="btn sidebar-normal-button btn-bgms ladda-button btn-form-details"
                data-style="slide-right"
                aria-label="Left Align"
                style="
                         /* z-index: 10; */
                         font-size: 22px;
                         color: rgba(56, 59, 61, 1);
                         padding: 0px 10px 0px 0px;
                         border: 0px;
                         background-color: transparent!important;
                         box-shadow: inset 0px 0px 0px 0px rgba(0, 0, 0, 0.00);
                         height: 35px;
                         padding-left: 0px;
                       "
                disabled
              >
                <span class="ladda-label"></span>
                <span class="fa fa-font" aria-hidden="true"></span>
              </button>
              <label>Font size:</label>
              <input
                v-model="fontSizeRange"
                style="background-color: rgb(201, 201, 201);border: 0px;width: 16px;font-weight: bold;"
                readonly
              />
            </div>
          </div>

          <div class="row">
            <div class="fieldWrapper form-group col-md-12">
              <input
                name="fuzzy_value"
                type="range"
                min="5"
                max="25"
                value="12"
                step="1"
                v-model="fontSizeRange"
                @change="changeFontSize()"
                class="input-range"
              />
              <span>5</span>
              <span style="float: right;">25</span>
            </div>
          </div>
        </div>

        <div class="row animated-checkbox">
          <div class="col-md-12" style="">
            <input
            :disabled="severalSurnames"
              type="checkbox"
              name="several-popup"
              id="several-popup"
              v-model="severalPopUps"
              @change="severalPopupCheckboxChange($event)"
            />
            <label for="several-popup" style="/* padding-top: 4px; */" class=""
              >Display full details</label
            >
          </div>
        </div>
        <!-- Only Surname Display Start --> 
        <div class="row animated-checkbox">
          <div class="col-md-12" style="">
            <input
            :disabled="severalPopUps"
              type="checkbox"
              name="surname-popup"
              id="surname-popup"
              v-model="severalSurnames"
              @change="LastNamesCheckboxChange($event)"
            />
            <label for="surname-popup" style="/* padding-top: 4px; */" class=""
              >Display Last Names only</label
            >
          </div>
        </div>
        <!-- Only Surname Display End -->

<!-- Safe pdf Start-->
        <div class="row">
          <div
            class="col-md-12"
            style=""
          >
            <button
              class="btn sidebar-normal-button btn-bgms ladda-button btn-form-details"
              data-style="slide-right"
              aria-label="Left Align"
              style="
                       /* z-index: 10; */
                       font-size: 22px;
                       color: rgba(56, 59, 61, 1);
                       padding: 0px 10px 0px 0px;
                       border: 0px;
                       background-color: transparent;
                       box-shadow: inset 0px 0px 0px 0px rgba(0, 0, 0, 0.00);
                       height: 35px;
                       padding-left: 0px;
                     "
              bgms-export-map
              @click="savePdf"
            >
              <span class="ladda-label"></span>
              <span class="icon-Save-Filled" aria-hidden="true"></span>
            </button>
            <label>Save PDF</label>
          </div>
        </div>
          <!-- Safe pdf End-->
          <!-- Safe PNG Start-->
        <div class="row">
          <div
            class="col-md-12"
            style=""
          >
            <button
              class="btn sidebar-normal-button btn-bgms ladda-button btn-form-details"
              data-style="slide-right"
              aria-label="Left Align"
              style="
                       /* z-index: 10; */
                       font-size: 22px;
                       color: rgba(56, 59, 61, 1);
                       padding: 0px 10px 0px 0px;
                       border: 0px;
                       background-color: transparent;
                       box-shadow: inset 0px 0px 0px 0px rgba(0, 0, 0, 0.00);
                       height: 35px;
                       padding-left: 0px;
                     "
              bgms-export-map
              @click="saveMap"
            >
              <span class="ladda-label"></span>
              <span class="icon-Save-Filled" aria-hidden="true"></span>
            </button>
            <label>Save Image</label>
          </div>
        </div>
        <div class="aligned-bottom">
          <div class="row">
            <div class="col-md-12">
              <label>Help</label>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <div class="col-md-1" style="padding: 0;text-align: center;">
                <i
                  class="far fa-lightbulb"
                  aria-hidden="true"
                  style="font-size: 15px;"
                ></i>
              </div>
              <div class="col-md-11" style="padding: 0">
                <label style="font-weight: normal;"
                  >Use Alt+Shift+Drag to rotate the map</label
                >
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <div class="col-md-1" style="padding: 0;text-align: center;">
                <i
                  class="far fa-lightbulb"
                  aria-hidden="true"
                  style="font-size: 15px;"
                ></i>
              </div>
              <div class="col-md-11" style="padding: 0">
                <label style="font-weight: normal;"
                  >Click on
                  <span class="glyphicon glyphicon-arrow-up"></span> to reset
                  rotation</label
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- panel right -->
    <div class="exportMap right"></div>

    <!-- title site -->
    <!-- <div class="exportMap float title">
      <h3 style="
        margin: 10px;
        font-weight: 600;">  exportMap.title  <!  capitalize  >
        <!  <small style="font-size: 15px;padding-left: 4px;"> exportMap.dateExport | date:'dd MMM yyyy' </small>   >
      </h3>
    </div> -->

    <!-- Map details bottom floating box-->
    <div class="exportMap float mapDetails">
      <div class="row">
        <div class="col-md-10 border-right">
          <div class="row">
            <div class="col-md-6 border-right">
              <div class="row margin-left-zero">
                <div class="col-md-12 padding-bottom border-bottom">
                  <label> Title: </label>
                  <input type="text" />
                </div>
              </div>
              <div class="row margin-zero">
                <div class="col-md-6 border-right padding-bottom">
                  <label> Printed by </label>
                  <input type="text" />
                </div>
                <div class="col-md-6 padding-bottom">
                  <label> Ref no. </label>
                  <input type="text" />
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <label> Notes </label>
             <textarea class="form-control" maxlength="250"></textarea>
            </div>
          </div>
        </div>
        <div class="col-md-2 padding-left-zero">
          <div class="row margin-zero">
            <div class="col-md-12 padding-bottom-div border-bottom">
              <label> Date: </label><br />
              {{ dateExport }}
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <img
                class="center-block"
                style="margin-top: 10px;"
                src="data:image/png;base64,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"
                crossorigin="anonymous"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { jsPDF } from "jspdf";
import Component, { mixins } from "vue-class-component";
import html2canvas from "html2canvas";
import FileSaver from "file-saver";
import moment from "moment";
import PersonMixin from "@/mapmanagement/mixins/personMixin.ts";
import {
  VISUALISATIONENUM,
  showMemorialIndicators,
  hideMemorialIndicators,
} from "@/mapmanagement/components/Map/models/Memorial";

/**
 * Class representing ExportMap component
 * @extends Vue
 */
@Component
export default class ExportMap extends mixins(PersonMixin) {
  showLabels: string = "5";
  fontSizeRange: number = 15;
  graves_response = [];
  burial_numbers=[]

  notificationHelper: any = this.$store.getters.notificationHelper;
  exportMapService: any = this.$store.getters.exportMapService;
  mapService: any = this.$store.getters.mapService;
  eventService = this.$store.getters.eventService;
  personInteractionService = this.$store.getters.personInteractionService;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    //Create panels to maximize printing area for A4 in any screen resolution
    this.exportMapService.createPrintingArea();

    //Hide other options in the map tools
    (window as any).jQuery("#memorialAccordion").css("display", "none");
    (window as any).jQuery("#burialAccordion").css("display", "none");
    (window as any).jQuery("#drawingToolsAccordion").css("display", "none");
    (window as any).jQuery("#otherAccordion .hide-opt").css("display", "none");

    (window as any).jQuery("#otherTools").css("z-index", "1030");
    (window as any).jQuery("#layersAccordion").css("z-index", "1030");

    //Close search container if it's is open
    this.$store.commit("opencloseExportMap", true);

    //bind resize event to window
    (window as any)
      .jQuery(window)
      .on("resize", this.exportMapService.createPrintingArea);

    //show control reset ratation
    (window as any).jQuery(".ol-rotate").css("display", "");

    //change style north arrow (reset button)
    this.mapService.changeResetButtonIcon();

    // initially display feature ids
    this.showLabels = "1";
    this.showOrHideMemorialLabels();
  }

  /**
   * Vue destroyed lifecycle hook
   */
  destroyed() {
    //Move back scale bar to the original place
    (window as any).jQuery(".olex-mouse-position").css("left", "84px");
    (window as any).jQuery(".ol-scale-line").css("left", "84px");
    (window as any).jQuery(".ol-scale-line").css("top", "25px");

    //Move back directional arrow
    (window as any).jQuery(".ol-rotate").css("left", "190px");
    (window as any).jQuery(".ol-rotate").css("top", "0.5em");

    //Show other map tools again
    (window as any).jQuery("#memorialAccordion").css("display", "");
    (window as any).jQuery("#burialAccordion").css("display", "");
    (window as any).jQuery("#drawingToolsAccordion").css("display", "");
    (window as any).jQuery("#otherAccordion .hide-opt").css("display", "");

    //Reopen search container in case it was open
    this.$store.commit("opencloseExportMap", false);

    // unbind resize event
    (window as any)
      .jQuery(window)
      .off("resize", this.exportMapService.createPrintingArea);

    //Set default true for checkbox options
    this.$store.commit("resetOptions");

    //clean popups
    this.eventService.removeEventsByGroup("ExportMap");
    this.exportMapService.cleanPopUps();

    this.exportMapService.restoreMemorialsStyle();
    hideMemorialIndicators();

    this.severalPopUps = false;
    this.severalSurnames=false
    
    let personController = (window as any).angular
      .element(
        document.querySelector("[ng-controller='personController as person']")
      )
      .controller();

    this.eventService.pushEvent({
      group: "person",
      name: "clickMemorialDetails",
      layerGroup: ["memorials"],
      type: "click",
      handler: personController.showMemorialOnClick
    });
  }

  /*** Computed ***/

  /**
   * Get severalPopUps
   * @returns {boolean}
   */
  get severalPopUps(): boolean {
    return this.$store.state.ExportMap.severalPopUps;
  }
  /**
   * Set severalPopUps
   * @param {boolean} value
   */
  set severalPopUps(value: boolean) {
    this.$store.commit("setSeveralPopUps", value);
  }
  
  /**
   * Get severalSurnames
   * @returns {boolean}
   */
  get severalSurnames(): boolean {
    return this.$store.state.ExportMap.severalSurnames;
  }
  /**
   * Set severalSurnames
   * @param {boolean} value
   */
  set severalSurnames(value: boolean) {
    this.$store.commit("setSeveralSurnames", value);
  }
 
  /**
   * Get title
   * @returns {string}
   */
  get title(): string {
    if (this.exportMapService) return this.exportMapService.title;
    return null;
  }

  /**
   * Get username
   * @returns {string}
   */
  get username(): string {
    if (this.exportMapService) return this.exportMapService.username;
    return null;
  }

  /**
   * Get dateExport
   * @returns {string}
   */
  get dateExport(): string {
    return moment().format("D MMM YYYY");
  }

  /*** Methods ***/
  /**
   * Show or Hide Label
   */
  async showOrHideLabel(){
    if (this.showLabels !== "4"){
      hideMemorialIndicators();
    }
    else {
      if(this.graves_response.length == 0){
        this.graves_response = await this.$store.dispatch('plot_lables').then((res)=>{return res})
      }
      hideMemorialIndicators();
      this.exportMapService.changeAllMemorialsLabel(this.fontSizeRange, this.graves_response);
    }
  }
  /**
   * Show or Hide Burial Number
   */
  async showOrHideBurialNumberLabels(){
    if (this.showLabels !== "5"){
      hideMemorialIndicators();
    }
    else {
      if(this.burial_numbers.length == 0){
        this.burial_numbers = await this.$store.dispatch('burial_number').then((res)=>{return res})
      }
      hideMemorialIndicators();
      this.exportMapService.burialNumber(this.fontSizeRange, this.burial_numbers)
    }
  }

  /**
   * Toggle memorial labels
   */
  showOrHideMemorialLabels() {
    if (this.showLabels !== "1") this.exportMapService.restoreMemorialsStyle();
    else this.exportMapService.changeAllMemorialsText(this.fontSizeRange);
  }

  /**
   * Toggle memorial image check
   */
  showOrHideMemorialImageCheck() {
    if (this.showLabels !== "2") hideMemorialIndicators();
    else showMemorialIndicators(VISUALISATIONENUM.image);
  }

  /**
   * Change font size of label
   */
  changeFontSize() {
    if (this.showLabels === "1") {
      this.exportMapService.changeFontSize(this.fontSizeRange);
    }
    if (this.showLabels === "4") {
      this.exportMapService.changeAllMemorialsLabel(this.fontSizeRange, this.graves_response);
    }
     if (this.showLabels === "5") {
      this.exportMapService.burialNumber(this.fontSizeRange, this.burial_numbers);
    }
  }

  /**
   * Save the map to pdf
   */
   savePdf() {
    /*this.notificationHelper.createInfoNotification('Save Map', 'Sorry, this feature is currently unavailable. Please take a screenshot instead.');*/

    // 'Screenshot' the page using html2canvas
    html2canvas(document.getElementById("MapManagementVueApp") as HTMLElement, {
      useCORS: true,
      allowTaint: false,
      scale: 1
    }).then(canvas => {
      /*
      72 ppi:
        1 cm = 37.795276px;
        1px = 0.02645833 cm;

      A4: 210 x 297 mm
      A4 - 72 dpi: 595 Pixels  X 842 Pixels
       */

      // Convert page screenshot from canvas to image
      var canvasSrc = canvas.toDataURL();
      var image = new Image();
      image.src = canvasSrc;

      // Wait for the image to load
      image.onload = event => {
        // Create canvas with A4 dimensions
        var canvasToExport = document.createElement("canvas");
        canvasToExport.width = this.exportMapService.ratioWidthA4;
        canvasToExport.height = this.exportMapService.heightMap;
        var contextCanvasToExport = canvasToExport.getContext("2d");
        // Source image x, y, width, height (a.k.a. crop the screenshot to the export map window)
        var sX = this.exportMapService.widthBackground / 2;
        var sY = 50;
        var sW = this.exportMapService.ratioWidthA4;
        var sH = this.exportMapService.heightMap;

        // Destination image x, y, width, height (a.k.a. the size you want the cropped image to be)
        var dX = 0;
        var dY = 0;
        var dW = canvasToExport.width;
        var dH = canvasToExport.height;

        contextCanvasToExport.drawImage(image, sX, sY, sW, sH, dX, dY, dW, dH);
        
        // // Put Map in frame after exporting
        var dw = canvasToExport.width-10; 
        var dh = canvasToExport.height-10;

      //Put white border around frame
      if (canvas.getContext) {
          var sw = canvasToExport.width-5;
          var sh = canvasToExport.height-5;

          var ctx = canvasToExport.getContext("2d");
        
        ctx.lineWidth = 8;
        ctx.fillStyle='white'
        ctx.strokeStyle ="white";
        ctx.strokeRect(1, 1, sw, sh);}
      
      //Uses canvas element HTML5 for frame
        contextCanvasToExport.rect(4, 3, dw, dh);
        contextCanvasToExport.lineWidth = 1;
        contextCanvasToExport.strokeStyle = "black";
        contextCanvasToExport.stroke();

        // check jsPDF documentation for explanation
        var imgWidth =(canvasToExport.width)/2
        var imgHeight =(canvasToExport.height)/2

        var imgData = canvasToExport.toDataURL('image/jpeg',1.0)
        // map extension
        var el = new URL(window.location.href)
        
        var doc = new jsPDF()
       
        if(imgWidth > imgHeight){

          doc = new jsPDF('l', 'px', [imgWidth, imgHeight]);
          doc.addImage(imgData,'JPEG',1, 1,imgWidth,imgHeight)
           try{
              doc.save((`${el.host.split(".")[0]}.pdf`))
              this.notificationHelper.createSuccessNotification( "Pdf exported successfully")
              }catch(e){
                this.notificationHelper.createErrorNotification( "An unexpected error has occurred exporting the Pdf, please contact support" )

              }
          }else{
                doc = new jsPDF('p', 'px', [imgWidth, imgHeight]);
                doc.addImage(imgData,'JPEG',1, 1,imgWidth,imgHeight)
                try{
              doc.save((`${el.host.split(".")[0]}.pdf`))
              this.notificationHelper.createSuccessNotification( "Pdf exported successfully")
              }catch(e){
                this.notificationHelper.createErrorNotification( "An unexpected error has occurred exporting the Pdf, please contact support" )

              }
                }
          
      };
    });
  }
  //  Save Map PNG
  saveMap() {
    /*this.notificationHelper.createInfoNotification('Save Map', 'Sorry, this feature is currently unavailable. Please take a screenshot instead.');*/

    // 'Screenshot' the page using html2canvas
    html2canvas(document.getElementById("MapManagementVueApp") as HTMLElement, {
      useCORS: true,
      allowTaint: false,
      scale: 1
    }).then(canvas => {
      /*
      72 ppi:
        1 cm = 37.795276px;
        1px = 0.02645833 cm;

      A4: 210 x 297 mm
      A4 - 72 dpi: 595 Pixels  X 842 Pixels
       */

      // Convert page screenshot from canvas to image
      var canvasSrc = canvas.toDataURL();
      var image = new Image();
      image.src = canvasSrc;

      // Wait for the image to load
      image.onload = event => {
        // Create canvas with A4 dimensions
        var canvasToExport = document.createElement("canvas");
        canvasToExport.style.position='absolute'
        canvasToExport.width = this.exportMapService.ratioWidthA4;
        canvasToExport.height = this.exportMapService.heightMap;
        var contextCanvasToExport = canvasToExport.getContext("2d");
        canvasToExport.id='canvas'
        
        // Source image x, y, width, height (a.k.a. crop the screenshot to the export map window)
        var sX = this.exportMapService.widthBackground / 2;
        var sY = 50;
        var sW = this.exportMapService.ratioWidthA4;
        var sH = this.exportMapService.heightMap;

        // Destination image x, y, width, height (a.k.a. the size you want the cropped image to be)
        var dX = 0;
        var dY = 0;
        var dW = canvasToExport.width;
        var dH = canvasToExport.height;

        contextCanvasToExport.drawImage(image, sX, sY, sW, sH, dX, dY, dW, dH);
        // creates white border around black border
        if (canvas.getContext) {
          var sw = canvasToExport.width-10;
          var sh = canvasToExport.height-7;

          var ctx = canvasToExport.getContext("2d");
        
        ctx.lineWidth = 10;
        ctx.fillStyle='white'
        ctx.strokeStyle ="white";
        ctx.strokeRect(5, 4, sw, sh);}

        // Put Map in frame after exporting
        var dw = canvasToExport.width-18;
        var dh = canvasToExport.height-17;

        //Uses canvas element HTML5
        contextCanvasToExport.rect(9, 10, dw, dh);
        contextCanvasToExport.lineWidth = 1;
        contextCanvasToExport.strokeStyle = "black";
        
        contextCanvasToExport.stroke();

        // // Put Map in frame after exporting
        // var dw = canvasToExport.width-22;
        // var dh = canvasToExport.height-17;


        // //Uses canvas element HTML5
        // contextCanvasToExport.rect(9, 10, dw, dh);
        // contextCanvasToExport.lineWidth = 1;
        // contextCanvasToExport.strokeStyle = "black";
        // contextCanvasToExport.stroke();

        // Convert the canvas to a saveable Blob and save it as PNG
        var el = new URL(window.location.href)

        canvasToExport.toBlob(blob => {
          try {
            FileSaver.saveAs(blob, `${el.host.split(".")[0]}.png`);
            this.notificationHelper.createSuccessNotification(
              "Map exported successfully"
            );
          } catch (e) {
            this.notificationHelper.createErrorNotification(
              "An unexpected error has occurred exporting the map, please contact support"
            );
          }
        });
      };
    });
  }

  /**
   * Clear popups when feature is turned off
   */
  severalPopupCheckboxChange(value) {
    if (!value) {
      this.exportMapService.cleanPopUps()
      }
    else{
      this.eventService.removeEventByName('clickMemorialDetails');
      this.eventService.pushEvent({
      group: "ExportMap",
      name: "clickMemorialDetails",
      layerGroup: ["memorials"],
      type: "click",
      handler: this.showDetails
    });
    }
  }
/**
   * Clear Lastname popups when feature is turned off
   */
LastNamesCheckboxChange(value){
  if (!value) {
      this.exportMapService.cleanPopUps()
      }
    else{
     this.eventService.removeEventByName('clickMemorialDetails');
      this.eventService.pushEvent({
      group: "ExportMap",
      name: "clickMemorialDetails",
      layerGroup: ["memorials"],
      type: "click",
      handler: this.showSurname
    });
    }
}
/*** Watchers ***/
  /**
   * show details of persons/burials linked to memorial/plot
   */
  showDetails(evt, features) {
    const feature = features[0];
    //considering only 1st feature because only one memorial layer (cluster/geojson) is active at a time

    if (feature && !this.personInteractionService.isFeatureSelected(feature)) {
      //hovering on top of memorial
      this.personInteractionService
        .getPersonsUnmarkedGravesFromFeature(feature)
        .then(personsUnmarkedGraves => {
          const personArray = personsUnmarkedGraves["personArray"];
          const personsReserved = personsUnmarkedGraves["personsReserved"];
          const noOfUnmarkedGraves =
            personsUnmarkedGraves["noOfUnmarkedGraves"];
          const memorialId = personsUnmarkedGraves["memorialId"];
          // ugly json to array done to prevent duplicate values appearing
          const arr = Object.keys(personArray).map(function(k) {
            return personArray[k];
          });
          const arrpr = Object.keys(personsReserved).map(function(k) {
            return personsReserved[k];
          });
          const template = this.personInteractionService.createDetailsTemplate(
            arr,
            arrpr,
            noOfUnmarkedGraves,
            memorialId
          );
          if (template)
            this.showClickDetails(
              evt.coordinate,
              feature.getId(),
              template,
              template.scope["closeHandler"]
            );
        });
    } else if (!feature) this.exportMapService.cleanPopUps();
  }
  // Display Only Lastname
  showSurname(evt, features) {
    const feature = features[0];
    //considering only 1st feature because only one memorial layer (cluster/geojson) is active at a time

    if (feature && !this.personInteractionService.isFeatureSelected(feature)) {
      //hovering on top of memorial
      this.personInteractionService
        .getPersonsUnmarkedGravesFromFeature(feature)
        .then(personsUnmarkedGraves => {
          const personArray = personsUnmarkedGraves["personArray"];
          const memorialId = personsUnmarkedGraves["memorialId"];
          // ugly json to array done to prevent duplicate values appearing
          const arr = Object.keys(personArray).map(function(k) {
            return personArray[k];
          });
          const template = this.personInteractionService.createMarkerTemplate(
            arr,
            memorialId
          );
          if (template)
            this.showClickDetails(
              evt.coordinate,
              feature.getId(),
              template,
              template.scope["closeHandler"]
            );
        });
    } else if (!feature) this.exportMapService.cleanPopUps();
  }
}
</script>
