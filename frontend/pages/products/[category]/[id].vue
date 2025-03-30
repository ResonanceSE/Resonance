<script setup>
import { useAuthStore } from '~/stores/useAuth';
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const categoryMapping = {
  '1': 'headphones',
  '2': 'speakers',
  '3': 'earphones',
};

const categoryDisplayNames = {
  'headphones': 'Headphones',
  'speakers': 'Speakers',
  'earphones': 'Earphones / IEMs',
};

const storeProductParams = (category, id) => {
  if (import.meta.client && category && id) {
    localStorage.setItem('lastProductCategory', category);
    localStorage.setItem('lastProductId', id);
  }
};

const getProductId = () => {
  const routeId = route.params.id || route.query.id;
  if (import.meta.client) {
    return routeId || localStorage.getItem('lastProductId');
  }
  return routeId;
};

const getCategory = () => {
  const routeCategory = route.params.category || route.query.category;
  if (import.meta.client) {
    return routeCategory || localStorage.getItem('lastProductCategory');
  }
  return routeCategory;
};

const productId = computed(() => getProductId());
const category = computed(() => getCategory());


const categorySlug = computed(() => {
  return route.params.category;
});

// Get display name for category
const categoryDisplayName = computed(() => {
  if (route.params.category && categoryDisplayNames[route.params.category]) {
    return categoryDisplayNames[route.params.category];
  }
  return capitalizeFirstLetter(categorySlug.value);
});

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
const relatedProducts = ref([]);

const layoutProps = computed(() => {
  if (!product.value) return {};
  const images = [];
  if (product.value.image_url) {
    images.push(product.value.image_url);
  }

  if (Array.isArray(product.value.images)) {
    images.push(...product.value.images);
  }

  if (images.length === 0) {
    images.push(`https://via.placeholder.com/500x500?text=Product+Image`);
  }


  const features = product.value.features || [];
  if (features.length === 0 && product.value.description) {
    const sentences = product.value.description.split(/[.!?]+/).filter(s => s.trim().length > 10);
    for (let i = 0; i < Math.min(sentences.length, 4); i++) {
      features.push(sentences[i].trim());
    }
  }

  return {
    brand: product.value.brand || '',
    name: product.value.name || '',
    price: product.value.price || 0,
    mainImage: images[selectedImage.value] || images[0],
    images: images,
    colors: product.value.colors || [],
    description: product.value.description || '',
    features: features,
    stock: product.value.stock || 0,
    connections: product.value.connections || ''
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
  if (quantity.value < layoutProps.value.stock) {
    quantity.value++;
  }
};

watch(product, (newProduct) => {
  if (newProduct) {
    quantity.value = Math.min(1, newProduct.stock);
  }
}, { immediate: true });

const handleAddToCart = async () => {
  if (!authStore.user) {
    router.push('/login');
  }
  if (!product.value || !import.meta.client) return;

  try {
    const stockCheckUrl = `${apiUrl}/api/products/check-stock/${product.value.id}/`;
    const stockResponse = await fetch(stockCheckUrl);

    if (!stockResponse.ok) {
      throw new Error('Failed to check product stock');
    }

    const stockData = await stockResponse.json();
    const availableStock = stockData.data.stock || 0;
    if (availableStock <= 0) {
      alert('Sorry, this item is out of stock.');
      return;
    }

    const cart = JSON.parse(localStorage.getItem(`cart_${authStore.user?.username || 'guest'}`) || '[]');
    const existingProductIndex = cart.findIndex(item => item.id === product.value.id);

    let currentCartQuantity = 0;
    if (existingProductIndex >= 0) {
      currentCartQuantity = cart[existingProductIndex].quantity;
    }

    if (quantity.value > availableStock) {
      alert(`Sorry, you can only add up to ${availableStock} items.`);
      return;
    }
    product.value.stock = availableStock;

    const priceToUse = product.value.sale_price && parseFloat(product.value.sale_price) > 0
      ? parseFloat(product.value.sale_price)
      : parseFloat(product.value.price);

    if (existingProductIndex >= 0) {
      if (currentCartQuantity + quantity.value > availableStock) {
        const additionalPossible = availableStock - currentCartQuantity;
        if (additionalPossible <= 0) {
          alert(`You already have ${currentCartQuantity} items in your cart, which is the maximum available.`);
          return;
        } else {
          alert(`You already have ${currentCartQuantity} items in your cart. You can add ${additionalPossible} more.`);
          quantity.value = additionalPossible;
        }
      }

      cart[existingProductIndex].quantity += quantity.value;
    } else {
      cart.push({
        id: product.value.id,
        name: product.value.name,
        price: priceToUse,
        image: product.value.image_url || '',
        category: product.value.category,
        quantity: quantity.value,
        stock: availableStock
      });
    }

    localStorage.setItem(`cart_${authStore.user?.username || 'guest'}`, JSON.stringify(cart));

    if (import.meta.client) {
      window.dispatchEvent(new CustomEvent('cart-updated'));
    }

    addToCartSuccess.value = true;
    setTimeout(() => {
      addToCartSuccess.value = false;
    }, 3000);
  } catch (error) {
    console.error('Error adding to cart:', error);
    alert('There was a problem adding this product to your cart. Please try again.');
  }
};

const getCategorySlug = (categoryValue) => {
  if (categoryValue && categoryMapping[categoryValue]) {
    return categoryMapping[categoryValue];
  }
  return categoryValue;
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
    fetchRelatedProducts();
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

const fetchRelatedProducts = async () => {
  try {
    if (!product.value || !product.value.id) return;
    const currentProductId = Number(product.value.id);
    const response = await fetch(`${apiUrl}/api/products/${category.value}/`);
    if (response.ok) {
      const data = await response.json();
      relatedProducts.value = data
        .filter(p => Number(p.id) !== currentProductId)
        .slice(0, 4);
    }
  } catch (error) {
    console.error('Error fetching related products:', error);
  }
};

const tryAgain = () => {
  error.value = null;
  const urlCategory = route.params.category;
  const urlProductId = route.params.id;

  if (urlCategory && urlProductId) {
    fetchProduct();
  } else if (import.meta.client) {
    const lastCategory = localStorage.getItem('lastProductCategory');
    const lastProductId = localStorage.getItem('lastProductId');

    if (lastCategory && lastProductId) {
      router.replace(`/products/${lastCategory}/${lastProductId}`);
    } else {
      error.value = 'Cannot find product information. Please browse products from the main page.';
      isLoading.value = false;
    }
  } else {
    error.value = 'Cannot find product information. Please browse products from the main page.';
    isLoading.value = false;
  }
};

const handlePopState = () => {
  const currentCategory = getCategory();
  const currentProductId = getProductId();
  
  console.log('After popstate:', { currentCategory, currentProductId });
  
  if (currentCategory && currentProductId) {
    fetchProduct();
  } else {
    // Handle case when back navigation doesn't have proper params
    if (route.path.includes('/products/')) {
      error.value = 'Product information not found. Redirecting to products page...';
      setTimeout(() => {
        router.push('/products');
      }, 1500);
    }
  }
};

onMounted(() => {
  if (import.meta.client) {
    const currentCategory = getCategory();
    const currentProductId = getProductId();
    if (currentCategory && currentProductId && !product.value) {
      fetchProduct();
    }
    
    window.addEventListener('popstate', handlePopState);
  }
});

onUnmounted(() => {
  if (import.meta.client) {
    window.removeEventListener('popstate', handlePopState);
  }
});

watch([productId, category], ([newId, newCategory]) => {
  if (newId && newCategory) {
    fetchProduct();
  } else if (attemptedFetch.value) {
    error.value = 'Invalid product URL. Missing category or ID.';
    isLoading.value = false;
  }
}, { immediate: true });

watch(
  () => route.fullPath,
  (newPath) => {
    console.log('Route changed:', newPath);
    const newCategory = route.params.category;
    const newProductId = route.params.id;
    
    if (newCategory && newProductId) {
      if (
        !product.value || 
        String(product.value.id) !== String(newProductId) || 
        getCategorySlug(product.value.category) !== newCategory
      ) {
        fetchProduct();
      }
    }
  },
  { immediate: true }
);

definePageMeta({
  layout: 'product-detail-layout'
});
</script>

<template>
  <div class="min-h-screen bg-base-100">
    <NavbarHeader />

    <div class="container mx-auto pt-4 pb-2 px-4 flex-grow">
      <div class="text-sm breadcrumbs">
        <ul>
          <li>
            <NuxtLink to="/">Home</NuxtLink>
          </li>
          <li>
            <NuxtLink to="/products">Products</NuxtLink>
          </li>
          <li v-if="categorySlug && categoryDisplayName && categoryDisplayName !== 'undefined'">
            <NuxtLink :to="`/products/${categorySlug}`">{{ categoryDisplayName.toLowerCase() === 'earbuds' ? 'Earbuds / IEMs' : categoryDisplayName }}</NuxtLink>
          </li>
          <li class="text-primary">{{ product?.name || 'Product' }}</li>
        </ul>
      </div>
    </div>

    <!-- Loading State with DaisyUI spinner -->
    <div v-if="isLoading" class="flex justify-center items-center py-32">
      <div class="text-center">
        <span class="loading loading-spinner loading-lg text-primary" />
        <p class="mt-4 text-gray-600">Loading product details...</p>
      </div>
    </div>

    <!-- Error State with DaisyUI alert -->
    <div v-else-if="error" class="container mx-auto px-4 py-12">
      <div class="alert alert-error max-w-lg mx-auto shadow-lg">
        <svg
xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none"
          viewBox="0 0 24 24">
          <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h3 class="font-bold">Unable to load product</h3>
          <div class="text-xs">{{ error }}</div>
        </div>
        <button class="btn btn-sm btn-outline" @click="tryAgain">Try Again</button>
      </div>
    </div>

    <!-- Product Display -->
    <div v-else-if="product" class="container mx-auto px-4 py-8">
      <div class="card lg:card-side bg-base-100 shadow-xl">
        <!-- Left side - Product Image Gallery -->
        <div class="card-body p-6 md:p-8 lg:w-1/2">
          <div
            class="relative bg-base-200 rounded-xl overflow-hidden flex justify-center items-center h-72 sm:h-96 mb-4">
            <img
:src="layoutProps.mainImage" :alt="layoutProps.name"
              class="max-h-full max-w-full object-contain transition-transform duration-300 hover:scale-105">

            <div class="absolute top-3 left-3">
              <div v-if="product.sale_price" class="badge badge-accent">SALE</div>
            </div>
          </div>
          <div v-if="layoutProps.images.length > 1" class="flex justify-center gap-2 overflow-x-auto pb-2">
            <div
v-for="(image, i) in layoutProps.images" :key="i"
              class="w-16 h-16 rounded-lg overflow-hidden border-2 cursor-pointer transition-all"
              :class="selectedImage === i ? 'border-primary' : 'border-transparent hover:border-base-300'"
              @click="selectImage(i)">
              <img :src="image" :alt="`${layoutProps.name} - view ${i + 1}`" class="w-full h-full object-cover">
            </div>
          </div>
          <div class="mt-4">
            <h3 class="font-medium mb-2">Description</h3>
            <p class="text-base-content/80">{{ layoutProps.description }}</p>
          </div>
        </div>
        <div class="divider lg:divider-horizontal" />
        <!-- Right side - Product Info -->
        <div class="card-body p-6 md:p-8 lg:w-1/2">
          <!-- Brand badge -->
          <div class="badge badge-outline mb-1">{{ layoutProps.brand }}</div>

          <!-- Product name -->
          <h1 class="card-title text-2xl sm:text-3xl font-bold text-base-content">{{ layoutProps.name }}</h1>

          <!-- Price display with sale price -->
          <div class="flex items-baseline gap-2 mt-2">
            <!-- If product has a sale price, show it as the main price -->
            <span v-if="product.sale_price" class="text-2xl font-bold text-primary">
              {{ formatCurrency(product.sale_price) }}
            </span>
            <!-- If product has a sale price, show regular price with strikethrough -->
            <span v-if="product.sale_price" class="text-sm text-base-content/60 line-through">
              {{ formatCurrency(product.price) }}
            </span>
            <!-- If no sale price, just show the regular price -->
            <span v-else class="text-2xl font-bold text-primary">
              {{ formatCurrency(product.price) }}
            </span>
          </div>


          <!-- Divider -->
          <div class="divider">Specifications</div>

          <!-- Product Specs -->
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <span class="font-semibold">Brand:</span> {{ layoutProps.brand }}
            </div>
            <div>
              <span class="font-semibold">Connectivity:</span> {{ layoutProps.connections }}
            </div>
            <div>
              <span class="font-semibold">Category:</span> {{ categoryDisplayName }}
            </div>
          </div>

          <!-- Stock Status -->
          <div class="mt-4">
            <div v-if="layoutProps.stock > 0" class="badge badge-success gap-2">
              <svg
xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                class="inline-block w-4 h-4 stroke-current">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              In Stock ({{ layoutProps.stock }} available)
            </div>
            <div v-else class="badge badge-error gap-2">
              <svg
xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                class="inline-block w-4 h-4 stroke-current">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Out of Stock
            </div>
          </div>

          <div class="card-actions justify-start gap-8 items-center mt-auto">
            <div class="join">
              <button class="btn join-item" :disabled="quantity <= 1" @click="decreaseQuantity">-</button>
              <span class="join-item px-4 flex items-center justify-center border border-base-300 min-w-12">
                {{ quantity }}
              </span>
              <button
class="btn join-item" :disabled="quantity >= layoutProps.stock"
                @click="increaseQuantity">+</button>
            </div>

            <!-- Add to cart button -->
            <button class="btn btn-primary" :disabled="layoutProps.stock <= 0" @click="handleAddToCart">
              <svg
xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
              {{ layoutProps.stock > 0 ? 'Add to Cart' : 'Out of Stock' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Related Products Section -->
      <div v-if="relatedProducts.length > 0" class="mt-12">
        <h2 class="text-2xl font-bold mb-4">You Might Also Like</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div
            v-for="relatedProduct in relatedProducts.filter(p => Number(p.id) !== Number(product?.id))" 
            :key="relatedProduct.id"
            class="card bg-base-100 shadow-sm hover:shadow-md transition-shadow"
          >
            <figure class="px-4 pt-4">
              <img
                :src="relatedProduct.image_url || 'https://via.placeholder.com/150'" 
                :alt="relatedProduct.name"
                class="rounded-xl h-32 object-contain"
              >
            </figure>
            <div class="card-body p-4">
              <h3 class="card-title text-sm">{{ relatedProduct.name }}</h3>
              
              <!-- Display price with sale price handling -->
              <div class="flex items-baseline gap-2">
                <span v-if="relatedProduct.sale_price" class="text-lg font-bold text-primary">
                  {{ formatCurrency(relatedProduct.sale_price) }}
                </span>
                <span v-if="relatedProduct.sale_price" class="text-sm text-base-content/60 line-through">
                  {{ formatCurrency(relatedProduct.price) }}
                </span>
                <span v-else class="text-lg font-bold text-primary">
                  {{ formatCurrency(relatedProduct.price) }}
                </span>
              </div>
              
              <div class="card-actions justify-end">
                <NuxtLink
                  :to="`/products/${getCategorySlug(relatedProduct.category)}/${relatedProduct.id}`"
                  class="btn btn-xs btn-outline btn-primary"
                >
                  View
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No product found state with DaisyUI card -->
    <div v-else class="flex justify-center items-center py-12">
      <div class="card w-96 bg-base-100 shadow-xl">
        <div class="card-body items-center text-center">
          <div class="text-error">
            <svg
xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 class="card-title">Product Not Found</h2>
          <p>We couldn't find the product you're looking for.</p>
          <div class="card-actions justify-center mt-4">
            <NuxtLink to="/products" class="btn btn-primary">Browse Products</NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <div v-if="addToCartSuccess" class="toast toast-right z-50">
      <div class="alert alert-success">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h3 class="font-bold">Added to Cart!</h3>
          <div class="text-xs">Your item was successfully added</div>
        </div>
        <NuxtLink to="/cart" class="btn btn-sm btn-ghost">View Cart</NuxtLink>
      </div>
    </div>
    <FooterSection />
  </div>
</template>

<style scoped>
.card-side {
  display: flex;
  flex-direction: column;
}

@media (min-width: 1024px) {
  .card-side {
    flex-direction: row;
  }
}

.btn,
img {
  transition: all 0.3s ease;
}


.toast {
  animation: slideUp 0.3s ease-out forwards;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>