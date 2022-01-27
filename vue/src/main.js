import Vue from "vue";
import App from "./App.vue";


// const vuetify = require("@/plugins/vuetify");
// const store = require("@/vuex");

import vuetify from "@/plugins/vuetify";
import store from "./vuex";
import message from "./plugins/message";
import VueNumericInput from 'vue-numeric-input';
// require("log-timestamp");

Vue.config.productionTip = false;
// Vue.prototype.$message = message;
// import("./assets/wasm/pkg").then(module => {
//   Vue.prototype.$wasm = module;
// });

new Vue({
  store,
  vuetify,
  VueNumericInput,
  render: (h) => h(App)
}).$mount("#app");
