<script setup>

definePageMeta({
  layout: 'product-layout'
})

const route = useRoute();
const categorySlug = ref(route.params.category);

const categoryNames = {
  'headphones': 'Headphones',
  'speakers': 'Speakers',
  'earphones': 'Earphones'
};

const pageTitle = computed(() => {
  return categoryNames[categorySlug.value] || 'Products';
});

provide('pageTitle', pageTitle);

// Use the composable to fetch products
const apiUrl = useRuntimeConfig().public.apiUrl;

const { data: products, error, pending } = useFetch(() => `${apiUrl}/api/products/${categorySlug.value}`, {
  method: 'GET',
  immediate: true,
});

// Get the appliedFilters from the layout - the layout handles all filtering UI
const appliedFilters = inject('appliedFilters', computed(() => ({ 
  activeFilter: 'All',
  searchQuery: '',
  sortBy: 'default',
  brands: [], 
  types: [], 
  connections: [], 
  priceRanges: [] 
})));

// Navigate to product detail
const viewProductDetails = (productId) => {
  window.location.href = `/products/${categorySlug.value}/${productId}`
};

// Fallback data in case API fails (for development)
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
];


const displayProducts = computed(() => {
  let result = Array.isArray(products.value) ? products.value : mockProducts;
  
  // Category filter - with safety check
  if (categorySlug.value) {
    result = result.filter(product => 
      product?.category === categorySlug.value || "DefaultType"
    );
  }
  console.log(result);
  // Apply search filter - with safety check
  if (appliedFilters.value.searchQuery) {
    const query = appliedFilters.value.searchQuery.toLowerCase();
    result = result.filter(product => 
      (product?.name?.toLowerCase()?.includes(query)) || 
      (product?.detail?.toLowerCase()?.includes(query))
    );
  }
  
  // Apply tag filters - with safety check
  if (appliedFilters.value.activeFilter !== 'All') {
    const filterLower = appliedFilters.value.activeFilter.toLowerCase();
    result = result.filter(product => 
      product?.tags && Array.isArray(product.tags) && 
      product.tags.includes(filterLower)
    );
  }
  
  // Apply brand filters - with safety check
  if (appliedFilters.value.brands && appliedFilters.value.brands.length > 0) {
    result = result.filter(product => 
      product?.brand && appliedFilters.value.brands.includes(product.brand)
    );
  }
  
  // Apply type filters - with safety check
  if (appliedFilters.value.types && appliedFilters.value.types.length > 0) {
    result = result.filter(product => 
      product?.type && appliedFilters.value.types.includes(product.type)
    );
  }
  
  // Apply connection filters - with safety check
  if (appliedFilters.value.connections && appliedFilters.value.connections.length > 0) {
    result = result.filter(product => 
      product?.connection && appliedFilters.value.connections.includes(product.connection)
    );
  }
  
  // Apply price range filters - with safety check
  if (appliedFilters.value.priceRanges && appliedFilters.value.priceRanges.length > 0) {
    result = result.filter(product => {
      if (!product?.price) return false;
      
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
      return false;
    });
  }
  
  // Apply sorting - with safety check
  if (appliedFilters.value.sortBy) {
    if (appliedFilters.value.sortBy === 'price-low') {
      result = [...result].sort((a, b) => (a?.price || 0) - (b?.price || 0));
    } else if (appliedFilters.value.sortBy === 'price-high') {
      result = [...result].sort((a, b) => (b?.price || 0) - (a?.price || 0));
    } else if (appliedFilters.value.sortBy === 'name') {
      result = [...result].sort((a, b) => (a?.name || '').localeCompare(b?.name || ''));
    }
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
    <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    <h3 class="text-lg font-medium text-gray-500">No products found</h3>
    <p class="text-gray-500 mt-1">Try changing your search or filter criteria</p>
  </div>

  <!-- Product grid -->
  <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div v-for="product in displayProducts" :key="product.id" class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow duration-300">
      <figure class="p-4 bg-base-200 h-48 flex items-center justify-center">
        <img :src="product.image || '/placeholder.png'" :alt="product.name" class="max-h-full" >
      </figure>
      <div class="card-body p-4">
        <h2 class="card-title text-lg">{{ product.name }}</h2>
        <p class="text-sm text-gray-600">{{ product.detail }}</p>
        <div class="flex justify-between items-center mt-2">
          <div class="text-lg font-bold">${{ product.price}}</div>
          <button class="btn btn-primary btn-sm" @click="viewProductDetails(product.id)">Buy Now</button>
        </div>
      </div>
    </div>
  </div>
</template>