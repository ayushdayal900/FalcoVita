<template>
  <div class="login-container">
    <h2>Login</h2>

    <form @submit.prevent="handleLogin">
      <input
        v-model="email"
        type="email"
        placeholder="Email"
        required
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      />

      <button type="submit">Login</button>
    </form>

    <p>
      Don't have an account?
      <router-link to="/register">Register</router-link>
    </p>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "Login",

  data() {
    return {
      email: "",
      password: "",
      error: ""
    };
  },

  methods: {
    ...mapActions("auth", ["login"]),

    async handleLogin() {
      this.error = "";

      try {
        const response = await this.login({
          email: this.email,
          password: this.password
        });

        // Redirect to dashboard
        this.$router.push("/dashboard");

      } catch (err) {
        this.error =
          err.response?.data?.message ||
          "Login failed. Please try again.";
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 350px;
  margin: 100px auto;
  padding: 20px;
  text-align: center;
  border-radius: 8px;
  border: 1px solid #ddd;
}

input {
  display: block;
  width: 90%;
  padding: 10px;
  margin: 10px auto;
}

button {
  width: 95%;
  padding: 10px;
  margin-top: 10px;
  cursor: pointer;
}

.error {
  color: red;
  margin-top: 12px;
}
</style>
