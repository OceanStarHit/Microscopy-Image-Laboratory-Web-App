import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import store from "./vuex";

require("log-timestamp");

Vue.config.productionTip = false;

import("./assets/wasm/pkg").then(module => {
  Vue.prototype.$wasm = module;
  new Vue({
    store,
    vuetify,
    render: h => h(App)
  }).$mount("#app");  
});

