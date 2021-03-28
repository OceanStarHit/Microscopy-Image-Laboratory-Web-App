import axios from "axios";

export const BASE_API_URL = "http://127.0.0.1:8000/apis/";
export const api = axios.create({
    baseURL: BASE_API_URL,
    headers: {
        // "Access-Control-Allow-Origin": "*",
        "X-Requested-With": "XMLHttpRequest",
        Accept: "application/json",
        "Content-Type": "application/json"
    }
});

api.interceptors.request.use(request => {
    console.log("[API Request]", request);

    return request;
});

api.interceptors.response.use(
    response => {
        console.log("[API Response]", response);
        return response.data;
    },
    error => {
        console.log("[API ERROR]", error);

        return Promise.reject(error);
    }
);
