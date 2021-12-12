import { InjectionKey } from 'vue'
import { createStore, useStore as baseUseStore, Store } from 'vuex'
import TestModel, { TestStore } from './test.module'
import { AuthState, AuthStore } from '@/store/auth.module'

// export interface State extends TestModel, AuthState {}
// interface storeTypes {
// }

export interface State {
  test: TestModel
  auth: AuthState
}

export const key: InjectionKey<Store<State>> = Symbol()

export const store = createStore<State>({
  modules: {
    test: TestStore,
    auth: AuthStore,
  },
})

// define your own `useStore` composition function
export function useStore(): Store<State> {
  return baseUseStore(key)
}
