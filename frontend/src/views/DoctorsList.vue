<template>
  <div class="d-flex min-vh-100 bg-light">
    <Sidebar />
    
    <main class="flex-grow-1 d-flex flex-column overflow-hidden">
      <!-- Header -->
      <header class="bg-white border-bottom py-3 px-4 d-flex align-items-center justify-content-between sticky-top z-2 shadow-sm">
        <div>
          <h2 class="h4 fw-bold text-dark mb-0">Find a Doctor</h2>
          <p class="text-muted small mb-0">Browse our specialists and book appointments</p>
        </div>
      </header>

      <div class="flex-grow-1 overflow-auto p-4 custom-scrollbar">
        <div class="container-fluid p-0" style="max-width: 1400px;">
          
          <!-- Search/Filter -->
          <div class="row g-3 mb-4">
            <div class="col-md-8">
              <div class="card border-0 shadow-sm">
                <div class="card-body p-2">
                  <SearchBar 
                    v-model="search" 
                    placeholder="Search by name or specialization..."
                    @clear="search = ''"
                  />
                </div>
              </div>
            </div>
            <div class="col-md-4" v-if="activeDepartmentId">
              <div class="card border-0 shadow-sm h-100 bg-primary bg-opacity-10 border-primary border-opacity-25">
                <div class="card-body p-2 d-flex align-items-center justify-content-between">
                  <div class="d-flex align-items-center gap-2 text-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                    </svg>
                    <span class="fw-bold small">Filtered by Department</span>
                  </div>
                  <button @click="clearDepartmentFilter" class="btn btn-sm btn-link text-primary p-0">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary mb-3" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted fw-medium">Loading doctors...</p>
          </div>

          <div v-else-if="filteredDoctors.length === 0" class="text-center py-5 bg-white rounded-4 border border-dashed">
            <div class="bg-light rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 64px; height: 64px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-muted">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="h5 fw-bold text-dark mb-1">No doctors found</h3>
            <p class="text-muted small">Try adjusting your search criteria.</p>
          </div>

          <div v-else class="row g-4">
            <div v-for="doctor in filteredDoctors" :key="doctor.id" class="col-md-6 col-lg-4">
              <div class="card h-100 border-0 shadow-sm hover-lift overflow-hidden">
                <div class="card-body p-4 d-flex flex-column">
                  <div class="d-flex align-items-center gap-3 mb-4">
                    <div class="rounded-circle bg-primary bg-opacity-10 text-primary d-flex align-items-center justify-content-center fw-bold fs-4" style="width: 64px; height: 64px;">
                      {{ doctor.user?.name?.charAt(0) }}
                    </div>
                    <div>
                      <h3 class="h5 fw-bold text-dark mb-1">{{ doctor.user?.name || 'Doctor' }}</h3>
                      <span class="badge bg-primary bg-opacity-10 text-primary rounded-pill fw-normal px-3">
                        {{ doctor.specialization }}
                      </span>
                    </div>
                  </div>
                  
                  <div class="mb-4 flex-grow-1">
                    <div class="d-flex align-items-center gap-2 mb-2 text-muted small">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                      <span class="fw-bold text-dark">Department:</span> {{ doctor.department?.name || 'General' }}
                    </div>
                    <div class="d-flex align-items-center gap-2 mb-2 text-muted small">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span class="fw-bold text-dark">Experience:</span> {{ doctor.experience }} years
                    </div>
                    <div class="d-flex align-items-center gap-2 text-muted small">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <span class="fw-bold text-dark">Qualifications:</span> {{ doctor.qualifications }}
                    </div>
                  </div>

                  <div class="mt-auto pt-3 border-top">
                    <button v-if="userRole === 'admin'" @click="openManageModal(doctor)" class="btn btn-outline-primary w-100 fw-bold">
                      Manage Doctor
                    </button>
                    <router-link v-else :to="`/doctors/${doctor.id}`" class="btn btn-primary w-100 fw-bold shadow-sm">
                      View Profile & Book
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Manage Doctor Modal -->
    <div v-if="showManageModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-bottom-0 pb-0">
            <h5 class="modal-title fw-bold fs-6">Manage Dr. {{ selectedDoctor?.user?.name }}</h5>
            <button type="button" class="btn-close" @click="closeManageModal"></button>
          </div>
          <div class="modal-body p-4">
            <div class="d-grid gap-2">
              <button @click="editDoctor" class="btn btn-light text-start fw-medium">
                Edit Details
              </button>
              <button @click="toggleBlock" class="btn btn-light text-start fw-medium" :class="selectedDoctor?.user?.blacklisted ? 'text-success' : 'text-warning'">
                {{ selectedDoctor?.user?.blacklisted ? 'Unblock' : 'Block' }} Doctor
              </button>
              <button @click="deleteDoctor" class="btn btn-light text-start fw-medium text-danger">
                Delete Doctor
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';
import Sidebar from '@/components/Sidebar.vue';
import SearchBar from '@/components/SearchBar.vue';
import api from '@/services/api';

const store = useStore();
const userRole = computed(() => store.getters.userRole);
const currentUser = computed(() => store.getters.currentUser);

const route = useRoute();
const router = useRouter();

const doctors = ref([]);
const loading = ref(true);
const search = ref('');
const showManageModal = ref(false);
const selectedDoctor = ref(null);
const activeDepartmentId = ref(route.query.department_id || null);

const fetchDoctors = async () => {
  try {
    loading.value = true;
    // Admin sees all (including blocked), Patients see only active (default backend behavior)
    let url = userRole.value === 'admin' ? '/doctors/?include_blocked=true' : '/doctors/';
    
    if (activeDepartmentId.value) {
      const separator = url.includes('?') ? '&' : '?';
      url += `${separator}department_id=${activeDepartmentId.value}`;
    }

    const response = await api.get(url);
    doctors.value = response.data;
  } catch (err) {
    console.error('Failed to fetch doctors', err);
  } finally {
    loading.value = false;
  }
};

const clearDepartmentFilter = () => {
  activeDepartmentId.value = null;
  router.replace({ query: {} });
  fetchDoctors();
};

const openManageModal = (doctor) => {
  selectedDoctor.value = doctor;
  showManageModal.value = true;
};

const closeManageModal = () => {
  showManageModal.value = false;
  selectedDoctor.value = null;
};

const editDoctor = () => {
  // Redirect to admin edit page or open edit modal
  // For now, let's just alert or redirect
  alert('Edit functionality is available in "Manage Doctors" page');
  closeManageModal();
};

const toggleBlock = async () => {
  if (!selectedDoctor.value) return;
  const action = selectedDoctor.value.user?.blacklisted ? 'unblock' : 'block';
  if (!confirm(`Are you sure you want to ${action} this doctor?`)) return;
  
  try {
    if (selectedDoctor.value.user?.blacklisted) {
      await api.delete(`/admin/blacklist/${selectedDoctor.value.user.id}`);
    } else {
      await api.post(`/admin/blacklist/${selectedDoctor.value.user.id}`);
    }
    alert(`Doctor ${action}ed successfully`);
    closeManageModal();
    fetchDoctors();
  } catch (err) {
    alert(`Failed to ${action} doctor`);
  }
};

const deleteDoctor = async () => {
  if (!selectedDoctor.value) return;
  if (!confirm('Are you sure you want to delete this doctor?')) return;
  try {
    await api.delete(`/admin/doctors/${selectedDoctor.value.id}`);
    alert('Doctor deleted successfully');
    closeManageModal();
    fetchDoctors();
  } catch (err) {
    alert('Failed to delete doctor');
  }
};

const filteredDoctors = computed(() => {
  if (!search.value) return doctors.value;
  const term = search.value.toLowerCase();
  return doctors.value.filter(doc => 
    (doc.user?.name && doc.user.name.toLowerCase().includes(term)) ||
    (doc.specialization && doc.specialization.toLowerCase().includes(term))
  );
});

onMounted(() => {
  fetchDoctors();
});
</script>

<style scoped>
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-5px);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.175)!important;
}

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
