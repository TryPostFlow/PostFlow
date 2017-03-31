import Vue from "vue";

import actions from "../actions";
import mutations from "../mutations";
import getters from "../getters";

import create_types from "../constants/types";

const types = create_types("setting");

export default {
  state: {
    data: {
      title: {},
      description: {},
      postsPerPage: {},
      ga_id: {},
      disqus_id: {},
      navigation: { value: null }
    },
    list: {
      // [request]:{
      //     data:[],
      //     total: 100,
      //     page: 1,
      //     page_size: 20
      // }
    }
  },
  getters: getters(types),
  actions: actions(types),
  mutations: mutations(types)
};
