import Vue from "vue";
import Vuex from "vuex";
import { createLogger } from "vuex";
import files from "./modules/files";
import image from "./modules/image";
import vessel from "./modules/vessel";
import VueFlashMessage from "vue-flash-message";

Vue.use(Vuex);
Vue.use(VueFlashMessage);

const debug = process.env.NODE_ENV !== "production";

export default new Vuex.Store({
  modules: {
    files,
    image,
    vessel
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
});
