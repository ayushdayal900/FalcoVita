<template>
  <div class="login-container">
    <div class="login-card">
      
      <!-- Left Side: Brand/Visual -->
      <div class="brand-section">
        <!-- Decorative Circles -->
        <div class="circle-1"></div>
        <div class="circle-2"></div>
        
        <div class="brand-content">
          <div class="brand-logo-wrapper">
            <div class="brand-logo">
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
              </svg>
            </div>
            <span class="brand-name">FalcoVita</span>
          </div>
          
          <div class="brand-text">
            <h2>
              Advanced Healthcare <br/> Management System
            </h2>
            <p>
              Streamline patient care, manage appointments, and access medical records with our state-of-the-art platform.
            </p>
          </div>
        </div>

        <div class="brand-footer">
          <div class="trusted-badge">
            <div class="avatars">
              <div class="avatar avatar-1"></div>
              <div class="avatar avatar-2"></div>
              <div class="avatar avatar-3"></div>
            </div>
            <p>Trusted by 500+ Medical Professionals</p>
          </div>
        </div>
      </div>

      <!-- Right Side: Login Form -->
      <div class="form-section">
        <div class="form-wrapper">
          <div class="form-header">
            <h3>Welcome Back</h3>
            <p>Please sign in to your account</p>
          </div>

          <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
              <label for="email">Email Address</label>
              <div class="input-wrapper">
                <div class="input-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                </div>
                <input 
                  type="email" 
                  id="email" 
                  v-model="email" 
                  class="form-input" 
                  placeholder="name@hospital.com" 
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <div class="password-header">
                <label for="password">Password</label>
                <a href="#" class="forgot-password">Forgot password?</a>
              </div>
              <div class="input-wrapper">
                <div class="input-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input 
                  type="password" 
                  id="password" 
                  v-model="password" 
                  class="form-input" 
                  placeholder="••••••••" 
                  required
                />
              </div>
            </div>

            <button 
              type="submit" 
              class="submit-btn"
              :disabled="loading"
            >
              <svg v-if="loading" class="spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? 'Signing in...' : 'Sign In' }}
            </button>
          </form>

          <div class="form-footer">
            <p>
              Don't have an account? 
              <router-link to="/register" class="create-account-link">
                Create an account
              </router-link>
            </p>
          </div>
          
          <div v-if="error" class="error-message">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
            <p>{{ error }}</p>
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
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--slate-50);
  padding: 1rem;
}

.login-card {
  width: 100%;
  max-width: 64rem; /* max-w-5xl */
  background-color: white;
  border-radius: 1.5rem; /* rounded-3xl */
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); /* shadow-2xl */
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 600px;
}

@media (min-width: 768px) {
  .login-card {
    flex-direction: row;
  }
}

/* Left Side: Brand/Visual */
.brand-section {
  position: relative;
  width: 100%;
  background: linear-gradient(135deg, var(--primary-600), var(--primary-900));
  padding: 3rem;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
}

@media (min-width: 768px) {
  .brand-section {
    width: 50%;
  }
}

/* Decorative Circles */
.circle-1 {
  position: absolute;
  top: 0;
  left: 0;
  width: 16rem;
  height: 16rem;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  filter: blur(40px);
}

.circle-2 {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 24rem;
  height: 24rem;
  background-color: rgba(99, 102, 241, 0.2); /* primary-500/20 */
  border-radius: 50%;
  transform: translate(33%, 33%);
  filter: blur(40px);
}

.brand-content {
  position: relative;
  z-index: 10;
}

.brand-logo-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.brand-logo {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  background-color: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.brand-logo .icon {
  width: 1.5rem;
  height: 1.5rem;
  color: white;
}

.brand-name {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.brand-text h2 {
  font-size: 2.25rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.brand-text p {
  color: var(--primary-100);
  font-size: 1.125rem;
  line-height: 1.6;
  max-width: 28rem;
}

.brand-footer {
  position: relative;
  z-index: 10;
  margin-top: 3rem;
}

.trusted-badge {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: var(--primary-200);
}

.avatars {
  display: flex;
  margin-left: -0.5rem;
}

.avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  border: 2px solid var(--primary-700);
  margin-left: -0.5rem;
}

.avatar-1 { background-color: var(--primary-400); }
.avatar-2 { background-color: var(--primary-300); }
.avatar-3 { background-color: var(--primary-200); }

/* Right Side: Form */
.form-section {
  width: 100%;
  padding: 2rem;
  background-color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

@media (min-width: 768px) {
  .form-section {
    width: 50%;
    padding: 3rem;
  }
}

.form-wrapper {
  max-width: 28rem;
  margin: 0 auto;
  width: 100%;
}

.form-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.form-header h3 {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--slate-900);
  margin-bottom: 0.5rem;
}

.form-header p {
  color: var(--slate-500);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--slate-700);
  margin-bottom: 0.5rem;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  padding-left: 0.75rem;
  display: flex;
  align-items: center;
  pointer-events: none;
}

.input-icon .icon {
  width: 1.25rem;
  height: 1.25rem;
  color: var(--slate-400);
}

.form-input {
  display: block;
  width: 100%;
  padding: 0.75rem 0.75rem 0.75rem 2.5rem; /* pl-10 */
  border: 1px solid var(--slate-200);
  border-radius: 0.75rem; /* rounded-xl */
  color: var(--slate-900);
  background-color: var(--slate-50);
  transition: all 0.2s;
  font-size: 1rem;
}

.form-input::placeholder {
  color: var(--slate-400);
}

.form-input:focus {
  outline: none;
  background-color: white;
  border-color: transparent;
  box-shadow: 0 0 0 2px var(--primary-500);
}

.password-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.password-header label {
  margin-bottom: 0;
}

.forgot-password {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--primary-600);
  text-decoration: none;
}

.forgot-password:hover {
  color: var(--primary-500);
}

.submit-btn {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 0.875rem 1rem;
  border: 1px solid transparent;
  border-radius: 0.75rem; /* rounded-xl */
  box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(to right, var(--primary-600), var(--primary-700));
  cursor: pointer;
  transition: all 0.2s;
}

.submit-btn:hover {
  background: linear-gradient(to right, var(--primary-500), var(--primary-600));
  transform: translateY(-2px);
}

.submit-btn:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--primary-500), 0 0 0 4px white;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spinner {
  animation: spin 1s linear infinite;
  margin-left: -0.25rem;
  margin-right: 0.75rem;
  height: 1.25rem;
  width: 1.25rem;
  color: white;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.form-footer {
  margin-top: 2rem;
  text-align: center;
}

.form-footer p {
  font-size: 0.875rem;
  color: var(--slate-500);
}

.create-account-link {
  font-weight: 600;
  color: var(--primary-600);
  transition: color 0.2s;
}

.create-account-link:hover {
  color: var(--primary-500);
}

.error-message {
  margin-top: 1.5rem;
  padding: 1rem;
  border-radius: 0.75rem;
  background-color: #fef2f2; /* red-50 */
  border: 1px solid #fee2e2; /* red-100 */
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.error-message .icon {
  width: 1.25rem;
  height: 1.25rem;
  color: var(--accent-500);
  margin-top: 0.125rem;
}

.error-message p {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--accent-600);
}
</style>
