import { ActionContext } from 'vuex';

import { State } from '@/store/index';
import {WindowSize} from '@/services/windowSizeService';


export interface ViewState {
  windowSize: WindowSize
}

const initialState: ViewState = {
  windowSize: {
    heightPx: window.innerHeight,
    widthPx: window.innerWidth
  }
};

export const ViewStore = {
  namespaced: true,
  state: {
    ...initialState
  },

  mutations: {
    setWindowSize(state: ViewState, windowSize: WindowSize) {
      state.windowSize = windowSize;
    }
  } // end of mutations
};
