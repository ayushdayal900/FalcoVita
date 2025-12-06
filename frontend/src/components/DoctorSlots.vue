<template>
  <div> <!-- Root wrapper to ensure HMR works correctly -->
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

    <!-- Payment Confirmation Modal -->
    <div v-if="showPaymentModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header bg-success text-white border-bottom-0 rounded-top-4">
            <h5 class="modal-title fw-bold">Complete Payment</h5>
            <button type="button" class="btn-close btn-close-white" @click="showPaymentModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <div class="text-center mb-4">
              <div class="bg-success bg-opacity-10 text-success rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 64px; height: 64px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h4 class="h5 fw-bold text-dark">Payment Required</h4>
              <p class="text-muted small">Please pay the consultation fee to confirm your booking.</p>
              <h2 class="display-6 fw-bold text-success mb-0">₹100</h2>
            </div>
            
            <form @submit.prevent="confirmPayment">
              <div class="mb-3">
                <label class="form-label fw-bold small">Card Number</label>
                <input type="text" class="form-control" placeholder="0000 0000 0000 0000" required>
              </div>
              <div class="row g-3">
                <div class="col-6">
                  <label class="form-label fw-bold small">Expiry</label>
                  <input type="text" class="form-control" placeholder="MM/YY" required>
                </div>
                <div class="col-6">
                  <label class="form-label fw-bold small">CVV</label>
                  <input type="text" class="form-control" placeholder="123" required>
                </div>
              </div>
              
              <div class="d-flex justify-content-end gap-2 pt-4 mt-2 border-top">
                <button type="button" @click="showPaymentModal = false" class="btn btn-light">Cancel</button>
                <button type="button" @click="confirmPayment('Pay Later')" class="btn btn-outline-primary fw-bold">Pay Later</button>
                <button type="submit" class="btn btn-success fw-bold px-4">Pay & Confirm</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div> <!-- Closing root wrapper -->
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
const showPaymentModal = ref(false);
const pendingBookingPayload = ref(null);
const pendingSlot = ref(null);

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

  // NOTE: Removed simple confirm prompt in favor of Payment Modal

  try {
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

    // Store payload and show payment modal
    pendingBookingPayload.value = payload;
    pendingSlot.value = slot;
    showPaymentModal.value = true;

  } catch (err) {
    console.error("Booking initiation failed", err);
    alert("Failed to initiate booking.");
  }
};

const confirmPayment = async (method = 'Credit Card') => {
  if (!pendingBookingPayload.value || !pendingSlot.value) return;

  try {
     const isPayLater = method === 'Pay Later';
     const finalPayDetails = isPayLater 
        ? { amount: 100, method: 'Pay Later' }
        : { amount: 100, method: "Credit Card" };

     const finalPayload = {
        ...pendingBookingPayload.value,
        payment_details: finalPayDetails
    };

    await api.post('/appointments/', finalPayload);
    await api.put(`/availability/${pendingSlot.value.id}`, { status: "booked" });

    showPaymentModal.value = false;
    pendingBookingPayload.value = null;
    pendingSlot.value = null;
    loadSlots();
    loadSlots();
    alert(method === 'Pay Later' ? "Booking Confirmed! Please pay from your dashboard." : "Payment successful! Appointment booked.");
  } catch (err) {
    console.error("Payment/Booking failed", err);
    alert("Failed to complete booking.");
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
