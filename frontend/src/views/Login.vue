<template>
  <div class="login-wrapper">
    <!-- Intro Animation Overlay -->
    <div v-if="showIntro" class="intro-overlay">
      <div class="bird-container">
        <!-- Wind Effect Lines -->
        <div class="wind-lines">
          <div class="wind-line" v-for="n in 50" :key="n"></div>
        </div>

        <!-- Flapping Bird Sprite -->
        <div class="f-bird-wrapper">
          <img src="@/assets/falcon_wings_up.png" alt="FalcoVita Bird" class="bird-mascot bird-up" :class="{ active: wingState === 'up' }" />
          <img src="@/assets/falcon_wings_down.png" alt="FalcoVita Bird" class="bird-mascot bird-down" :class="{ active: wingState === 'down' }" />
        </div>
      </div>
    </div>

    <!-- Main Login Content -->
    <div class="d-flex align-items-center justify-content-center min-vh-100 login-content" :class="{ 'fade-in-content': !showIntro }">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-6 col-lg-5 col-xl-4">
            <div class="text-center mb-4 text-white hover-scale">
               <!-- New Logo -->
              <img src="@/assets/falcon_logo.png" alt="FalcoVita Logo" class="mb-2" style="width: 80px; height: auto;">
              <h1 class="h3 fw-bold mb-1">FalcoVita</h1>
              <p class="small opacity-75">Healthcare Management System</p>
            </div>

            <div class="card glass-card border-0 rounded-4 overflow-hidden">
              <div class="card-body p-4 p-md-5">
                <div class="text-center mb-4">
                  <h2 class="h4 fw-bold text-dark">Welcome Back</h2>
                  <p class="text-muted small">Please sign in to your account</p>
                </div>

                <form @submit.prevent="handleLogin">
                  <div class="form-floating mb-3">
                    <input 
                      type="email" 
                      class="form-control bg-light-transparent" 
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
                      class="form-control bg-light-transparent" 
                      id="password" 
                      v-model="password" 
                      placeholder="Password" 
                      required
                    >
                    <label for="password">Password</label>
                  </div>

                  <div class="d-flex justify-content-end mb-4">
                    <a href="#" class="text-decoration-none text-primary small fw-semibold hover-underline">Forgot password?</a>
                  </div>

                  <button 
                    type="submit" 
                    class="btn btn-primary w-100 py-3 fw-bold shadow-sm gradient-btn"
                    :disabled="loading"
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    {{ loading ? 'Signing in...' : 'Sign In' }}
                  </button>
                </form>

                <div class="text-center mt-4 pt-3 border-top border-light">
                  <p class="text-muted small mb-0">
                    Don't have an account? 
                    <router-link to="/register" class="text-primary text-decoration-none fw-bold hover-scale-sm d-inline-block">Create an account</router-link>
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
            
            <div class="text-center mt-4 text-white-50">
              <p class="small">&copy; 2024 FalcoVita. All rights reserved.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const email = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');
const showIntro = ref(true);
const wingState = ref('up');

let wingInterval = null;

onMounted(() => {
  // Start flapping animation
  wingInterval = setInterval(() => {
    wingState.value = wingState.value === 'up' ? 'down' : 'up';
  }, 800); // Flap every 200ms

  // Show intro for 4 seconds then fade it out
  setTimeout(() => {
    showIntro.value = false;
    clearInterval(wingInterval);
  }, 4000);
});

onUnmounted(() => {
  if (wingInterval) clearInterval(wingInterval);
});

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
.login-wrapper {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background: url('@/assets/app_background.png') no-repeat center center;
  background-size: cover;
  overflow: hidden;
}

/* Intro Overlay */
.intro-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: white;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeOut 0.5s ease-in-out 3.5s forwards;
}

.bird-container {
  position: relative;
  text-align: center;
  animation: flyIn 2s ease-out, float 2s ease-in-out infinite alternate; 
}

/* Flapping Bird Styles */
.f-bird-wrapper {
  position: relative;
  width: 600px;
  height: 480px; /* Adjust based on image aspect ratio approx */
  margin: 0 auto;
}

.bird-mascot {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: auto;
  opacity: 0;
  transition: opacity 0s; /* Instant swap */
  filter: drop-shadow(0 15px 25px rgba(0,0,0,0.15));
}

.bird-mascot.active {
  opacity: 1;
}

.quote-text {
  position: absolute;
  top: 65%; /* Relative to the wrapper now */
  left: 65%; 
  transform: translate(-50%, -50%);
  width: 220px;
  font-family: 'Georgia', serif;
  font-style: italic;
  font-size: 1.1rem;
  color: #2c3e50;
  line-height: 1.3;
  text-align: center;
  text-shadow: none;
  z-index: 10;
}

/* Wind Lines Animation */
.wind-lines {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
}

.wind-line {
  position: absolute;
  background: rgba(200, 230, 255, 0.6);
  height: 2px;
  border-radius: 2px;
  animation: windMove 1s linear infinite;
}

.wind-line:nth-child(1) { top: 20%; left: -100px; width: 100px; animation-duration: 0.8s; }
.wind-line:nth-child(2) { top: 40%; left: -150px; width: 150px; animation-duration: 1.2s; animation-delay: 0.2s; }
.wind-line:nth-child(3) { top: 60%; left: -80px; width: 80px; animation-duration: 0.6s; animation-delay: 0.5s; }
.wind-line:nth-child(4) { top: 30%; left: -200px; width: 200px; animation-duration: 1.5s; animation-delay: 0.1s; }
.wind-line:nth-child(5) { top: 70%; left: -120px; width: 120px; animation-duration: 0.9s; animation-delay: 0.3s; }

@keyframes windMove {
  0% { transform: translateX(0); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateX(120vw); opacity: 0; }
}

@keyframes flyIn {
  from {
    transform: translateX(-120vw) rotate(-5deg);
  }
  to {
    transform: translateX(0) rotate(0);
  }
}

@keyframes float {
  from { transform: translateY(0); }
  to { transform: translateY(-15px); }
}

@keyframes fadeOut {
  from { opacity: 1; visibility: visible; }
  to { opacity: 0; visibility: hidden; }
}

/* Content Transitions */
.login-content {
  opacity: 0;
  transition: opacity 1s ease-in-out;
}

.fade-in-content {
  opacity: 1;
}

/* Glassmorphism Card */
.glass-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.4);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.25);
}

.bg-light-transparent {
  background-color: rgba(248, 249, 250, 0.7);
  border: 1px solid rgba(0,0,0,0.05);
}

.bg-light-transparent:focus {
  background-color: #fff;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15);
}

/* Enhancements */
.gradient-btn {
  background: linear-gradient(135deg, #0d6efd, #0099ff);
  border: none;
  transition: all 0.3s ease;
}

.gradient-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(13, 110, 253, 0.3);
}

.hover-scale {
  transition: transform 0.3s ease;
}

.hover-scale:hover {
  transform: scale(1.05);
}

.hover-scale-sm {
  transition: transform 0.2s ease;
}

.hover-scale-sm:hover {
  transform: scale(1.05);
}

.hover-underline:hover {
  text-decoration: underline !important;
}
</style>