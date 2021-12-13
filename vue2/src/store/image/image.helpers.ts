import {ImageParameters, ImageState} from '@/store/image/image.module';

export function changeParameters(state: ImageState, params: Partial<ImageParameters>): any {
    const newParams = Object.assign({}, state.parameters, {}); // copy
    if (typeof params.Z !== 'undefined') {
        newParams.Z = params.Z;
    }
    if (typeof params.T !== 'undefined') {
        newParams.T = params.T;
    }
    if (typeof params.C !== 'undefined') {
        newParams.C = params.C;
    }
    if (typeof params.brightness !== 'undefined') {
        newParams.brightness = params.brightness;
    }
    if (typeof params.contrast !== 'undefined') {
        newParams.contrast = params.contrast;
    }
    if (typeof params.gamma !== 'undefined') {
        newParams.gamma = params.gamma;
    }
    if (typeof params.objective !== 'undefined') {
        newParams.objective = params.objective;
    }

    return newParams;

    // commit("changeParameterData", {
    //     params: newParams
    // });

    // if (state.loading) return;

    // commit("setLoading", true);

    // API.changeParameter(params)
    //   .then(response => {
    //     const imageObj = new Image();
    //     imageObj.src = response.imageData;

    //     setTimeout(() => {
    //       if (imageObj.height) {
    //         commit("changeParameterData", {
    //           imageData: imageObj.src,
    //           params
    //         });
    //       } else {
    //         setTimeout(function() {
    //           commit("changeParameterData", {
    //             imageData: imageObj.src,
    //             params
    //           });
    //         }, 1000);
    //       }
    //     }, 100);

    //     commit("setLoading", false);
    //   })
    //   .catch(error => {
    //     commit("setLoading", false);

    //     console.log(error);
    //   });
}




export function filteredByParameters(parameters: ImageParameters, images: any) {
    // filter by z position
    let filtered = images.filter((img: any) => img.extParams.z == parameters.Z);

    // filter by objective lense
    filtered = images.filter((img: any) => img.extParams.objective == parameters.objective);

    // filter by timeline
    filtered = images.filter((img: any) => img.extParams.timeline == parameters.T);

    return filtered;
}
