<template>
  <div class="card p-6">
    <h3 class="text-lg font-bold mb-4">Availability Calendar</h3>

    <table class="w-full border-collapse">
      <thead>
        <tr class="bg-slate-100 text-left">
          <th class="p-3 border">Day</th>
          <th class="p-3 border">Status</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="day in weekDays" :key="day">
          <td class="p-3 border">{{ day }}</td>
          <td class="p-3 border">
            <span v-if="bookedDays.includes(day)" class="text-red-500 font-semibold">
              Booked
            </span>
            <span v-else class="text-green-600 font-semibold">
              Available
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/services/api";

const weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
const bookedDays = ref([]);

onMounted(async () => {
  const doctorId = localStorage.getItem("doctor_id");

  const res = await api.get("/appointments/");
  const all = res.data;

  bookedDays.value = all
    .filter(a => a.doctor_id == doctorId)
    .map(a =>
      new Date(a.appointment_date).toLocaleDateString("en-US", { weekday: "long" })
    );
});
</script>
