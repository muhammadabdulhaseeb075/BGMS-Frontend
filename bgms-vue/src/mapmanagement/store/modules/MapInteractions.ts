import store from '@/mapmanagement/store/index';
import MapInteraction from '@/mapmanagement/components/Map/models/Interaction';

// add jquery markers to be used in angularjs
(window as any).jQuery(document).on("pushInteraction", (e,interaction) => {
  store.commit('pushInteraction', interaction);
});
(window as any).jQuery(document).on("removeInteractionsByGroup", (e,interactionGroup) => {
  store.commit('removeInteractionsByGroup', interactionGroup);
});

function getInteractionPositionInStack(key, value) {

  let positions = [-1];
  let i = 0;

  store.getters.getInteractions.forEach((interaction, index) => {
    if(interaction[key] === value)
      positions[i++] = index;
  });

  return positions;
}

const state = {
  interactions: []
}

// getters
const getters = {
  getInteractions: (state) => {
    return state.interactions;
  },
}

// actions
const actions = {
}

// mutations
const mutations = {

  pushInteraction(state, interaction) {

    if (getInteractionPositionInStack('type', interaction.type)[0]===-1) {
      let newInteraction = new MapInteraction(interaction);
      state.interactions.push(newInteraction);

      newInteraction.addInteractionToMap();
    }
    else {
      console.log('interaction cannot be added because interaction of type '+interaction.type+' already exists in group '+interaction.group);
      console.log(state.events);
    }
  },

  removeInteractionByType(state, interactionType){
    const positions = getInteractionPositionInStack('type', interactionType);
    if(positions[0] != -1) {
      state.interactions[positions[0]].removeInteractionFromMap();
      state.interactions.splice(positions[0], 1);
    }
  },

  removeInteractionsByGroup(state, interactionGroup){
    const positions = getInteractionPositionInStack('group', interactionGroup);
    if(positions[0] != -1) {
      for(let i=positions.length-1; i>=0; i--){
        state.interactions[positions[i]].removeInteractionFromMap();
        state.interactions.splice(positions[i], 1);
      }
    }
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};

(window as any).MapInteractions = state.interactions;