import getters from './image.getters';
import actions from './image.actions';
import mutations from './image.mutations';

export interface ImageParameters {
  Z: number;
  T: number;
  C: number;
  brightness: number;
  contrast: number;
  gamma: number;
  objective: number;
}

export interface ImageObjectiveModel {
  calibratedMagnification: number;
  nominalMagnification: number;
}

export interface ImageInfo {

}


export interface ImageState {

  isLoading: boolean;
  loadingCount: number;
  loadingCountMax: number;

  coreMetadata: any;
  originMetadata: any;
  imageId: number;
  imageInfo: any;
  imageData: any;
  plateId: number;
  wellId: number;
  positionX: number;
  positionY: number;
  plates: any[];
  wellSamples: any[];

  // allData: {[key: number]: any}[]; /* I have no idea what this list of objects is */
  allData: Map<number, any>[]; /* I have no idea what this list of objects is, it is used in the ViewTab */
  allDataMap: any;
  allIndice: any[];
  allIndices: any[][];
  newRes: any[];
  // newData: [],

  currentPageIndex: number;

  originData: any;
  parameters: ImageParameters;
  isNew: boolean;
}

export const DEFAULT_IMAGE_PARAMS: ImageParameters = {
  Z: 1,
  T: 1,
  C: 0,
  brightness: 0,
  contrast: 0,
  gamma: 0,
  objective: 4
};

const initialState: ImageState = {
  isLoading: false,
  loadingCount: 0,
  loadingCountMax: 0,

  coreMetadata: null,
  originMetadata: null,
  imageId: -1,
  imageInfo: null,
  imageData: null,
  plateId: -1,
  wellId: -1,
  positionX: -1,
  positionY: -1,
  plates: [],
  wellSamples: [],

  allData: [],
  allDataMap: {},
  allIndice: [],
  allIndices: [],
  newRes: [],
  // newData: [],

  currentPageIndex: -1,

  originData: null,
  parameters: DEFAULT_IMAGE_PARAMS,
  isNew: false
};

export const ImageStore = {
  namespaced: true,
  state: {
    ...initialState
  },
  getters,
  actions,
  mutations,
};
