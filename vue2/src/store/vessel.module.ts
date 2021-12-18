import {getVesselById, VESSELS, VesselWellPlateModel} from '@/utils/vessel_types';

export interface VesselBaseModel {
  id: number;
  title: string;
  type: string;
}

export interface VesselState {
  loading: boolean;
  currentVesselId: number;
  activeHole: boolean;
  activeHoles: boolean[];
}

const initialState: VesselState = {
  loading: false,
  currentVesselId: 1,
  activeHole: false,
  activeHoles: []
};

export const VesselStore = {
  namespaced: true,
  state: {
    ...initialState
  },

  getters: {
    currentVessel(state: VesselState): VesselBaseModel | null {
      /* legacy fake */
      if (state.currentVesselId) {
        return getVesselById(state.currentVesselId);
      }

      return null
    }
  },

  mutations: {

    selectVessel(state: VesselState, vesselId: number): void {
      state.currentVesselId = vesselId;
    },
    setActiveHoles(state: VesselState, activeHoles: boolean[]) {
      state.activeHoles = activeHoles;
    },
    setActiveHole(state: VesselState, activeHole: boolean) {
      state.activeHole = activeHole;
    },

    setVesselId(state: VesselState, files: any[]) {
      // TODO: use new methods
      let col = -1;
      let row = -1;

      // get column and row from name type
      files.forEach(file => {
        if (file.metaData) {
          const r = file.metaData.row;
          const c = file.metaData.col;

          row = row > r ? row : r;
          col = col > c ? col : c;
        }
      });

      // calc the current vessel id
      if (row !== -1 && col !== -1) {
        const r = row;
        const c = col;
        for (let idx = 0; idx < 6; idx++) {
          const item = VESSELS[1][idx] as VesselWellPlateModel; // TODO what is this...just fake data without any explanation
          if (r <= item.rowCount && c <= item.columnCount) {
            state.currentVesselId = item.id;
            break;
          }
        }
      } else {
        state.currentVesselId = files.length <= 2 ? files.length : 3;
      }
    }
  } // end of mutations
};
