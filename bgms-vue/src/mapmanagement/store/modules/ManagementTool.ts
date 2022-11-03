const state = {
  managementToolOpen: false,
  title: undefined,
  history: [],
  goBackFlag: false,
  goForwardFlag: false,
  closeFlag: false,
  restoreSavedDataFlag: false,
  future: [],
  currentInformation: {},
  currentInformationSaved: {},
  statusList: null,
  stateList: null,
  typeList: null,
  currencyList: null,
  ownerStatusList: null,
  professionList: null,
  burialOfficialList: null,
  burialOfficialType: null,
  eventList: null,
  religionList: null,
  parishList: null
}

// getters
const getters = {
}

// actions
const actions = {
  resetFeatureData({ commit }) {
    commit('resetSidebar', { root: true });
    commit('resetMemorialCaptureSidebar', { root: true });
    commit('resetFeatureData');
  }
}

// mutations
const mutations = {
  setManagementToolOpen(state, open: boolean) {
    state.managementToolOpen = open;
  },
  setTitle(state, title) {
    state.title = title;
  },
  routerChange(state, path) {
    // we have moved forward
    if (state.history[state.history.length-1] !== path) {
      state.history.push(path);
      state.future = [];
    }
  },
  goBackFlag(state, value) {
    state.goBackFlag = value;
  },
  goForwardFlag(state, value) {
    state.goForwardFlag = value;
  },
  closeFlag(state, value) {
    state.closeFlag = value;
  },
  goBack(state) {
    state.future.push(state.history[state.history.length-1]);
    state.history.pop();
  },
  goForward(state) {
    state.history.push(state.future[state.future.length-1]);
    state.future.pop();
  },
  resetHistory(state) {
    state.history = [];
    state.future = [];
  },
  commitRestoreSavedDataFlag(state, componentName) {
    state.restoreSavedDataFlag = componentName;
  },
  resetFeatureData(state) {
    state.currentInformation = {};
    state.currentInformationSaved = {};
    state.restoreSavedDataFlag = false;
  },
  setCurrentInformation(state, currentInformation) {
    state.currentInformation[currentInformation.componentName] = currentInformation.data;
  },
  componentHasUnsavedChanges(state, componentName) {
    if (state.currentInformation[componentName])
     state.currentInformation[componentName].unsavedChanges = true;
  },
  componentHasNoUnsavedChanges(state, componentName) {
    if (state.currentInformation[componentName])
     state.currentInformation[componentName].unsavedChanges = false;
  },
  cloneUnsavedToSaved(state, currentInformation) {
    state.currentInformationSaved[currentInformation.componentName] = deepClone(currentInformation.data);
  },
  removeComponentData(state, componentName) {
    delete state.currentInformation[componentName];
    delete state.currentInformationSaved[componentName];
  },
  cloneSavedToUnsaved(state, componentName) {
    state.currentInformation[componentName] = deepClone(state.currentInformationSaved[componentName]);
  },
  appendToComponentData(state, data) {
    if (!state.currentInformation[data.componentName])
      state.currentInformation[data.componentName] = {};
      
    state.currentInformation[data.componentName][data.fieldName] = data.value;
  },
  setComponentsCollapsedTrue(state, componentid) {
    state.componentsCollapsed[componentid  + 'Collapsed'] = true;
  },
  setComponentsCollapsedFalse(state, componentid) {
    state.componentsCollapsed[componentid  + 'Collapsed'] = false;
  },
  setGraveDetailLists(state, value) {
    state.statusList = value.status;
    state.stateList = value.state;
    state.typeList = value.type;
  },
  setPersonDetailLists(state, value) {
    state.professionList = value.profession;
    state.eventList = value.event;
    state.religionList = value.religion;
    state.parishList = value.parish;
  },
  setBurialDetailLists(state, value) {
    state.burialOfficialList = value.burial_official_list;
    state.burialOfficialType = value.burial_official_type;
  },
  setOwnershipLists(state, value) {
    state.currencyList = value.currency;
    state.ownerStatusList = value.ownerStatus;
  },
  appendStatusList(state, newStatus) {
    state.ownerStatusList.push(newStatus);

    // sort alphabetically
    state.ownerStatusList.sort((a,b) => {
      a = a.status || '';
      b = b.status || '';
      a.localeCompare(b, undefined, {ignorePunctuation: true})
    });
  },
  appendProfessionList(state, newProfession) {
    state.professionList.push(newProfession);

    // sort alphabetically
    state.professionList.sort((a,b) => {
      a = a.profession || '';
      b = b.profession || '';
      a.localeCompare(b, undefined, {ignorePunctuation: true})
    });
  },
  appendReligionList(state, newReligion) {
    state.religionList.push(newReligion);

    // sort alphabetically
    state.religionList.sort((a,b) => {
      a = a.religion || '';
      b = b.religion || '';
      a.localeCompare(b, undefined, {ignorePunctuation: true})
    });
  },
  appendParishList(state, newParish) {
    state.parishList.push(newParish);

    // sort alphabetically
    state.parishList.sort((a,b) => {
      a = a.parish || '';
      b = b.parish || '';
      a.localeCompare(b, undefined, {ignorePunctuation: true})
    });
  },
  appendEventList(state, newEvent) {
    state.eventList.push(newEvent);

    // sort alphabetically
    state.eventList.sort((a,b) => {
      a = a.name || '';
      b = b.name || '';
      a.localeCompare(b, undefined, {ignorePunctuation: true})
    });
  }
}

/**
 * 
 * @param o Object to be cloned
 * @returns a deep clone of the original object
 */
function deepClone(o) {
  let output, v, key;

  if (!o)
    return o;
  output = Array.isArray(o) ? [] : {};
  for (key in o) {
      v = o[key];
      output[key] = (typeof v === "object") ? deepClone(v) : v;
  }
  return output;
}

export default {
  state,
  getters,
  actions,
  mutations
}
