<template>
  <div id="DataMatchingIndex">
    <div class="loading-overlay" v-if="loadingText">
      <i class="fa fa-spinner fa-spin"></i>
      <p>{{ loadingText }}</p>
    </div>
    <div class="container full-height">
      <div class="row">
        <div class="col-xs-6 image-panel">
          <h3 v-if="featureId">Feature ID: {{ featureId }}</h3>
          <section id="focal" v-if="memorialImages">
            <div v-if="selectedImage">
              <div class="parent panzoom-fit-img">
                <div class="panzoom">
                  <img ref="panzoomImage" :src="selectedImage.image_url">
                </div>
              </div>
            </div>
            <div class="thumbnail-images">
              <div v-for="(image, index) in memorialImages" :key="index">
                <a href="#" @click="selectedImage = image"><img :src="image.thumbnail_url" width="60" height="60" :class="[selectedImage === image ? 'selected' : '', 'thumb']"></a>
              </div>
            </div>
          </section>
        </div>
        <div class="col-xs-3 full-height sidebar-form search-panel">
          <h2 class="">Search <small style="padding-left: 4px;">Find person and link memorial</small></h2>
          <div class="search-form-container"></div>
          <div class="collapse-menu-results">
              <div class="search-results-div"></div>
          </div>
        </div>
        <div class="col-xs-3 right-panel">
          <div class="no-touch options">
            <div class="hi-icon-wrap hi-icon-effect-2 hi-icon-effect-2b">
              <div class="row">
                <div class="col-md-4 option-container">
                  <i class='hi-icon fa fa-arrow-left' style="color: #000000;"> <a href="javascript:{}" @click="changeMemorial(false)"></a></i>
                  <div>
                    <h4>
                      Previous Memorial
                    </h4>
                  </div>
                </div>
                <div class="col-md-4 option-container">
                  <i class='hi-icon fa fa-arrow-right' style="color: #000000;"> <a href="javascript:{}" @click="changeMemorial(true)"></a></i>
                  <div>
                    <h4>
                      Next Memorial
                    </h4>
                  </div>
                </div>
                <div class="col-md-4 option-container">
                  <i class='hi-icon fa fa-check' style="color: green;"> <a href="javascript:{}" @click="finishValidation"></a></i>
                  <div>
                    <h4>
                      Finished Validation
                    </h4>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-4 option-container">
                  <i class='hi-icon fa fa-times' style="color: #FF3434;"> <a href="javascript:{}" @click="skipMemorial"></a></i>
                  <div>
                    <h4>
                      Skip
                    </h4>
                  </div>
                </div>
                <div class="col-md-4 option-container">
                <i class='hi-icon fa fa-user-plus' style="color: #C2AD42;">
                  <a href="javascript:{}" onclick="memorialModule.showEmptyPersonDetails()"></a>
                </i>
                <div>
                  <h4>
                    Add Person
                  </h4>
                </div>
                </div>
              </div>
            </div>
          </div>
          <h2 class="">People <small style="font-size: 15px;padding-left: 4px;">linked to memorial</small></h2>
          <table id="table-people-sorter" class='table table-fixed borderless' style="width: 100%;background-color: #E0D9B0;">
            <thead>
            <tr>
              <th>Name</th>
              <th>Age</th>
              <th>Break Link</th>
            </tr>
            </thead>
            <tbody>
              <tr v-for="person in linkedPeople" :key="person.person_id">
                <td>{{person.first_names}} {{person.last_name}}</td>
                <td>{{formatAgeYears(person.age_years, person.age_months, person.age_weeks, person.age_days, person.age_hours, person.age_minutes)}}</td>
                <td>
                  <button type="submit" @click="breakLink(person.person_id, person.first_names, person.last_name)" class="btn btn-bgms btn-form btn-table ladda-button" data-style="slide-right" aria-label="Left Align">
                    <span class="fa fa-minus-circle" aria-hidden="true" style="color: red;"></span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-if="inscriptions && inscriptions.length > 0">
            <h2 class="">Memorial Inscriptions</h2>
            <table id="table-people-sorter" class='table table-fixed borderless' style="width: 100%;background-color: #E0D9B0;">
              <thead>
              <tr>
                <th>Name</th>
                <th>Age</th>
              </tr>
              </thead>
              <tbody>
                <tr v-for="inscription in inscriptions" :key="inscription.id">
                  <td>{{ inscription.first_names }} {{ inscription.last_name }}</td>
                  <td>{{ inscription.age }}</td>
                  <td class="col-xs-1"><button title="Search" id="searchForm" type="submit" class="btn btn-bgms btn-form ladda-button" data-style="slide-right" aria-label="Left Align" style="font-size: 20px; height: 25px;"
                  @click="inscriptionSearch(inscription.first_names, inscription.last_name, inscription.age)"><span class="ladda-label">
                  </span><span class="icon-Search-Filled" aria-hidden="true"></span></button></td>
                  <td id="remove-icon" class="col-xs-1">
                    <form :id="'remove-inscription-form-' + inscription.id" action="" method="post">
                      <input type="hidden" name="id" :value="inscription.id"/>
                    </form>
                    <a :id="'remove-' + inscription.id" class="glyphicon glyphicon-remove"
                      @click="deleteMemorialInscription(inscription.id)"></a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import Component from 'vue-class-component'
import { Watch } from 'vue-property-decorator'
import axios from 'axios'
import panzoom from 'panzoom'
import PNotify from 'pnotify/dist/es/PNotify.js';
import PNotifyButtons from 'pnotify/dist/es/PNotifyButtons.js';
import PNotifyConfirm from 'pnotify/dist/es/PNotifyConfirm.js';
import { messages } from '@/global-static/messages.js';
import { formatAgeYears } from '@/global-static/dataFormattingAndValidation.ts';

Vue.use(Vuex);

/**
 * Class representing Index component
 * @extends Vue
 */
@Component
export default class Index extends Vue {

  formatAgeYears = formatAgeYears;

  memorialId = null;
  featureId = null;
  memorialImages = null;
  linkedPeople = [];
  inscriptions = [];

  selectedImage = null;
  
  loadingText = null;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    
    let v = this;

    // load memorial data
    v.loadMemorialData();

    // get the search form
    axios.get('/datamatching/searchPerson/')
      .then(function(response) {
        (window as any).jQuery( ".search-form-container" ).append(response.data);
      })
      .catch(function(response) {
        console.warn('Couldn\'t get unmatched memorials count:', response);
      });

    // event is used when a person from search results is selected for linking
    (window as any).jQuery(document).on('personSelectedForLinking', this.personSelectedForLinking);

    // Initiate the required modules for PNotify
    PNotifyButtons;
    PNotifyConfirm;
  }
  
  /**
   * Vue destroyed lifecycle hook
   * - remove jQuery event used by search form to add person to memorial
   */
  destroyed() {
    (window as any).jQuery(document).off('personSelectedForLinking', this.personSelectedForLinking);
  }

  /*** Watchers ***/
  /**
   * Watcher: When the selected image is changed reapply the panzoom (resetting zoom level)
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('selectedImage', { immediate: true})
  onImageChanged(val: any, oldVal: any) {
    if (val) {
      Vue.nextTick(() => {
        let area = this.$refs.panzoomImage as HTMLElement;
        panzoom(area, {
          zoomSpeed: 0.1 // 6.5% per mouse wheel event
        });
      });
    }
  }

  /*** Computed ***/

  /*** Methods ***/

  resetData() {
    this.memorialImages = null;
    this.selectedImage = null;

    this.linkedPeople = [];
    this.inscriptions = [];
    this.memorialId = null;
    this.featureId = null;
  }

  setData(data) {
    this.memorialImages = data.images;
    this.selectedImage = this.memorialImages[0];

    this.linkedPeople = data.memorial_persons;
    this.inscriptions = data.memorial_inscriptions;
    this.memorialId = data.id;
    this.featureId = data.feature_id;
  }
  
  /**
   * Load memorial data
   */
  loadMemorialData() {
    let v = this;
    
    v.loadingText = 'Loading';

    axios.get('/datamatching/unmatchedMemorials/')
      .then(function(response) {
        v.setData(response.data);
        v.loadingText = null;
      })
      .catch(function(response) {
        console.warn('Couldn\'t get memorial data:', response);
        v.loadingText = null;
      });
  }

  /**
   * Break link between memorial and person
   * @param personId Person's id
   */
  breakLink(personId, first_names, last_name) {
    let v = this;

    v.confirmationNotice('Break link with person: ' + first_names + ' ' + last_name + '?', 
    () => {
      v.loadingText = 'Breaking link';

      const postData = {
        "personId": personId,
        "memorialId": v.memorialId
      }

      axios.post('/datamatching/breakLink/', postData)
        .then(function(response) {
          //remove link on page
          for(var i = 0; i < v.linkedPeople.length; i++) {
            if(v.linkedPeople[i].person_id == personId) {
              v.linkedPeople.splice(i, 1);
              v.loadingText = null;
              break;
            }
          }
        })
        .catch(function(response) {
          console.warn('Couldn\'t break link with person:', response);
          v.loadingText = null;
        });
    }, () => {});
  }

  /**
   * Link person to memorial (asking user for confirmation first)
   * @param e
   * @param personData Object {first_names, last_name, personId, age}
   */
  personSelectedForLinking(e, personData){

    let v = this;

    const newPerson = personData.newPerson;

    const postData = {
      "personId": personData.personId,
      "memorialId": v.memorialId
    }

    const yesCallback = () => {
      v.loadingText = "Linking person";

      axios.post('/datamatching/linkMemorial/', postData)
      .then(function(response) {
        //add linked person
        v.linkedPeople.push({
          age_years: personData.age_years,
          age_months: personData.age_months,
          age_weeks: personData.age_weeks,
          age_days: personData.age_days,
          age_hours: personData.age_hours,
          age_minutes: personData.age_minutes,
          first_names: personData.first_names,
          last_name: personData.last_name,
          person_id: personData.personId
        });
        
        if (!newPerson) {
          //this will refresh the search results (currently the only way to get linked icon to change in results)
          let searchSubmitButton = document.getElementById("searchForm");
          searchSubmitButton.click();
        }

        v.loadingText = null;
      })
      .catch(function(response) {
        console.warn('Couldn\'t create link between person and memorial:', response);
        v.loadingText = null;
      });
    }

    if (newPerson) {
      // don't ask for confirmation
      yesCallback();
    }
    else {
      // ask for confirmation
      v.confirmationNotice('Add memorial to ' + personData.first_names + ' ' + personData.last_name + '?', yesCallback, () => {});
    }
  }

  /**
   * Search for inscription
   */
  inscriptionSearch(firstNames, lastName, age) {
    (window as any).memorialModule.inscriptionSearch(firstNames, lastName, age);
  }

  /**
   * Delete inscription
   */
  deleteMemorialInscription(id) {
    let v = this;

    v.loadingText = "Deleting inscription";

    let postData = {
      "id": id
    }

    axios.delete('/api/memorialInscriptions/', { params: postData })
      .then(function (response) {
        console.log(response);
        (window as any).memorialModule.successNotification(messages.memorialInscriptions.delete.success.title);
        v.loadingText = null;

        //remove record
        for(var i = 0; i < v.inscriptions.length; i++) {
          if(v.inscriptions[i].id == id) {
            v.inscriptions.splice(i, 1);
            break;
          }
        }
      })
      .catch(function (error) {
        console.log(error);
        v.loadingText = null;
        (window as any).memorialModule.failNotification(messages.memorialInscriptions.delete.fail.title);
      });
  }

  finishValidation() {
    let v = this;

    v.loadingText = "Validating memorial";

    axios.post('/datamatching/memorialValidated/')
      .then(function (response) {
        (window as any).memorialModule.successNotification("Memorial has been successfully validated");
        v.resetData();
        v.setData(response.data);
        v.loadingText = null;
      })
      .catch(function (error) {
        console.log(error);
        v.loadingText = null;
        (window as any).memorialModule.failNotification("Memorial validation has failed");
      });
  }

  skipMemorial() {
    let v = this;

    v.loadingText = "Skipping memorial";

    axios.post('/datamatching/memorialSkipped/')
      .then(function (response) {
        (window as any).memorialModule.successNotification("Memorial has been successfully skipped");
        v.resetData();
        v.setData(response.data);
        v.loadingText = null;
      })
      .catch(function (error) {
        console.log(error);
        v.loadingText = null;
        (window as any).memorialModule.failNotification("Memorial skip has failed");
      });
  }

  changeMemorial(forwardDirection) {
    let v = this;

    v.loadingText = "Loading";

    axios.post('/datamatching/changeMemorial/', { forwardDirection: forwardDirection })
      .then(function (response) {
        v.resetData();
        v.setData(response.data);
        v.loadingText = null;
      })
      .catch(function (error) {
        console.log(error);
        v.loadingText = null;
        (window as any).memorialModule.failNotification("Memorial change has failed");
      });
  }

  confirmationNotice(text, yesCallback, noCallback) {
    let notice = PNotify.notice({
      title: 'Confirmation Needed',
      text: text,
      icon: 'glyphicon glyphicon-question-sign',
      hide: false,
      styling: 'bootstrap3',
      modules: {
        Confirm: {
          confirm: true,
          buttons: [
            {
              text: 'Yes',
              primary: true,
              promptTrigger: true,
              click: (notice, value) => {
                notice.close();
                yesCallback();
              }
            },
            {
              text: 'No',
              click: (notice) => {
                notice.close();
                noCallback();
              }
            }
          ]
        },
        Buttons: {
          closer: false,
          sticker: false
        },
        History: {
          history: false
        }
      },
      stack: {"dir1": "down","dir2": "right","firstpos1": ((window as any).innerHeight / 2 - 150),"firstpos2": ((window as any).innerWidth / 2 - 150)}
    });
  }
}
</script>