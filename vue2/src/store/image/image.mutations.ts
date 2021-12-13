import {DEFAULT_IMAGE_PARAMS, ImageParameters, ImageState} from '@/store/image/image.module';
import {ActionContext} from 'vuex';
import {State} from '@/store';
import {LoginModel} from '@/services/authService.api';
import {changeParameters} from '@/store/image/image.helpers';

export default {
    setIsLoading(state: ImageState, isLoading: boolean) {
        state.isLoading = isLoading;
    },

    incrementLoadingCount(state: ImageState) {
        state.loadingCount++;
        state.loadingCountMax = state.loadingCount;
    },

    decreaseLoadingCount(state: ImageState) {
        state.loadingCount--;
        if (state.loadingCount == 0) {
            state.loadingCountMax = state.loadingCount;
        }
    },
    setImageResponse(state: ImageState, payload: ImageState) {
        state.coreMetadata = payload.coreMetadata;
        state.originMetadata = payload.originMetadata;
        state.imageId = payload.imageId;
        state.imageInfo = payload.imageInfo;
        state.plateId = payload.plateId;
        state.wellId = payload.wellId;
        state.positionX = payload.positionX;
        state.positionY = payload.positionY;
        state.plates = payload.plates;
        state.wellSamples = payload.wellSamples;
    },

    setNewResponse(state: ImageState, newRes:any) {
        state.newRes = newRes;
    },

    setImageData(state: ImageState, imageData: any) {
        state.imageData = imageData;
        state.originData = imageData;
        state.isNew = true;

        state.parameters = Object.assign({}, state.parameters, DEFAULT_IMAGE_PARAMS);
    },

    changeCurrentPage(state: ImageState, currentPageIndex: number) {
        state.currentPageIndex = currentPageIndex;
    },

    changeCurrentData(state: ImageState, payload: any) {
        state.allIndice = state.allIndice.map((val, index) =>
            index == state.currentPageIndex - 1 ? payload : val
        );
    },
    changeCurrentMultiData(state: ImageState, indices: number[]) {
        state.allIndices = state.allIndices.map((prevIndices, idx) =>
            idx == state.currentPageIndex - 1 ? indices : prevIndices
        );
    },
    addData(state: ImageState, payload: any) {
        const files = payload.files;

        if (files.size == 0) return;

        const append = payload.appendToCurrentPage;

        if (append) {
            // state.newData.push.apply(state.newData, files);
            state.allData = state.allData.map((oldData, idx) => {
                if (idx == state.currentPageIndex - 1) {
                    return new Map([...oldData, ...files]);
                } else {
                    return oldData;
                }
            });
        } else {
            // state.newData = files;
            state.allData.push(files);
            const minIdx = Math.min(...files.keys());
            state.allIndice.push(minIdx);
            state.allIndices.push([minIdx]);
            state.currentPageIndex = state.allData.length;
        }
    },
    removeData(state: ImageState, index: number) {
        state.allData.splice(index, 1);
    },
    updateAllData(state: ImageState, allData: any) {
        state.allData = allData;
    },
    changeImageData(state: ImageState, payload: ImageState) {
        state.imageData = payload.imageData;
        state.originData = payload.imageData;
        state.isNew = false;

        (state.coreMetadata = payload.coreMetadata),
        (state.imageId = payload.imageId),
        (state.imageInfo = payload.imageInfo),
        (state.plateId = payload.plateId),
        (state.wellId = payload.wellId),
        (state.positionX = payload.positionX),
        (state.positionY = payload.positionY);

        state.parameters = Object.assign({}, state.parameters, DEFAULT_IMAGE_PARAMS);
    },
    changeParameterData(state: ImageState, params: ImageParameters) {
        // state.imageData = payload.imageData;
        // state.originData = payload.imageData;
        // state.isNew = false;

        state.parameters = Object.assign({}, state.parameters, {
            Z: params.Z,
            T: params.T,
            C: params.C,
            brightness: params.brightness,
            contrast: params.contrast,
            gamma: params.gamma,
            objective: params.objective
        });
    },

    adjustImage(state: ImageState, payload: ImageState) {
        state.imageData = payload.imageData;
        state.parameters = Object.assign({}, state.parameters, {
            brightness: payload.parameters.brightness,
            contrast: payload.parameters.contrast,
            gamma: payload.parameters.gamma
        });
        state.isNew = false;
    },

    resetAdjust(state: ImageState) {
        state.imageData = state.originData;
        state.parameters = Object.assign({}, state.parameters, {
            brightness: 0,
            contrast: 0,
            gamma: 0
        });
        state.isNew = false;
    }
}
