var vessel = require("../../utils/vessel-types");

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
    let column = "";
    let row = "";

    // get column and row from name type
    data.forEach(val => {
      const filename = val.filename;
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      if (type && type.length > 6) {
        row = row > type[5] ? row : type[5];
        column = column > type[6] ? column : type[6];
      }
    });

    // calc the current vessel id
    if (column != "" && row != "") {
      let rows = row.charCodeAt(0) - "A".charCodeAt(0) + 1;
      let cols = parseInt(column);
      for (let idx = 0; idx < 6; idx++) {
        const item = vessel.VESSELS[1][idx];
        if (rows <= item.rows && cols <= item.cols) {
          state.currentVesselId = item.id;
          break;
        }
      }
    } else {
      state.currentVesselId = data.length <= 2 ? data.length : 3;
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
