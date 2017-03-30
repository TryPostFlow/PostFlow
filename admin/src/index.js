import "font-awesome/css/font-awesome.css";
import "bootstrap/dist/css/bootstrap.css";
import "./css/app.css";

import Vue from "vue";
import { sync } from "vuex-router-sync";

import App from "./App.vue";
import store from "./store";
import router from "./router";
import axios from "./http";

Vue.prototype.$http = axios;

sync(store, router);

// 页面刷新时，重新赋值token
if (window.localStorage.getItem("auth")) {
  var auth = JSON.parse(window.localStorage.getItem("auth"));
  store.commit("auth/SET_ITEM", auth);
}

const app = new Vue({
  axios,
  router,
  store,
  render: h => h(App)
});
require("es6-promise").polyfill();
app.$mount("#app");
