import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import Endpoints from '@/analytics/services/endpoints';

Vue.use(Vuex);

export default new Vuex.Store({
  actions: {
    getAllModels({commit}) {
      return Endpoints.getModelsWithFields()
      .then((response: any) => {
        commit('addingReportModels', response.data);
      })
      .catch(error => {
        console.error('ERROR: Calling endpoints ', error);
      });
    },
    getModelEntries({ commit }, { name, options }) {
      return Endpoints.getModelEntries(name, options)
      .then((response: any) => {
        commit('addingReportData', response.data);
        return response;
      })
      .catch(error => {
        console.error('ERROR: Calling endpoints ', error);
      });
    },
    filterSuggestions({commit}, { modelName, field }) {
      return Endpoints.filterSuggestions(modelName, field)
      .then((response: any) => {
        return response;
      })
      .catch(error => {
        console.error('ERROR: Calling endpoints ', error);
      });
    },
    createReport({commit}, {payload}) {
      return Endpoints.createReport(payload)
      .then((response: any) => {
        commit('selectingReport', response.data);
        return response;
      })
      .catch(error => {
        console.error('ERROR: calling endpoints ', error);
      });
    },
    updateReport({commit}, {id, payload}) {
      return Endpoints.updateReport(id, payload)
      .catch(error => {
        console.error('ERROR: calling endpoints ', error);
      });
    },
    getAllReports({commit}) {
      return Endpoints.getAllReports()
      .then((response: any) => {
        commit('updateReportList', response.data);
        return response;
      })
      .catch(error => {
        console.error('ERROR: calling endpoints ', error);
      });
    },
    setReport({commit}, report) {
      commit('selectingReport', report);
    },
    getReportTemplates() {
      return Endpoints.getReportTemplates();
    },
    saveReportTemplate({commit}, report) {
      return Endpoints.createReportTemplate(report);
    },
    exportReport({commit}, reportId) {
      return Endpoints.exportToExcel(reportId);
    }
  },
  getters: {},
  state: {
    mainModelSelected: null,
    reportModels: null,
    reportData: null,
    reportList: null,
    selectedReport: null
  },
  mutations: {
    addingReportModels(state, models): void {
      state.reportModels = models;
    },
    addingReportData(state, data): void {
      state.reportData = data;
    },
    updateReportList(state, reportList): void {
      state.reportList = reportList;
    },
    selectingReport(state, report): void {
      state.selectedReport = report;
    }
  }
});
