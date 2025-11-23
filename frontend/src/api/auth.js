import api from "./axios";

export default {
  login(data) {
    return api.post("/auth/login", data);
  },

  register(data) {
    return api.post("/auth/register", data);
  }
};
