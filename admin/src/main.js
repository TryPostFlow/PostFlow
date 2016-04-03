import Vue from 'vue'
import Router from 'vue-router'
import Resource from 'vue-resource'

import App from './components/app.vue'
import SignIn from './components/signin.vue'
import SignOut from './components/signin.vue'
import PostIndex from './components/post/index.vue'
import PostView from './components/post/view.vue'
import PostEdit from './components/post/edit.vue'
import PostNew from './components/post/new.vue'

Vue.use(Router)
Vue.use(Resource)
Vue.http.options.root = 'http://127.0.0.1:5000'
if (localStorage.getItem('auth')) {
  var auth = JSON.parse(localStorage.getItem('auth'))
  Vue.http.headers.common['Authorization'] = 'Bearer ' + auth.access_token
}

Vue.http.interceptors.push({
  response: function (response) {
    switch (response.status) {
      case 401:
        router.go({'name': 'SignIn'})
        break
      case 402:
        router.go({'name': 'SignIn'})
        break
      case 403:
        router.go({'name': 'SignIn'})
        break
      default:
        return response
    }
    return response
  }
})

var router = new Router({
  linkActiveClass: 'active'
})

router.map({
  '/signin': {
    name: 'SignIn',
    component: SignIn
  },
  '/signout': {
    name: 'signout',
    component: SignOut
  },
  '/posts': {
    name: 'PostIndex',
    component: PostIndex
  },
  '/posts/:post_id': {
    name: 'PostView',
    component: PostView
  },
  '/posts/:post_id/edit': {
    name: 'PostEdit',
    component: PostEdit
  },
  '/posts/new': {
    name: 'PostNew',
    component: PostNew
  }
})

router.redirect({
  '*': '/posts'
})

router.start(App, '#app')
