import Vue from 'vue'
import Router from 'vue-router'
import Resource from 'vue-resource'

import { format } from './filters'
require('./css/yue.css')
require('./css/site.css')
import App from './components/app.vue'
import Index from './components/index.vue'
import Post from './components/post.vue'
import Tag from './components/tag.vue'

Vue.use(Router)
Vue.use(Resource)

Vue.filter('format', format)

Vue.http.options.root = 'http://127.0.0.1:5000'

var router = new Router({
  // hashbang: false,
  // history: true,
  saveScrollPosition: true
})

router.map({
  '/': {
    name: 'Index',
    component: Index
  },
  '/posts/:post_id': {
    name: 'post',
    component: Post
  },
  '/tags/:tag_id': {
    name: 'Tag',
    component: Tag
  }
})

router.redirect({
  '*': '/'
})

router.start(App, '#app')
