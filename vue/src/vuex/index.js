import Vue from "vue";
import Vuex from "vuex";
import { createLogger } from "vuex";
import image from "./modules/image";
import vessel from "./modules/vessel";

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== "production";

export default new Vuex.Store({
    modules: {
        image,
        vessel
    },
    strict: debug,
    plugins: debug ? [createLogger()] : []
});
