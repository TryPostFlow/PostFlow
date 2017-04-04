import Vue from "vue";

import actions from "../actions";
import mutations from "../mutations";
import getters from "../getters";

import create_types from "../constants/types";

const types = create_types("role");

export default {
  state: {
    data: {},
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
