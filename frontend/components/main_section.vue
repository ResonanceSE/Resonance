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

const apiUrl = useRuntimeConfig().public.apiUrl;

const { data: recommendedProducts, error } = await useFetch<Product[]>(`${apiUrl}/api/products/recommendations/`);

if (error.value) {
  console.error("Failed to fetch recommendations:", error.value);
}

const categoryMapping: Record<string | number, string> = {
  '1': 'headphones',
  '2': 'speakers',
  '3': 'earphones',
};

const router = useRouter();
const route = useRoute();

const viewProductDetails = (productId: number, category: string | number): void => {
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
  
  // Fallback
  router.push(`/products/${productId}`);
};
</script>

<template>
  <section class="container mx-auto py-10 px-4">
    <div class="text-center mb-8">
      <h2 class="text-2xl font-bold mb-2">Recommended For You</h2>
      <div class="w-16 h-1 bg-primary mx-auto"/>
    </div>

    <div v-if="recommendedProducts && recommendedProducts.length > 0" class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div 
        v-for="product in recommendedProducts" 
        :key="product.id" 
        class="card bg-base-100 shadow-md hover:shadow-xl transition-all duration-300"
      >
        <figure class="relative overflow-hidden">
          <img 
            :src="product.image_url || '/placeholder.png'" 
            :alt="product.name" 
            class="w-full h-48 object-cover transition-transform duration-500 hover:scale-105" 
          >
          <div class="absolute top-2 right-2 badge badge-primary">
            {{ typeof product.price === 'number' ? '$' + product.price.toFixed(2) : '$' + product.price }}
          </div>
        </figure>

        <div class="card-body">
          <h3 class="card-title text-lg font-semibold">{{ product.name }}</h3>
          <p class="text-sm text-gray-600 line-clamp-2">{{ product.description || 'No description available' }}</p>
          <div class="card-actions justify-end mt-4">
            <button 
              class="btn btn-primary btn-sm"
              @click="viewProductDetails(product.id, product.category || '')"
            >
              <Icon name="material-symbols:arrow-right-alt-rounded" class="mr-2"/>
              View Detail
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