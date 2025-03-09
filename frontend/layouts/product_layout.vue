<script setup>
// Active states for filters
const activeFilter = ref('All');
const searchQuery = ref('');
const sortBy = ref('default');

const filters = [
  { name: 'All', active: true },
  { name: 'Promotion', active: false },
  { name: 'New', active: false },
  { name: 'Popular', active: false },
  { name: 'Recommend', active: false },
];

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

// Connection filter options
const connections = ref([
  { name: 'Bluetooth', selected: false },
  { name: 'Wireless', selected: false },
  { name: 'Wired', selected: false },
  { name: 'USB-C', selected: false },
]);

// Price range filter options
const priceRanges = ref([
  { name: 'Under $100', selected: false },
  { name: '$100 - $300', selected: false },
  { name: '$300 - $500', selected: false },
  { name: 'Over $500', selected: false },
]);

// Handle filter click
const setFilter = (filter) => {
  activeFilter.value = filter;
};

// Toggle collapsible sections
const brandExpanded = ref(true);
const typeExpanded = ref(true);
const connectionExpanded = ref(true);
const priceExpanded = ref(true);

// Mobile drawer state
const isFilterDrawerOpen = ref(false);

// Emitting events to parent components
const emit = defineEmits(['filterChange', 'searchChange', 'sortChange']);

// Watch for filter changes and emit events
watch([activeFilter, searchQuery, sortBy], () => {
  emit('filterChange', {
    filter: activeFilter.value,
    brands: brands.value.filter(b => b.selected).map(b => b.name),
    types: types.value.filter(t => t.selected).map(t => t.name),
    connections: connections.value.filter(c => c.selected).map(c => c.name),
    priceRanges: priceRanges.value.filter(p => p.selected).map(p => p.name)
  });
  
  emit('searchChange', searchQuery.value);
  emit('sortChange', sortBy.value);
});

const route = useRoute();
const productSlug = ref(route.params.product);
const apiUrl = useRuntimeConfig().public.apiUrl
const { data: product, error, pending } = useFetch(() => `${apiUrl}/api/products/${productSlug.value}`, {
  method: 'GET',
  immediate: true, //
});

</script>

<template>
  <div class="w-full bg-base-100">
    <navbar_header/>
    <div class="container mx-auto px-4 py-8">
      <!-- Category header - slot for page-specific header -->
      <div class="mb-8">
        <slot name="header">
          <!-- Default header if none provided -->
          <h1 class="text-3xl font-bold text-center md:text-right">{{ productSlug }}</h1>
        </slot>
      </div>

      <!-- Main content area with sidebar and products -->
      <div class="flex flex-col md:flex-row gap-8">
        <!-- Sidebar with filters -->
        <div class="w-full md:w-64 flex-shrink-0">
          <!-- Mobile filter toggle -->
          <div class="block md:hidden mb-4">
            <button 
              class="btn btn-outline w-full"
              @click="isFilterDrawerOpen = !isFilterDrawerOpen"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
              </svg>
              Filters
            </button>
          </div>

          <!-- Desktop filters -->
          <div class="hidden md:block card bg-base-100 shadow-md">
            <div class="card-body p-4">
              <h2 class="text-xl font-bold mb-4">Filter</h2>

              <!-- Filter before sidebar slot -->
              <slot name="before-sidebar-filters"/>

              <!-- Brand filter -->
              <div class="collapse collapse-arrow border-b">
                <input v-model="brandExpanded" type="checkbox" >
                <div class="collapse-title font-medium">
                  Brand
                </div>
                <div class="collapse-content">
                  <div v-for="(brand, index) in brands" :key="index" class="form-control">
                    <label class="cursor-pointer label justify-start">
                      <input v-model="brand.selected" type="checkbox" class="checkbox checkbox-sm checkbox-primary" >
                      <span class="label-text ml-2">{{ brand.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Type filter -->
              <div class="collapse collapse-arrow border-b">
                <input v-model="typeExpanded" type="checkbox" >
                <div class="collapse-title font-medium">
                  Type <span class="text-xs text-gray-400">(Portable/Desktop)</span>
                </div>
                <div class="collapse-content">
                  <div v-for="(type, index) in types" :key="index" class="form-control">
                    <label class="cursor-pointer label justify-start">
                      <input v-model="type.selected" type="checkbox" class="checkbox checkbox-sm checkbox-primary" >
                      <span class="label-text ml-2">{{ type.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Connection filter -->
              <div class="collapse collapse-arrow border-b">
                <input v-model="connectionExpanded" type="checkbox" >
                <div class="collapse-title font-medium">
                  Connection
                </div>
                <div class="collapse-content">
                  <div v-for="(connection, index) in connections" :key="index" class="form-control">
                    <label class="cursor-pointer label justify-start">
                      <input v-model="connection.selected" type="checkbox" class="checkbox checkbox-sm checkbox-primary" >
                      <span class="label-text ml-2">{{ connection.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Price Range filter -->
              <div class="collapse collapse-arrow">
                <input v-model="priceExpanded" type="checkbox" >
                <div class="collapse-title font-medium">
                  Price Range
                </div>
                <div class="collapse-content">
                  <div v-for="(range, index) in priceRanges" :key="index" class="form-control">
                    <label class="cursor-pointer label justify-start">
                      <input v-model="range.selected" type="checkbox" class="checkbox checkbox-sm checkbox-primary" >
                      <span class="label-text ml-2">{{ range.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Filter after sidebar slot -->
              <slot name="after-sidebar-filters"/>
            </div>
          </div>

          <!-- Mobile filter drawer -->
          <div class="drawer drawer-end md:hidden">
            <input id="filter-drawer" v-model="isFilterDrawerOpen" type="checkbox" class="drawer-toggle" >
            <div class="drawer-side z-10">
              <label for="filter-drawer" class="drawer-overlay"/>
              <div class="p-4 w-80 min-h-full bg-base-100 text-base-content">
                <h2 class="text-xl font-bold mb-4">Filter</h2>
                
                <!-- Mobile filters (same as desktop) -->
                <!-- Brand filter -->
                <div class="collapse collapse-arrow border-b">
                  <input v-model="brandExpanded" type="checkbox" >
                  <div class="collapse-title font-medium">
                    Brand
                  </div>
                  <div class="collapse-content">
                    <div v-for="(brand, index) in brands" :key="index" class="form-control">
                      <label class="cursor-pointer label justify-start">
                        <input v-model="brand.selected" type="checkbox" class="checkbox checkbox-sm checkbox-primary" >
                        <span class="label-text ml-2">{{ brand.name }}</span>
                      </label>
                    </div>
                  </div>
                </div>
                
                <!-- Repeat other mobile filters... -->
                
                <!-- Apply button -->
                <button 
                  class="btn btn-primary w-full mt-4"
                  @click="isFilterDrawerOpen = false"
                >
                  Apply Filters
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Products area -->
        <div class="flex-1">
          <!-- Filter tabs and search -->
          <div class="flex flex-col md:flex-row gap-4 justify-between mb-6">
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="filter in filters" 
                :key="filter.name" 
                :class="[
                  'btn btn-sm', 
                  activeFilter === filter.name ? 'btn-primary' : 'btn-outline'
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

          <!-- Main content slot -->
          <slot/>
        </div>
      </div>
    </div>
    <footer_section />    
  </div>
</template>

<style scoped>
.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}
</style>