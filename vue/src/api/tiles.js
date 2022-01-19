import { api, BASE_API_URL } from "./base";
import axios from "axios";

export const listTiles = (success, failed) => {
  api
    .get("image/tile/list")
    .then(function(response) {
      success(response);
    })
    .catch(function(error) {
      failed(error);
    });
};

export const alignTiles = (rows, method, success, fail) => {
  api
    .post("image/tile/align_tiles_naive", { method: method, rows: rows })
    .then(function(response) {
      console.log("align success callback");
      if (success) {
        success(response);
      }
    })
    .catch(function(error) {
      console.log("align failed callback");
      if (fail) {
        fail(error);
      }
    });
};

export const uploadImageTiles = files => {
  const formData = new FormData();
  for (let i in files) {
    console.log(i);
    let f = files[i];
    formData.append("files", f);
  }

  return api.post("image/tile/upload_image_tiles", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
};

export const exportTiles = (success, fail) => {
  // axios({
  //   url: BASE_API_URL + "tiles/export/",
  //   method: "GET",
  //   responseType: "blob",
  //   headers: {
  //     Authorization: "Token " + sessionStorage.getItem("authToken")
  //   }
  // })
  //   .then(response => {
  //     success(response);
  //   })
  //   .catch(function(error) {
  //     console.log("export failed callback");
  //     console.log(error);
  //     if (fail) {
  //       fail(error);
  //     }
  //   });
};
