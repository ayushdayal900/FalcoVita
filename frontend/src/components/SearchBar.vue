<template>
  <div class="w-full">
    <!-- Main Container -->
    <div class="flex items-center gap-4 p-4 bg-white rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100">
      
      <!-- Input Wrapper -->
      <div class="flex-1 relative group flex items-center">
        
        <!-- Type Selector -->
        <div v-if="showTypeSelector" class="relative border-r border-slate-200 pr-2 mr-2">
          <select 
            :value="searchType"
            @input="$emit('update:searchType', $event.target.value)"
            class="appearance-none bg-transparent font-medium text-slate-600 py-3 pl-4 pr-8 focus:outline-none cursor-pointer hover:text-primary-600 transition-colors"
          >
            <option value="all">All</option>
            <option v-for="type in types" :key="type" :value="type">
              {{ type.charAt(0).toUpperCase() + type.slice(1) }}
            </option>
          </select>
          <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none text-slate-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none" :class="{'pl-0 left-auto relative': showTypeSelector}">
          <svg v-if="!showTypeSelector" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400 group-focus-within:text-primary-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input 
          type="text" 
          :value="modelValue" 
          @input="$emit('update:modelValue', $event.target.value)"
          :placeholder="placeholder" 
          class="w-full py-3 bg-white border-none text-slate-700 placeholder-slate-400 text-base font-medium focus:outline-none focus:ring-0 transition-all duration-300"
          :class="showTypeSelector ? 'pl-2' : 'pl-11 pr-4 border border-slate-200 rounded-xl focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10'"
          @keyup.enter="$emit('search')"
        />
      </div>
      
      <!-- Actions -->
      <div class="flex items-center gap-3">
        <!-- Search Button -->
        <button 
          @click="$emit('search')" 
          class="px-8 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-xl font-semibold text-base shadow-lg shadow-primary-500/30 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-primary-500/40 active:translate-y-0 active:shadow-md"
        >
          Search
        </button>

        <!-- Clear Button -->
        <button 
          v-if="modelValue"
          @click="$emit('clear')" 
          class="px-6 py-3 bg-white border border-slate-200 text-slate-600 hover:text-slate-800 hover:bg-slate-50 hover:border-slate-300 rounded-xl font-medium transition-all duration-200"
        >
          Clear
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
