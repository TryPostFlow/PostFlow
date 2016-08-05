import SignIn from './SignIn.vue'
import SignOut from './SignOut.vue'
import PostList from './PostList.vue'
import PostView from './PostView.vue'
import PostEdit from './PostEdit.vue'
import PostCreate from './PostCreate.vue'
import TagList from './TagList.vue'
import TagCreate from './TagCreate.vue'
import TagEdit from './TagEdit.vue'

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
  },
  '/tags': {
    component: TagList,
    auth: true,
    subRoutes: {
      '/': {
        name: 'TagList',
        component: TagList
      },
      '/new': {
        name: 'TagCreate',
        component: TagCreate
      },
       '/:tag_id': {
        name: 'TagEdit',
        component: TagEdit,
        // auth: true
      }
    }
  },

}
