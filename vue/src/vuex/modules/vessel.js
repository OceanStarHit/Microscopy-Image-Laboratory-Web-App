import { getPosition } from "./files";

var vessel = require("../../utils/vessel-types");

// import { position } from "./image";

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
  },
  // selectVessel({ commit, state }, vesselId) {
  //   commit("selectVessel", vesselId);
  // }

  setVesselId({ commit }, data) {
    commit("setVesselId", data);
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

  setVesselId(state, data) {
    // TODO: use new methods
    let col = "";
    let row = "";

    // get column and row from name type
    data.pageData.forEach(item => {
      let p = getPosition(item.filename);
      let r = p[0];
      let c = p[1];

      row = row > r ? row : r;
      col = col > c ? col : c;
    });

    // calc the current vessel id
    if (row != "" && col != "") {
      let r = row;
      let c = col;
      for (let idx = 0; idx < 6; idx++) {
        const item = vessel.VESSELS[1][idx];
        if (r <= item.rows && c <= item.cols) {
          state.currentVesselId = item.id;
          break;
        }
      }
    } else {
      state.currentVesselId =
        data.pageData.length <= 2 ? data.pageData.length : 3;
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
