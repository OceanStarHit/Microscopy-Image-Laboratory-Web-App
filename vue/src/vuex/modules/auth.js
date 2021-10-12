const DEFAULT_PARAMS = {
  logind: sessionStorage.getItem("logind")
    ? sessionStorage.getItem("logind")
    : false,
  token: "aa",
  showRegist: false
};

// state
const state = () => ({
  ...DEFAULT_PARAMS
});

const getters = {
  logind: (state, getter) => state.logind,
  token: (state, getter) => state.token,
  showRegist: (state, getter) => state.logind
};

const actions = {
  setLogind({ commit }, data) {
    commit("setLogind", data);
  },
  setShowRegist({ commit }, data) {
    commit("changeShowRegist", data);
  }
};

const mutations = {
  setLogind(state, data) {
    state.logind = data.logind;
    state.token = data.token;
  },
  changeShowRegist(state, data) {
    state.showRegist = data.showRegist;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
