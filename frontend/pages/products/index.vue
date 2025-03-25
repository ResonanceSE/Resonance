<script setup lang="ts">
// Define the Product interface directly
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
  tags?: string[];
}

// Define the layout metadata
definePageMeta({
  layout: 'product-layout'
});

// Set page title
const pageTitle = ref('All Products');
provide('pageTitle', pageTitle);

provide('currentCategory', ref(''));

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

const viewProductDetails = (productId: number, category: string): void => {
  if (category) {
    window.location.href = (`/products/${category}/${productId}`);
  } else {
    window.location.href = (`/products/${productId}`);
  }
};
</script>

<template>
  <!-- Product grid -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div 
      v-for="product in filteredProducts" 
      :key="product.id" 
      class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow duration-300"
    >
      <figure class="p-4 bg-base-200 h-48 flex items-center justify-center">
        <img 
          :src="product.image_url || '/placeholder.png'" 
          :alt="product.name" 
          class="max-h-full"
        >
      </figure>
      <div class="card-body p-4">
        <div class="flex justify-between items-start">
          <h2 class="card-title text-lg">{{ product.name }}</h2>
          <!-- Category badge -->
          <div v-if="product.category" class="badge badge-accent text-white">
            {{ product.category }}
          </div>
        </div>
        <p class="text-sm text-gray-600">{{ product.description }}</p>
        <div class="flex justify-between items-center mt-2">
          <div class="text-lg font-bold">{{ formatPrice(product.price) }}</div>
          <button 
            class="btn btn-primary btn-sm" 
            @click="viewProductDetails(product.id, product.category || '')"
          >
            View Details
          </button>
        </div>
      </div>
    </div>
  </div>
</template>