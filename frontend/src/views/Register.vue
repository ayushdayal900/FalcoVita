<template>
  <div class="register-wrapper d-flex align-items-center justify-content-center min-vh-100 py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8 col-xl-6">
          <div class="text-center mb-4 text-white hover-scale">
            <h1 class="h3 fw-bold mb-1">FalcoVita</h1>
            <p class="small opacity-75">Healthcare Management System</p>
          </div>

          <div class="card glass-card border-0 rounded-4 overflow-hidden">
            <div class="card-body p-4 p-md-5">
              <div class="text-center mb-4">
                <h2 class="h4 fw-bold text-dark">Create Account</h2>
                <p class="text-muted small">Get started with your free account</p>
              </div>

              <form @submit.prevent="handleRegister">
                <!-- Role Selection -->
                <div class="d-flex justify-content-center mb-4">
                  <div class="btn-group w-100" role="group" aria-label="Role selection">
                    <input type="radio" class="btn-check" name="role" id="role-patient" value="patient" v-model="role" autocomplete="off">
                    <label class="btn btn-outline-primary py-2 fw-semibold" for="role-patient">Patient</label>

                    <input type="radio" class="btn-check" name="role" id="role-doctor" value="doctor" v-model="role" autocomplete="off">
                    <label class="btn btn-outline-primary py-2 fw-semibold" for="role-doctor">Doctor</label>
                  </div>
                </div>

                <div class="row g-3">
                  <!-- Common Fields -->
                  <div class="col-12">
                    <div class="form-floating">
                      <input type="text" class="form-control bg-light-transparent" id="name" v-model="form.name" placeholder="John Doe" required>
                      <label for="name">Full Name</label>
                    </div>
                  </div>
                  
                  <div class="col-md-6">
                    <div class="form-floating">
                      <input type="email" class="form-control bg-light-transparent" id="email" v-model="form.email" placeholder="name@example.com" required>
                      <label for="email">Email Address</label>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="form-floating">
                      <input type="text" class="form-control bg-light-transparent" id="contact" v-model="form.contact_number" placeholder="+1 (555) 000-0000">
                      <label for="contact">Contact Number</label>
                    </div>
                  </div>

                  <div class="col-12">
                    <div class="form-floating">
                      <input type="password" class="form-control bg-light-transparent" id="password" v-model="form.password" placeholder="Password" required>
                      <label for="password">Password</label>
                    </div>
                  </div>

                  <!-- Doctor Specific Fields -->
                  <template v-if="role === 'doctor'">
                    <div class="col-12 border-top pt-3 mt-3">
                      <h6 class="text-muted text-uppercase small fw-bold mb-3">Professional Details</h6>
                    </div>
                    <div class="col-md-6">
                      <div class="form-floating">
                        <select class="form-select bg-light-transparent" id="department" v-model="form.department_id" required>
                          <option value="" disabled selected>Select Department</option>
                          <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                            {{ dept.name }}
                          </option>
                        </select>
                        <label for="department">Department</label>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="form-floating">
                        <input type="number" class="form-control bg-light-transparent" id="experience" v-model="form.experience" placeholder="Years" required>
                        <label for="experience">Experience (Years)</label>
                      </div>
                    </div>
                    <div class="col-12">
                      <div class="form-floating">
                        <input type="text" class="form-control bg-light-transparent" id="specialization" v-model="form.specialization" placeholder="Cardiology" required>
                        <label for="specialization">Specialization</label>
                      </div>
                    </div>
                    <div class="col-12">
                      <div class="form-floating">
                        <input type="text" class="form-control bg-light-transparent" id="qualifications" v-model="form.qualifications" placeholder="MBBS, MD" required>
                        <label for="qualifications">Qualifications</label>
                      </div>
                    </div>
                  </template>

                  <!-- Patient Specific Fields -->
                  <template v-if="role === 'patient'">
                    <div class="col-12 border-top pt-3 mt-3">
                      <h6 class="text-muted text-uppercase small fw-bold mb-3">Medical Details</h6>
                    </div>
                    <div class="col-md-6">
                      <div class="form-floating">
                        <input type="date" class="form-control bg-light-transparent" id="dob" v-model="form.dob" required>
                        <label for="dob">Date of Birth</label>
                      </div>
                    </div>
                  </template>
                </div>

                <button 
                  type="submit" 
                  class="btn btn-primary w-100 py-3 fw-bold shadow-sm mt-4 gradient-btn"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  {{ loading ? 'Creating Account...' : 'Create Account' }}
                </button>
              </form>

              <div class="text-center mt-4 pt-3 border-top border-light">
                <p class="text-muted small mb-0">
                  Already have an account? 
                  <router-link to="/login" class="text-primary text-decoration-none fw-bold hover-scale-sm d-inline-block">Sign In</router-link>
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
  department_id: '',
  specialization: '',
  qualifications: '',
  experience: '',
  dob: '',
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
      contact: form.contact_number,
    });
  }

  try {
    await store.dispatch('register', payload);
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
.register-wrapper {
  background: url('@/assets/app_background.png') no-repeat center center;
  background-size: cover;
  background-attachment: fixed; /* Parallax-like effect */
}

/* Glassmorphism Card (Shared with Login) */
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
</style>
