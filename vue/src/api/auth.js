import { api } from "./base";

export const login = params => {
  console.log(params);
  return api.post("login", params);
};

export const logout = params => {
  return api.post("logout", params);
};

export const regist = params => {
  return api.post("regist", params);
};

export const setAuthToken = token => {
  // alert(token);
  api.defaults.headers["Authorization"] = "Token " + token;
};
