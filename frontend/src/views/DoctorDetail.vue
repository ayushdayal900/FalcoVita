<template>
  <div class="d-flex min-vh-100 bg-light">
    <Sidebar />
    
    <main class="flex-grow-1 d-flex flex-column overflow-hidden">
      <!-- Header -->
      <header class="bg-white border-bottom py-3 px-4 d-flex align-items-center justify-content-between sticky-top z-2 shadow-sm">
        <div class="d-flex align-items-center gap-3">
          <router-link 
            to="/doctors"
            class="btn btn-light btn-sm rounded-circle d-flex align-items-center justify-content-center"
            style="width: 32px; height: 32px;"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </router-link>
          <div>
            <h2 class="h5 fw-bold text-dark mb-0">Doctor Profile</h2>
          </div>
        </div>
      </header>

      <div class="flex-grow-1 overflow-auto p-4 custom-scrollbar">
        <div class="container-fluid p-0" style="max-width: 1000px;">
          
          <!-- Doctor Profile Card -->
          <div class="card border-0 shadow-sm mb-4 overflow-hidden">
            <div class="card-body p-0">
              <div class="bg-primary bg-gradient p-5 text-white">
                <div class="d-flex align-items-center gap-4">
                  <div class="bg-white rounded-circle p-1 shadow-lg">
                    <div class="bg-light rounded-circle d-flex align-items-center justify-content-center text-primary fw-bold display-4" style="width: 100px; height: 100px;">
                      {{ doctor.name?.charAt(0) }}
                    </div>
                  </div>
                  <div>
                    <h1 class="h2 fw-bold mb-1">{{ doctor.name }}</h1>
                    <p class="text-white-50 mb-2 fs-5">{{ doctor.specialization }}</p>
                    <div class="d-flex gap-3 text-white-50 small">
                      <span class="d-flex align-items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                        </svg>
                        {{ doctor.experience }} Years Experience
                      </span>
                      <span class="d-flex align-items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                        </svg>
                        {{ doctor.qualifications }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Availability Slots Component -->
          <DoctorSlots 
            v-if="doctor.id"
            :doctorId="doctor.id" 
            :patientId="patientId" 
            :departmentId="doctor.department_id" 
          />

        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import api from "@/services/api";
import Sidebar from '@/components/Sidebar.vue';
import DoctorSlots from "@/components/DoctorSlots.vue";

const route = useRoute();
const store = useStore();

const doctorId = Number(route.params.id);
const patientId = store.getters.currentUser?.id;

const doctor = ref({});

const loadDoctor = async () => {
  try {
    const res = await api.get(`/doctors/${doctorId}`);
    doctor.value = {
      id: res.data.id,
      name: res.data.user?.name,
      specialization: res.data.specialization,
      qualifications: res.data.qualifications,
      experience: res.data.experience,
      department_id: res.data.department_id
    };
  } catch (err) {
    console.error("Failed to load doctor info", err);
  }
};

onMounted(() => {
  loadDoctor();
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
