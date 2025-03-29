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
});

const router = useRouter();

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
    currency: 'THB'
  }).format(numPrice);
};

const categoryMapping: Record<string | number, string> = {
  '1': 'headphones',
  '2': 'speakers',
  '3': 'earphones',
};

const viewProductDetails = (productId: number, category: string | number): void => {
  const route = useRoute();
  
  if (category && categoryMapping[category]) {
    router.push(`/products/${categoryMapping[category]}/${productId}`);
    return;
  }
  
  const currentCategory = route.params.category;
  if (currentCategory) {
    router.push(`/products/${currentCategory}/${productId}`);
    return;
  }
  
  if (category) {
    const categorySlug = String(category).toLowerCase();
    router.push(`/products/${categorySlug}/${productId}`);
    return;
  }
};
</script>

<template>
  <!-- Loading state -->
  <div v-if="isLoadingProducts" class="flex justify-center items-center py-12">
    <div class="loading loading-spinner loading-lg text-primary"/>
  </div>
  
  <!-- Error state -->
  <div v-else-if="productsError" class="alert alert-error shadow-lg my-4">
    <div>
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>{{ productsError }}</span>
    </div>
  </div>
  
  <!-- Empty state -->
  <div v-else-if="filteredProducts.length === 0" class="text-center py-12">
    <h3 class="text-lg font-semibold">No products found</h3>
    <p class="text-gray-600">Try adjusting your filters or search criteria</p>
  </div>

  <!-- Product grid -->
  <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div 
      v-for="product in filteredProducts" 
      :key="product.id" 
      class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow duration-300"
      :class="[
        product.stock !== undefined ? (
          product.stock > 0 ? 'bg-green-50' : 'bg-red-50'
        ) : ''
      ]"
    >
      <figure class="p-4 bg-base-200 h-48 flex items-center justify-center">
        <img 
          :src="product.image_url || '/placeholder.png'" 
          :alt="product.name" 
          class="max-h-full object-contain"
        >
      </figure>
      <div class="card-body p-4">
        <div class="flex justify-between items-start">
          <h2 class="card-title text-lg">{{ product.name }}</h2>
          <!-- Stock badge -->
          <div 
            v-if="product.stock !== undefined" 
            class="badge text-white"
            :class="product.stock > 0 ? 'bg-green-500' : 'bg-red-500'"
          >
            {{ product.stock > 0 ? product.stock : 'Out of stock' }}
          </div>
        </div>
        <p class="text-sm text-gray-600 mt-2 line-clamp-2">{{ product.description || 'No description available' }}</p>
        <div class="flex justify-between items-center mt-4">
          <div>
            <span v-if="product.sale_price" class="text-lg font-bold text-primary">
              {{ formatPrice(product.sale_price) }}
              <span class="text-sm line-through text-gray-400 ml-1">{{ formatPrice(product.price) }}</span>
            </span>
            <span v-else class="text-lg font-bold">{{ formatPrice(product.price) }}</span>
          </div>
          <button 
            class="btn btn-primary btn-sm" 
            :disabled="product.stock !== undefined && product.stock <= 0"
            @click="viewProductDetails(product.id, product.category || '')"
          >
            View Details
          </button>
        </div>
      </div>
    </div>
  </div>
</template>