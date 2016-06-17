import Vue from 'vue'
import Router from 'vue-router'
import Resource from 'vue-resource'

import App from './App.vue'
import views from './views'

Vue.use(Router)
Vue.use(Resource)

if (process.env.NODE_ENV === 'production') {
  require('./ga')
  Vue.http.options.root = 'http://api.test.com'
} else {
  window.ga = function () {}
  Vue.config.debug = true
  Vue.http.options.root = 'http://127.0.0.1:5000'
}

if (localStorage.getItem('auth')) {
  var auth = JSON.parse(localStorage.getItem('auth'))
  Vue.http.headers.common['Authorization'] = 'Bearer ' + auth.access_token
}

// Vue.http.interceptors.push({
//   response: function (response) {
//     switch (response.status) {
//       case 401:
//         router.go({'name': 'SignIn'})
//         break
//       case 402:
//         router.go({'name': 'SignIn'})
//         break
//       case 403:
//         router.go({'name': 'SignIn'})
//         break
//       default:
//         return response
//     }
//     return response
//   }
// })

var router = new Router({
  linkActiveClass: 'active'
})

router.map(views)

router.redirect({
  '*': '/posts'
})

router.start(App, '#app')
