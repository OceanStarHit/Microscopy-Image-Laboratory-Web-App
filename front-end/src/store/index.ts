import Auth from '../types/authType'
import { InjectionKey } from 'vue'
import { createStore, Store } from 'vuex'
import { authStore } from '@/store/auth.module'
// import { AuthStore } from './authStore'

interface State {}

// interface storeTypes extends Auth {}
export const key: InjectionKey<Store<State>> = Symbol()

export const store = createStore<State>({
  modules: {
    auth: authStore,
  },
})

