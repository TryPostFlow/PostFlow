import Vue from "vue";

import Router from "vue-router";
import views from "./views";

Vue.use(Router);

const router = new Router({
  base: base,
  mode: "history",
  scrollBehavior: () => ({ y: 0 }),
  routes: views
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.auth)) {
    var auth = localStorage.getItem("auth")
      ? JSON.parse(localStorage.getItem("auth"))
      : null;
    if (!auth) {
      next({
        name: "SignIn",
        query: { redirect: to.fullpath }
      });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
