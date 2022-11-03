<template>
  <div v-show="surveysExist">
    <li class="top-border" @click="$emit('toggle_survey_subbuttons', subbuttonNames.SURVEYSUBBUTTONS)" v-if="loadingSurveys || (surveys && surveys.length>0) || siteAdminOrSiteWarden">
      <a href="javascript:void(0)" :class="{ active: showSurveySubbuttons }"><span>Surveys</span></a>
    </li>
    <div class="management-tool-subbuttons">
      <transition name="list">
        <ul v-show="showSurveySubbuttons && !loadingSurveys">
          
          <li @click="openCloseSurvey(null)" v-if="siteAdminOrSiteWarden">
            <a href="javascript:void(0)" class="add-new" :class="{ active: ($route.name===surveysRoute && !$route.params.surveyID) }"><i class="fas fa-plus"/> Add New</a>
          </li>

          <li v-for="survey in surveys" :key="survey.id" @click="openCloseSurvey(survey.survey_id.toString())">
            <a href="javascript:void(0)" :class="{ active: ($route.name===surveysRoute && $route.params.surveyID===survey.survey_id.toString()) }">{{ formatDate(survey.survey_date) }}</a>
          </li>

        </ul>
      </transition>
      <ul v-show="showSurveySubbuttons && loadingSurveys" class="loading-placeholder-contents">
        <li><i class="fa fa-spinner fa-spin"/></li>
      </ul>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import axios from 'axios'
import Component, { mixins } from 'vue-class-component'
import { Prop } from 'vue-property-decorator';
import FeatureTools from '@/mapmanagement/mixins/featureTools.ts';
import { SUBBUTTONNAMES } from '@/mapmanagement/static/constants.ts';
import constants from '@/global-static/constants.ts';
import { formatDate } from '@/global-static/dataFormattingAndValidation.ts';

/**
 * Class representing SurveyButtons component
 */
@Component
export default class SurveyButtons extends mixins(FeatureTools) {
  
  formatDate = formatDate;

  @Prop() surveysRoute;
  @Prop() managementToolRoute;
  @Prop() showSurveySubbuttons;

  surveys = null;
  subbuttonNames;

  availablePlotID = null;
  
  loadingSurveys: boolean = false;
  surveysExist: boolean = false;

  siteAdminOrSiteWarden: boolean = this.$store.state.siteAdminOrSiteWarden;

  mounted() {
    this.loadingSurveys = true;
    this.surveys = null;
    const id = this.$route.params.id;
    const layer = this.$route.params.layer;
    this.subbuttonNames = SUBBUTTONNAMES;

    // if this is a memorial or grave, we need to find the feature id, i.e. not memorial id or graveplot id
    if (this.managementToolRoute===constants.MEMORIAL_MANAGEMENT_PATH || this.managementToolRoute===constants.GRAVE_MANAGEMENT_PATH) {

      if (layer==="available_plot" && this.$route.params.availablePlotID) {
        this.availablePlotID = this.$route.params.availablePlotID;
        // we already know the topopolygon id (same as feature id) for available plots
        this.getSurveyList(this.availablePlotID);
      }
      else {
        this.getMemorialPlotFeatureID(layer, id)
        .then(featureID => {
          this.getSurveyList(featureID);
        });
      }
    }
    else
      this.getSurveyList(id);
  }

  /**
   * Gets a list of surveys completed for this feature
   * @param id This must be the id for the feature model (not feature_id)
   */
  getSurveyList(id) {
    // load list of surveys relating to feature
    axios.get('/survey/featureSurveysList?feature_id=' + id)
    .then((result) => {
      this.surveys = result.data;

      if (this.surveys && this.surveys.length > 0) {
        Vue.nextTick(() => {
          this.surveysExist = true;
          this.loadingSurveys = false;
        });
      }
      else {
        this.surveyTemplatesExist();
      }
    })
    .catch(() => {
      this.loadingSurveys = false;
    });
  }

  /**
   * Finds out if at least one survey template exists for this layer
  */
  surveyTemplatesExist() {
    axios.get('/survey/layerSurveyTemplatesExist/?layer=' + this.$route.params.layer)
    .then((response) => {
      if (response.data.surveyExists)
        this.surveysExist = response.data.surveyExists;
        
        Vue.nextTick(() => {
          this.loadingSurveys = false;
        });
    });
  }

  openCloseSurvey(surveyID) {
    if (this.$route.name!==this.surveysRoute || this.$route.params.surveyID!==surveyID) {
      // we're opening a survey

      let params = { surveyID: surveyID };

      if (this.availablePlotID)
        params['availablePlotID'] = this.availablePlotID;

      this.$router.push({ name: this.surveysRoute, params: params});
    }
    else
      this.$router.push({ name: this.managementToolRoute });
  }
}

</script>