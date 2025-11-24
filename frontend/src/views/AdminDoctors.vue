<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-medium">Manage Doctors</h2>
        <button @click="showAddModal = true" class="btn btn-primary text-sm">
          Add New Doctor
        </button>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="container mx-auto">
          
          <!-- Enhanced Search -->
          <div class="card p-4 mb-6">
            <div class="flex gap-4">
              <input 
                type="text" 
                v-model="search" 
                placeholder="Search doctors by name, email or specialization..." 
                class="input"
                style="min-width: 400px; flex: 1;"
                @keyup.enter="search = search"
              />
              <button class="btn btn-primary">Search</button>
              <button @click="search = ''" class="btn btn-outline">Clear</button>
            </div>
          </div>

          <div v-if="loading" class="text-center py-10">
            <p class="text-muted">Loading doctors...</p>
          </div>

          <div v-else-if="displayedDoctors.length === 0" class="text-center py-10">
            <p class="text-muted">No doctors found.</p>
          </div>

          <div v-else class="card overflow-hidden">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-50 text-muted text-sm border-b border-slate-200">
                  <th class="p-4 font-medium">Name</th>
                  <th class="p-4 font-medium">Email</th>
                  <th class="p-4 font-medium">Specialization</th>
                  <th class="p-4 font-medium">Department</th>
                  <th class="p-4 font-medium">Experience</th>
                  <th class="p-4 font-medium">Status</th>
                  <th class="p-4 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="doctor in displayedDoctors" :key="doctor.id" class="border-b border-slate-100 hover:bg-slate-50">
                  <td class="p-4 font-medium">{{ doctor.user?.name || 'Doctor' }}</td>
                  <td class="p-4 text-sm">{{ doctor.user?.email }}</td>
                  <td class="p-4 text-sm">{{ doctor.specialization }}</td>
                  <td class="p-4 text-sm">{{ doctor.department?.name || 'N/A' }}</td>
                  <td class="p-4 text-sm">{{ doctor.experience }} years</td>
                  <td class="p-4">
                    <span v-if="doctor.user?.blacklisted" class="text-xs px-2 py-1 bg-red-100 text-red-600 rounded font-medium">Inactive</span>
                    <span v-else class="text-xs px-2 py-1 bg-green-100 text-green-600 rounded font-medium">Active</span>
                  </td>
                  <td class="p-4">
                    <div class="flex gap-2">
                      <button @click="editDoctor(doctor)" class="text-primary hover:underline text-sm font-medium">Edit</button>
                      <button @click="toggleBlock(doctor)" class="text-orange-500 hover:underline text-sm font-medium">
                        {{ doctor.user?.blacklisted ? 'Unblock' : 'Block' }}
                      </button>
                      <button @click="deleteDoctor(doctor.id)" class="text-red-500 hover:underline text-sm font-medium">Delete</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>
      </div>
    </main>

    <!-- Add/Edit Doctor Modal -->
    <div v-if="showAddModal" class="modal-overlay">
      <div class="card bg-white w-full max-w-2xl p-6 max-h-80vh overflow-y-auto">
        <h3 class="text-lg font-bold mb-4">{{ editingDoctor ? 'Edit Doctor' : 'Add New Doctor' }}</h3>
        
        <form @submit.prevent="saveDoctor" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="form-group">
              <label class="label">Full Name</label>
              <input v-model="doctorForm.name" class="input" required />
            </div>
            <div class="form-group">
              <label class="label">Email</label>
              <input type="email" v-model="doctorForm.email" class="input" required :disabled="editingDoctor" />
            </div>
            <div class="form-group" v-if="!editingDoctor">
              <label class="label">Password</label>
              <input type="password" v-model="doctorForm.password" class="input" required />
            </div>
            <div class="form-group">
              <label class="label">Contact Number</label>
              <input v-model="doctorForm.contact_number" class="input" required />
            </div>
            <div class="form-group">
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
              <input v-model="doctorForm.specialization" class="input" required />
            </div>
            <div class="form-group">
              <label class="label">Qualifications</label>
              <input v-model="doctorForm.qualifications" class="input" required />
            </div>
            <div class="form-group">
              <label class="label">Experience (Years)</label>
              <input type="number" v-model="doctorForm.experience" class="input" required />
            </div>
          </div>
          
          <div class="flex gap-4 mt-6">
            <button type="button" @click="closeModal" class="btn btn-outline flex-1">Cancel</button>
            <button type="submit" class="btn btn-primary flex-1">{{ editingDoctor ? 'Update' : 'Create' }} Doctor</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Sidebar from '@/components/Sidebar.vue';
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
