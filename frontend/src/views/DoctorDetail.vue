<template>
  <div class="p-6">
    <router-link 
      to="/doctors"
      class="text-blue-600 hover:underline text-sm"
    >
      ← Back to Doctors
    </router-link>

    <!-- Doctor Profile Card -->
    <div class="card p-6 mt-4 shadow-sm">
      <div class="flex items-center gap-6">

        <div class="w-20 h-20 bg-slate-200 rounded-full flex items-center justify-center">
          <span class="text-3xl">👨‍⚕️</span>
        </div>

        <div>
          <h2 class="text-2xl font-bold">{{ doctor.name }}</h2>
          <p class="text-muted">{{ doctor.specialization }}</p>
          <p class="text-sm">
            {{ doctor.qualifications }} • {{ doctor.experience }} years experience
          </p>
        </div>

      </div>
    </div>

    <!-- Availability Slots Component -->
    <div class="mt-6">
      <DoctorSlots :doctorId="doctorId" :patientId="patientId" :departmentId="doctor.department_id" />
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import api from "@/services/api";
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
.text-muted {
  color: #6b7280;
}
.card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}
</style>
