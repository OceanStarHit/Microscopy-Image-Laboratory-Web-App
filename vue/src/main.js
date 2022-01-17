import Vue from "vue";
import App from "./App.vue";
import vuetify from "@/plugins/vuetify";
import store from "./vuex";
import message from "./plugins/message";

Vue.config.productionTip = false;

new Vue({
  store,
  vuetify,
  render: (h) => h(App)
}).$mount("#app");
