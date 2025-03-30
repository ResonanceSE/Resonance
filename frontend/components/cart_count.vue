<script setup lang="ts">
import { cartService } from '~/services/cartService';
import { useAuthStore } from '~/stores/useAuth';

const authStore = useAuthStore();
const itemCount = ref(0);
const isLoading = ref(false);

const fetchCartCount = async () => {
  if (import.meta.client) {
    try {
      isLoading.value = true;
      itemCount.value = await cartService.getCartItemCount();
    } catch (error) {
      console.error('Error fetching cart count:', error);
    } finally {
      isLoading.value = false;
    }
  }
};

// Listen for cart-updated events
const handleCartUpdated = () => {
  fetchCartCount();
};

onMounted(() => {
  // Initial fetch
  fetchCartCount();
  
  // Add event listener for cart updates
  if (import.meta.client) {
    window.addEventListener('cart-updated', handleCartUpdated);
  }
});

onBeforeUnmount(() => {
  // Remove event listener when component is unmounted
  if (import.meta.client) {
    window.removeEventListener('cart-updated', handleCartUpdated);
  }
});

// Watch for auth state changes
watch(() => authStore.isAuthenticated, () => {
  fetchCartCount();
});
</script>

<template>
  <div class="relative">
    <Icon name="heroicons:shopping-cart" class="h-5 w-5" />
    
    <!-- Loading indicator -->
    <div v-if="isLoading" class="absolute -top-1 -right-1 w-4 h-4">
      <div class="w-full h-full border-2 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
    </div>
    
    <!-- Item count badge -->
    <div 
      v-else-if="itemCount > 0" 
      class="absolute -top-2 -right-2 bg-orange-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
    >
      {{ itemCount > 9 ? '9+' : itemCount }}
    </div>
  </div>
</template>