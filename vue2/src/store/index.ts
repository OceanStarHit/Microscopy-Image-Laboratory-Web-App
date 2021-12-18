// import { InjectionKey } from 'vue'
// import { createStore, useStore as baseUseStore, Store } from 'vuex'
import { AuthState, AuthStore } from '@/store/auth.module';

import Vue from 'vue';
import Vuex, {Store} from 'vuex';
import {ViewState, ViewStore} from '@/store/view.module';
import {ToolBarViewState, ToolBarViewStore} from '@/store/toolBar.view.module';
import {ImageState, ImageStore} from '@/store/image/image.module';
import {VesselState, VesselStore} from '@/store/vessel.module';
import {TileState, TileStore} from '@/store/tiles.module';

Vue.use(Vuex);

export interface State {
  auth: AuthState;
  view: ViewState;
  toolBarView: ToolBarViewState;
  image: ImageState;
  vessel: VesselState;
  tiles: TileState;
}

export default new Vuex.Store<State>({
  modules: {
    auth: AuthStore,
    view: ViewStore,
    toolBarView: ToolBarViewStore,
    image: ImageStore,
    vessel: VesselStore,
    tiles: TileStore,
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
