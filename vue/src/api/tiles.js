import { api } from "./base";

function client() {
  api.defaults.headers["Authorization"] =
    "Token " + sessionStorage.getItem("authToken");
  api.defaults.headers["Content-Type"] = "application/json";

  return api;
}

export const batchCreate = files => {
  let c = client();
  c.defaults.headers["Content-Type"] = "multipart/form-data";

  const formData = new FormData();
  // alert(files);
  for (let i in files) {
    console.log(i);
    let f = files[i];
    formData.append("files", f);
  }
  // files.forEach(file => {
  //   console.log(file);
  //   formData.append("files", file);
  // });
  console.log(formData);
  return api.post("tiles/batch_create/", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
};
