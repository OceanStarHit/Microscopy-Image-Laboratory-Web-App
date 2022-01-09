import * as authApi from "@/api/auth";
const LOGIN_PAGE = "loginPage";
// const REGISTRATION_PAGE = "registrationPage";
const OTP_QR_PAGE = "otpQRPage";

const DEFAULT_PARAMS = {
  isLoggedIn: sessionStorage.getItem("authToken") != null,
  token: sessionStorage.getItem("authToken"),
  tokenType: sessionStorage.getItem("authTokenType"),
  authPage: sessionStorage.getItem("authToken") ? null : LOGIN_PAGE,
  user: null,
  otpSecrets: null
};

// state
const state = () => ({
  ...DEFAULT_PARAMS
});

// const getters = {
//   isLoggedIn: (state, getter) => state.isLoggedIn,
//   token: (state, getter) => state.token,
//   showRegist: (state, getter) => state.isLoggedIn,
//   showRegisterOTP_QR: (state, getter) => state.isLoggedIn
// };

const actions = {
  logIn(context, loginForm) {
    authApi
      .login(loginForm)
      .then(response => {
        if (response.status === 200) {
          context.dispatch("loggedIn", {
            token: response.data.accessToken,
            tokenType: response.data.tokenType,
            user: response.data.user
          });
          context.dispatch("setAuthPage", null);
        }
      })
      .catch(error => {
        if (error.status === 401) {
          context.dispatch("logOut");
          // this.$message({
          //   content: "Email, password or code incorrect!",
          //   type: "err"
          // }).show();
        }
      });
  },

  registerUser(context, registerForm) {
    authApi
      .register_user(registerForm)
      .then(response => {
        console.log("register works well")
        if (response.status === 201) {
          /* After successful registration user is logged in */
          context.dispatch("loggedIn", {
            token: response.data.accessToken,
            user: response.data.user
          });
          /* set the otp secrets, should be deleted from state after showing QR code */
          context.commit("setAuthSecrets", {
            secret: response.data.otpSecret,
            uri: response.data.otpUri,
            qrSVG: response.data.otpQrSvg
          });
          /* then we show the QR code so that the user may save it */
          context.commit("setAuthPage", OTP_QR_PAGE);
        }
      })
      .catch(error => {
        /* Error with registration of user */
        context.dispatch("logOut");
        console.log(error);
        // if (error.status === 401) {
        //   context.dispatch("logOut");
        //   this.$message({
        //     content: "Email, password or code incorrect!",
        //     type: "err"
        //   }).show();
        // }
      });
  },

  loggedIn({ commit }, payload) {
    /* Called once we are logged in */
    commit("setLoggedIn", {
      token: payload.token,
      tokenType: payload.tokenType
    });
    commit("setUser", payload.user);
    sessionStorage.setItem("authToken", payload.token);
    sessionStorage.setItem("authTokenType", payload.tokenType);
    // this.$message({
    //   content: "Login Success!",
    //   type: "success"
    // }).show();
  },
  logOut({ commit }) {
    /* called when logged out */

    sessionStorage.removeItem("authToken");
    sessionStorage.removeItem("authTokenType");
    commit("setLoggedOut");
    // this.$message({
    //   content: "Logged out!",
    //   type: "success"
    // }).show();
  },
  setAuthPage({ commit }, authPage) {
    commit("setAuthPage", authPage);
  }
};

const mutations = {
  setUser(state, user) {
    state.user = user;
  },
  setLoggedIn(state, payload) {
    state.isLoggedIn = true;
    state.token = payload.token;
    state.tokenType = payload.tokenType;
  },
  setLoggedOut(state) {
    state.isLoggedIn = false;
    state.token = null;
    state.tokenType = null;
    state.authPage = LOGIN_PAGE;
  },
  setAuthPage(state, page) {
    state.authPage = page;

    if (page !== OTP_QR_PAGE) {
      state.commit("auth/setAuthSecrets", null);
    }
  },
  setAuthSecrets(state, otpSecrets) {
    state.otpSecrets = otpSecrets;
  }
};

export default {
  namespaced: true,
  state,
  // getters,
  actions,
  mutations
};
