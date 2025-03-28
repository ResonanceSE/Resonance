<script setup>
const apiUrl = useRuntimeConfig().public.apiUrl;
const { data: recommendedProducts, error } = useFetch(`${apiUrl}/api/products/recommendations/`);

if (error.value) {
  console.error("Failed to fetch recommendations:", error.value);
}
</script>

<template>
  <section class="container mx-auto py-10 px-4">
    <div class="text-center mb-8">
      <h2 class="text-2xl font-bold mb-2">Recommended For You</h2>
      <div class="w-16 h-1 bg-primary mx-auto"/>
    </div>

    <div v-if="recommendedProducts?.length" class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div 
        v-for="product in recommendedProducts" 
        :key="product.id" 
        class="card bg-base-100 shadow-md hover:shadow-xl transition-all duration-300"
      >
        <figure class="relative overflow-hidden">
          <img 
            :src="product.image_url" 
            :alt="product.name" 
            class="w-full h-48 object-cover transition-transform duration-500 hover:scale-105" 
          >
          <div class="absolute top-2 right-2 badge badge-primary">
            ${{ product.price }}
          </div>
        </figure>

        <div class="card-body">
          <h3 class="card-title text-lg font-semibold">{{ product.name }}</h3>
          <p class="text-sm text-gray-600">{{ product.description }}</p>
          <div class="card-actions justify-end mt-4">
            <button class="btn btn-primary btn-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center text-gray-500">
      No recommended products available.
    </div>
  </section>
</template>
