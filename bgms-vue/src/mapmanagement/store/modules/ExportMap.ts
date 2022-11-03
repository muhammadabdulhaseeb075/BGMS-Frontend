import axios from "axios"

const state = { 
  memorialLabels: true,
  severalPopUps: false,
  severalSurnames:false,
  graveplot_list:[] ,//array for all grave labels
  mapDataExtend: undefined
}

// getters
const getters = {
}

// actions
const actions = {
  plot_lables ({commit,state}){
    let axios_call = new Promise(function(resolve, reject)
    { //asynchronous task
      axios.get('/mapmanagement/getGraveNumbers/')
      .then(response => {
        resolve(response.data)
      })
      .catch(response=>{
        console.warn('grave number not found', response);
        reject();
      })
    })
    return axios_call;
  },
  burial_number({commit,state}){
    let promise = new Promise(function(resolve,reject)
    {
      axios.get('/mapmanagement/burialNumber/')
      .then(response=>{
        resolve(response.data)
      })
      .catch(response=>{
        console.warn('burial numbers not found',response)
        reject()
      })
    })
    return promise
  }
}

// mutations
const mutations = {
  resetOptions(state){
    state.memorialLabels = true;
    state.severalPopUps = false;
    state.severalSurnames = false;
  },
  setSeveralPopUps(state, value: boolean) {
    state.severalPopUps = value;
  },
  setSeveralSurnames(state, value: boolean) {
    state.severalSurnames = value;
  },
  setMapDataExtend(state, dataExtend) {
    state.mapDataExtend = dataExtend;
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
