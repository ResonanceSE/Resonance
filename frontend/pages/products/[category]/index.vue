<script setup lang="ts">

interface Product {
  id: number;
  name: string;
  description?: string;
  slug?: string;
  category?: string;
  brand?: string;
  connections?: string;
  price: number | string;
  sale_price?: number | string | null;
  stock?: number;
  is_active?: boolean;
  is_new?: boolean;
  is_featured?: boolean;
  image_url?: string;
}

definePageMeta({
  layout: 'product-layout'
})

const route = useRoute();
const categorySlug = ref(route.params.category as string);

const categoryNames: Record<string, string> = {
  'headphones': 'Headphones',
  'speakers': 'Speakers',
  'earphones': 'Earphones',
};

// Compute the page title from the category
const pageTitle = computed(() => {
  return categoryNames[categorySlug.value] || 'Products';
});

provide('pageTitle', pageTitle);
provide('currentCategory', categorySlug);

watch(() => route.params.category, (newCategory) => {
  if (newCategory && typeof newCategory === 'string') {
    categorySlug.value = newCategory;
  }
}, { immediate: true });

const filteredProducts = inject<Ref<Product[]>>('filteredProducts', ref([]));
const isLoadingProducts = inject<Ref<boolean>>('isLoadingProducts', ref(false));
const productsError = inject<Ref<string | null>>('productsError', ref(null));

const formatPrice = (price: number | string): string => {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(numPrice);
};

const viewProductDetails = (productId: number): void => {
  window.location.href = (`/products/${categorySlug.value}/${productId}`);
};

</script>

<template>
  <!-- Loading State -->
  <div v-if="isLoadingProducts" class="flex justify-center items-center min-h-[50vh]">
    <div class="text-center">
      <span class="loading loading-spinner loading-lg text-primary"/>
      <p class="mt-4 text-gray-600">Loading products...</p>
    </div>
  </div>

  <!-- Error State -->
  <div v-else-if="productsError" class="alert alert-error">
    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
      <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    <span>Error: {{ productsError }}</span>
  </div>

  <!-- No results state -->
  <div v-else-if="filteredProducts.length === 0" class="flex flex-col items-center justify-center h-48 text-center">
    <svg
xmlns="http://www.w3.org/2000/svg" class="w-12 h-12 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24"
      stroke="currentColor">
      <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    <h3 class="text-lg font-medium text-gray-500">No products found</h3>
    <p class="text-gray-500 mt-1">Try changing your search or filter criteria</p>
  </div>

  <!-- Product grid -->
  <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div
v-for="product in filteredProducts" :key="product.id"
      class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow duration-300" :class="[
        product.stock !== undefined ? (
          product.stock > 0 ? 'bg-green-50' : 'bg-red-50'
        ) : ''
      ]">
      <figure class="p-4 bg-base-200 h-48 flex items-center justify-center">
        <img :src="product.image_url || '/placeholder.png'" :alt="product.name" class="max-h-full">
      </figure>
      <div class="card-body p-4">
        <div class="flex justify-between items-start">
          <div class="flex flex-col">
            <h2 class="card-title text-lg">{{ product.name }}</h2>
            <h2 class="card-title text-sm text-primary">{{ product.brand }}</h2>
          </div>
          <!-- Stock badge -->
          <div
v-if="product.stock !== undefined" class="badge text-white"
            :class="product.stock > 0 ? 'bg-green-500' : 'bg-red-500'">
            {{ product.stock > 0 ? product.stock : 'Out of stock' }}
          </div>
        </div>
        <p class="text-sm text-gray-600 mt-2 line-clamp-2">{{ product.description || 'No description available' }}</p>
        <div class="flex justify-between items-center mt-2">
          <div>
            <span v-if="product.sale_price" class="text-lg font-bold text-primary">
              {{ formatPrice(product.sale_price) }}
              <span class="text-sm line-through text-gray-400 ml-1">{{ formatPrice(product.price) }}</span>
            </span>
            <span v-else class="text-lg font-bold">{{ formatPrice(product.price) }}</span>
          </div>
          <button
class="btn btn-primary btn-sm" :disabled="product.stock !== undefined && product.stock <= 0"
            @click="viewProductDetails(product.id)">
            View Details
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Add any category-specific styles here */
</style>