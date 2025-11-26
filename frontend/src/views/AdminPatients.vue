<template>
  <div class="dashboard-layout flex h-screen overflow-hidden bg-slate-50">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden relative">
      <!-- Top Header -->
      <header class="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10">
        <div>
          <h2 class="text-2xl font-bold text-slate-800">Manage Patients</h2>
          <p class="text-sm text-slate-500">View and manage patient records</p>
        </div>
      </header>

      <div class="flex-1 overflow-y-auto p-8 custom-scrollbar">
        <div class="max-w-7xl mx-auto">
          
          <!-- Search & Filter Bar -->
          <SearchBar 
            v-model="search" 
            placeholder="Search by name, email or medical record..." 
            @clear="search = ''"
            class="mb-6"
          />

          <!-- Loading State -->
          <div v-if="loading" class="flex flex-col items-center justify-center py-20">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600 mb-4"></div>
            <p class="text-slate-500 font-medium">Loading patients...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="displayedPatients.length === 0" class="flex flex-col items-center justify-center py-20 bg-white rounded-3xl border border-dashed border-slate-300">
            <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4 text-slate-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-bold text-slate-800 mb-1">No patients found</h3>
            <p class="text-slate-500">Try adjusting your search criteria.</p>
          </div>

          <!-- Patients Table -->
          <div v-else class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="bg-slate-50/50 border-b border-slate-200">
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Patient</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Medical Record #</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Date of Birth</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Contact</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="patient in displayedPatients" :key="patient.id" class="hover:bg-slate-50/80 transition-colors group">
                    <td class="p-5">
                      <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-100 to-emerald-200 text-emerald-700 flex items-center justify-center font-bold shadow-sm">
                          {{ patient.user?.name?.charAt(0) }}
                        </div>
                        <div>
                          <p class="font-bold text-slate-800">{{ patient.user?.name || 'Unknown' }}</p>
                          <p class="text-xs text-slate-500">{{ patient.user?.email }}</p>
                        </div>
                      </div>
                    </td>
                    <td class="p-5 text-sm font-mono text-slate-600">{{ patient.medical_record_number }}</td>
                    <td class="p-5 text-sm text-slate-600">{{ patient.dob ? new Date(patient.dob).toLocaleDateString() : '-' }}</td>
                    <td class="p-5 text-sm text-slate-600">{{ patient.contact }}</td>
                    <td class="p-5">
                      <span v-if="patient.user?.blacklisted" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        <span class="w-1.5 h-1.5 rounded-full bg-red-600 mr-1.5"></span>
                        Deactivated
                      </span>
                      <span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-600 mr-1.5"></span>
                        Active
                      </span>
                    </td>
                    <td class="p-5 text-right">
                      <div class="flex items-center justify-end gap-2">
                        <button @click="editPatient(patient)" class="p-2 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-all" title="Edit">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button @click="toggleBlock(patient)" 
                                class="p-2 rounded-lg transition-all"
                                :class="patient.user?.blacklisted ? 'text-emerald-500 hover:bg-emerald-50' : 'text-orange-400 hover:text-orange-600 hover:bg-orange-50'"
                                :title="patient.user?.blacklisted ? 'Unblock' : 'Block'">
                          <svg v-if="patient.user?.blacklisted" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                          </svg>
                        </button>
                        <button @click="deletePatient(patient.id)" class="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all" title="Delete">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Pagination (Visual Only for now) -->
            <div class="p-4 border-t border-slate-100 flex items-center justify-between text-sm text-slate-500">
              <p>Showing <span class="font-medium text-slate-900">{{ displayedPatients.length }}</span> results</p>
              <div class="flex gap-2">
                <button class="px-3 py-1 border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-50" disabled>Previous</button>
                <button class="px-3 py-1 border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-50" disabled>Next</button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Edit Patient Modal -->
    <div v-if="showEditModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h3 class="text-xl font-bold text-slate-800">Edit Patient</h3>
          <button @click="closeModal" class="text-slate-400 hover:text-slate-600 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6">
          <form @submit.prevent="savePatient" class="space-y-5">
            <div class="form-group">
              <label class="label">Full Name</label>
              <input v-model="patientForm.name" class="input" required />
            </div>
            <div class="form-group">
              <label class="label">Email Address</label>
              <input type="email" v-model="patientForm.email" class="input" required />
            </div>
            <div class="form-group">
              <label class="label">Contact Number</label>
              <input v-model="patientForm.contact" class="input" required />
            </div>
            <div class="form-group">
              <label class="label">Medical Record Number</label>
              <input v-model="patientForm.medical_record_number" class="input" required />
            </div>
            <div class="form-group">
              <label class="label">Date of Birth</label>
              <input type="date" v-model="patientForm.dob" class="input" required />
            </div>
            
            <div class="flex gap-4 pt-4 border-t border-slate-100 mt-4">
              <button type="button" @click="closeModal" class="btn btn-outline flex-1 rounded-xl">Cancel</button>
              <button type="submit" class="btn btn-primary flex-1 rounded-xl shadow-lg shadow-primary-500/20">
                Update Patient
              </button>
            </div>
          </form>
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
