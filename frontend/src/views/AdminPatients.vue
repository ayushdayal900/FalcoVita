<template>
  <div class="d-flex min-vh-100 bg-light">
    <Sidebar />
    
    <main class="flex-grow-1 d-flex flex-column overflow-hidden">
      <!-- Top Header -->
      <header class="bg-white border-bottom py-3 px-4 d-flex align-items-center justify-content-between sticky-top z-2 shadow-sm">
        <div>
          <h2 class="h4 fw-bold text-dark mb-0">Manage Patients</h2>
          <p class="text-muted small mb-0">View and manage patient records</p>
        </div>
      </header>

      <div class="flex-grow-1 overflow-auto p-4 custom-scrollbar">
        <div class="container-fluid p-0" style="max-width: 1400px;">
          
          <!-- Search & Filter Bar -->
          <div class="card border-0 shadow-sm mb-4" style="max-width: 600px;">
            <div class="card-body p-2">
              <SearchBar 
                v-model="search" 
                placeholder="Search by name, email or medical record..." 
                @clear="search = ''"
              />
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary mb-3" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted fw-medium">Loading patients...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="displayedPatients.length === 0" class="text-center py-5 bg-white rounded-4 border border-dashed">
            <div class="bg-light rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 64px; height: 64px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-muted">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
            <h3 class="h5 fw-bold text-dark mb-1">No patients found</h3>
            <p class="text-muted small">Try adjusting your search criteria.</p>
          </div>

          <!-- Patients Table -->
          <div v-else class="card border-0 shadow-sm overflow-hidden">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="bg-light">
                  <tr>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Patient</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Medical Record #</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Date of Birth</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Contact</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Status</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0 text-end">Actions</th>
                  </tr>
                </thead>
                <tbody class="border-top-0">
                  <tr v-for="patient in displayedPatients" :key="patient.id">
                    <td class="px-4 py-3 border-bottom-0">
                      <div class="d-flex align-items-center gap-3">
                        <div class="rounded-circle bg-success bg-opacity-10 text-success d-flex align-items-center justify-content-center fw-bold" style="width: 40px; height: 40px;">
                          {{ patient.user?.name?.charAt(0) }}
                        </div>
                        <div>
                          <p class="fw-bold text-dark mb-0">{{ patient.user?.name || 'Unknown' }}</p>
                          <p class="text-muted small mb-0">{{ patient.user?.email }}</p>
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-3 border-bottom-0 font-monospace text-muted">{{ patient.medical_record_number }}</td>
                    <td class="px-4 py-3 border-bottom-0 text-muted">{{ patient.dob ? new Date(patient.dob).toLocaleDateString() : '-' }}</td>
                    <td class="px-4 py-3 border-bottom-0 text-muted">{{ patient.contact }}</td>
                    <td class="px-4 py-3 border-bottom-0">
                      <span v-if="patient.user?.blacklisted" class="badge bg-danger bg-opacity-10 text-danger rounded-pill fw-normal px-3 d-inline-flex align-items-center gap-1">
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
                        <button @click="editPatient(patient)" class="btn btn-sm btn-light text-primary" title="Edit">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button @click="toggleBlock(patient)" 
                                class="btn btn-sm btn-light"
                                :class="patient.user?.blacklisted ? 'text-success' : 'text-warning'"
                                :title="patient.user?.blacklisted ? 'Unblock' : 'Block'">
                          <svg v-if="patient.user?.blacklisted" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                          </svg>
                        </button>
                        <button @click="deletePatient(patient.id)" class="btn btn-sm btn-light text-danger" title="Delete">
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

    <!-- Edit Patient Modal -->
    <div v-if="showEditModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-bottom-0 pb-0">
            <h5 class="modal-title fw-bold">Edit Patient</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          
          <div class="modal-body p-4">
            <form @submit.prevent="savePatient">
              <div class="mb-3">
                <label class="form-label fw-bold small">Full Name</label>
                <input v-model="patientForm.name" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold small">Email Address</label>
                <input type="email" v-model="patientForm.email" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold small">Contact Number</label>
                <input v-model="patientForm.contact" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold small">Medical Record Number</label>
                <input v-model="patientForm.medical_record_number" class="form-control" required />
              </div>
              <div class="mb-4">
                <label class="form-label fw-bold small">Date of Birth</label>
                <input type="date" v-model="patientForm.dob" class="form-control" required />
              </div>
              
              <div class="d-flex justify-content-end gap-2 pt-4 border-top mt-4">
                <button type="button" @click="closeModal" class="btn btn-light">Cancel</button>
                <button type="submit" class="btn btn-primary fw-bold px-4">
                  Update Patient
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
import { useRouter } from 'vue-router';
import Sidebar from '@/components/Sidebar.vue';
import SearchBar from '@/components/SearchBar.vue';
import api from '@/services/api';

const router = useRouter();
const patients = ref([]);
const loading = ref(true);
const search = ref('');
const showEditModal = ref(false);
const editingPatient = ref(null);

const patientForm = ref({
  name: '',
  email: '',
  contact: '',
  medical_record_number: '',
  dob: ''
});

const fetchPatients = async () => {
  try {
    const response = await api.get('/patients/');
    patients.value = response.data;
  } catch (err) {
    console.error('Failed to fetch patients', err);
  } finally {
    loading.value = false;
  }
};

const displayedPatients = computed(() => {
  if (!search.value) return patients.value;
  const term = search.value.toLowerCase();
  return patients.value.filter(p => 
    (p.user?.name?.toLowerCase().includes(term)) ||
    (p.medical_record_number?.toLowerCase().includes(term)) ||
    (p.user?.email?.toLowerCase().includes(term))
  );
});

const editPatient = (patient) => {
  editingPatient.value = patient;
  patientForm.value = {
    name: patient.user?.name || '',
    email: patient.user?.email || '',
    contact: patient.contact || '',
    medical_record_number: patient.medical_record_number || '',
    dob: patient.dob ? new Date(patient.dob).toISOString().split('T')[0] : ''
  };
  showEditModal.value = true;
};

const closeModal = () => {
  showEditModal.value = false;
  editingPatient.value = null;
  patientForm.value = {
    name: '',
    email: '',
    contact: '',
    medical_record_number: '',
    dob: ''
  };
};

const savePatient = async () => {
  try {
    if (editingPatient.value) {
      await api.put(`/api/patients/${editingPatient.value.id}`, patientForm.value);
      alert('Patient updated successfully');
      closeModal();
      fetchPatients();
    }
  } catch (err) {
    alert(err.response?.data?.message || 'Failed to update patient');
  }
};

const toggleBlock = async (patient) => {
  const action = patient.user?.blacklisted ? 'unblock' : 'block';
  if (!confirm(`Are you sure you want to ${action} this patient?`)) return;
  
  try {
    if (patient.user?.blacklisted) {
      await api.delete(`/admin/blacklist/${patient.user.id}`);
    } else {
      await api.post(`/admin/blacklist/${patient.user.id}`);
    }
    alert(`Patient ${action}ed successfully`);
    fetchPatients();
  } catch (err) {
    alert(`Failed to ${action} patient`);
  }
};

const deletePatient = async (id) => {
  if (!confirm('Are you sure you want to delete this patient?')) return;
  try {
    await api.delete(`/admin/patients/${id}`);
    alert('Patient deleted successfully');
    fetchPatients();
  } catch (err) {
    alert('Failed to delete patient');
  }
};

onMounted(() => {
  fetchPatients();
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
