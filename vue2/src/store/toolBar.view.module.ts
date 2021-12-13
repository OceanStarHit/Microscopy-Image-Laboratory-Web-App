import { ActionContext } from 'vuex';
import authService, {
  LoggedInModel,
  LoginModel,
  RegisteredModel,
  RegisterModel
} from '@/services/authService.api';
import { AxiosResponse } from 'axios';
import { State } from '@/store/index';
import {WindowSize} from '@/services/windowSizeService';
import {AuthState} from '@/store/auth.module';
// import { State } from '@/store/index'


export interface ToolBarViewState {
  leftToolBarSelectedTab: string;
  rightToolBarSelectedTab: string;
}

const initialState: ToolBarViewState = {
  leftToolBarSelectedTab: '1',
  rightToolBarSelectedTab: '1'
};

export const ToolBarViewStore = {
  namespaced: true,
  state: {
    ...initialState
  },

  actions: {
    actionChangeLeftToolBarTab(context: ActionContext<AuthState, State>, tab: string) {
      context.commit('setLeftToolBarSelectedTab', tab)
    },

    actionChangeRightToolBarTab(context: ActionContext<AuthState, State>, tab: string) {
      context.commit('setRightToolBarSelectedTab', tab)
    },
  },

  mutations: {
    setLeftToolBarSelectedTab(state: ToolBarViewState, tab: string) {
      state.leftToolBarSelectedTab = tab;
    },
    setRightToolBarSelectedTab(state: ToolBarViewState, tab: string) {
      state.rightToolBarSelectedTab = tab;
    },
  } // end of mutations
};
