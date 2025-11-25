<template>
  <div class="card p-6 shadow-sm">
    <h3 class="text-lg font-bold mb-4">Available Slots</h3>

    <div v-if="loading" class="text-center py-4 text-muted">Loading slots...</div>

    <div v-if="slots.length === 0" class="text-center py-8 text-red-500">
      No available slots
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="slot in slots"
        :key="slot.id"
        class="p-4 border rounded bg-slate-50 flex justify-between items-center"
      >
        <div>
          <p class="font-medium">
            {{ new Date(slot.available_date).toLocaleDateString() }}
          </p>
          <p class="text-sm text-muted">{{ slot.time_slot }}</p>
        </div>

        <button
          class="btn btn-primary px-3 py-1"
          @click="bookSlot(slot)"
          :disabled="slot.status === 'booked'"
        >
          Book
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
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
