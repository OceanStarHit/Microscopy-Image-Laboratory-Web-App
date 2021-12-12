import { useStore, State as _State } from '@/store'
import { Store } from 'vuex'

// https://stackoverflow.com/questions/64412243/vue-js-3-and-typescript-property-store-does-not-exist-on-type-componentpub

declare module '@vue/runtime-core' {
  // Declare your own store states.
  interface State extends _State {}

  interface ComponentCustomProperties {
    $store: Store<State>
  }
}
