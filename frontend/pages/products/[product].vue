<script setup>
// Define a base URL to ensure consistency
const apiBaseUrl = process.env.API_URL;
const route = useRoute();
const productSlug = computed(() => route.params.product);

// Use relative fetch with baseURL option
const { data: product, error, pending } = useFetch(`${apiBaseUrl}/api/products/${productSlug.value}`, {
  method: 'GET',
  immediate: true,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  },
  retry: 1,
});
</script>

<template>
  <div class="w-full">
    <navbar_header />
    <div class="container mx-auto py-8">
      <!-- Loading State -->
      <div v-if="pending" class="flex items-center justify-center h-48">
        <span class="loading loading-spinner loading-lg" />
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-error">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <span>Error: {{ error.message }}</span>
      </div>

      <!-- Product Details -->
      <div v-else-if="product" class="card w-full bg-base-100 shadow-xl">
        <div class="card-body">
          <h1 class="card-title text-3xl">{{ product.name }}</h1>
          <p class="text-gray-600">{{ product.description }}</p>
          <div class="text-2xl font-bold text-success mt-4">${{ product.price }}</div>
          <div class="card-actions justify-end">
            <nuxt-link to="/products" class="btn btn-primary">Back to Products</nuxt-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
