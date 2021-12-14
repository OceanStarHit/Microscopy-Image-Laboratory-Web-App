import Vue from 'vue';
import App from './App.vue';
import router from '@/router';
import store from '@/store';

// eslint-disable-next-line @typescript-eslint/ban-ts-ignore
// @ts-ignore
import vuetify from '@/plugins/vuetify';

import VueLodash from 'vue-lodash'
import lodash from 'lodash'
import {debounce} from 'lodash';

Vue.use(VueLodash, { name: 'custom', lodash: { debounce } })

Vue.config.productionTip = false;
// Vue.prototype.$message = message;
// import("./assets/wasm/pkg").then(module => {
//   Vue.prototype.$wasm = module;
// });

new Vue({
  store,
  // eslint-disable-next-line @typescript-eslint/ban-ts-ignore
  // @ts-ignore
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app');
