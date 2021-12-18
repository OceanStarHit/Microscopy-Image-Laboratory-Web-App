import {ImageState} from '@/store/image/image.module';
import {ActionContext} from 'vuex';
import {State} from '@/store';
import {changeParameters} from '@/store/image/image.helpers';

export default {
    setImage(context: ActionContext<ImageState, State>, data: any) {
        if (context.state.isLoading) return;

        context.commit('setLoading', true);

        console.log('set Image');


        // TODO
        // API.setImage(formData)
        //     .then(response => {
        //         const imageObj = new Image();
        //         imageObj.src = response.imageData;
        //
        //         setTimeout(() => {
        //             if (imageObj.height) {
        //                 commit('setImageData', imageObj.src);
        //             } else {
        //                 setTimeout(function() {
        //                     commit('setImageData', imageObj.src);
        //                 }, 1000);
        //             }
        //         }, 100);
        //
        //         commit('setImageResponse', response);
        //
        //         commit('setLoading', false);
        //     })
        //     .catch(error => {
        //         commit('setLoading', false);
        //
        //         console.log(error);
        //     });
    },

    setImageDataFromPosition(context: ActionContext<ImageState, State>, imageData: any) {
        if (context.state.isLoading) return;

        context.commit('setLoading', true);
        context.commit('setImageData', imageData);
        context.commit('setLoading', false);
    },

    changeCurrentPage(context: ActionContext<ImageState, State>, index: number) {
        if (context.state.isLoading) return;

        context.commit('changeCurrentPage', index);
    },

    changeCurrentData(context: ActionContext<ImageState, State>, index: number) {
        if (context.state.isLoading) return;

        context.commit('changeCurrentData', index);
    },

    changeCurrentMultiData(context: ActionContext<ImageState, State>, indices: number[]) {
        if (context.state.isLoading) return

        context.commit('changeCurrentMultiData', indices);
    },

    addData(context: ActionContext<ImageState, State>, data: any) {
        // if (state.loading) return;

        context.commit('addData', data);
    },

    removeData(context: ActionContext<ImageState, State>, index: number) {
        if (context.state.isLoading) return

        context.commit('removeData', index);
    },

    updateAllData(context: ActionContext<ImageState, State>, data: any) {
        if (context.state.isLoading) return

        context.commit('updateAllData', data);
    },

    setMetadataFromPosition(context: ActionContext<ImageState, State>, metadata: any) {
        if (context.state.isLoading) return

        context.commit('setLoading', true);

        const imageObj = new Image();
        imageObj.src = metadata.imageData;

        setTimeout(() => {
            if (imageObj.height) {
                context.commit('setImageData', imageObj.src);
            } else {
                setTimeout(function() {
                    context.commit('setImageData', imageObj.src);
                }, 1000);
            }
        }, 100);

        context.commit('setImageResponse', metadata);

        context.commit('setLoading', false);
    },

    setNewFiles(context: ActionContext<ImageState, State>, data: any) {
        // if (state.loading) return;
        context.commit('incLoadingCount');

        // TODO

        // API.setMetadata(formData)
        //     .then(response => {
        //         commit('setNewResponse', response);
        //
        //         commit('decLoadingCount');
        //         console.log('loading count:' + state.loading_count);
        //     })
        //     .catch(error => {
        //         commit('decLoadingCount');
        //         console.log('loading count:' + state.loading_count);
        //
        //         console.log(error);
        //     });
    },

    changeImage(context: ActionContext<ImageState, State>, imageId: number) {
        if (context.state.isLoading) return

        context.commit('setLoading', true);

        // TODO

        // API.changeImage({ imageId })
        //     .then(response => {
        //         const imageObj = new Image();
        //         imageObj.src = response.imageData;
        //
        //         setTimeout(() => {
        //             if (imageObj.height) {
        //                 commit('changeImageData', response);
        //             } else {
        //                 setTimeout(function() {
        //                     commit('changeImageData', response);
        //                 }, 1000);
        //             }
        //         }, 100);
        //
        //         commit('setLoading', false);
        //     })
        //     .catch(error => {
        //         commit('setLoading', false);
        //
        //         console.log(error);
        //     });
    },

    changeParameterByObjective(context: ActionContext<ImageState, State>, objective: number) {
        if (context.state.parameters.objective != objective) {
            const newParams = changeParameters(context.state, {
                objective: objective
            });

            context.commit('changeParameterData', newParams);
        }
    },

    changeParameterByZ(context: ActionContext<ImageState, State>, z: number) {
        if (context.state.parameters.Z != z) {
            const newParams = changeParameters(context.state, {
                Z: z
            });

            context.commit('changeParameterData', newParams);
        }
    },

    changeParameterByT(context: ActionContext<ImageState, State>, t: number) {
        const newParams = changeParameters(context.state, {
            T: t,
        });

        context.commit('changeParameterData', newParams);
    },

    changeParameterByC(context: ActionContext<ImageState, State>, c: number) {
        const newParams = changeParameters(context.state, {
            T: context.state.parameters.T,
            Z: context.state.parameters.Z,
            C: c,
            brightness: context.state.parameters.brightness,
            contrast: context.state.parameters.contrast,
            gamma: context.state.parameters.gamma
        });

        context.commit('changeParameterData', newParams);
    },

    adjustImageByBrightness(context: ActionContext<ImageState, State>, b: number) {

        context.dispatch('adjustImage', {
                brightness: b,
                contrast: context.state.parameters.contrast,
                gamma: context.state.parameters.gamma
            }
        );
    },

    adjustImageByContrast(context: ActionContext<ImageState, State>, c: number) {
        context.dispatch('adjustImage', {
                brightness: context.state.parameters.brightness,
                contrast: c,
                gamma: context.state.parameters.gamma
            }
        );
    },

    adjustImageByGamma(context: ActionContext<ImageState, State>, g: number) {
        context.dispatch('adjustImage', {
                brightness: context.state.parameters.brightness,
                contrast: context.state.parameters.contrast,
                gamma: g
            }
        );
    },

    adjustImage(context: ActionContext<ImageState, State>, params: any) {
    if (context.state.isLoading) return;

    context.commit('setLoading', true);


    // todo
    // API.adjustImage({
    //     imageData: state.originData,
    //     ...params
    // })
    //     .then(response => {
    //         const imageObj = new Image();
    //         imageObj.src = response.imageData;
    //
    //         setTimeout(() => {
    //             if (imageObj.height) {
    //                 commit("adjustImage", {
    //                     imageData: imageObj.src,
    //                     params
    //                 });
    //             } else {
    //                 setTimeout(function() {
    //                     commit("adjustImage", {
    //                         imageData: imageObj.src,
    //                         params
    //                     });
    //                 }, 1000);
    //             }
    //         }, 100);
    //
    //         commit("setLoading", false);
    //     })
    //     .catch(error => {
    //         commit("setLoading", false);
    //
    //         console.log(error);
    //     });
    },

    resetAdjust(context: ActionContext<ImageState, State>) {
        context.commit('resetAdjust');
    }
}
