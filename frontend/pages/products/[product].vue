<script setup>

const route = useRoute();
const productSlug = ref(route.params.product);
const product = ref(null);

onMounted(async () => {
  if (productSlug.value) {
    try {
      const response = await fetch(`http://localhost:8000/api/products/${productSlug.value}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      product.value = await response.json();
    } catch (error) {
      console.error('Could not fetch product:', error);
      product.value = { error: true, message: 'Failed to load product.' };
    }
  }
});

</script>

<template>
  <div class="w-full">
    <navbar_header />
    <div class="container mx-auto py-8">
      <!-- Loading State -->
      <div v-if="product === null" class="flex items-center justify-center h-48">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <!-- Error State -->
      <div v-else-if="product.error" class="alert alert-error">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <span>Error: {{ product.message }}</span>
      </div>

      <!-- Product Details -->
      <div v-else class="card w-full bg-base-100 shadow-xl">
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

