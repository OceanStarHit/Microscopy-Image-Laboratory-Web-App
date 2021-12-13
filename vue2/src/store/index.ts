// import { InjectionKey } from 'vue'
// import { createStore, useStore as baseUseStore, Store } from 'vuex'
import { AuthState, AuthStore } from '@/store/auth.module';

import Vue from 'vue';
import Vuex from 'vuex';
import {ViewStore} from '@/store/view.module';
import {ToolBarViewStore} from '@/store/toolBar.view.module';
import {ImageStore} from '@/store/image/image.module';

Vue.use(Vuex);

export interface State {
  auth: AuthState;
}

export default new Vuex.Store<State>({
  modules: {
    auth: AuthStore,
    view: ViewStore,
    toolBarView: ToolBarViewStore,
    image: ImageStore,
  }
});

// export interface State extends TestModel, AuthState {}
// interface storeTypes {
// }
//
// export interface State {
//   test: TestModel
//   auth: AuthState
// }
//
// export const key: InjectionKey<Store<State>> = Symbol()
//
// export const store = createStore<State>({
//   modules: {
//     test: TestStore,
//     auth: AuthStore,
//   },
// })
//
// // define your own `useStore` composition function
// export function useStore(): Store<State> {
//   return baseUseStore(key)
// }
