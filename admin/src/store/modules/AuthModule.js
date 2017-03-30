import axios from "../../http";
import create_types from "../constants/types";

const types = create_types("auth");

export default {
  state: {
    user: {},
    token: null
  },
  actions: {
    [types.SIGNIN]({ commit, state }, { params }) {
      return new Promise((resolve, reject) => {
        axios
          .post("login", params)
          .then(function(response) {
            commit(types.SET_ITEM, response.data);
            resolve(response);
          })
          .catch(function(error) {
            reject(error);
          });
      });
    }
  },
  mutations: {
    [types.SET_ITEM]: (state, data) => {
      localStorage.setItem("auth", JSON.stringify(data));
      state.token = data.access_token;
    },
    [types.DELETE_ITEM]: state => {
      localStorage.removeItem("auth");
      state.token = null;
    }
  }
};
