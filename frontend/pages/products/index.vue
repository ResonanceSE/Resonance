<script setup>
// Use the product layout
definePageMeta({
  layout: 'product-layout'
})

// Set the page title for the layout
const pageTitle = ref('All Products');
provide('pageTitle', pageTitle);

// API URL from runtime config
const apiUrl = useRuntimeConfig().public.apiUrl;

// Get the applied filters from the layout
const appliedFilters = inject('appliedFilters', computed(() => ({ 
  activeFilter: 'All',
  searchQuery: '',
  sortBy: 'default',
  brands: [], 
  types: [], 
  connections: [], 
  priceRanges: [] 
})));

// Fetch all products
const { data: products, error, pending } = useFetch(() => `${apiUrl}/api/products`, {
  method: 'GET',
  immediate: true,
});

// Navigate to product detail
const viewProductDetails = (productId) => {
  window.location.href = `/products/${productId}`;
};

// Mock products for development or when API is unavailable
const mockProducts = [
  { 
    id: 1, 
    name: 'Premium Headphones', 
    detail: 'Noise cancelling with crystal clear sound', 
    price: 299.99, 
    image: '/placeholder.png',
    category: 'headphones',
    brand: 'Sony',
    type: 'Portable',
    connection: 'Bluetooth',
    tags: ['new', 'popular']
  },
  { 
    id: 2, 
    name: 'Wireless Earbuds', 
    detail: 'Compact design with 24-hour battery life', 
    price: 149.99, 
    image: '/placeholder.png',
    category: 'earphones',
    brand: 'Bose',
    type: 'Portable',
    connection: 'Wireless',
    tags: ['promotion']
  },
  { 
    id: 3, 
    name: 'Studio Monitoring Headphones', 
    detail: 'Professional grade for music production', 
    price: 349.99, 
    image: '/placeholder.png',
    category: 'headphones',
    brand: 'JBL',
    type: 'Desktop',
    connection: 'Wired',
    tags: ['recommend']
  },
  { 
    id: 4, 
    name: 'Portable Bluetooth Speaker', 
    detail: 'Waterproof with 20-hour battery life', 
    price: 99.99, 
    image: '/placeholder.png',
    category: 'speakers',
    brand: 'Sonos',
    type: 'Portable',
    connection: 'Bluetooth',
    tags: ['promotion', 'popular']
  },
  { 
    id: 5, 
    name: 'Home Theater System', 
    detail: 'Premium 5.1 surround sound system', 
    price: 899.99, 
    image: '/placeholder.png',
    category: 'speakers',
    brand: 'Harman Kardon',
    type: 'Desktop',
    connection: 'Wired',
    tags: ['new']
  },
  { 
    id: 6, 
    name: 'Gaming Headset', 
    detail: 'Immersive audio with noise-canceling microphone', 
    price: 199.99, 
    image: '/placeholder.png',
    category: 'headphones',
    brand: 'Sony',
    type: 'Desktop',
    connection: 'Wired',
    tags: ['popular', 'recommend']
  },
];

// Filter products based on user selections AND layout filters
const displayProducts = computed(() => {
  let result = products.value || mockProducts;
  
  // Apply search filter from layout
  if (appliedFilters.value.searchQuery) {
    const query = appliedFilters.value.searchQuery.toLowerCase();
    result = result.filter(product => 
      product.name.toLowerCase().includes(query) || 
      product.detail.toLowerCase().includes(query)
    );
  }
  
  // Apply tag filters (promotion, new, popular, etc) from layout
  if (appliedFilters.value.activeFilter !== 'All') {
    result = result.filter(product => 
      product.tags && product.tags.includes(appliedFilters.value.activeFilter.toLowerCase())
    );
  }
  
  // Apply sidebar filters from layout
  if (appliedFilters.value.brands && appliedFilters.value.brands.length > 0) {
    result = result.filter(product => 
      appliedFilters.value.brands.includes(product.brand)
    );
  }
  
  if (appliedFilters.value.types && appliedFilters.value.types.length > 0) {
    result = result.filter(product => 
      appliedFilters.value.types.includes(product.type)
    );
  }
  
  if (appliedFilters.value.connections && appliedFilters.value.connections.length > 0) {
    result = result.filter(product => 
      appliedFilters.value.connections.includes(product.connection)
    );
  }
  
  if (appliedFilters.value.priceRanges && appliedFilters.value.priceRanges.length > 0) {
    result = result.filter(product => {
      if (appliedFilters.value.priceRanges.includes('Under $100') && product.price < 100) {
        return true;
      }
      if (appliedFilters.value.priceRanges.includes('$100 - $300') && product.price >= 100 && product.price <= 300) {
        return true;
      }
      if (appliedFilters.value.priceRanges.includes('$300 - $500') && product.price > 300 && product.price <= 500) {
        return true;
      }
      if (appliedFilters.value.priceRanges.includes('Over $500') && product.price > 500) {
        return true;
      }
      return appliedFilters.value.priceRanges.length === 0;
    });
  }
  
  // Apply sorting from layout
  if (appliedFilters.value.sortBy === 'price-low') {
    result = [...result].sort((a, b) => a.price - b.price);
  } else if (appliedFilters.value.sortBy === 'price-high') {
    result = [...result].sort((a, b) => b.price - a.price);
  } else if (appliedFilters.value.sortBy === 'name') {
    result = [...result].sort((a, b) => a.name.localeCompare(b.name));
  }
  
  return result;
});
</script>

<template>
  <!-- Loading State -->
  <div v-if="pending" class="flex items-center justify-center h-48">
    <span class="loading loading-spinner loading-lg"/>
  </div>

  <!-- Error State -->
  <div v-else-if="error" class="alert alert-error">
    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
    <span>Error: {{ error.message }}</span>
  </div>

  <!-- No results state -->
  <div v-else-if="displayProducts.length === 0" class="flex flex-col items-center justify-center h-48 text-center">
    <Icon name="heroicons:face-frown" class="w-12 h-12 text-gray-400 mb-2" />
    <h3 class="text-lg font-medium text-gray-500">No products found</h3>
    <p class="text-gray-500 mt-1">Try changing your search or filter criteria</p>
  </div>

  <!-- Product grid -->
  <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div v-for="product in displayProducts" :key="product.id" class="card bg-base-100 shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
      <figure class="p-4 bg-base-200 h-48 flex items-center justify-center">
        <img :src="product.image || '/placeholder.png'" :alt="product.name" class="max-h-full" >
      </figure>
      <div class="card-body p-4">
        <!-- Category badge -->
        <div class="badge badge-outline text-xs mb-2">{{ product.category }}</div>
        
        <h2 class="card-title text-lg">{{ product.name }}</h2>
        <p class="text-sm text-gray-600">{{ product.detail }}</p>
        
        <!-- Tags section -->
        <div class="flex flex-wrap gap-1 mt-1">
          <div 
            v-for="tag in product.tags" 
            :key="tag" 
            class="badge badge-sm"
            :class="{
              'badge-primary': tag === 'new',
              'badge-secondary': tag === 'popular',
              'badge-accent': tag === 'promotion',
              'badge-info': tag === 'recommend'
            }"
          >
            {{ tag }}
          </div>
        </div>
        
        <div class="flex justify-between items-center mt-3">
          <div class="text-lg font-bold">${{ product.price.toFixed(2) }}</div>
          <button class="btn btn-primary btn-sm" @click="viewProductDetails(product.id)">View Details</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.badge-primary {
  background-color: #f97316;
  color: white;
}

.badge-secondary {
  background-color: #6366f1;
  color: white;
}

.badge-accent {
  background-color: #10b981;
  color: white;
}

.badge-info {
  background-color: #0ea5e9;
  color: white;
}
</style>