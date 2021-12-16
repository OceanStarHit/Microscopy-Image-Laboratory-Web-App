const vessel = require('../../utils/vessel-types');

// import { position } from "./image";

/* eslint-disable no-unused-vars */
const DEFAULT_PARAMS = {
  loading: false,

  currentVessel: 1,
  activeHole: false,
  activeHoles: []
};

// state
const state = () => ({
  ...DEFAULT_PARAMS
});

const getters = {
  getSelectedVessel()
}

// actions
const actions = {
  selectVessel({ commit }, vesselId) {
    commit('selectVessel', vesselId);
  },
  setActiveHoles({ commit }, activeHoles) {
    commit('setActiveHoles', activeHoles);
  },
  setActiveHole({ commit }, activeHole) {
    commit('setActiveHole', activeHole);
  },
  // selectVessel({ commit, state }, vesselId) {
  //   commit("selectVessel", vesselId);
  // }

  setVesselId({ commit }, data) {
    commit('setVesselId', data);
  }
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
  },

  setVesselId(state, files) {
    // TODO: use new methods
    let col = -1;
    let row = -1;

    // get column and row from name type
    files.forEach(file => {
      if (file.metaData) {
        const r = file.metaData.row;
        const c = file.metaData.col;

        row = row > r ? row : r;
        col = col > c ? col : c;
      }
    });

    // calc the current vessel id
    if (row !== -1 && col !== -1) {
      const r = row;
      const c = col;
      for (let idx = 0; idx < 6; idx++) {
        const item = vessel.VESSELS[1][idx];
        if (r <= item.rows && c <= item.cols) {
          state.currentVesselId = item.id;
          break;
        }
      }
    } else {
      state.currentVesselId = files.length <= 2 ? files.length : 3;
    }
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
