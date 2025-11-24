<template>
  <div class="auth-container flex items-center justify-center min-h-screen py-10">
    <div class="card auth-card fade-enter-active">
      <div class="text-center mb-6">
        <h1 class="text-xl font-bold text-primary">Create Account</h1>
        <p class="text-sm text-muted">Join FalcoVita today</p>
      </div>

      <form @submit.prevent="handleRegister">
        <!-- Role Selection -->
        <div class="flex justify-center gap-4 mb-6">
          <button 
            type="button" 
            class="role-btn" 
            :class="{ active: role === 'patient' }"
            @click="role = 'patient'"
          >
            Patient
          </button>
          <button 
            type="button" 
            class="role-btn" 
            :class="{ active: role === 'doctor' }"
            @click="role = 'doctor'"
          >
            Doctor
          </button>
        </div>

        <!-- Common Fields -->
        <div class="grid grid-cols-1 gap-4 mb-4">
          <div class="form-group">
            <label class="label">Full Name</label>
            <input type="text" v-model="form.name" class="input" required />
          </div>
          
          <div class="form-group">
            <label class="label">Email Address</label>
            <input type="email" v-model="form.email" class="input" required />
          </div>

          <div class="form-group">
            <label class="label">Password</label>
            <input type="password" v-model="form.password" class="input" required />
          </div>

          <div class="form-group">
            <label class="label">Contact Number</label>
            <input type="text" v-model="form.contact_number" class="input" />
          </div>
        </div>

        <!-- Doctor Specific Fields -->
        <div v-if="role === 'doctor'" class="doctor-fields grid grid-cols-1 gap-4 mb-4 fade-enter-active">
          <div class="form-group">
            <label class="label">Department ID</label>
            <input type="number" v-model="form.department_id" class="input" required />
          </div>
          <div class="form-group">
            <label class="label">Specialization</label>
            <input type="text" v-model="form.specialization" class="input" required />
          </div>
          <div class="form-group">
            <label class="label">Qualifications</label>
            <input type="text" v-model="form.qualifications" class="input" required />
          </div>
          <div class="form-group">
            <label class="label">Experience (Years)</label>
            <input type="number" v-model="form.experience" class="input" required />
          </div>
        </div>

        <!-- Patient Specific Fields -->
        <div v-if="role === 'patient'" class="patient-fields grid grid-cols-1 gap-4 mb-4 fade-enter-active">
          <div class="form-group">
            <label class="label">Date of Birth</label>
            <input type="date" v-model="form.dob" class="input" required />
          </div>
          <div class="form-group">
            <label class="label">Medical Record Number</label>
            <input type="text" v-model="form.medical_record_number" class="input" required />
          </div>
          <!-- Optional Doctor Selection could go here -->
        </div>

        <button type="submit" class="btn btn-primary w-full mt-2" :disabled="loading">
          {{ loading ? 'Creating Account...' : 'Register' }}
        </button>
      </form>

      <div class="mt-4 text-center text-sm">
        <span class="text-muted">Already have an account? </span>
        <router-link to="/login" class="text-primary font-medium hover:underline">Sign In</router-link>
      </div>

      <div v-if="error" class="mt-4 p-2 text-sm text-center text-red-500 bg-red-50 rounded">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const role = ref('patient');
const loading = ref(false);
const error = ref('');

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
</script>

<style scoped>
.auth-container {
  background: linear-gradient(135deg, var(--primary-50) 0%, var(--primary-100) 100%);
}

.auth-card {
  width: 100%;
  max-width: 500px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: var(--shadow-xl);
}

.role-btn {
  padding: 0.5rem 1.5rem;
  border-radius: 2rem;
  border: 1px solid var(--border-color);
  font-weight: 500;
  color: var(--text-muted);
  transition: all 0.2s;
  background: white;
}

.role-btn:hover {
  border-color: var(--primary-400);
  color: var(--primary-600);
}

.role-btn.active {
  background-color: var(--primary-600);
  color: white;
  border-color: var(--primary-600);
  box-shadow: var(--shadow-md);
  transform: scale(1.05);
}
</style>
