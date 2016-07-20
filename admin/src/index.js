import 'font-awesome/css/font-awesome.css'
import 'bootstrap/dist/css/bootstrap.css'
import './css/app.css'
import './css/yue.css'

import 'select2/dist/css/select2.css'
import 'toastr/build/toastr.css'

import Vue from 'vue'
import Router from 'vue-router'
import Resource from 'vue-resource'

import App from './App.vue'
import views from './views'

Vue.use(Router)
Vue.use(Resource)

if (process.env.NODE_ENV === 'production') {
  // require('./ga')
  Vue.http.options.root = '/api'
} else {
  window.ga = function () {}
  Vue.config.debug = true
  Vue.http.options.root = 'http://127.0.0.1:5000/api'
}

if (localStorage.getItem('auth')) {
  var auth = JSON.parse(localStorage.getItem('auth'))
  Vue.http.headers.common['Authorization'] = 'Bearer ' + auth.access_token
}

var router = new Router({
  linkActiveClass: 'active'
})

router.map(views)

router.redirect({
  '*': '/posts'
})

router.beforeEach(function (transition) {
  if (transition.to.auth) {
    var auth = localStorage.getItem('auth')? JSON.parse(localStorage.getItem('auth')): null
    if (!auth) {
      transition.redirect({name: 'SignIn'})
    }
  }
  transition.next()
})

router.start(App, '#app')
