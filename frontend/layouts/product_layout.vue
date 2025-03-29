<script setup>
import { useProductFiltering } from '~/composables/useProductFiltering';

const pageTitle = inject('pageTitle', ref('Products'));
const route = useRoute();
const currentCategory = inject('currentCategory', ref(''));
currentCategory.value = route.params.category || '';


const filterModalOpen = ref(false);

const {
  products,
  filteredProducts,
  filters,
  isLoading,
  error,
  fetchProducts,
  fetchFilters: fetchFilterOptions,
  applyFilters,
  updateFilters
} = useProductFiltering();


const brands = ref([]);
const connections = ref([]);
const priceRanges = ref([]);
const searchQuery = ref('');
const sortBy = ref('default');

const brandExpanded = ref(true);
const connectionExpanded = ref(true);
const priceExpanded = ref(true);

const modalBrandExpanded = ref(true);
const modalConnectionExpanded = ref(true);
const modalPriceExpanded = ref(true);

const isLoadingFilters = ref(true);
const filtersError = ref(null);

watch(
  () => route.params.category,
  (newCategory) => {
    console.log("Route category changed to:", newCategory);
    const category = newCategory || '';
    currentCategory.value = category;

    updateFilters({
      category: category,
      brands: [],
      connections: [],
      priceRanges: [],
      searchQuery: '',
      sortBy: 'default'
    });

    fetchProducts(category);

    searchQuery.value = '';
    sortBy.value = 'default';
    brands.value.forEach(b => b.selected = false);
    connections.value.forEach(c => c.selected = false);
    priceRanges.value.forEach(p => p.selected = false);
  },
  { immediate: true }
);

const convertFiltersForUI = (apiFilterData) => {
  try {
    brands.value = (apiFilterData.brands || []).map(brand => ({
      name: brand.brand,
      selected: filters.brands.includes(brand.brand),
      count: brand.count
    }));

    connections.value = (apiFilterData.connections || []).map(conn => ({
      name: conn.connections,
      selected: filters.connections.includes(conn.connections),
      count: conn.count
    }));


    priceRanges.value = (apiFilterData.price_ranges || []).map(range => ({
      name: range.name,
      selected: filters.priceRanges.includes(range.name),
      count: range.count,
      min: range.min,
      max: range.max
    }));
  } catch (error) {
    console.error('Error converting filters for UI:', error);
  }
};


const loadFilters = async () => {
  isLoadingFilters.value = true;
  filtersError.value = null;

  try {
    const apiFilterData = await fetchFilterOptions();
    convertFiltersForUI(apiFilterData);
  } catch (error) {
    console.error('Error loading filters:', error);
    filtersError.value = error.message;
    setDefaultFilters();
  } finally {
    isLoadingFilters.value = false;
  }
};

watch(brands, (newBrands) => {
  const selectedBrands = newBrands.filter(b => b.selected).map(b => b.name);
  updateFilters({ brands: selectedBrands });
}, { deep: true });

watch(connections, (newConnections) => {
  const selectedConnections = newConnections.filter(c => c.selected).map(c => c.name);
  updateFilters({ connections: selectedConnections });
}, { deep: true });


watch(priceRanges, (newPriceRanges) => {
  const selectedPriceRanges = newPriceRanges.filter(p => p.selected).map(p => p.name);
  updateFilters({ priceRanges: selectedPriceRanges });
}, { deep: true });


watch(searchQuery, (newQuery) => {
  updateFilters({ searchQuery: newQuery });
});


watch(sortBy, (newSortBy) => {
  updateFilters({ sortBy: newSortBy });
});

const getSortLabel = computed(() => {
  switch (sortBy.value) {
    case 'price-low': return 'Price: Low to High';
    case 'price-high': return 'Price: High to Low';
    case 'name': return 'Name';
    default: return 'Default';
  }
});

const getSelectedBrands = computed(() =>
  brands.value.filter(b => b.selected).map(b => b.name)
);

const getSelectedConnections = computed(() =>
  connections.value.filter(c => c.selected).map(c => c.name)
);

const getSelectedPrices = computed(() =>
  priceRanges.value.filter(p => p.selected).map(p => p.name)
);

const activeFilterCount = computed(() => {
  let count = 0;
  if (searchQuery.value) count++;
  count += getSelectedBrands.value.length;
  count += getSelectedConnections.value.length;
  count += getSelectedPrices.value.length;
  if (showOnlyAvailable.value) count++;
  return count;
});

const hasActiveFilters = computed(() => activeFilterCount.value > 0);

const unselectFilter = (filterType, value) => {
  switch (filterType) {
    case 'brand': {
      const brandIndex = brands.value.findIndex(b => b.name === value);
      if (brandIndex >= 0) brands.value[brandIndex].selected = false;
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

const showOnlyAvailable = ref(false);
watch(showOnlyAvailable, (newValue) => {
  updateFilters({ showOnlyAvailable: newValue });
});

const clearAllFilters = () => {
  brands.value.forEach(b => b.selected = false);
  connections.value.forEach(c => c.selected = false);
  priceRanges.value.forEach(p => p.selected = false);
  searchQuery.value = '';
  sortBy.value = 'default';
  showOnlyAvailable.value = false;
  filterModalOpen.value = false;
  const currentCat = currentCategory.value;
  updateFilters({
    searchQuery: '',
    brands: [],
    priceRanges: [],
    connections: [],
    sortBy: 'default',
    category: currentCat,
    showOnlyAvailable: false
  });
};

const closeSortDropdown = () => {
  document.activeElement.blur();
  const dropdownElements = document.querySelectorAll('.sort-dropdown [tabindex="0"]');
  dropdownElements.forEach(el => {
    el.blur();
  });
};

onMounted(async () => {
  await loadFilters();
});

provide('filteredProducts', filteredProducts);
provide('isLoadingProducts', isLoading);
provide('productsError', error);
</script>

<template>
  <div class="w-full bg-base-100">
    <NavbarHeader />
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
                <div
class="flex justify-between items-center mb-2 cursor-pointer"
                  @click="brandExpanded = !brandExpanded">
                  <h3 class="font-medium">Brand</h3>
                  <button class="text-gray-500">
                    <svg
v-if="brandExpanded" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20"
                      fill="currentColor">
                      <path
fill-rule="evenodd"
                        d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z"
                        clip-rule="evenodd" />
                    </svg>
                    <svg
v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20"
                      fill="currentColor">
                      <path
fill-rule="evenodd"
                        d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                        clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
                <div v-if="brandExpanded" class="space-y-2 pl-1">
                  <div v-for="(brand, index) in brands" :key="index" class="form-control">
                    <label class="flex items-center gap-2 cursor-pointer hover:text-orange-500">
                      <input
v-model="brand.selected" type="checkbox"
                        class="checkbox checkbox-sm checkbox-warning border-gray-300">
                      <span class="label-text">{{ brand.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Connection filter -->
              <div class="border-b pb-2 mb-3">
                <div
class="flex justify-between items-center mb-2 cursor-pointer"
                  @click="connectionExpanded = !connectionExpanded">
                  <h3 class="font-medium">Connection</h3>
                  <button class="text-gray-500">
                    <svg
v-if="connectionExpanded" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5"
                      viewBox="0 0 20 20" fill="currentColor">
                      <path
fill-rule="evenodd"
                        d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z"
                        clip-rule="evenodd" />
                    </svg>
                    <svg
v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20"
                      fill="currentColor">
                      <path
fill-rule="evenodd"
                        d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                        clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
                <div v-if="connectionExpanded" class="space-y-2 pl-1">
                  <div v-for="(connection, index) in connections" :key="index" class="form-control">
                    <label class="flex items-center gap-2 cursor-pointer hover:text-orange-500">
                      <input
v-model="connection.selected" type="checkbox"
                        class="checkbox checkbox-sm checkbox-warning border-gray-300">
                      <span class="label-text">{{ connection.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Price Range filter -->
              <div>
                <div
class="flex justify-between items-center mb-2 cursor-pointer"
                  @click="priceExpanded = !priceExpanded">
                  <h3 class="font-medium">Price Range</h3>
                  <button class="text-gray-500">
                    <svg
v-if="priceExpanded" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20"
                      fill="currentColor">
                      <path
fill-rule="evenodd"
                        d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z"
                        clip-rule="evenodd" />
                    </svg>
                    <svg
v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20"
                      fill="currentColor">
                      <path
fill-rule="evenodd"
                        d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                        clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
                <div v-if="priceExpanded" class="space-y-2 pl-1">
                  <div v-for="(range, index) in priceRanges" :key="index" class="form-control">
                    <label class="flex items-center gap-2 cursor-pointer hover:text-orange-500">
                      <input
v-model="range.selected" type="checkbox"
                        class="checkbox checkbox-sm checkbox-warning border-gray-300">
                      <span class="label-text">{{ range.name }}</span>
                    </label>
                  </div>
                </div>
              </div>
              <!-- Clear filters button -->
              <div v-if="hasActiveFilters" class="mt-6">
                <button
class="btn btn-outline btn-sm w-full hover:bg-orange-500 hover:border-orange-500"
                  @click="clearAllFilters">
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
            <!-- Search, Filter Button, and Sort -->
            <div class="flex flex-col md:flex-row gap-4">
              <!-- Search bar -->
              <div class="relative flex-grow">
                <input
v-model="searchQuery" type="text" placeholder="Search products..."
                  class="input input-bordered w-full pr-10 focus:border-orange-500">
                <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                  <svg
xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>

              <!-- Simple Filter Button (Mobile) -->
              <button
                class="md:hidden btn btn-outline flex justify-between items-center hover:bg-orange-500 hover:border-orange-500"
                @click="filterModalOpen = true">
                <div class="flex items-center gap-2">
                  <svg
xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 4a1 1 0 011-1h16a1 1 0 010 2H4a1 1 0 01-1-1zm3 4a1 1 0 011-1h10a1 1 0 010 2H7a1 1 0 01-1-1zm2 4a1 1 0 011-1h6a1 1 0 010 2h-6a1 1 0 01-1-1z" />
                  </svg>
                  Filter
                </div>
                <span v-if="activeFilterCount > 0" class="badge badge-sm bg-orange-500 text-white border-orange-500">{{
                  activeFilterCount }}</span>
              </button>

              <!-- Sort dropdown -->
              <div class="dropdown dropdown-end sort-dropdown">
                <label tabindex="0" class="btn btn-outline gap-2 hover:bg-orange-500 hover:border-orange-500">
                  <svg
xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                  </svg>
                  Sort: {{ getSortLabel }}
                </label>
                <ul tabindex="0" class="dropdown-content z-10 menu p-2 shadow bg-base-100 rounded-box w-52 mt-1">
                  <li><a
:class="{ 'font-bold text-orange-500': sortBy === 'default' }"
                      @click="sortBy = 'default', closeSortDropdown()">Default</a></li>
                  <li><a
:class="{ 'font-bold text-orange-500': sortBy === 'price-low' }"
                      @click="sortBy = 'price-low', closeSortDropdown()">Price: Low to High</a></li>
                  <li><a
:class="{ 'font-bold text-orange-500': sortBy === 'price-high' }"
                      @click="sortBy = 'price-high', closeSortDropdown()">Price: High to Low</a></li>
                  <li><a
:class="{ 'font-bold text-orange-500': sortBy === 'name' }"
                      @click="sortBy = 'name', closeSortDropdown()">Name</a></li>
                </ul>
              </div>
            </div>

            <!-- Selected Filters Summary (Mobile) -->
            <div v-if="hasActiveFilters" class="md:hidden flex flex-wrap gap-2">
              <div v-if="getSelectedBrands.length > 0" class="badge badge-sm bg-orange-100 text-orange-800 p-2">
                Brand: {{ getSelectedBrands.join(', ') }}
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

              <button
v-if="hasActiveFilters"
                class="btn btn-xs bg-transparent hover:bg-orange-500 border border-gray-300 hover:border-orange-500"
                @click="clearAllFilters">
                Clear all
              </button>
            </div>
          </div>

          <!-- Loading state -->
          <div v-if="isLoading" class="flex justify-center items-center py-12">
            <div class="loading loading-spinner loading-lg text-orange-500" />
          </div>

          <!-- Error state -->
          <div v-else-if="error" class="alert alert-error">
            <svg
xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none"
              viewBox="0 0 24 24">
              <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ error }}</span>
          </div>

          <!-- No products found -->
          <div v-else-if="filteredProducts.length === 0" class="flex flex-col items-center justify-center py-12">
            <svg
xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="mt-4 text-lg font-medium">No products found</h3>
            <p class="mt-1 text-gray-500">Try adjusting your filters or search query</p>
          </div>

          <!-- Slot for page content (products) -->
          <slot v-else />
        </div>
      </div>
    </div>

    <!-- Mobile Filter Modal with Expandable Sections -->
    <div class="modal" :class="{ 'modal-open': filterModalOpen }">
      <div class="modal-box">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold text-lg">Filters</h3>
          <button class="btn btn-sm btn-circle btn-ghost" @click="filterModalOpen = false">✕</button>
        </div>

        <!-- All filters in a single modal with expandable sections -->
        <div class="overflow-y-auto max-h-[60vh]">
          <!-- Brand Section - Expandable -->
          <div class="collapse collapse-arrow border-b">
            <input v-model="modalBrandExpanded" type="checkbox" class="min-h-0">
            <div class="collapse-title font-medium py-3 flex items-center justify-between">
              <span>Brand</span>
              <span v-if="getSelectedBrands.length > 0" class="badge badge-sm badge-primary ml-2">{{
                getSelectedBrands.length }}</span>
            </div>
            <div class="collapse-content">
              <div class="space-y-2 pt-2">
                <div v-for="(brand, index) in brands" :key="index" class="form-control">
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input
v-model="brand.selected" type="checkbox"
                      class="checkbox checkbox-sm checkbox-warning border-gray-300">
                    <span class="label-text">{{ brand.name }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Connection Section - Expandable -->
          <div class="collapse collapse-arrow border-b">
            <input v-model="modalConnectionExpanded" type="checkbox" class="min-h-0">
            <div class="collapse-title font-medium py-3 flex items-center justify-between">
              <span>Connection</span>
              <span v-if="getSelectedConnections.length > 0" class="badge badge-sm badge-primary ml-2">{{
                getSelectedConnections.length }}</span>
            </div>
            <div class="collapse-content">
              <div class="space-y-2 pt-2">
                <div v-for="(connection, index) in connections" :key="index" class="form-control">
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input
v-model="connection.selected" type="checkbox"
                      class="checkbox checkbox-sm checkbox-warning border-gray-300">
                    <span class="label-text">{{ connection.name }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Price Range Section - Expandable -->
          <div class="collapse collapse-arrow">
            <input v-model="modalPriceExpanded" type="checkbox" class="min-h-0">
            <div class="collapse-title font-medium py-3 flex items-center justify-between">
              <span>Price Range</span>
              <span v-if="getSelectedPrices.length > 0" class="badge badge-sm badge-primary ml-2">{{
                getSelectedPrices.length }}</span>
            </div>
            <div class="collapse-content">
              <div class="space-y-2 pt-2">
                <div v-for="(range, index) in priceRanges" :key="index" class="form-control">
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input
v-model="range.selected" type="checkbox"
                      class="checkbox checkbox-sm checkbox-warning border-gray-300">
                    <span class="label-text">{{ range.name }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
          <!-- Availability/Stock filter -->
        </div>

        <div class="modal-action mt-6">
          <button
class="btn bg-orange-500 border-orange-500 hover:bg-orange-600 text-white"
            @click="filterModalOpen = false">
            Apply Filters
          </button>
          <button class="btn btn-outline" :disabled="!hasActiveFilters" @click="clearAllFilters">
            Clear All
          </button>
        </div>
      </div>

      <label class="modal-backdrop" @click="filterModalOpen = false" />
    </div>

    <FooterSection />
  </div>
</template>

<style scoped>

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

.checkbox-warning {
  border-width: 1.5px;
}
.collapse-title,
.form-control label {
  min-height: 48px;
  display: flex;
  align-items: center;
}

.collapse+.collapse {
  margin-top: 1px;
}
</style>