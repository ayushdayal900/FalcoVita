import authAPI from "../api/auth";

export default {
  namespaced: true,

  state: () => ({
    user: null,
    token: localStorage.getItem("token") || null,
  }),

  mutations: {
    SET_USER(state, payload) {
      state.user = payload;
    },
    SET_TOKEN(state, token) {
      state.token = token;
      localStorage.setItem("token", token);
    },
    LOGOUT(state) {
      state.token = null;
      state.user = null;
      localStorage.removeItem("token");
    }
  },

  actions: {
    async login({ commit }, payload) {
      const res = await authAPI.login(payload);

      commit("SET_TOKEN", res.data.token);
      commit("SET_USER", res.data);

      return res;
    },

    async register(_, payload) {
      const res = await authAPI.register(payload);
      return res;
    },

    logout({ commit }) {
      commit("LOGOUT");
    }
  }
};
