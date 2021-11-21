const DEFAULT_PARAMS = {
  isLoggedIn: sessionStorage.getItem("isLoggedIn")
    ? sessionStorage.getItem("isLoggedIn")
    : false,
  token: "aa",
  showRegist: false
};

// state
const state = () => ({
  ...DEFAULT_PARAMS
});

const getters = {
  isLoggedIn: (state, getter) => state.isLoggedIn,
  token: (state, getter) => state.token,
  showRegist: (state, getter) => state.isLoggedIn
};

const actions = {
  setIsLoggedIn({ commit }, data) {
    commit("setIsLoggedIn", data);
  },
  setShowRegist({ commit }, data) {
    commit("changeShowRegist", data);
  }
};

const mutations = {
  setIsLoggedIn(state, data) {
    state.isLoggedIn = data.isLoggedIn;
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
