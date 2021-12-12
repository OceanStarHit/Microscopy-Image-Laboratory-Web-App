import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { store } from '@/store'

const BASE_API_URL = 'http://127.0.0.1:8000/'

export const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_API_URL,
  headers: {
    'Content-type': 'application/json',
    Accept: 'application/json',
  },
})
//
//
//
// // export const BASE_API_URL = "api:8000/apis/";
// // export const BASE_API_URL = "http://docker.for.mac.localhost:8000/apis/";
//
// export const api = axios.create({
//   baseURL: BASE_API_URL,
//   headers: {
//     // "Access-Control-Allow-Origin": "*",
//     "X-Requested-With": "XMLHttpRequest",
//     Accept: "application/json",
//     "Content-Type": "application/json",
//   },
// });

apiClient.interceptors.request.use((request: AxiosRequestConfig) => {
  console.log('[API Request]', request)
  console.log(store.state)

  // /* add auth headers */
  // if (store.state..count) {
  //   request.headers["Authorization"] =
  //     store.state.auth.tokenType + " " + store.state.auth.token;
  //   request.headers["Content-Type"] = "application/json";
  // }

  return request
})

apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // console.log("[API Response]", response);
    // return response.data;
    return response
  },
  (error: any) => {
    console.log('[API ERROR]', error)
    if (error.response.status === 401) {
      store.dispatch('auth/logOut')
    }
    return Promise.reject(error)
  }
)
