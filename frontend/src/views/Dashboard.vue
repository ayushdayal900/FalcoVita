<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />

    <!-- Main Content -->
    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-medium">Dashboard</h2>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="container mx-auto">
          <!-- Dashboard Content -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div class="card p-6">
              <h3 class="text-sm font-medium text-muted mb-2">Total Appointments</h3>
              <p class="text-2xl font-bold">12</p>
            </div>
            <div class="card p-6">
              <h3 class="text-sm font-medium text-muted mb-2">Upcoming</h3>
              <p class="text-2xl font-bold">3</p>
            </div>
            <div class="card p-6">
              <h3 class="text-sm font-medium text-muted mb-2">Messages</h3>
              <p class="text-2xl font-bold">5</p>
            </div>
          </div>

          <div class="card p-6">
            <h3 class="text-lg font-medium mb-4">Recent Activity</h3>
            <p class="text-muted text-sm">No recent activity to show.</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import Sidebar from '@/components/Sidebar.vue';
</script>

<style scoped>
.bg-white { background-color: #ffffff; }
.bg-slate-50 { background-color: #f8fafc; }
.overflow-hidden { overflow: hidden; }
.overflow-auto { overflow: auto; }
</style>
