import Vue from 'vue'
import Vuex from 'vuex'
import createLogger from 'vuex/dist/logger'
import { Post, Tag, Account } from './modules'

Vue.use(Vuex)

const store = new Vuex.Store({
  plugins: [createLogger()],
  modules: {
    Account,
    Post,
    Tag
  }
})

if (module.hot) {
  module.hot.accept(['./modules'], () => {
    const newMutations = require('./modules').default

    store.hotUpdate({
      mutations: newMutations
    })
  })
}

export default store
