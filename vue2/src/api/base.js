import axios from 'axios';
import store from '../__legacy_vuex';

export const BASE_API_URL = 'http://127.0.0.1:8000/';
// export const BASE_API_URL = "api:8000/apis/";
// export const BASE_API_URL = "http://docker.for.mac.localhost:8000/apis/";

export const api = axios.create({
  baseURL: BASE_API_URL,
  headers: {
    // "Access-Control-Allow-Origin": "*",
    'X-Requested-With': 'XMLHttpRequest',
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
});

api.interceptors.request.use(request => {
  console.log('[API Request]', request);
  console.log(store.state);

  /* add auth headers */
  if (store.state.auth.token) {
    request.headers['Authorization'] =
      store.state.auth.tokenType + ' ' + store.state.auth.token;
    request.headers['Content-Type'] = 'application/json';
  }
  
  //
  // if (sessionStorage.getItem("authToken")) {
  //   request.headers["Authorization"] =
  //     sessionStorage.getItem("authTokenType") +
  //     " " +
  //     sessionStorage.getItem("authToken");
  //   request.headers["Content-Type"] = "application/json";
  // }

  return request;
});

api.interceptors.response.use(
  response => {
    // console.log("[API Response]", response);
    // return response.data;
    return response;
  },
  error => {
    console.log('[API ERROR]', error);
    if (error.response.status === 401) {
      store.dispatch('auth/logOut');
    }
    return Promise.reject(error);
  }
);
