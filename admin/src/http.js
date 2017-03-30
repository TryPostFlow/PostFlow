import axios from "axios";
import store from "./store";
import router from "./router";

axios.defaults.timeout = 5000;
axios.defaults.baseURL = "/api";

axios.interceptors.request.use(
  config => {
    if (store.state.Auth.token) {
      config.headers.Authorization = `Bearer ${store.state.Auth.token}`;
    }
    return config;
  },
  err => {
    return Promise.reject(err);
  }
);

axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 401 清除token信息并跳转到登录页面
          store.commit("auth/DELETE_ITEM");
          router.replace({
            name: "SignIn",
            query: { redirect: router.currentRoute.fullPath }
          });
      }
    }
    // console.log(JSON.stringify(error));//console : Error: Request failed with status code 402
    return Promise.reject(error.response.data);
  }
);

export default axios;
