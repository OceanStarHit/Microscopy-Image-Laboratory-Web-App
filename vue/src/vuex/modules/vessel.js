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
        let col = "";
        let row = "";

        // get column and row from name type
        data.pageData.forEach(item => {
            const type = item.filename.match(
                /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
            );
            if (type) {
                row = row > type[5] ? row : type[5];
                col = col > type[6] ? col : type[6];
            }
        });

        // calc the current vessel id
        if (row != "" && col != "") {
            let r = row.charCodeAt(0) - "A".charCodeAt(0) + 1;
            let c = parseInt(col);
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
