import SignIn from './SignIn.vue'
import SignOut from './SignOut.vue'
import PostList from './PostList.vue'
import PostView from './PostView.vue'
import PostEdit from './PostEdit.vue'
import PostCreate from './PostCreate.vue'
import TagList from './TagList.vue'
import TagCreate from './TagCreate.vue'
import TagEdit from './TagEdit.vue'
import Settings from './Settings.vue'
import AccountList from './AccountList.vue'
import AccountEdit from './AccountEdit.vue'

export default [
  {
    path: '/signin',
    name: 'SignIn',
    component: SignIn,
    meta: {
      auth: false
    }
  },
  {
    path: '/signout',
    name: 'SignOut',
    component: SignOut,
    meta: {
      auth: false
    }
  },
  {
    path: '/posts/new',
    name: 'PostCreate',
    component: PostCreate,
    meta: {
      auth: true
    }
  },
  {
    path: '/posts',
    component: PostList,
    children: [
      {
        path: '',
        name: 'PostList',
        // component: PostList,
        meta: {
          auth: true
        }
      },
      {
        path: ':post_id',
        name: 'PostView',
        component: PostView,
        meta: {
          auth: true
        }
      }
    ]
  },
  {
    path: '/posts/:post_id/edit',
    name: 'PostEdit',
    component: PostEdit,
    meta: {
      auth: true
    }
  },
  {
    path: '/tags',
    component: TagList,
    children: [
      {
        path: '',
        name: 'TagList',
        component: TagList,
        meta: {
          auth: true
        }
      },
      {
        path: 'new',
        name: 'TagCreate',
        component: TagCreate,
        meta: {
          auth: true
        }
      },
      {
        path:  ':tag_id',
        name: 'TagEdit',
        component: TagEdit,
        meta: {
          auth: true
        }
      }
    ]
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: {
      auth: true
    }
  },
  {
    path: '/accounts',
    name: 'AccountList',
    component: AccountList,
    meta:{
      auth: true
    }
  },
  {
    path: '/accounts/:account_id/edit',
    name: 'AccountEdit',
    component: AccountEdit,
    meta:{
      auth: true
    }
  },
  {
    path: '*',
    redirect: {name: 'SignIn'}
  }
]
