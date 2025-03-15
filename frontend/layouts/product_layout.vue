<script setup>
// Shared layout state
const pageTitle = inject('pageTitle', ref('Products'));

// Top filter tabs
const activeFilter = ref('All');
const filters = [
  { name: 'All', active: true },
  { name: 'Promotion', active: false },
  { name: 'New', active: false },
  { name: 'Popular', active: false },
  { name: 'Recommend', active: false },
];

const setFilter = (filter) => {
  activeFilter.value = filter;
};

// Search functionality
const searchQuery = ref('');

// Sort functionality
const sortBy = ref('default');

// Brand filter options
const brands = ref([
  { name: 'Sony', selected: false },
  { name: 'Bose', selected: false },
  { name: 'JBL', selected: false },
  { name: 'Sonos', selected: false },
  { name: 'Harman Kardon', selected: false },
]);

// Type filter options
const types = ref([
  { name: 'Portable', selected: false },
  { name: 'Desktop', selected: false },
  { name: 'Bookshelf', selected: false },
  { name: 'Floor Standing', selected: false },
]);

const connections = ref([
  { name: 'Bluetooth', selected: false },
  { name: 'Wireless', selected: false },
  { name: 'Wired', selected: false },
  { name: 'USB-C', selected: false },
]);

const priceRanges = ref([
  { name: 'Under $100', selected: false },
  { name: '$100 - $300', selected: false },
  { name: '$300 - $500', selected: false },
  { name: 'Over $500', selected: false },
]);

// Collapse state for sidebar sections
const brandExpanded = ref(true);
const typeExpanded = ref(true);
const connectionExpanded = ref(true);
const priceExpanded = ref(true);

// Get the applied filters for filtering in pages
const appliedFilters = computed(() => {
  return {
    activeFilter: activeFilter.value,
    searchQuery: searchQuery.value,
    sortBy: sortBy.value,
    brands: brands.value.filter(b => b.selected).map(b => b.name),
    types: types.value.filter(t => t.selected).map(t => t.name),
    connections: connections.value.filter(c => c.selected).map(c => c.name),
    priceRanges: priceRanges.value.filter(p => p.selected).map(p => p.name)
  };
});

// Clear all filters
const clearAllFilters = () => {
  // Reset sidebar filters
  brands.value.forEach(b => b.selected = false);
  types.value.forEach(t => t.selected = false);
  connections.value.forEach(c => c.selected = false);
  priceRanges.value.forEach(p => p.selected = false);
  
  // Reset top filters
  activeFilter.value = 'All';
  searchQuery.value = '';
  sortBy.value = 'default';
};

// Share applied filters with pages - this is what the page will use
provide('appliedFilters', appliedFilters);
</script>

<template>
  <div class="w-full bg-base-100">
    <navbar_header/>
    <div class="container mx-auto px-4 py-8">
      <!-- Category header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-center md:text-right">{{ pageTitle }}</h1>
      </div>

      <!-- Main content area with sidebar and products -->
      <div class="flex flex-col md:flex-row gap-8">
        <!-- Sidebar with filters -->
        <div class="w-full md:w-64 flex-shrink-0">
          <div class="card bg-base-100 shadow-md">
            <div class="card-body p-4">
              <h2 class="text-xl font-bold mb-4">Filter</h2>

              <!-- Brand filter -->
              <div class="collapse collapse-arrow border-b" :class="{'collapse-open': brandExpanded}">
                <input v-model="brandExpanded" type="checkbox" class="min-h-0">
                <div class="collapse-title font-medium py-2">
                  Brand
                </div>
                <div class="collapse-content pt-0">
                  <div v-for="(brand, index) in brands" :key="index" class="form-control">
                    <label class="cursor-pointer label justify-start py-1">
                      <input v-model="brand.selected" type="checkbox" class="checkbox checkbox-sm checkbox-primary">
                      <span class="label-text ml-2">{{ brand.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Type filter -->
              <div class="collapse collapse-arrow border-b" :class="{'collapse-open': typeExpanded}">
                <input v-model="typeExpanded" type="checkbox" class="min-h-0">
                <div class="collapse-title font-medium py-2">
                  Type <span class="text-xs text-gray-400">(Portable/Desktop)</span>
                </div>
                <div class="collapse-content pt-0">
                  <div v-for="(type, index) in types" :key="index" class="form-control">
                    <label class="cursor-pointer label justify-start py-1">
                      <input v-model="type.selected" type="checkbox" class="checkbox checkbox-sm checkbox-primary">
                      <span class="label-text ml-2">{{ type.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Connection filter -->
              <div class="collapse collapse-arrow border-b" :class="{'collapse-open': connectionExpanded}">
                <input v-model="connectionExpanded" type="checkbox" class="min-h-0">
                <div class="collapse-title font-medium py-2">
                  Connection
                </div>
                <div class="collapse-content pt-0">
                  <div v-for="(connection, index) in connections" :key="index" class="form-control">
                    <label class="cursor-pointer label justify-start py-1">
                      <input v-model="connection.selected" type="checkbox" class="checkbox checkbox-sm checkbox-primary">
                      <span class="label-text ml-2">{{ connection.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Price Range filter -->
              <div class="collapse collapse-arrow" :class="{'collapse-open': priceExpanded}">
                <input v-model="priceExpanded" type="checkbox" class="min-h-0">
                <div class="collapse-title font-medium py-2">
                  Price Range
                </div>
                <div class="collapse-content pt-0">
                  <div v-for="(range, index) in priceRanges" :key="index" class="form-control">
                    <label class="cursor-pointer label justify-start py-1">
                      <input v-model="range.selected" type="checkbox" class="checkbox checkbox-sm checkbox-primary">
                      <span class="label-text ml-2">{{ range.name }}</span>
                    </label>
                  </div>
                </div>
              </div>
              
              <!-- Clear filters button -->
              <div
v-if="appliedFilters.brands.length + appliedFilters.types.length + 
                        appliedFilters.connections.length + appliedFilters.priceRanges.length > 0 ||
                        appliedFilters.activeFilter !== 'All' || 
                        appliedFilters.searchQuery !== ''" 
                   class="mt-4 flex justify-between items-center">
                <span class="text-sm text-gray-500">
                  Filters applied
                </span>
                <button class="btn btn-xs btn-outline" @click="clearAllFilters">
                  Clear All
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Products area -->
        <div class="flex-1">
          <!-- Filter tabs and search (moved to layout) -->
          <div class="flex flex-col md:flex-row gap-4 justify-between mb-6">
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="filter in filters" 
                :key="filter.name" 
                :class="[
                  'btn btn-sm', 
                  activeFilter === filter.name ? 'btn-warning' : 'btn-outline'
                ]"
                @click="setFilter(filter.name)"
              >
                {{ filter.name }}
              </button>
            </div>
            <div class="flex gap-2 w-full md:w-auto">
              <input v-model="searchQuery" type="text" placeholder="Search Products" class="input input-bordered w-full md:w-auto" >
              <div class="dropdown dropdown-end">
                <label tabindex="0" class="btn btn-sm btn-outline gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                  </svg>
                  Sort by
                </label>
                <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
                  <li><a @click="sortBy = 'default'">Default</a></li>
                  <li><a @click="sortBy = 'price-low'">Price: Low to High</a></li>
                  <li><a @click="sortBy = 'price-high'">Price: High to Low</a></li>
                  <li><a @click="sortBy = 'name'">Name</a></li>
                </ul>
              </div>
            </div>
          </div>
          
          <!-- Slot for page content (products) -->
          <slot />
        </div>
      </div>
    </div>
    <footer_section />
  </div>
</template>

<style scoped>
/* Custom styling for filters */
:deep(.btn-primary) {
  background-color: #f97316;
  border-color: #f97316;
}

:deep(.btn-primary:hover) {
  background-color: #ea580c;
  border-color: #ea580c;
}

:deep(.checkbox-primary) {
  --chkbg: #f97316;
  --chkfg: white;
}

:deep(.btn-warning) {
  background-color: #f97316;
  border-color: #f97316;
}
</style>