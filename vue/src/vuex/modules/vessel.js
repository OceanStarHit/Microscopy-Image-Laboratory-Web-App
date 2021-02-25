/* eslint-disable no-unused-vars */
const DEFAULT_PARAMS = {
  loading: false,

  currentVesselId: 1,
  activeHole: false,
  activeHoles: []
};

// state
const state = () => ({
  ...DEFAULT_PARAMS
});

// getters
const getters = {
  currentVesselId: (state, getters) => state.currentVesselId,
  activeHoles: (state, getters) => state.activeHoles,
  activeHole: (state, getters) => state.activeHole
};

// actions
const actions = {
  selectVessel({ commit }, vesselId) {
    commit("selectVessel", vesselId);
  },
  setActiveHoles({ commit }, activeHoles) {
    commit("setActiveHoles", activeHoles);
  },
  setActiveHole({ commit }, activeHole) {
    commit("setActiveHole", activeHole);
  }
  // selectVessel({ commit, state }, vesselId) {
  //   commit("selectVessel", vesselId);
  // }
};

// mutations
const mutations = {
  selectVessel(state, vesselId) {
    state.currentVesselId = vesselId;
  },
  setActiveHoles(state, activeHoles) {
    state.activeHoles = activeHoles;
  },
  setActiveHole(state, activeHole) {
    state.activeHole = activeHole;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
