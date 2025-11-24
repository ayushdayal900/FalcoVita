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
          @click="bookSlot(slot.id)"
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
  patientId: Number
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

const bookSlot = async (slotId) => {
  try {
    await api.put(`/availability/${slotId}`, { status: "booked" });
    loadSlots();
    alert("Slot booked successfully!");
  } catch (err) {
    console.error("Booking failed", err);
  }
};

onMounted(loadSlots);
</script>
