<template>
  <div class="card p-4 mb-6">
    <div class="flex gap-4">
      <input 
        type="text" 
        :value="modelValue" 
        @input="$emit('update:modelValue', $event.target.value)"
        :placeholder="placeholder" 
        class="input"
        style="min-width: 400px; flex: 1;"
        @keyup.enter="$emit('search')"
      />
      <select 
        v-if="showTypeSelector"
        :value="searchType" 
        @change="$emit('update:searchType', $event.target.value)"
        class="input" 
        style="width: 120px;"
      >
        <option value="all">All</option>
        <option v-if="types.includes('doctor')" value="doctor">Doctors</option>
        <option v-if="types.includes('patient')" value="patient">Patients</option>
      </select>
      <button @click="$emit('search')" class="btn btn-primary">Search</button>
      <button @click="$emit('clear')" class="btn btn-outline">Clear</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Search...'
  },
  showTypeSelector: {
    type: Boolean,
    default: false
  },
  searchType: {
    type: String,
    default: 'all'
  },
  types: {
    type: Array,
    default: () => ['doctor', 'patient']
  }
});

defineEmits(['update:modelValue', 'update:searchType', 'search', 'clear']);
</script>
