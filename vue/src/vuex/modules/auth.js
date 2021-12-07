import * as API from "@/api/auth";

const LOGIN_PAGE = "loginPage";
const REGISTRATION_PAGE = "registrationPage";
const OTP_QR_PAGE = "otpQRPage";

const DEFAULT_PARAMS = {
  isLoggedIn: sessionStorage.getItem("authToken")
    ? sessionStorage.getItem("authToken")
    : false,
  token: sessionStorage.getItem("authToken"),
  authPage: sessionStorage.getItem("authToken")
    ? null
    : LOGIN_PAGE,
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
    API.login(loginForm)
      .then(response => {
        if (response.status === 200) {
          context.dispatch("loggedIn", {
            token: response.data.access_token,
            user: response.data.user
          });
          context.dispatch("setAuthPage", null);
        }
      })
      .catch(error => {
        if (error.status === 401) {
          context.dispatch("logOut");
          this.$message({
            content: "Email, password or code incorrect!",
            type: "err"
          }).show();
        }
      });
  },

  loggedIn({ commit }, payload) {
    /* Called once we are logged in */
    commit("setLoggedIn", payload.token);
    commit("setUser", payload.user);
    sessionStorage.setItem("authToken", token);
    this.$message({
      content: "Login Success!",
      type: "success"
    }).show();
  },
  logOut({ commit }) {
    /* called when logged out */
    commit("setLoggedOut");
    sessionStorage.removeItem("authToken");
    this.$message({
      content: "Logged out!",
      type: "success"
    }).show();
  },
  setAuthPage(context, authPage) {
    context.commit("setAuthPage", authPage);
  },

  registerUser(context, registerForm) {
    API.register_user(registerForm)
      .then(response => {
        if (response.status === 200) {
          /* After successful registration user is logged in */
          context.dispatch("loggedIn", {
            token: response.data.access_token,
            user: response.data.user
          });
          /* set the otp secrets, should be deleted from state after showing QR code */
          context.dispatch("setAuthSecrets", {
            otpSecrets: {
              secret: response.data.otp_secret,
              uri: response.data.otp_uri,
              qr_svg: response.data.otp_uri_qr
            }
          });
          /* then we show the QR code so that the user may save it */
          context.dispatch("setAuthPage", OTP_QR_PAGE);
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

};

const mutations = {
  setUser(state, user) {
    state.user = user;
  },
  setLoggedIn(state, token) {
    state.isLoggedIn = true;
    state.token = token;
  },
  setLoggedOut(state) {
    state.isLoggedIn = false;
    state.token = null;
    state.authPage = LOGIN_PAGE;
  },
  setAuthPage(state, page) {
    state.authPage = page;
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
