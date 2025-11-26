<template>
  <div class="d-flex min-vh-100 bg-light">
    <Sidebar />
    
    <main class="flex-grow-1 d-flex flex-column overflow-hidden">
      <!-- Top Header -->
      <header class="bg-white border-bottom py-3 px-4 d-flex align-items-center justify-content-between sticky-top z-2 shadow-sm">
        <div>
          <h2 class="h4 fw-bold text-dark mb-0">Manage Doctors</h2>
          <p class="text-muted small mb-0">View and manage medical staff</p>
        </div>
        <button @click="showAddModal = true" class="btn btn-primary d-flex align-items-center gap-2 shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Add New Doctor
        </button>
      </header>

      <div class="flex-grow-1 overflow-auto p-4 custom-scrollbar">
        <div class="container-fluid p-0" style="max-width: 1400px;">
          
          <!-- Search & Filter Bar -->
          <div class="card border-0 shadow-sm mb-4" style="max-width: 600px;">
            <div class="card-body p-2">
              <SearchBar 
                v-model="search" 
                placeholder="Search by name, email or specialization..." 
                @clear="search = ''"
              />
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary mb-3" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted fw-medium">Loading doctors...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="displayedDoctors.length === 0" class="text-center py-5 bg-white rounded-4 border border-dashed">
            <div class="bg-light rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 64px; height: 64px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-muted">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="h5 fw-bold text-dark mb-1">No doctors found</h3>
            <p class="text-muted small">Try adjusting your search or add a new doctor.</p>
          </div>

          <!-- Doctors Table -->
          <div v-else class="card border-0 shadow-sm overflow-hidden">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="bg-light">
                  <tr>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Doctor</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Specialization</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Department</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Experience</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Status</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0 text-end">Actions</th>
                  </tr>
                </thead>
                <tbody class="border-top-0">
                  <tr v-for="doctor in displayedDoctors" :key="doctor.id">
                    <td class="px-4 py-3 border-bottom-0">
                      <div class="d-flex align-items-center gap-3">
                        <div class="rounded-circle bg-primary bg-opacity-10 text-primary d-flex align-items-center justify-content-center fw-bold" style="width: 40px; height: 40px;">
                          {{ doctor.user?.name?.charAt(0) }}
                        </div>
                        <div>
                          <p class="fw-bold text-dark mb-0">{{ doctor.user?.name || 'Unknown' }}</p>
                          <p class="text-muted small mb-0">{{ doctor.user?.email }}</p>
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-3 border-bottom-0">
                      <span class="badge bg-primary bg-opacity-10 text-primary rounded-pill fw-normal px-3">
                        {{ doctor.specialization }}
                      </span>
                    </td>
                    <td class="px-4 py-3 border-bottom-0 text-muted fw-medium">{{ doctor.department?.name || 'N/A' }}</td>
                    <td class="px-4 py-3 border-bottom-0 text-muted">{{ doctor.experience }} years</td>
                    <td class="px-4 py-3 border-bottom-0">
                      <span v-if="doctor.user?.blacklisted" class="badge bg-danger bg-opacity-10 text-danger rounded-pill fw-normal px-3 d-inline-flex align-items-center gap-1">
                        <span class="d-inline-block rounded-circle bg-danger" style="width: 6px; height: 6px;"></span>
                        Deactivated
                      </span>
                      <span v-else class="badge bg-success bg-opacity-10 text-success rounded-pill fw-normal px-3 d-inline-flex align-items-center gap-1">
                        <span class="d-inline-block rounded-circle bg-success" style="width: 6px; height: 6px;"></span>
                        Active
                      </span>
                    </td>
                    <td class="px-4 py-3 border-bottom-0 text-end">
                      <div class="d-flex align-items-center justify-content-end gap-2">
                        <button @click="editDoctor(doctor)" class="btn btn-sm btn-light text-primary" title="Edit">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button @click="toggleBlock(doctor)" 
                                class="btn btn-sm btn-light"
                                :class="doctor.user?.blacklisted ? 'text-success' : 'text-warning'"
                                :title="doctor.user?.blacklisted ? 'Unblock' : 'Block'">
                          <svg v-if="doctor.user?.blacklisted" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                          </svg>
                        </button>
                        <button @click="deleteDoctor(doctor.id)" class="btn btn-sm btn-light text-danger" title="Delete">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Add/Edit Doctor Modal -->
    <div v-if="showAddModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-bottom-0 pb-0">
            <h5 class="modal-title fw-bold">{{ editingDoctor ? 'Edit Doctor Profile' : 'Add New Doctor' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          
          <div class="modal-body p-4">
            <form @submit.prevent="saveDoctor">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label fw-bold small">Full Name</label>
                  <input v-model="doctorForm.name" class="form-control" placeholder="Dr. John Doe" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small">Email Address</label>
                  <input type="email" v-model="doctorForm.email" class="form-control" placeholder="doctor@hospital.com" required :disabled="editingDoctor" />
                </div>
                <div class="col-md-6" v-if="!editingDoctor">
                  <label class="form-label fw-bold small">Password</label>
                  <input type="password" v-model="doctorForm.password" class="form-control" placeholder="••••••••" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small">Contact Number</label>
                  <input v-model="doctorForm.contact_number" class="form-control" placeholder="+1 234 567 890" required />
                </div>
                <div class="col-12">
                  <label class="form-label fw-bold small">Department</label>
                  <select v-model="doctorForm.department_id" class="form-select" required>
                    <option value="">Select Department</option>
                    <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                      {{ dept.name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small">Specialization</label>
                  <input v-model="doctorForm.specialization" class="form-control" placeholder="e.g. Cardiology" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small">Experience (Years)</label>
                  <input type="number" v-model="doctorForm.experience" class="form-control" placeholder="e.g. 10" required />
                </div>
                <div class="col-12">
                  <label class="form-label fw-bold small">Qualifications</label>
                  <input v-model="doctorForm.qualifications" class="form-control" placeholder="e.g. MBBS, MD, PhD" required />
                </div>
              </div>
              
              <div class="d-flex justify-content-end gap-2 pt-4 border-top mt-4">
                <button type="button" @click="closeModal" class="btn btn-light">Cancel</button>
                <button type="submit" class="btn btn-primary fw-bold px-4">
                  {{ editingDoctor ? 'Update Profile' : 'Create Account' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Sidebar from '@/components/Sidebar.vue';
import SearchBar from '@/components/SearchBar.vue';
import api from '@/services/api';

const doctors = ref([]);
const departments = ref([]);
const loading = ref(true);
const search = ref('');
const showAddModal = ref(false);
const editingDoctor = ref(null);

const doctorForm = ref({
  name: '',
  email: '',
  password: '',
  contact_number: '',
  department_id: '',
  specialization: '',
  qualifications: '',
  experience: ''
});

const fetchDoctors = async () => {
  try {
    const response = await api.get('/doctors/?include_blocked=true');
    doctors.value = response.data;
  } catch (err) {
    console.error('Failed to fetch doctors', err);
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

const displayedDoctors = computed(() => {
  if (!search.value) return doctors.value;
  const term = search.value.toLowerCase();
  return doctors.value.filter(doc => 
    (doc.user?.name?.toLowerCase().includes(term)) ||
    (doc.specialization?.toLowerCase().includes(term)) ||
    (doc.user?.email?.toLowerCase().includes(term))
  );
});

const editDoctor = (doctor) => {
  editingDoctor.value = doctor;
  doctorForm.value = {
    name: doctor.user?.name || '',
    email: doctor.user?.email || '',
    password: '',
    contact_number: doctor.user?.contact_number || '',
    department_id: doctor.department_id,
    specialization: doctor.specialization,
    qualifications: doctor.qualifications,
    experience: doctor.experience
  };
  showAddModal.value = true;
};

const closeModal = () => {
  showAddModal.value = false;
  editingDoctor.value = null;
  doctorForm.value = {
    name: '',
    email: '',
    password: '',
    contact_number: '',
    department_id: '',
    specialization: '',
    qualifications: '',
    experience: ''
  };
};

const saveDoctor = async () => {
  try {
    if (editingDoctor.value) {
      // Update existing doctor
      await api.put(`/admin/doctors/${editingDoctor.value.id}`, doctorForm.value);
      alert('Doctor updated successfully');
    } else {
      // Create new doctor
      await api.post('/admin/doctors', doctorForm.value);
      alert('Doctor created successfully');
    }
    closeModal();
    fetchDoctors();
  } catch (err) {
    alert(err.response?.data?.message || 'Failed to save doctor');
  }
};

const toggleBlock = async (doctor) => {
  const action = doctor.user?.blacklisted ? 'unblock' : 'block';
  if (!confirm(`Are you sure you want to ${action} this doctor?`)) return;
  
  try {
    if (doctor.user?.blacklisted) {
      await api.delete(`/admin/blacklist/${doctor.user.id}`);
    } else {
      await api.post(`/admin/blacklist/${doctor.user.id}`);
    }
    alert(`Doctor ${action}ed successfully`);
    fetchDoctors();
  } catch (err) {
    alert(`Failed to ${action} doctor`);
  }
};

const deleteDoctor = async (id) => {
  if (!confirm('Are you sure you want to delete this doctor?')) return;
  try {
    await api.delete(`/admin/doctors/${id}`);
    alert('Doctor deleted successfully');
    fetchDoctors();
  } catch (err) {
    alert(err.response?.data?.message || 'Failed to delete doctor');
  }
};

onMounted(() => {
  fetchDoctors();
  fetchDepartments();
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.1);
  border-radius: 10px;
}

.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.2);
}
</style>
