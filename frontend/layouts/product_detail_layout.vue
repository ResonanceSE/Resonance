<script setup>
import { useAuthStore } from '~/stores/useAuth';
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const storeProductParams = (category, id) => {
  if (category && id) {
    localStorage.setItem('lastProductCategory', category);
    localStorage.setItem('lastProductId', id);
    console.log('Stored product params:', { category, id });
  }
};

const getProductId = () => {
  const routeId = route.params.id || route.query.id;
  return routeId || localStorage.getItem('lastProductId');
};

const getCategory = () => {
  const routeCategory = route.params.category || route.query.category;
  return routeCategory || localStorage.getItem('lastProductCategory');
};

const productId = computed(() => getProductId());
const category = computed(() => getCategory());

watch([productId, category], ([newId, newCategory]) => {
  console.log("Product parameters:", { category: newCategory, productId: newId, path: route.path });
}, { immediate: true });

const apiUrl = useRuntimeConfig().public.apiUrl || 'http://localhost:8000';

const product = ref(null);
const isLoading = ref(true);
const error = ref(null);
const addToCartSuccess = ref(false);
const selectedImage = ref(0);
const quantity = ref(1);
const attemptedFetch = ref(false);

const breadcrumbs = computed(() => [
  { name: 'Home', path: '/' },
  { name: 'Products', path: '/products' },
  { name: capitalizeFirstLetter(category.value), path: `/products/${category.value}` },
  { name: product.value?.name || 'Product Details', path: '' }
]);

const layoutProps = computed(() => {
  if (!product.value) return {};
  
  return {
    brand: product.value.brand || '',
    name: product.value.name || '',
    price: product.value.price || 0,
    mainImage: product.value.image_url || product.value.images?.[selectedImage.value] || `https://via.placeholder.com/500x500?text=Product+Image`,
    images: product.value.images || [],
    colors: product.value.colors || [],
    description: product.value.description || '',
    features: product.value.features || [],
    stock: product.value.stock || 0
  };
});

const capitalizeFirstLetter = (string) => {
  if (!string) return '';
  return string.charAt(0).toUpperCase() + string.slice(1);
};

const formatCurrency = (price) => {
  const numericPrice = typeof price === 'string' ? parseFloat(price) : price;
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(numericPrice || 0);
};

const selectImage = (index) => {
  selectedImage.value = index;
};

const decreaseQuantity = () => {
  if (quantity.value > 1) {
    quantity.value--;
  }
};

const increaseQuantity = () => {
  if (quantity.value < 10) {
    quantity.value++;
  }
};

const handleAddToCart = () => {
  if (!product.value) return;
  const cart = JSON.parse(localStorage.getItem(`cart_${authStore.user.username || 'guest'}`) || '[]');
  const existingProductIndex = cart.findIndex(item => 
    item.id === product.value.id && 
    item.category === product.value.category
  );
  
  if (existingProductIndex >= 0) {
    cart[existingProductIndex].quantity += quantity.value;
  } else {
    cart.push({
      id: product.value.id,
      name: product.value.name,
      price: product.value.price,
      image: product.value.images?.[0] || '',
      category: product.value.category,
      quantity: quantity.value
    });
  }
  localStorage.setItem(`cart_${authStore.user.username || 'guest'}`, JSON.stringify(cart));
  
  addToCartSuccess.value = true;
  setTimeout(() => {
    addToCartSuccess.value = false;
  }, 2000);
};

const fetchProduct = async () => {
  const currentCategory = category.value;
  const currentProductId = productId.value;
  
  if (!currentCategory || !currentProductId) {
    console.error('Missing required parameters for product fetch', { currentCategory, currentProductId });
    error.value = 'Invalid product URL. Missing category or ID.';
    isLoading.value = false;
    attemptedFetch.value = true;
    return;
  }
  isLoading.value = true;
  error.value = null;
  attemptedFetch.value = true;

  const url = `${apiUrl}/api/products/${currentCategory}/${currentProductId}`;
  console.log(`Fetching product: ${url}`);
  
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch product: ${response.status}`);
    }
    
    const data = await response.json();
    product.value = data;
    
    storeProductParams(currentCategory, currentProductId);

    selectedImage.value = 0;
    quantity.value = 1;
  } catch (err) {
    console.error('Error fetching product:', err);
    error.value = 'Failed to load product details. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

const tryAgain = () => {
  error.value = null;
  const urlCategory = route.params.category || extractCategoryFromPath(route.path) || route.query.category;
  const urlProductId = route.params.id || route.query.id;
  
  if (urlCategory && urlProductId) {
    fetchProduct();
  } else {
    const lastCategory = localStorage.getItem('lastProductCategory');
    const lastProductId = localStorage.getItem('lastProductId');
    
    if (lastCategory && lastProductId) {
      console.log('Redirecting to last known product:', { lastCategory, lastProductId });
      router.replace(`/products/${lastCategory}/${lastProductId}`);
    } else {
      error.value = 'Cannot find product information. Please browse products from the main page.';
      isLoading.value = false;
    }
  }
};
watch([productId, category], ([newId, newCategory]) => {
  if (newId && newCategory) {
    fetchProduct();
  } else if (attemptedFetch.value) {
    error.value = 'Invalid product URL. Missing category or ID.';
    isLoading.value = false;
  }
}, { immediate: true });

onMounted(() => {
  window.addEventListener('popstate', () => {
    console.log('Back/forward navigation detected');
    setTimeout(() => {
      const currentCategory = getCategory();
      const currentProductId = getProductId();
      
      console.log('After popstate:', { currentCategory, currentProductId });
      
      if (currentCategory && currentProductId) {
        fetchProduct();
      }
    }, 50);
  });
});

onUnmounted(() => {
  window.removeEventListener('popstate', () => {});
});

provide('product', product);
provide('isLoading', isLoading);
provide('error', error);
provide('layoutProps', layoutProps);
provide('handleAddToCart', handleAddToCart);
provide('formatCurrency', formatCurrency);
provide('tryAgain', tryAgain);
</script>

<template>
  <div>
    <!-- Header -->
    <NavbarHeader/>
    
    <div class="bg-gray-50">
      <!-- Loading state -->
      <div v-if="isLoading" class="container mx-auto px-4 py-24 text-center">
        <div class="flex flex-col items-center justify-center">
          <div class="loading-spinner"/>
          <p class="mt-4 text-gray-500">Loading product details...</p>
        </div>
      </div>
      
      <!-- Error state -->
      <div v-else-if="error" class="container mx-auto px-4 py-16">
        <div class="bg-white rounded-lg shadow-md p-8 max-w-2xl mx-auto">
          <div class="flex items-center text-red-500 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h2 class="text-xl font-bold">Error Loading Product</h2>
          </div>
          <p class="text-gray-600 mb-6">{{ error }}</p>
          <button class="btn btn-primary" @click="fetchProduct">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Try Again
          </button>
        </div>
      </div>
      
      <!-- Product display -->
      <div v-else-if="product" class="container mx-auto px-4 py-8">
        <!-- Breadcrumbs -->
        <div class="mb-6 hidden md:block">
          <div class="flex items-center text-sm text-gray-500">
            <NuxtLink
v-for="(crumb, index) in breadcrumbs.slice(0, -1)" :key="index" :to="crumb.path" 
              class="hover:text-orange-500 transition-colors">
              {{ crumb.name }}
              <span v-if="index < breadcrumbs.length - 2" class="mx-2">/</span>
            </NuxtLink>
            <span class="mx-2 text-gray-300">/</span>
            <span class="text-gray-700 font-medium">{{ breadcrumbs[breadcrumbs.length - 1].name }}</span>
          </div>
        </div>
        
        <!-- Main product section -->
        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-0">
            <!-- Product Images Section -->
            <div class="bg-gray-50 p-6 flex flex-col">
              <!-- Main image with zoom effect -->
              <div class="relative bg-white rounded-lg overflow-hidden mb-4 h-80 md:h-96">
                <img 
                  :src="layoutProps.images[selectedImage]" 
                  :alt="layoutProps.name" 
                  class="w-full h-full object-contain hover:scale-105 transition-transform duration-500"
                >
              </div>
              
              <!-- Thumbnails -->
              <div class="flex gap-3 overflow-x-auto pb-2">
                <button 
                  v-for="(image, index) in layoutProps.images" 
                  :key="index" 
                  class="w-20 h-20 p-1 rounded-md flex-shrink-0 transition-all duration-200 overflow-hidden"
                  :class="selectedImage === index ? 'ring-2 ring-orange-500 bg-white shadow-md' : 'bg-white hover:shadow-md'"
                  @click="selectImage(index)"
                >
                  <img 
                    :src="image" 
                    :alt="`${layoutProps.name} thumbnail ${index + 1}`" 
                    class="w-full h-full object-contain"
                  >
                </button>
              </div>
            </div>
            
            <!-- Product Details Section -->
            <div class="p-6 md:p-8 flex flex-col">
              <!-- Brand and Name -->
              <div class="mb-6">
                <div class="inline-block px-3 py-1 bg-gray-100 text-gray-600 text-xs font-medium rounded-full mb-2">
                  {{ layoutProps.brand }}
                </div>
                <h1 class="text-2xl md:text-3xl font-bold text-gray-900">{{ layoutProps.name }}</h1>
              </div>
              
              <!-- Price -->
              <div class="text-3xl font-bold text-orange-500 mb-6">
                {{ formatCurrency(layoutProps.price) }}
              </div>
              
              <!-- Description -->
              <div class="mb-6">
                <h2 class="text-lg font-semibold mb-2 text-gray-900">Description</h2>
                <p class="text-gray-700 leading-relaxed">{{ layoutProps.description }}</p>
              </div>
              
              <!-- Colors -->
              <div v-if="layoutProps.colors && layoutProps.colors.length > 0" class="mb-6">
                <h2 class="text-lg font-semibold mb-3 text-gray-900">Colors</h2>
                <div class="flex flex-wrap gap-3">
                  <div 
                    v-for="color in layoutProps.colors" 
                    :key="color.value"
                    class="relative w-10 h-10 rounded-full cursor-pointer border-2 border-white shadow-sm hover:shadow-md transition-shadow"
                    :style="`background-color: ${color.hex}`"
                    :title="color.label"
                  >
                    <span class="sr-only">{{ color.label }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Features -->
              <div class="mb-6">
                <h2 class="text-lg font-semibold mb-3 text-gray-900">Features</h2>
                <ul class="space-y-2">
                  <li v-for="(feature, index) in layoutProps.features" :key="index" class="flex items-start">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <span class="text-gray-700">{{ feature }}</span>
                  </li>
                </ul>
              </div>
              
              <!-- Quantity and Add to Cart -->
              <div class="mt-auto">
                <div class="flex flex-col sm:flex-row sm:items-center gap-4 mb-4">
                  <!-- Stock status -->
                  <div v-if="layoutProps.stock > 0" class="flex items-center text-green-600 text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    In Stock
                  </div>
                  <div v-else class="flex items-center text-red-500 text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    Out of Stock
                  </div>
                  
                  <!-- Quantity selector -->
                  <div class="join border border-gray-300 rounded-lg">
                    <button 
                      class="join-item btn btn-sm btn-ghost text-gray-700 px-3" 
                      :disabled="quantity <= 1"
                      @click="decreaseQuantity"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                      </svg>
                    </button>
                    <div class="join-item flex items-center justify-center w-10 bg-white text-gray-800">
                      {{ quantity }}
                    </div>
                    <button 
                      class="join-item btn btn-sm btn-ghost text-gray-700 px-3" 
                      :disabled="quantity >= 10"
                      @click="increaseQuantity"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                      </svg>
                    </button>
                  </div>
                </div>
                
                <!-- Add to cart button -->
                <button 
                  class="btn btn-primary btn-lg w-full group"
                  :disabled="layoutProps.stock <= 0"
                  @click="handleAddToCart"
                >
                  <span class="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 group-hover:animate-bounce" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    {{ layoutProps.stock > 0 ? 'Add to Cart' : 'Out of Stock' }}
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Additional product information -->
        <div class="mt-12 bg-white rounded-xl shadow-sm overflow-hidden">
          <div class="tabs tabs-bordered">
            <a class="tab tab-bordered tab-active">Details</a>
            <a class="tab tab-bordered">Specifications</a>
          </div>
          <div class="p-6">
            <div class="prose max-w-none">
              <p>{{ layoutProps.description }}</p>
              
              <h3>Key Features</h3>
              <ul>
                <li v-for="(feature, index) in layoutProps.features" :key="index">
                  {{ feature }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <div class="mt-12">
          <slot/>
        </div>
      </div>
      
      <!-- No product found state -->
      <div v-else class="container mx-auto px-4 py-16 text-center">
        <div class="bg-white rounded-lg shadow-md p-8 max-w-2xl mx-auto">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h2 class="text-2xl font-bold mb-2">Product Not Found</h2>
          <p class="text-gray-600 mb-6">We couldn't find the product you're looking for. It may have been removed or the URL might be incorrect.</p>
          
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <NuxtLink :to="`/products/${category}`" class="btn btn-primary">
              Browse {{ capitalizeFirstLetter(category) }}
            </NuxtLink>
            <NuxtLink to="/products" class="btn btn-outline">
              View All Products
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Mobile sticky add to cart -->
    <div v-if="product && !isLoading" class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-3 md:hidden z-10">
      <div class="flex items-center justify-between">
        <div>
          <div class="text-lg font-bold text-orange-500">{{ formatCurrency(layoutProps.price) }}</div>
          <div v-if="layoutProps.stock > 0" class="text-xs text-green-600">In Stock</div>
          <div v-else class="text-xs text-red-500">Out of Stock</div>
        </div>
        <button 
          class="btn btn-primary"
          :disabled="layoutProps.stock <= 0"
          @click="handleAddToCart"
        >
          Add to Cart
        </button>
      </div>
    </div>
    
    <!-- Add to cart success toast -->
    <div v-if="addToCartSuccess" class="toast toast-end z-50">
      <div class="alert alert-success shadow-lg">
        <div class="flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h3 class="font-bold">Added to Cart!</h3>
            <div class="text-xs">{{ quantity }} × {{ layoutProps.name }}</div>
          </div>
        </div>
        <div class="flex-none">
          <NuxtLink to="/cart" class="btn btn-sm btn-ghost">View Cart</NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.loading-spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 3px solid rgba(249, 115, 22, 0.2);
  border-radius: 50%;
  border-top-color: rgba(249, 115, 22, 1);
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Add hover effect to product thumbnails */
.thumbnail-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Smooth transitions */
.btn, .btn-primary, img {
  transition: all 0.3s ease;
}

/* Group hover animation for add to cart icon */
.group:hover .group-hover\:animate-bounce {
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(-5%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}
</style>