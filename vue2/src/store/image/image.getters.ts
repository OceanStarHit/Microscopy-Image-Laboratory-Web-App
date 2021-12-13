import {ImageState} from '@/store/image/image.module';
import {filteredByParameters} from '@/store/image/image.helpers';

export default {
    imageData: (state: ImageState) => {
        return {
            url: state.imageData,
            isNew: state.isNew
        };
    },
    currentPageData: (state: ImageState) => state.allData[state.currentPageIndex - 1],
    newRes: (state: ImageState) => state.newRes,
    // newData: (state: ImageState) => state.newData,
    imageId: (state: ImageState) => state.imageId,
    imageParams: (state: ImageState) => state.parameters,
    curPageIdx: (state: ImageState) => state.currentPageIndex,
    allData: (state: ImageState) => state.allData,
    currentPageInfo: (state: ImageState) => {
        return {
            pageData: state.allData[state.currentPageIndex - 1],
            dataIndex: state.allIndice[state.currentPageIndex - 1],
            dataIndexes: state.allIndices[state.currentPageIndex - 1]
        };
    },
    selectedImagesAtRowCol: (state: ImageState) => {
        const pageIdx = state.currentPageIndex;
        const pageData = state.allData;
        if (pageIdx > 0 && pageData.length > 0) {
            const idxes = state.allIndices[state.currentPageIndex - 1];
            const data = state.allData[state.currentPageIndex - 1];

            if (idxes.length > 0) {
                return idxes.map(idx => data.get(idx));
            }
        }
        return [];
    },
    metaData: (state: ImageState) => {
        if (state.currentPageIndex > 0 && state.allData.length > 0) {
            const idxes = state.allIndices[state.currentPageIndex - 1];
            const data = state.allData[state.currentPageIndex - 1];

            if (idxes.length > 0) {
                const rs = idxes.map(idx => data.get(idx));
                const images = filteredByParameters(state.parameters, rs);
                if (images.length > 0) return images[0].metadata.imageData;
            }
        }
        return null;
    },
    objectiveX: (state: ImageState) => {
        let X = 0;
        if (!state.imageInfo || !state.imageInfo.objective) return X;

        const cm = state.imageInfo.objective.calibratedMagnification;
        const nm = state.imageInfo.objective.nominalMagnification;

        if (cm && nm) {
            X = cm > nm ? cm : nm;
        } else if (cm && !nm) {
            X = cm;
        } else if (!cm && nm) {
            X = nm;
        }

        return Math.ceil(X * 100) / 100;
    },
    channelInfo: (state: ImageState) => {
        if (state.imageInfo) {
            return {
                channels: state.imageInfo.channels
            };
        } else {
            return {
                channels: []
            };
        }
    },
    seriesCount: (state: ImageState) => {
        if (state.coreMetadata) {
            return state.coreMetadata.seriesCount;
        }
        return 0;
    },
    sizeZ: (state: ImageState) => {
        if (state.imageInfo && state.imageInfo.pixels) {
            return state.imageInfo.pixels.sizeZ;
        }
        return 1;
    },
    sizeT: (state: ImageState) => {
        if (state.imageInfo && state.imageInfo.pixels) {
            return state.imageInfo.pixels.sizeT;
        }
        return 1;
    }
}
