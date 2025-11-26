<template>
  <div class="card border-0 shadow-sm">
    <div class="card-header bg-white border-bottom py-3 px-4">
      <h3 class="h5 fw-bold text-dark mb-0">Available Slots</h3>
    </div>

    <div class="card-body p-4">
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary mb-2" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="text-muted small mb-0">Loading slots...</p>
      </div>

      <div v-else-if="slots.length === 0" class="text-center py-5">
        <div class="bg-light rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 48px; height: 48px;">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-muted">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-muted fw-medium mb-0">No available slots found.</p>
      </div>

      <div v-else class="row g-3">
        <div
          v-for="slot in slots"
          :key="slot.id"
          class="col-md-6 col-lg-4"
        >
          <div class="p-3 border rounded-3 bg-light d-flex justify-content-between align-items-center hover-shadow transition-all">
            <div>
              <p class="fw-bold text-dark mb-0">
                {{ new Date(slot.available_date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }) }}
              </p>
              <p class="text-primary small fw-bold mb-0">{{ slot.time_slot }}</p>
            </div>

            <button
              class="btn btn-sm btn-primary px-3 fw-bold"
              @click="bookSlot(slot)"
              :disabled="slot.status === 'booked'"
            >
              Book
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from "vue";
import api from "@/services/api";

const props = defineProps({
  doctorId: Number,
  patientId: Number,
  departmentId: Number
});

const slots = ref([]);
const loading = ref(true);

const loadSlots = async () => {
  try {
    const res = await api.get(`/availability/doctor/${props.doctorId}`);
    slots.value = res.data.filter(s => s.status === "available");
  } catch (err) {
    console.error("Failed to load slots", err);
  } finally {
    loading.value = false;
  }
};

const bookSlot = async (slot) => {
  if (!props.departmentId) {
    alert("Error: Missing department information.");
    return;
  }

  if (!confirm(`Confirm booking for ${new Date(slot.available_date).toLocaleDateString()} at ${slot.time_slot}?`)) {
    return;
  }

  try {
    // 1. Create Appointment
    const startTime = slot.time_slot.split('-')[0];
    const appointmentDate = new Date(slot.available_date);
    const [hours, minutes] = startTime.split(':');
    appointmentDate.setHours(parseInt(hours), parseInt(minutes));

    const payload = {
      doctor_id: props.doctorId,
      department_id: props.departmentId,
      patient_id: props.patientId,
      appointment_date: appointmentDate.toISOString(),
      status: 'scheduled'
    };

    await api.post('/appointments/', payload);

    // 2. Mark Slot as Booked
    await api.put(`/availability/${slot.id}`, { status: "booked" });
    
    loadSlots();
    alert("Appointment booked successfully!");
  } catch (err) {
    console.error("Booking failed", err);
    alert("Failed to book appointment.");
  }
};

onMounted(loadSlots);
</script>

<style scoped>
.hover-shadow:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.05);
  background-color: #fff !important;
  border-color: var(--bs-primary) !important;
}
.transition-all {
  transition: all 0.2s ease-in-out;
}
</style>
