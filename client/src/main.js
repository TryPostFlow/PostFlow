import Vue from 'vue'
import Router from 'vue-router'
import Resource from 'vue-resource'

require('./css/yue.css')
require('./css/site.css')

import { format } from './filters'
import App from './app.vue'
import views from './views'


Vue.use(Router)
Vue.use(Resource)

Vue.filter('format', format)

Vue.http.options.root = 'http://127.0.0.1:5000'

var router = new Router({
  // hashbang: false,
  // history: true,
  saveScrollPosition: true
})

router.map(views)

router.redirect({
  '*': '/'
})

router.start(App, '#app')
