import {ActionContext} from 'vuex';
import {State} from '@/store/index';
import imageServiceApi, {ImageChannelModel, TileApiModel} from '@/services/imageService.api';
import {AxiosResponse} from 'axios';
import {TilePositionDialogViewStore} from '@/store/tilePositionDialog.view.module';
/**
 * Tile Store
 *
 * Tiles are individual images that when stitched together make up a complete image.
 */


export interface NamePatternBase {
  start: number;
  finish: number;
}

export interface NamePatterns {
  totalLength?: number;

  series?: NamePatternBase;

  row?: NamePatternBase;
  col?: NamePatternBase;

  field?: NamePatternBase;
  channel?: NamePatternBase;
  z?: NamePatternBase;
  time?: NamePatternBase;
}

export interface LensObjectiveModel {
  id: number;
  m: number; // todo what is m?
  isActive: boolean;
}

export interface TileModel extends TileApiModel {
  /** this is what is stored in the state, same as the apiModel but also includes the file so that we can view it */
  file: File
}

export interface TileSelection {
  rowIndex?: number;
  columnIndex?: number;
  zIndex?: number;
  timeIndex?: number;
  fieldIndex?: number;
  lensObjectiveM?: number;  // only M value
  channels?: ImageChannelModel[];
}

export interface TileState {
  tiles: TileModel[],
  tilesUpdatedCount: number,
  namePatterns: NamePatterns,

  selection: TileSelection
}

const initialState: TileState = {
  tiles: [] as TileModel[],
  tilesUpdatedCount: 0,
  namePatterns: {} as NamePatterns,

  selection: {} as TileSelection,
};

export const TileStore = {
  namespaced: true,
  state: {
    ...initialState
  },

  modules: {
    view: TilePositionDialogViewStore,
  },

  actions: {
    uploadTileFiles(context: ActionContext<TileState, State>, files: File[]): Promise<AxiosResponse<any> | void> {
      return imageServiceApi.uploadTiles(files).then((response: AxiosResponse<TileApiModel[]>) => {
        const tiles: TileApiModel[] = response.data;
          context.commit('addTiles', tiles);
        })
    },

    deleteAllTiles(context: ActionContext<TileState, State>, data: string): Promise<AxiosResponse<any> | void> {
      // return imageServiceApi.deleteTiles(context.state.tiles).then(response => {
      return imageServiceApi.deleteTiles([]).then(response => {
        console.log(response);
      })
    }
  },

  getters: {

    getTilesAtSelection(state: TileState): TileModel[] {
      return state.tiles.filter(tile => {
        if (state.selection.rowIndex && tile.rowIndex !== state.selection.rowIndex) {
          return false;
        }
        if (state.selection.columnIndex && tile.columnIndex !== state.selection.columnIndex) {
          return false;
        }
        if (state.selection.zIndex && tile.zIndex !== state.selection.zIndex) {
          return false;
        }
        if (state.selection.timeIndex && tile.timeIndex !== state.selection.timeIndex) {
          return false;
        }
        if (state.selection.fieldIndex && tile.fieldIndex !== state.selection.fieldIndex) {
          return false;
        }
        if (state.selection.lensObjectiveM && tile.lensObjectiveM !== state.selection.lensObjectiveM) { // todo only uses m, should change?
          return false;
        }
        if (state.selection.channels && tile.channel && !state.selection.channels.includes(tile.channel)) {
          return false;
        }

        return true;
      })
    },

    getTilesAtRowAndColumnSelection(state: TileState): TileModel[] {
      /**
       * Returns tiles selected only by row and column, ignores all other selections
       */

      return state.tiles.filter(tile => {
        if (state.selection.rowIndex && tile.rowIndex !== state.selection.rowIndex) {
          return false;
        }
        if (state.selection.columnIndex && tile.columnIndex !== state.selection.columnIndex) {
          return false;
        }

        return true;
      })
    },

    getTilesSortedByFileName(state: TileState): TileModel[] {
      return state.tiles.sort((tileA, tileB) => {
        /**
         * If filenames are the same length then sort alphabetically
         * otherwise sort by filename lenght.
         *
         * TODO. does this actually make sense? this is taken from the legacy store.
         */
        if (tileA.fileName.length === tileB.fileName.length) {
          return tileA.fileName.localeCompare(tileB.fileName) // alphabetic comparison
        } else {
          return tileA.fileName.length - tileB.fileName.length;
        }
      })
    },

    getAllChannels(state: TileState): ImageChannelModel[] {
      /**
       * Returns an array of all the available channels in the array of tiles.
       */
      const channels: ImageChannelModel[] = [];

      state.tiles.forEach(tile => {
        if (tile.channel) {
          channels.push(tile.channel);
        }
      })

      return [...new Set(channels)] // no duplicates
    },

    getAllLensObjectives(state: TileState): number[] {
      /**
       * Returns an array of all the available lens objectives in the array of tiles.
       */
      const lensObjectives: number[] = [];

      state.tiles.forEach(tile => {
        if (tile.lensObjectiveM) {
          lensObjectives.push(tile.lensObjectiveM);
        }
      })

      return [...new Set(lensObjectives)] // no duplicates
    },

    getMaxZIndex(state: TileState): number {
      const zValues: number[] = [];
      state.tiles.forEach(tile => {
        if (tile.zIndex) {
          zValues.push(tile.zIndex);
        }
      })

      if (zValues.length > 0) {
        return Math.max(...zValues);
      } else {
        return 0;
      }
    },

    getMinZIndex(state: TileState): number {
      const zValues: number[] = [];
      state.tiles.forEach(tile => {
        if (tile.zIndex) {
          zValues.push(tile.zIndex);
        }
      })
      if (zValues.length > 0) {
        return Math.min(...zValues);
      } else {
        return 0;
      }
    },

    getMaxTimeIndex(state: TileState): number {
      const timeValues: number[] = [];
      state.tiles.forEach(tile => {
        if (tile.timeIndex) {
          timeValues.push(tile.timeIndex);
        }
      })

      if (timeValues.length > 0) {
        return Math.max(...timeValues);
      } else {
        return 0;
      }
    },

    getMinTimeIndex(state: TileState): number {
      const timeValues: number[] = [];
      state.tiles.forEach(tile => {
        if (tile.timeIndex) {
          timeValues.push(tile.timeIndex);
        }
      })

      if (timeValues.length > 0) {
        return Math.min(...timeValues);
      } else {
        return 0;
      }
    },

  }, // END OF GETTERS

  mutations: {

    addTiles(state: TileState, tiles: TileModel[]): void {
      state.tiles = state.tiles.concat(tiles);
    },

    addSelection(state: TileState, selection: Partial<TileSelection>): void {
      /**
       * Given a selection the selection is added and alterered only for the keys given, other keys are not updated.
       * If the selection is meant to update the entire selection, then the selection should be reset first.
       */
      for (const [k, v] of Object.entries(selection)) {
        // eslint-disable-next-line @typescript-eslint/ban-ts-ignore
        // @ts-ignore
        state.selection[k] = v;
      }
    },

    resetSelection(state: TileState): void {
      state.selection = {};
    },

    addNamePattern(state: TileState, namePatterns: Partial<NamePatterns>): void {
      for (const [k, v] of Object.entries(namePatterns)) {
        // eslint-disable-next-line @typescript-eslint/ban-ts-ignore
        // @ts-ignore
        state.namePatterns[k] = v;
      }
    },

    resetNamePattern(state: TileState): void {
      state.namePatterns = {};
    },


  } // end of mutations
};
