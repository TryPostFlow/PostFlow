import SignIn from './SignIn.vue'
import SignOut from './SignOut.vue'
import PostList from './PostList.vue'
import PostView from './PostView.vue'
import PostEdit from './PostEdit.vue'
import PostCreate from './PostCreate.vue'

export default {
  '/signin': {
    name: 'SignIn',
    component: SignIn,
    auth: false
  },
  '/signout': {
    name: 'SignOut',
    component: SignOut,
    auth: false
  },
  '/posts': {
    component: PostList,
    auth: true,
    subRoutes: {
      '/': {
        name: 'PostList',
        component: PostList
      },
       '/:post_id': {
        name: 'PostView',
        component: PostView,
        // auth: true
      },
    }
  },
  '/posts/:post_id/edit': {
    name: 'PostEdit',
    component: PostEdit,
    auth: true
  },
  '/posts/new': {
    name: 'PostCreate',
    component: PostCreate,
    auth: true
  }
}
