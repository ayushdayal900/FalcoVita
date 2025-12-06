<template>
  <div class="card border-0 shadow-sm">
    <div class="card-body p-2">
      <div class="input-group">
        <!-- Type Selector -->
        <select 
          v-if="showTypeSelector"
          :value="searchType"
          @input="$emit('update:searchType', $event.target.value)"
          class="form-select bg-light border-0 fw-medium"
          style="max-width: 150px;"
        >
          <option value="all">All</option>
          <option v-for="type in types" :key="type" :value="type">
            {{ type.charAt(0).toUpperCase() + type.slice(1) }}
          </option>
        </select>

        <!-- Input -->
        <input 
          type="text" 
          :value="modelValue" 
          @input="$emit('update:modelValue', $event.target.value)"
          :placeholder="placeholder" 
          class="form-control border-0 shadow-none"
          @keyup.enter="$emit('search')"
        />

        <!-- Clear Button -->
        <button 
          v-if="modelValue"
          @click="$emit('clear')" 
          class="btn btn-link text-muted text-decoration-none"
          type="button"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
            <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
          </svg>
        </button>

        <!-- Search Button -->
        <button 
          @click="$emit('search')" 
          class="btn btn-primary px-4 fw-bold"
          type="button"
        >
          Search
        </button>
      </div>
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
  types: {
    type: Array,
    default: () => []
  },
  searchType: {
    type: String,
    default: 'all'
  }
});

defineEmits(['update:modelValue', 'update:searchType', 'search', 'clear']);
</script>

<style scoped>
.form-select:focus,
.form-control:focus {
  box-shadow: none;
  border-color: transparent;
}
</style>