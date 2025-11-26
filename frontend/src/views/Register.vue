<template>
  <div class="register-container">
    <div class="register-card">
      
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
              Join Our <br/> Healthcare Network
            </h2>
            <p>
              Create an account to manage your health journey or provide exceptional care to your patients.
            </p>
          </div>
        </div>

        <div class="brand-footer">
          <div class="testimonial-card">
            <p class="testimonial-text">"FalcoVita has revolutionized how we manage patient care. It's intuitive, fast, and secure."</p>
            <div class="testimonial-author">
              <div class="author-avatar">DR</div>
              <div>
                <p class="author-name">Dr. Sarah Mitchell</p>
                <p class="author-role">Chief of Cardiology</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Side: Register Form -->
      <div class="form-section">
        <div class="form-wrapper">
          <div class="form-header">
            <h3>Create Account</h3>
            <p>Get started with your free account</p>
          </div>

          <form @submit.prevent="handleRegister" class="register-form">
            <!-- Role Selection -->
            <div class="role-selector">
              <button 
                type="button" 
                class="role-btn"
                :class="{ 'active': role === 'patient' }"
                @click="role = 'patient'"
              >
                Patient
              </button>
              <button 
                type="button" 
                class="role-btn"
                :class="{ 'active': role === 'doctor' }"
                @click="role = 'doctor'"
              >
                Doctor
              </button>
            </div>

            <!-- Common Fields -->
            <div class="form-grid">
              <div class="form-group full-width">
                <label>Full Name</label>
                <input type="text" v-model="form.name" class="form-input" placeholder="John Doe" required />
              </div>
              
              <div class="form-group">
                <label>Email Address</label>
                <input type="email" v-model="form.email" class="form-input" placeholder="john@example.com" required />
              </div>

              <div class="form-group">
                <label>Contact Number</label>
                <input type="text" v-model="form.contact_number" class="form-input" placeholder="+1 (555) 000-0000" />
              </div>

              <div class="form-group full-width">
                <label>Password</label>
                <input type="password" v-model="form.password" class="form-input" placeholder="••••••••" required />
              </div>
            </div>

            <!-- Doctor Specific Fields -->
            <div v-if="role === 'doctor'" class="form-grid specific-fields animate-fade-in">
              <div class="form-group">
                <label>Department</label>
                <div class="relative">
                  <select v-model="form.department_id" class="form-input appearance-none cursor-pointer" required>
                    <option value="" disabled>Select Department</option>
                    <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                      {{ dept.name }}
                    </option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center px-3 pointer-events-none text-slate-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label>Experience (Years)</label>
                <input type="number" v-model="form.experience" class="form-input" placeholder="e.g. 5" required />
              </div>
              <div class="form-group full-width">
                <label>Specialization</label>
                <input type="text" v-model="form.specialization" class="form-input" placeholder="e.g. Cardiology" required />
              </div>
              <div class="form-group full-width">
                <label>Qualifications</label>
                <input type="text" v-model="form.qualifications" class="form-input" placeholder="e.g. MBBS, MD" required />
              </div>
            </div>

            <!-- Patient Specific Fields -->
            <div v-if="role === 'patient'" class="form-grid specific-fields animate-fade-in">
              <div class="form-group">
                <label>Date of Birth</label>
                <input type="date" v-model="form.dob" class="form-input" required />
              </div>
              <div class="form-group">
                <label>Medical Record Number</label>
                <input type="text" v-model="form.medical_record_number" class="form-input" placeholder="MRN-12345" required />
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
              {{ loading ? 'Creating Account...' : 'Create Account' }}
            </button>
          </form>

          <div class="form-footer">
            <p>
              Already have an account? 
              <router-link to="/login" class="sign-in-link">
                Sign In
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
import { ref, reactive, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const store = useStore();
const router = useRouter();

const role = ref('patient');
const loading = ref(false);
const error = ref('');
const departments = ref([]);

const form = reactive({
  name: '',
  email: '',
  password: '',
  contact_number: '',
  // Doctor
  department_id: '',
  specialization: '',
  qualifications: '',
  experience: '',
  // Patient
  dob: '',
  medical_record_number: '',
});

const handleRegister = async () => {
  loading.value = true;
  error.value = '';

  const payload = {
    role: role.value,
    name: form.name,
    email: form.email,
    password: form.password,
    contact_number: form.contact_number,
  };

  if (role.value === 'doctor') {
    Object.assign(payload, {
      department_id: form.department_id,
      specialization: form.specialization,
      qualifications: form.qualifications,
      experience: form.experience,
    });
  } else {
    Object.assign(payload, {
      dob: form.dob,
      contact: form.contact_number, // Backend expects 'contact' for patient
      medical_record_number: form.medical_record_number,
    });
  }

  try {
    await store.dispatch('register', payload);
    // Redirect to login after successful registration
    router.push('/login');
  } catch (err) {
    error.value = err.response?.data?.message || 'Registration failed.';
  } finally {
    loading.value = false;
  }
};

const fetchDepartments = async () => {
  try {
    const response = await api.get('/departments/');
    departments.value = response.data;
  } catch (err) {
    console.error('Failed to fetch departments', err);
  }
};

onMounted(() => {
  fetchDepartments();
});

</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--slate-50);
  padding: 1rem;
}

.register-card {
  width: 100%;
  max-width: 72rem; /* max-w-6xl */
  background-color: white;
  border-radius: 1.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 700px;
}

@media (min-width: 768px) {
  .register-card {
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
    width: 41.666667%; /* w-5/12 */
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
  background-color: rgba(99, 102, 241, 0.2);
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

.testimonial-card {
  padding: 1.5rem;
  border-radius: 1rem;
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.testimonial-text {
  font-size: 0.875rem;
  font-weight: 500;
  font-style: italic;
  margin-bottom: 1rem;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.author-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
}

.author-name {
  font-size: 0.75rem;
  font-weight: 700;
}

.author-role {
  font-size: 0.625rem;
  color: var(--primary-200);
}

/* Right Side: Form */
.form-section {
  width: 100%;
  padding: 2rem;
  background-color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow-y: auto;
  max-height: 90vh;
}

@media (min-width: 768px) {
  .form-section {
    width: 58.333333%; /* w-7/12 */
    padding: 3rem;
  }
}

.form-wrapper {
  max-width: 36rem; /* max-w-xl */
  margin: 0 auto;
  width: 100%;
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
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

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Role Selector */
.role-selector {
  display: flex;
  justify-content: center;
  padding: 0.25rem;
  background-color: var(--slate-100);
  border-radius: 0.75rem;
  margin-bottom: 1rem;
}

.role-btn {
  flex: 1;
  padding: 0.625rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s;
  color: var(--slate-500);
  cursor: pointer;
}

.role-btn:hover {
  color: var(--slate-700);
}

.role-btn.active {
  background-color: white;
  color: var(--primary-600);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

@media (min-width: 768px) {
  .form-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--slate-700);
  margin-bottom: 0.5rem;
}

.form-input {
  display: block;
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--slate-200);
  border-radius: 0.75rem;
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

.full-width {
  grid-column: 1 / -1;
}

.specific-fields {
  padding-top: 1rem;
  border-top: 1px solid var(--slate-100);
}

.submit-btn {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 0.875rem 1rem;
  border: 1px solid transparent;
  border-radius: 0.75rem;
  box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(to right, var(--primary-600), var(--primary-700));
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 1.5rem;
}

.submit-btn:hover {
  background: linear-gradient(to right, var(--primary-500), var(--primary-600));
  transform: translateY(-2px);
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

.sign-in-link {
  font-weight: 600;
  color: var(--primary-600);
  transition: color 0.2s;
}

.sign-in-link:hover {
  color: var(--primary-500);
}

.error-message {
  margin-top: 1.5rem;
  padding: 1rem;
  border-radius: 0.75rem;
  background-color: #fef2f2;
  border: 1px solid #fee2e2;
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

.animate-fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
