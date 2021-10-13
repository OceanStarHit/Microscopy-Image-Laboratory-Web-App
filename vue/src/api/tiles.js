import { api, BASE_API_URL } from "./base";
import axios from "axios";

function client() {
  api.defaults.headers["Authorization"] =
    "Token " + sessionStorage.getItem("authToken");
  api.defaults.headers["Content-Type"] = "application/json";

  return api;
}

export const listTiles = (success, failed) => {
  let c = client();
  c.get("tiles/")
    .then(function(response) {
      success(response);
    })
    .catch(function(error) {
      failed(error);
    });
};

export const alignTiles = (row, method, success, fail) => {
  let c = client();

  const formData = new FormData();
  formData.append("method", method);
  formData.append("row", row);

  c.post("tiles/align/", formData)
    .then(function(response) {
      console.log("align success callback");
      if (success) {
        success(response);
      }
    })
    .catch(function(error) {
      console.log("align failed callback");
      fail(error);
    });
};

export const batchCreateTiles = files => {
  let c = client();
  c.defaults.headers["Content-Type"] = "multipart/form-data";

  const formData = new FormData();
  for (let i in files) {
    console.log(i);
    let f = files[i];
    formData.append("files", f);
  }
  return c.post("tiles/batch_create/", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
};

export const exportTiles = (success, fail) => {
  axios({
    url: BASE_API_URL + "tiles/export/",
    method: "GET",
    responseType: "blob",
    headers: {
      Authorization: "Token " + sessionStorage.getItem("authToken")
    }
  })
    .then(response => {
      success(response);
    })
    .catch(function(error) {
      console.log("export failed callback");
      console.log(error);
      if (fail) {
        fail(error);
      }
    });
};
