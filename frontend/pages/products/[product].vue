<!-- pages/products/index.vue -->
<script setup>
import { NuxtImg } from '#components';

// Access route params
const route = useRoute();
const productSlug = ref(route.params.product);
const apiUrl = useRuntimeConfig().public.apiUrl
const { data: product, error, pending } = useFetch(() => `${apiUrl}/api/products/${productSlug.value}`, {
  method: 'GET',
  immediate: true, //
});

const activeCategory = ref('Headphones'); 
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

// Navigate to product detail
const viewProductDetails = (productId) => {
  route.push(`/products/${productSlug.value}/${productId}`);
};

// Default Template
const mockProducts = [
  { id: 1, name: 'Premium Bookshelf Speaker', detail: 'High-fidelity audio with deep bass', price: 299.99, image: '/placeholder.png' },
  { id: 2, name: 'Portable Bluetooth Speaker', detail: 'Waterproof design with 20-hour battery', price: 149.99, image: '/placeholder.png' },
  { id: 3, name: 'Wireless Surround System', detail: 'Complete 5.1 cinema experience', price: 599.99, image: '/placeholder.png' },
  { id: 4, name: 'Desktop Gaming Speakers', detail: 'RGB lighting with powerful sound', price: 199.99, image: '/placeholder.png' },
  { id: 5, name: 'Smart Home Speaker', detail: 'Voice control with premium sound', price: 249.99, image: '/placeholder.png' },
  { id: 6, name: 'Outdoor Party Speaker', detail: 'Weather-resistant with LED lights', price: 329.99, image: '/placeholder.png' },
];

const displayProducts = computed(() => {
  return product.value || mockProducts;
});
</script>

<template>
  <div class="w-full bg-base-100">
    <navbar_header/>
    <div class="container mx-auto px-4 py-8">
      <!-- Category header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-center md:text-right">{{ activeCategory }}</h1>
      </div>

      <!-- Main content area with sidebar and products -->
      <div class="flex flex-col md:flex-row gap-8">
        <!-- Sidebar with filters -->
        <div class="w-full md:w-64 flex-shrink-0">
          <div class="card bg-base-100 shadow-md">
            <div class="card-body p-4">
              <h2 class="text-xl font-bold mb-4">Filter</h2>

              <!-- Brand filter -->
              <div class="collapse collapse-arrow border-b">
                <input type="checkbox" v-model="brandExpanded" />
                <div class="collapse-title font-medium">
                  Brand
                </div>
                <div class="collapse-content">
                  <div v-for="(brand, index) in brands" :key="index" class="form-control">
                    <label class="cursor-pointer label justify-start">
                      <input type="checkbox" v-model="brand.selected" class="checkbox checkbox-sm checkbox-primary" />
                      <span class="label-text ml-2">{{ brand.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Type filter -->
              <div class="collapse collapse-arrow border-b">
                <input type="checkbox" v-model="typeExpanded" />
                <div class="collapse-title font-medium">
                  Type <span class="text-xs text-gray-400">(Portable/Desktop)</span>
                </div>
                <div class="collapse-content">
                  <div v-for="(type, index) in types" :key="index" class="form-control">
                    <label class="cursor-pointer label justify-start">
                      <input type="checkbox" v-model="type.selected" class="checkbox checkbox-sm checkbox-primary" />
                      <span class="label-text ml-2">{{ type.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Connection filter -->
              <div class="collapse collapse-arrow border-b">
                <input type="checkbox" v-model="connectionExpanded" />
                <div class="collapse-title font-medium">
                  Connection
                </div>
                <div class="collapse-content">
                  <div v-for="(connection, index) in connections" :key="index" class="form-control">
                    <label class="cursor-pointer label justify-start">
                      <input type="checkbox" v-model="connection.selected" class="checkbox checkbox-sm checkbox-primary" />
                      <span class="label-text ml-2">{{ connection.name }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Price Range filter -->
              <div class="collapse collapse-arrow">
                <input type="checkbox" v-model="priceExpanded" />
                <div class="collapse-title font-medium">
                  Price Range
                </div>
                <div class="collapse-content">
                  <div v-for="(range, index) in priceRanges" :key="index" class="form-control">
                    <label class="cursor-pointer label justify-start">
                      <input type="checkbox" v-model="range.selected" class="checkbox checkbox-sm checkbox-primary" />
                      <span class="label-text ml-2">{{ range.name }}</span>
                    </label>
                  </div>
                </div>
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
                @click="setFilter(filter.name)"
                :class="[
                  'btn btn-sm', 
                  activeFilter === filter.name ? 'btn-warning' : 'btn-outline'
                ]"
              >
                {{ filter.name }}
              </button>
            </div>
            <div class="flex gap-2 w-full md:w-auto">
              <input type="text" placeholder="Search Products" class="input input-bordered w-full md:w-auto" v-model="searchQuery" />
              <div class="dropdown dropdown-end">
                <label tabindex="0" class="btn btn-sm btn-outline gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h- w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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

          <!-- Loading State -->
          <div v-if="pending" class="flex items-center justify-center h-48">
            <span class="loading loading-spinner loading-lg"></span>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="alert alert-error">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <span>Error: {{ error.message }}</span>
          </div>

          <!-- Product grid -->
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="product in displayProducts" :key="product.id" class="card bg-base-100 shadow-xl">
              <figure class="p-4 bg-base-200 h-48 flex items-center justify-center">
                <NuxtImg src="" alt="Product" />
              </figure>
              <div class="card-body p-4">
                <h2 class="card-title text-lg">{{ product.name }}</h2>
                <p class="text-sm text-gray-600">{{ product.detail }}</p>
                <div class="flex justify-between items-center mt-2">
                  <div class="text-lg font-bold">${{ product.price }}</div>
                  <button class="btn btn-primary btn-sm" @click="viewProductDetails(product.id)">Buy Now</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>