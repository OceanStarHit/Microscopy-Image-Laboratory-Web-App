import { api } from "./base";
export const setImage = params => {
  return api.post("set-image", params);
};

export const setMetadata = params => {
  return api.post("/image/tile/upload_image_tiles", params);
};

export const sendImageFile = params => {
  return api.post("/image/tile/convol2D", params);
}

export const send3DFile = params => {
  return api.post("/image/tile/convol3D", params);
}

export const changeImage = params => {
  return api.post("change-image", params);
};

export const changeParameter = params => {
  return api.post("change-parameter", params);
};

export const adjustImage = params => {
  return api.post("adjust-image", params);
};
