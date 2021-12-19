import { ActionContext } from 'vuex';
import { State } from '@/store/index';
import {TileModel} from '@/store/tiles.module';
import store from '@/store/index';

export interface TilePositionDialogViewState {
  selectedDefaultTile: TileModel | null;
  progressBarPercentage: number;
  isLoading: boolean; /* true if we are waiting for the backend to respond */
  backgroundText: string;
}

const initialState: TilePositionDialogViewState = {
  selectedDefaultTile: null,
  progressBarPercentage: 0,
  isLoading: false,
  backgroundText: 'Drag and drop files or a folder',
};

export const TilePositionDialogViewStore = {
  namespaced: true,
  state: {
    ...initialState
  },

  actions: {

    // changeAuthPage(context: ActionContext<AuthState, State>, authPage: AuthPageEnum) {
    //   context.commit('setAuthPage', authPage);
    // },

  }, // END OF ACTIONS

  mutations: {


    setIsLoading(state: TilePositionDialogViewState, isLoading: boolean) {
      state.isLoading = isLoading;
      state.backgroundText = state.isLoading ? 'Loading...' : 'Drag and drop files or a folder'
    },

    setSelectedDefaultTile(state: TilePositionDialogViewState, tile: TileModel | null = null) {
      /* no tiles so doesnt matter if tile was given, we set the default to null, same is true if given tile is null */
      if(store.state.tiles.tiles.length === 0 || tile == null) {
        state.selectedDefaultTile = null;
      } else if (tile) {
        /* use given tile */
        state.selectedDefaultTile = tile;
      }
    },

  } // end of mutations
};
