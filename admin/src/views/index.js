import SignIn from './SignIn.vue'
import SignOut from './SignOut.vue'
import PostList from './PostList.vue'
import PostView from './PostView.vue'
import PostEdit from './PostEdit.vue'
import PostCreate from './PostCreate.vue'

export default {
  '/signin': {
    name: 'SignIn',
    component: SignIn
  },
  '/signout': {
    name: 'SignOut',
    component: SignOut
  },
  '/posts': {
    name: 'PostList',
    component: PostList
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
    name: 'PostCreate',
    component: PostCreate
  }
}
