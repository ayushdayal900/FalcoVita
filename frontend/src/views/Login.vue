<template>
  <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5 col-xl-4">
          <div class="text-center mb-4">
            <h1 class="h3 fw-bold text-dark">FalcoVita</h1>
            <p class="text-muted small">Healthcare Management System</p>
          </div>

          <div class="card shadow-lg border-0 rounded-4">
            <div class="card-body p-4 p-md-5">
              <div class="text-center mb-4">
                <h2 class="h4 fw-bold text-dark">Welcome Back</h2>
                <p class="text-muted small">Please sign in to your account</p>
              </div>

              <form @submit.prevent="handleLogin">
                <div class="form-floating mb-3">
                  <input 
                    type="email" 
                    class="form-control" 
                    id="email" 
                    v-model="email" 
                    placeholder="name@hospital.com" 
                    required
                  >
                  <label for="email">Email Address</label>
                </div>

                <div class="form-floating mb-3">
                  <input 
                    type="password" 
                    class="form-control" 
                    id="password" 
                    v-model="password" 
                    placeholder="Password" 
                    required
                  >
                  <label for="password">Password</label>
                </div>

                <div class="d-flex justify-content-end mb-4">
                  <a href="#" class="text-decoration-none text-primary small fw-semibold">Forgot password?</a>
                </div>

                <button 
                  type="submit" 
                  class="btn btn-primary w-100 py-3 fw-bold shadow-sm"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  {{ loading ? 'Signing in...' : 'Sign In' }}
                </button>
              </form>

              <div class="text-center mt-4 pt-3 border-top">
                <p class="text-muted small mb-0">
                  Don't have an account? 
                  <router-link to="/register" class="text-primary text-decoration-none fw-bold">Create an account</router-link>
                </p>
              </div>
              
              <div v-if="error" class="alert alert-danger d-flex align-items-center mt-3 mb-0 small" role="alert">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2" viewBox="0 0 16 16">
                  <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                </svg>
                <div>
                  {{ error }}
                </div>
              </div>
            </div>
          </div>
          
          <div class="text-center mt-4">
            <p class="text-muted small opacity-75">&copy; 2024 FalcoVita. All rights reserved.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const email = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

const handleLogin = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    await store.dispatch('login', {
      email: email.value,
      password: password.value
    });
    router.push('/dashboard');
  } catch (err) {
    error.value = err.response?.data?.message || 'Login failed. Please check your credentials.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.tracking-tight {
  letter-spacing: -0.025em;
}
</style>