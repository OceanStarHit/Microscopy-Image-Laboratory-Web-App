/* eslint-disable no-unused-vars */
import * as API from "../../api";

const DEFAULT_PARAMS = {
    Z: 1,
    T: 1,
    C: 0,
    brightness: 0,
    contrast: 0,
    gamma: 0
};

// state
const state = () => ({
    loading: false,

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
    allIndice: [],
    newRes: [],
    newData: [],

    curPageIdx: -1,

    originData: null,
    parameters: DEFAULT_PARAMS,
    isNew: false
});

// getters
const getters = {
    imageData: (state, getters) => {
        return {
            url: state.imageData,
            isNew: state.isNew
        };
    },
    currentPageData: (state, getters) => state.allData[state.curPageIdx - 1],
    newRes: (state, getters) => state.newRes,
    newData: (state, getters) => state.newData,
    imageId: (state, getters) => state.imageId,
    imageParams: (state, getters) => state.parameters,
    currentPageInfo: (state, getters) => {
        return {
            pageData: state.allData[state.curPageIdx - 1],
            dataIndex: state.allIndice[state.curPageIdx - 1]
        };
    },
    metaData: (state, getters) =>
        state.curPageIdx == -1
            ? null
            : state.allData[state.curPageIdx - 1][
                state.allIndice[state.curPageIdx - 1]
            ].metadata.imageData,
    objectiveX: (state, getters) => {
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
    channelInfo: (state, getters) => {
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
    seriesCount: (state, getters) => {
        if (state.coreMetadata) {
            return state.coreMetadata.seriesCount;
        }
        return 0;
    },
    sizeZ: (state, getters) => {
        if (state.imageInfo && state.imageInfo.pixels) {
            return state.imageInfo.pixels.sizeZ;
        }
        return 1;
    },
    sizeT: (state, getters) => {
        if (state.imageInfo && state.imageInfo.pixels) {
            return state.imageInfo.pixels.sizeT;
        }
        return 1;
    }
};

// actions
const actions = {
    setImage({ commit, state }, formData) {
        if (state.loading) return;

        commit("setLoading", true);

        API.setImage(formData)
            .then(response => {
                const imageObj = new Image();
                imageObj.src = response.imageData;

                setTimeout(() => {
                    if (imageObj.height) {
                        commit("setImageData", imageObj.src);
                    } else {
                        setTimeout(function () {
                            commit("setImageData", imageObj.src);
                        }, 1000);
                    }
                }, 100);

                commit("setImageResponse", response);

                commit("setLoading", false);
            })
            .catch(error => {
                commit("setLoading", false);

                console.log(error);
            });
    },

    setImageDataFromPosition({ commit, state }, imageData) {
        if (state.loading) return;

        commit("setLoading", true);

        commit("setImageData", imageData);

        commit("setLoading", false);
    },

    changeCurrentPage({ commit, state }, idx) {
        if (state.loading) return;

        commit("changeCurrentPage", idx);
    },

    changeCurrentData({ commit, state }, idx) {
        if (state.loading) return;

        commit("changeCurrentData", idx);
    },

    addData({ commit, state }, data) {
        if (state.loading) return;

        commit("addData", data);
    },

    removeData({ commit, state }, idx) {
        if (state.loading) return;

        commit("removeData", idx);
    },

    updateAllData({ commit, state }, data) {
        if (state.loading) return;

        commit("updateAllData", data);
    },

    setMetadataFromPosition({ commit, state }, metadata) {
        if (state.loading) return;

        commit("setLoading", true);

        const imageObj = new Image();
        imageObj.src = metadata.imageData;

        setTimeout(() => {
            if (imageObj.height) {
                commit("setImageData", imageObj.src);
            } else {
                setTimeout(function () {
                    commit("setImageData", imageObj.src);
                }, 1000);
            }
        }, 100);

        commit("setImageResponse", metadata);

        commit("setLoading", false);
    },

    setNewFiles({ commit, state }, formData) {
        if (state.loading) return;

        commit("setLoading", true);

        API.setMetadata(formData)
            .then(response => {
                commit("setNewResponse", response);

                commit("setLoading", false);
            })
            .catch(error => {
                commit("setLoading", false);

                console.log(error);
            });
    },

    changeImage({ commit, state }, imageId) {
        if (state.loading) return;

        commit("setLoading", true);

        API.changeImage({ imageId })
            .then(response => {
                const imageObj = new Image();
                imageObj.src = response.imageData;

                setTimeout(() => {
                    if (imageObj.height) {
                        commit("changeImageData", response);
                    } else {
                        setTimeout(function () {
                            commit("changeImageData", response);
                        }, 1000);
                    }
                }, 100);

                commit("setLoading", false);
            })
            .catch(error => {
                commit("setLoading", false);

                console.log(error);
            });
    },

    changeParameterByZ({ commit, state }, z) {
        changeParameter(commit, state, {
            T: state.parameters.T,
            Z: z,
            C: state.parameters.C
        });
    },

    changeParameterByT({ commit, state }, t) {
        changeParameter(commit, state, {
            T: t,
            Z: state.parameters.Z,
            C: state.parameters.C
        });
    },

    changeParameterByC({ commit, state }, c) {
        changeParameter(commit, state, {
            T: state.parameters.T,
            Z: state.parameters.Z,
            C: c
        });
    },

    adjustImageByBrightness({ commit, state }, b) {
        adjustImage(
            { commit, state },
            {
                brightness: b,
                contrast: state.parameters.contrast,
                gamma: state.parameters.gamma
            }
        );
    },

    adjustImageByContrast({ commit, state }, c) {
        adjustImage(
            { commit, state },
            {
                brightness: state.parameters.brightness,
                contrast: c,
                gamma: state.parameters.gamma
            }
        );
    },

    adjustImageByGamma({ commit, state }, g) {
        adjustImage(
            { commit, state },
            {
                brightness: state.parameters.brightness,
                contrast: state.parameters.contrast,
                gamma: g
            }
        );
    },

    resetAdjust({ commit }) {
        commit("resetAdjust");
    }
};

// mutations
const mutations = {
    setLoading(state, data) {
        state.loading = data;
    },

    setImageResponse(state, payload) {
        (state.coreMetadata = payload.coreMetadata),
            (state.originMetadata = payload.originMetadata),
            (state.imageId = payload.imageId),
            (state.imageInfo = payload.imageInfo),
            (state.plateId = payload.plateId),
            (state.wellId = payload.wellId),
            (state.positionX = payload.positionX),
            (state.positionY = payload.positionY),
            (state.plates = payload.plates),
            (state.wellSamples = payload.wellSamples);
    },

    setNewResponse(state, payload) {
        state.newRes = payload;
    },

    setImageData(state, payload) {
        state.imageData = payload;
        state.originData = payload;
        state.isNew = true;

        state.parameters = Object.assign({}, state.parameters, DEFAULT_PARAMS);
    },

    changeCurrentPage(state, payload) {
        state.curPageIdx = payload;
    },

    changeCurrentData(state, payload) {
        state.allIndice = state.allIndice.map((val, idx) =>
            idx == state.curPageIdx - 1 ? payload : val
        );
    },

    addData(state, payload) {
        state.newData = payload;
        state.allData.push(payload);
        state.allIndice.push(0);
        state.curPageIdx = state.allData.length;
    },

    removeData(state, payload) {
        state.allData.splice(payload, 1);
    },

    updateAllData(state, payload) {
        state.allData = payload;
    },

    changeImageData(state, payload) {
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

        state.parameters = Object.assign({}, state.parameters, DEFAULT_PARAMS);
    },

    changeParameterData(state, payload) {
        state.imageData = payload.imageData;
        state.originData = payload.imageData;
        state.isNew = false;

        state.parameters = Object.assign({}, state.parameters, {
            Z: payload.params.Z,
            T: payload.params.T,
            C: payload.params.C,
            brightness: 0,
            contrast: 0,
            gamma: 0
        });
    },

    adjustImage(state, payload) {
        state.imageData = payload.imageData;
        state.parameters = Object.assign({}, state.parameters, {
            brightness: payload.params.brightness,
            contrast: payload.params.contrast,
            gamma: payload.params.gamma
        });
        state.isNew = false;
    },

    resetAdjust(state) {
        state.imageData = state.originData;
        state.parameters = Object.assign({}, state.parameters, {
            brightness: 0,
            contrast: 0,
            gamma: 0
        });
        state.isNew = false;
    }
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};

//////////////////////////////////////

function changeParameter(commit, state, params) {
    if (state.loading) return;

    commit("setLoading", true);

    API.changeParameter(params)
        .then(response => {
            const imageObj = new Image();
            imageObj.src = response.imageData;

            setTimeout(() => {
                if (imageObj.height) {
                    commit("changeParameterData", {
                        imageData: imageObj.src,
                        params
                    });
                } else {
                    setTimeout(function () {
                        commit("changeParameterData", {
                            imageData: imageObj.src,
                            params
                        });
                    }, 1000);
                }
            }, 100);

            commit("setLoading", false);
        })
        .catch(error => {
            commit("setLoading", false);

            console.log(error);
        });
}

function adjustImage({ commit, state }, params) {
    if (state.loading) return;

    commit("setLoading", true);

    API.adjustImage({
        imageData: state.originData,
        ...params
    })
        .then(response => {
            const imageObj = new Image();
            imageObj.src = response.imageData;

            setTimeout(() => {
                if (imageObj.height) {
                    commit("adjustImage", {
                        imageData: imageObj.src,
                        params
                    });
                } else {
                    setTimeout(function () {
                        commit("adjustImage", {
                            imageData: imageObj.src,
                            params
                        });
                    }, 1000);
                }
            }, 100);

            commit("setLoading", false);
        })
        .catch(error => {
            commit("setLoading", false);

            console.log(error);
        });
}
