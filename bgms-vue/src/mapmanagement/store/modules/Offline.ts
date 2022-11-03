const state = {
  swInstallMiniumumMB: 100,
  queuesMinimumMB: 25,
  serviceWorkerSupported: false,
  indexedDBSupported: false,
  online: true,
  offlineReady: false,
  swInControl: false,
  swQueueLength: 0,
  estimateQuotaAvailableMB: undefined,
  syncInProgress: false
}

// getters
const getters = {
  storageTooSmallForImageUpload: state => {
    // NaN when unavailable
    if ((state.swQueueLength || !state.online) && isNaN(state.estimateQuotaAvailableMB) && state.estimateQuotaAvailableMB<=state.queuesMinimumMB)
      return true;
    else
      return false;
  }
}

// actions
const actions = {
}

// mutations
const mutations = {
  updateServiceWorkerSupported (state, value) {
    state.serviceWorkerSupported = value;
  },
  updateIndexedDBSupported (state, value) {
    state.indexedDBSupported = value;
  },
  updateOnline(state, online) {
    state.online = online;
  },
  updateSwInControl(state, swInControl) {
    state.swInControl = swInControl;
  },
  updateSWQueueLength(state, value) {
    state.swQueueLength = value;
  },
  updateEstimateQuotaAvailableMB(state, estimate) {
    // NaN when unavailable
    if (isNaN(estimate.quota) || isNaN(estimate.usage))
      state.estimateQuotaAvailableMB = NaN
    else
      state.estimateQuotaAvailableMB = Math.round(estimate.quota/1048576 - estimate.usage/1048576);
  },
  updateSyncInProgress(state, value) {
    state.syncInProgress = value;
  },
  updateOfflineReady(state, value) {
    state.offlineReady = value;
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
