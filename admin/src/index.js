import 'font-awesome/css/font-awesome.css'
import 'bootstrap/dist/css/bootstrap.css'
import './css/app.css'

import Vue from 'vue'

import Router from 'vue-router'
import { sync } from 'vuex-router-sync'

import App from './App.vue'
import views from './views'
import store from './store'

Vue.use(Router)
Vue.use(ElementUI)

const router = new Router({
  // mode: 'history',
  // scrollBehavior: () => ({ y: 0 }),
  // scrollBehavior: function(to, from, savedPosition) {
  //     if (to.hash) {
  //         return {selector: to.hash}
  //     } else {
  //         return { x: 0, y: 0 }
  //     }
  // },
  routes: views
})

sync(store, router)

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.auth)) {
    var auth = localStorage.getItem('auth')? JSON.parse(localStorage.getItem('auth')): null
    if (!auth) {
      next({
        path: '/signin',
        query: {redirect: to.fullpath}
      })
    }else{
      next()
    }
  }else{
    next()
  }
})

const app = new Vue(
  Vue.util.extend({
    router,
    store
  }, App) // Object spread copying everything from App.vue
)
require('es6-promise').polyfill()
app.$mount('#app')
