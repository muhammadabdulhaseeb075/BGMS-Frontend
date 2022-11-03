const state = {
  photos: [],
  inscriptions: [],
  inspections: [],
  memorialLayers: [],
  unsavedInscription: false,
  unsavedDetails: false,
  unsavedInspection: false,
  offlineController: null,
  photoCollapsed: false,
  detailCollapsed: false,
  inspectionCollapsed: true,
  inscriptionCollapsed: true,
  materials: undefined,
}

// getters
const getters = {
  narrowSidebar: state => {
    if (state.inspectionCollapsed && state.inscriptionCollapsed)
      return true;
    else
      return false;
  },
  unsavedMemorialCaptureChanges: state => {
    return state.unsavedInscription
      || state.unsavedDetails
      || state.unsavedInspection
  }
}

// actions
const actions = {
}

// mutations
const mutations = {
  resetMemorialCaptureSidebar (state) {
    state.photos = [];
    state.inscriptions = [];
    state.inspections = [];
    state.unsavedInscription = false;
    state.unsavedDetails = false;
    state.unsavedInspection = false;
  },
  resetPhotos (state) {
    state.photos = [];
  },
  addPhoto(state, photo) {
    state.photos.push(photo);
  },
  removePhoto(state, position) {
    state.photos.splice(position, 1);
  },
  addInscription(state, inscription) {
    state.inscriptions.unshift(inscription);
  },
  addInspection(state, inspection) {
    state.inspections.unshift(inspection);
  },
  removeInscription(state, inscription) {
    const index = state.inscriptions.indexOf(inscription);

    if (index !== -1) {
        state.inscriptions.splice(index, 1);
    }
  },
  toggleUnsavedInscription (state, value) {
    state.unsavedInscription = value;
  },
  toggleUnsavedDetails (state, value) {
    state.unsavedDetails = value;
  },
  toggleUnsavedInspection (state, value) {
    state.unsavedInspection = value;
  },
  commitOfflineController (state, value) {
    state.offlineController = value;
  },
  setPhotoCollapsed (state, value) {
    state.photoCollapsed = value;
  },
  setDetailCollapsed (state, value) {
    state.detailCollapsed = value;
  },
  setInspectionCollapsed (state, value) {
    state.inspectionCollapsed = value;
  },
  setInscriptionCollapsed (state, value) {
    state.inscriptionCollapsed = value;
  },
  populateMaterials (state, materials) {
    state.materials = materials;
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
