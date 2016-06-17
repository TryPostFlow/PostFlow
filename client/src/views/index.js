import Home from './Home.vue'
import Post from './Post.vue'
import Tag from './Tag.vue'

export default{
  '/': {
    name: 'home',
    component: Home
  },
  '/posts/:post_id': {
    name: 'post',
    component: Post
  },
  '/tags/:tag_id': {
    name: 'Tag',
    component: Tag
  }
}
