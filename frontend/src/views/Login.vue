<template>
  <div class="auth-container flex items-center justify-center h-screen">
    <div class="card auth-card fade-enter-active">
      <div class="text-center mb-6">
        <h1 class="text-xl font-bold text-primary">FalcoVita Hospital</h1>
        <p class="text-sm text-muted">Sign in to your account</p>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group mb-4">
          <label class="label" for="email">Email Address</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            class="input" 
            placeholder="name@example.com" 
            required
          />
        </div>

        <div class="form-group mb-6">
          <label class="label" for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            class="input" 
            placeholder="••••••••" 
            required
          />
        </div>

        <button type="submit" class="btn btn-primary w-full" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <div class="mt-4 text-center text-sm">
        <span class="text-muted">Don't have an account? </span>
        <router-link to="/register" class="text-primary font-medium hover:underline">Register</router-link>
      </div>
      
      <div v-if="error" class="mt-4 p-2 text-sm text-center text-red-500 bg-red-50 rounded">
        {{ error }}
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
    error.value = err.response?.data?.message || 'Login failed. Please try again.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-container {
  background: linear-gradient(135deg, var(--primary-50) 0%, var(--primary-100) 100%);
  padding: 2rem;
}

.auth-card {
  width: 100%;
  max-width: 520px;
  padding: 3rem 2.5rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}
</style>
