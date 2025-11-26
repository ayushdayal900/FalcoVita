<template>
  <div class="dashboard-layout flex h-screen overflow-hidden bg-slate-50">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden relative">
      <!-- Top Header -->
      <header class="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10">
        <div>
          <h2 class="text-2xl font-bold text-slate-800">Manage Doctors</h2>
          <p class="text-sm text-slate-500">View and manage medical staff</p>
        </div>
        <button @click="showAddModal = true" class="btn bg-primary-600 hover:bg-primary-700 text-white shadow-lg shadow-primary-500/30 flex items-center gap-2 px-4 py-2.5 rounded-xl transition-all hover:-translate-y-0.5">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Add New Doctor
        </button>
      </header>

      <div class="flex-1 overflow-y-auto p-8 custom-scrollbar">
        <div class="max-w-7xl mx-auto">
          
          <!-- Search & Filter Bar -->
          <SearchBar 
            v-model="search" 
            placeholder="Search by name, email or specialization..." 
            @clear="search = ''"
            class="mb-6"
          />

          <!-- Loading State -->
          <div v-if="loading" class="flex flex-col items-center justify-center py-20">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4"></div>
            <p class="text-slate-500 font-medium">Loading doctors...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="displayedDoctors.length === 0" class="flex flex-col items-center justify-center py-20 bg-white rounded-3xl border border-dashed border-slate-300">
            <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4 text-slate-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-bold text-slate-800 mb-1">No doctors found</h3>
            <p class="text-slate-500">Try adjusting your search or add a new doctor.</p>
          </div>

          <!-- Doctors Table -->
          <div v-else class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="bg-slate-50/50 border-b border-slate-200">
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Doctor</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Specialization</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Department</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Experience</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="doctor in displayedDoctors" :key="doctor.id" class="hover:bg-slate-50/80 transition-colors group">
                    <td class="p-5">
                      <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-primary-100 to-primary-200 text-primary-700 flex items-center justify-center font-bold shadow-sm">
                          {{ doctor.user?.name?.charAt(0) }}
                        </div>
                        <div>
                          <p class="font-bold text-slate-800">{{ doctor.user?.name || 'Unknown' }}</p>
                          <p class="text-xs text-slate-500">{{ doctor.user?.email }}</p>
                        </div>
                      </div>
                    </td>
                    <td class="p-5">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700">
                        {{ doctor.specialization }}
                      </span>
                    </td>
                    <td class="p-5 text-sm text-slate-600 font-medium">{{ doctor.department?.name || 'N/A' }}</td>
                    <td class="p-5 text-sm text-slate-600">{{ doctor.experience }} years</td>
                    <td class="p-5">
                      <span v-if="doctor.user?.blacklisted" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
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
                        <button @click="editDoctor(doctor)" class="p-2 text-slate-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all" title="Edit">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button @click="toggleBlock(doctor)" 
                                class="p-2 rounded-lg transition-all"
                                :class="doctor.user?.blacklisted ? 'text-emerald-500 hover:bg-emerald-50' : 'text-orange-400 hover:text-orange-600 hover:bg-orange-50'"
                                :title="doctor.user?.blacklisted ? 'Unblock' : 'Block'">
                          <svg v-if="doctor.user?.blacklisted" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                          </svg>
                        </button>
                        <button @click="deleteDoctor(doctor.id)" class="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all" title="Delete">
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
              <p>Showing <span class="font-medium text-slate-900">{{ displayedDoctors.length }}</span> results</p>
              <div class="flex gap-2">
                <button class="px-3 py-1 border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-50" disabled>Previous</button>
                <button class="px-3 py-1 border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-50" disabled>Next</button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Add/Edit Doctor Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h3 class="text-xl font-bold text-slate-800">{{ editingDoctor ? 'Edit Doctor Profile' : 'Add New Doctor' }}</h3>
          <button @click="closeModal" class="text-slate-400 hover:text-slate-600 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto custom-scrollbar">
          <form @submit.prevent="saveDoctor" class="space-y-5">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div class="form-group">
                <label class="label">Full Name</label>
                <input v-model="doctorForm.name" class="input" placeholder="Dr. John Doe" required />
              </div>
              <div class="form-group">
                <label class="label">Email Address</label>
                <input type="email" v-model="doctorForm.email" class="input" placeholder="doctor@hospital.com" required :disabled="editingDoctor" />
              </div>
              <div class="form-group" v-if="!editingDoctor">
                <label class="label">Password</label>
                <input type="password" v-model="doctorForm.password" class="input" placeholder="••••••••" required />
              </div>
              <div class="form-group">
                <label class="label">Contact Number</label>
                <input v-model="doctorForm.contact_number" class="input" placeholder="+1 234 567 890" required />
              </div>
              <div class="form-group md:col-span-2">
                <label class="label">Department</label>
                <select v-model="doctorForm.department_id" class="input" required>
                  <option value="">Select Department</option>
                  <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                    {{ dept.name }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label class="label">Specialization</label>
                <input v-model="doctorForm.specialization" class="input" placeholder="e.g. Cardiology" required />
              </div>
              <div class="form-group">
                <label class="label">Experience (Years)</label>
                <input type="number" v-model="doctorForm.experience" class="input" placeholder="e.g. 10" required />
              </div>
              <div class="form-group md:col-span-2">
                <label class="label">Qualifications</label>
                <input v-model="doctorForm.qualifications" class="input" placeholder="e.g. MBBS, MD, PhD" required />
              </div>
            </div>
            
            <div class="flex gap-4 pt-4 border-t border-slate-100 mt-4">
              <button type="button" @click="closeModal" class="btn btn-outline flex-1 rounded-xl">Cancel</button>
              <button type="submit" class="btn btn-primary flex-1 rounded-xl shadow-lg shadow-primary-500/20">
                {{ editingDoctor ? 'Update Profile' : 'Create Account' }}
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
    alert('Failed to delete doctor');
  }
};

onMounted(() => {
  fetchDoctors();
  fetchDepartments();
});
</script>
