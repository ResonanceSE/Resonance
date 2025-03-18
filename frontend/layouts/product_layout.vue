<script setup>
import { FooterSection, NavbarHeader } from '#components';

// Shared layout state
const pageTitle = inject('pageTitle', ref('Products'));

// Mobile filter modal state
const filterModalOpen = ref(false);

// Expandable sections state in the modal
const modalBrandExpanded = ref(true);
const modalTypeExpanded = ref(true);
const modalConnectionExpanded = ref(true);
const modalPriceExpanded = ref(true);

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

// Get sort label for display
const getSortLabel = computed(() => {
  switch(sortBy.value) {
    case 'price-low': return 'Price: Low to High';
    case 'price-high': return 'Price: High to Low';
    case 'name': return 'Name';
    default: return 'Default';
  }
});

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

// Helper getters for active filters display
const getSelectedBrands = computed(() => 
  brands.value.filter(b => b.selected).map(b => b.name)
);

const getSelectedTypes = computed(() => 
  types.value.filter(t => t.selected).map(t => t.name)
);

const getSelectedConnections = computed(() => 
  connections.value.filter(c => c.selected).map(c => c.name)
);

const getSelectedPrices = computed(() => 
  priceRanges.value.filter(p => p.selected).map(p => p.name)
);

// Counter for active filters badge
const activeFilterCount = computed(() => {
  let count = 0;
  if (activeFilter.value !== 'All') count++;
  if (searchQuery.value) count++;
  count += getSelectedBrands.value.length;
  count += getSelectedTypes.value.length;
  count += getSelectedConnections.value.length;
  count += getSelectedPrices.value.length;
  return count;
});

// Has active filters for conditional displays
const hasActiveFilters = computed(() => activeFilterCount.value > 0);

// Collapse state for sidebar sections (desktop)
const brandExpanded = ref(true);
const typeExpanded = ref(true);
const connectionExpanded = ref(true);
const priceExpanded = ref(true);

// Method to unselect a specific filter
const unselectFilter = (filterType, value) => {
  switch(filterType) {
    case 'brand': {
      const brandIndex = brands.value.findIndex(b => b.name === value);
      if (brandIndex >= 0) brands.value[brandIndex].selected = false;
      break;
    }
    case 'type': {
      const typeIndex = types.value.findIndex(t => t.name === value);
      if (typeIndex >= 0) types.value[typeIndex].selected = false;
      break;
    }
    case 'connection': {
      const connIndex = connections.value.findIndex(c => c.name === value);
      if (connIndex >= 0) connections.value[connIndex].selected = false;
      break;
    }
    case 'price': {
      const priceIndex = priceRanges.value.findIndex(p => p.name === value);
      if (priceIndex >= 0) priceRanges.value[priceIndex].selected = false;
      break;
    }
  }
};

// Get the applied filters for filtering in pages
const appliedFilters = computed(() => {
  return {
    activeFilter: activeFilter.value,
    searchQuery: searchQuery.value,
    sortBy: sortBy.value,
    brands: getSelectedBrands.value,
    types: getSelectedTypes.value,
    connections: getSelectedConnections.value,
    priceRanges: getSelectedPrices.value
  };
});

// Clear all filters
const clearAllFilters = () => {
  brands.value.forEach(b => b.selected = false);
  types.value.forEach(t => t.selected = false);
  connections.value.forEach(c => c.selected = false);
  priceRanges.value.forEach(p => p.selected = false);
  activeFilter.value = 'All';
  searchQuery.value = '';
  sortBy.value = 'default';
  filterModalOpen.value = false;
};

provide('appliedFilters', appliedFilters);
</script>

<template>
  <div class="w-full bg-base-100">
    <NavbarHeader/>
    <div class="container mx-auto px-4 py-8">
      <!-- Category header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold">{{ pageTitle }}</h1>
      </div>

      <!-- Main content area with sidebar and products -->
      <div class="flex flex-col md:flex-row gap-6">
        <!-- Sidebar with filters - Desktop view only -->
        <div class="hidden md:block w-64 flex-shrink-0">
          <div class="bg-base-100 rounded-lg border border-gray-200">
            <div class="p-4">
              <h2 class="text-lg font-bold mb-4">Filters</h2>

              <!-- Brand filter -->
              <div class="border-b pb-2 mb-3">
                <div class="flex justify-between items-center mb-2 cursor-pointer" @click="brandExpanded = !brandExpanded">
                  <h3 class="font-medium">Brand</h3>
                  <button class="text-gray-500">
                    <svg v-if="brandExpanded" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
                <div v-if="brandExpanded" class="space-y-2 pl-1">
                  <div v-for="(brand, index) in brands" :key="index" class="form-control">
                    <label class="flex items-center gap-2 cursor-pointer hover:text-orange-500">
                      <input v-model="brand.selected" type="checkbox" class="checkbox checkbox-sm checkbox-orange border-gray-300" >
                      <span class="label-text">{{ brand.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Type filter -->
              <div class="border-b pb-2 mb-3">
                <div class="flex justify-between items-center mb-2 cursor-pointer" @click="typeExpanded = !typeExpanded">
                  <h3 class="font-medium">Type</h3>
                  <button class="text-gray-500">
                    <svg v-if="typeExpanded" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
                <div v-if="typeExpanded" class="space-y-2 pl-1">
                  <div v-for="(type, index) in types" :key="index" class="form-control">
                    <label class="flex items-center gap-2 cursor-pointer hover:text-orange-500">
                      <input v-model="type.selected" type="checkbox" class="checkbox checkbox-sm checkbox-orange border-gray-300" >
                      <span class="label-text">{{ type.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Connection filter -->
              <div class="border-b pb-2 mb-3">
                <div class="flex justify-between items-center mb-2 cursor-pointer" @click="connectionExpanded = !connectionExpanded">
                  <h3 class="font-medium">Connection</h3>
                  <button class="text-gray-500">
                    <svg v-if="connectionExpanded" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
                <div v-if="connectionExpanded" class="space-y-2 pl-1">
                  <div v-for="(connection, index) in connections" :key="index" class="form-control">
                    <label class="flex items-center gap-2 cursor-pointer hover:text-orange-500">
                      <input v-model="connection.selected" type="checkbox" class="checkbox checkbox-sm checkbox-orange border-gray-300" >
                      <span class="label-text">{{ connection.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Price Range filter -->
              <div>
                <div class="flex justify-between items-center mb-2 cursor-pointer" @click="priceExpanded = !priceExpanded">
                  <h3 class="font-medium">Price Range</h3>
                  <button class="text-gray-500">
                    <svg v-if="priceExpanded" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
                <div v-if="priceExpanded" class="space-y-2 pl-1">
                  <div v-for="(range, index) in priceRanges" :key="index" class="form-control">
                    <label class="flex items-center gap-2 cursor-pointer hover:text-orange-500">
                      <input v-model="range.selected" type="checkbox" class="checkbox checkbox-sm checkbox-orange border-gray-300" >
                      <span class="label-text">{{ range.name }}</span>
                    </label>
                  </div>
                </div>
              </div>
              
              <!-- Clear filters button -->
              <div v-if="hasActiveFilters" class="mt-6">
                <button 
                  class="btn btn-outline btn-sm w-full hover:bg-orange-500 hover:border-orange-500" 
                  @click="clearAllFilters"
                >
                  Clear All Filters
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Products area -->
        <div class="flex-1">
          <!-- Top filter bar -->
          <div class="mb-6 space-y-4">
            <!-- Filter tabs -->
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="filter in filters" 
                :key="filter.name" 
                :class="[
                  'btn btn-sm', 
                  activeFilter === filter.name ? 'bg-orange-500 text-white border-orange-500 hover:bg-orange-600' : 'btn-outline hover:bg-orange-500 hover:border-orange-500'
                ]"
                @click="setFilter(filter.name)"
              >
                {{ filter.name }}
              </button>
            </div>
            
            <!-- Search, Filter Button, and Sort -->
            <div class="flex flex-col md:flex-row gap-4">
              <!-- Search bar -->
              <div class="relative flex-grow">
                <input 
                  v-model="searchQuery" 
                  type="text" 
                  placeholder="Search products..." 
                  class="input input-bordered w-full pr-10 focus:border-orange-500" 
                >
                <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>
              
              <!-- Simple Filter Button (Mobile) -->
              <button 
                class="md:hidden btn btn-outline flex justify-between items-center hover:bg-orange-500 hover:border-orange-500" 
                @click="filterModalOpen = true"
              >
                <div class="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 010 2H4a1 1 0 01-1-1zm3 4a1 1 0 011-1h10a1 1 0 010 2H7a1 1 0 01-1-1zm2 4a1 1 0 011-1h6a1 1 0 010 2h-6a1 1 0 01-1-1z" />
                  </svg>
                  Filter
                </div>
                <span v-if="activeFilterCount > 0" class="badge badge-sm bg-orange-500 text-white border-orange-500">{{ activeFilterCount }}</span>
              </button>
              
              <!-- Sort dropdown -->
              <div class="dropdown dropdown-end">
                <label tabindex="0" class="btn btn-outline gap-2 hover:bg-orange-500 hover:border-orange-500">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                  </svg>
                  Sort: {{ getSortLabel }}
                </label>
                <ul tabindex="0" class="dropdown-content z-10 menu p-2 shadow bg-base-100 rounded-box w-52 mt-1">
                  <li><a :class="{'font-bold text-orange-500': sortBy === 'default'}" @click="sortBy = 'default'">Default</a></li>
                  <li><a :class="{'font-bold text-orange-500': sortBy === 'price-low'}" @click="sortBy = 'price-low'">Price: Low to High</a></li>
                  <li><a :class="{'font-bold text-orange-500': sortBy === 'price-high'}" @click="sortBy = 'price-high'">Price: High to Low</a></li>
                  <li><a :class="{'font-bold text-orange-500': sortBy === 'name'}" @click="sortBy = 'name'">Name</a></li>
                </ul>
              </div>
            </div>
            
            <!-- Selected Filters Summary (Mobile) -->
            <div v-if="hasActiveFilters" class="md:hidden flex flex-wrap gap-2">
              <div v-if="getSelectedBrands.length > 0" class="badge badge-sm bg-orange-100 text-orange-800 p-2">
                Brand: {{ getSelectedBrands.join(', ') }}
              </div>
              <div v-if="getSelectedTypes.length > 0" class="badge badge-sm bg-orange-100 text-orange-800 p-2">
                Type: {{ getSelectedTypes.join(', ') }}
              </div>
              <div v-if="getSelectedConnections.length > 0" class="badge badge-sm bg-orange-100 text-orange-800 p-2">
                Connection: {{ getSelectedConnections.join(', ') }}
              </div>
              <div v-if="getSelectedPrices.length > 0" class="badge badge-sm bg-orange-100 text-orange-800 p-2">
                Price: {{ getSelectedPrices.join(', ') }}
              </div>
            </div>
            
            <!-- Active filters display (Desktop) -->
            <div v-if="hasActiveFilters" class="hidden md:flex flex-wrap gap-2">
              <div v-if="activeFilter !== 'All'" class="badge bg-orange-500 text-white border-orange-500 gap-1 p-3">
                {{ activeFilter }}
                <button class="ml-1" @click="setFilter('All')">×</button>
              </div>
              
              <div v-if="searchQuery" class="badge bg-orange-100 text-orange-800 border-orange-200 gap-1 p-3">
                "{{ searchQuery }}"
                <button class="ml-1" @click="searchQuery = ''">×</button>
              </div>
              
              <template v-for="brand in getSelectedBrands" :key="'brand-'+brand">
                <div class="badge bg-gray-100 text-gray-800 gap-1 p-3">
                  Brand: {{ brand }}
                  <button class="ml-1" @click="unselectFilter('brand', brand)">×</button>
                </div>
              </template>
              
              <template v-for="type in getSelectedTypes" :key="'type-'+type">
                <div class="badge bg-gray-100 text-gray-800 gap-1 p-3">
                  Type: {{ type }}
                  <button class="ml-1" @click="unselectFilter('type', type)">×</button>
                </div>
              </template>
              
              <template v-for="conn in getSelectedConnections" :key="'conn-'+conn">
                <div class="badge bg-gray-100 text-gray-800 gap-1 p-3">
                  Connection: {{ conn }}
                  <button class="ml-1" @click="unselectFilter('connection', conn)">×</button>
                </div>
              </template>
              
              <template v-for="price in getSelectedPrices" :key="'price-'+price">
                <div class="badge bg-gray-100 text-gray-800 gap-1 p-3">
                  {{ price }}
                  <button class="ml-1" @click="unselectFilter('price', price)">×</button>
                </div>
              </template>
              
              <button v-if="hasActiveFilters" class="btn btn-xs bg-transparent hover:bg-orange-500 border border-gray-300 hover:border-orange-500" @click="clearAllFilters">
                Clear all
              </button>
            </div>
          </div>
          
          <!-- Slot for page content (products) -->
          <slot />
        </div>
      </div>
    </div>

    <!-- Mobile Filter Modal with Expandable Sections -->
    <div class="modal" :class="{'modal-open': filterModalOpen}">
      <div class="modal-box">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold text-lg">Filters</h3>
          <button class="btn btn-sm btn-circle btn-ghost" @click="filterModalOpen = false">✕</button>
        </div>
        
        <!-- All filters in a single modal with expandable sections -->
        <div class="overflow-y-auto max-h-[60vh]">
          <!-- Brand Section - Expandable -->
          <div class="collapse collapse-arrow border-b">
            <input v-model="modalBrandExpanded" type="checkbox" class="min-h-0" > 
            <div class="collapse-title font-medium py-3 flex items-center justify-between">
              <span>Brand</span>
              <span v-if="getSelectedBrands.length > 0" class="badge badge-sm badge-primary ml-2">{{ getSelectedBrands.length }}</span>
            </div>
            <div class="collapse-content">
              <div class="space-y-2 pt-2">
                <div v-for="(brand, index) in brands" :key="index" class="form-control">
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input v-model="brand.selected" type="checkbox" class="checkbox checkbox-sm checkbox-orange border-gray-300" >
                    <span class="label-text">{{ brand.name }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Type Section - Expandable -->
          <div class="collapse collapse-arrow border-b">
            <input v-model="modalTypeExpanded" type="checkbox" class="min-h-0" > 
            <div class="collapse-title font-medium py-3 flex items-center justify-between">
              <span>Type</span>
              <span v-if="getSelectedTypes.length > 0" class="badge badge-sm badge-primary ml-2">{{ getSelectedTypes.length }}</span>
            </div>
            <div class="collapse-content">
              <div class="space-y-2 pt-2">
                <div v-for="(type, index) in types" :key="index" class="form-control">
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input v-model="type.selected" type="checkbox" class="checkbox checkbox-sm checkbox-orange border-gray-300" >
                    <span class="label-text">{{ type.name }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Connection Section - Expandable -->
          <div class="collapse collapse-arrow border-b">
            <input v-model="modalConnectionExpanded" type="checkbox" class="min-h-0" > 
            <div class="collapse-title font-medium py-3 flex items-center justify-between">
              <span>Connection</span>
              <span v-if="getSelectedConnections.length > 0" class="badge badge-sm badge-primary ml-2">{{ getSelectedConnections.length }}</span>
            </div>
            <div class="collapse-content">
              <div class="space-y-2 pt-2">
                <div v-for="(connection, index) in connections" :key="index" class="form-control">
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input v-model="connection.selected" type="checkbox" class="checkbox checkbox-sm checkbox-orange border-gray-300" >
                    <span class="label-text">{{ connection.name }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Price Range Section - Expandable -->
          <div class="collapse collapse-arrow">
            <input v-model="modalPriceExpanded" type="checkbox" class="min-h-0" > 
            <div class="collapse-title font-medium py-3 flex items-center justify-between">
              <span>Price Range</span>
              <span v-if="getSelectedPrices.length > 0" class="badge badge-sm badge-primary ml-2">{{ getSelectedPrices.length }}</span>
            </div>
            <div class="collapse-content">
              <div class="space-y-2 pt-2">
                <div v-for="(range, index) in priceRanges" :key="index" class="form-control">
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input v-model="range.selected" type="checkbox" class="checkbox checkbox-sm checkbox-orange border-gray-300" >
                    <span class="label-text">{{ range.name }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-action mt-6">
          <button class="btn bg-orange-500 border-orange-500 hover:bg-orange-600 text-white" @click="filterModalOpen = false">
            Apply Filters
          </button>
          <button 
            class="btn btn-outline"
            :disabled="!hasActiveFilters"
            @click="clearAllFilters"
          >
            Clear All
          </button>
        </div>
      </div>
      
      <label class="modal-backdrop" @click="filterModalOpen = false"/>
    </div>
    
    <FooterSection />
  </div>
</template>


<style scoped>
:deep(.checkbox-orange:checked) {
  background-color: #f97316 !important;
  border-color: #f97316 !important;
}

:deep(.checkbox-orange:focus) {
  box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.3);
}

:deep(.badge-primary) {
  background-color: #f97316;
  color: white;
}

.collapse-arrow .collapse-title:after {
  color: #888;
}

.modal-box {
  max-height: 90vh;
}

.badge {
  font-weight: normal;
}

.badge:hover button {
  color: currentColor;
  opacity: 0.8;
}

.collapse-arrow .collapse-title:after {
  color: #666;
}

.collapse-content {
  transition: all 0.2s ease-in-out;
}

.checkbox-orange {
  border-width: 1.5px;
}

.collapse-title, .form-control label {
  min-height: 48px;
  display: flex;
  align-items: center;
}

.collapse + .collapse {
  margin-top: 1px;
}
</style>