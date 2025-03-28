<script setup lang="ts">
import { cartService } from '~/services/cartService'

interface CartItem {
  id: number
  name: string
  category: string
  price: number
  quantity: number
  image?: string
}

definePageMeta({
  layout: 'default'
})

const router = useRouter()

const cartItems = ref<CartItem[]>([])
const selectedItemIds = ref<number[]>([])
const isLoading = ref(true)

onMounted(() => {
  loadCart()
})

const loadCart = () => {
  isLoading.value = true
  try {
    cartItems.value = cartService.getCart()
    selectedItemIds.value = cartItems.value.map(item => item.id)
  } catch (error) {
    console.error('Error loading cart:', error)
  } finally {
    isLoading.value = false
  }
}

const isItemSelected = (id: number): boolean => {
  return selectedItemIds.value.includes(id)
}

const toggleItem = (id: number, event?: Event): void => {
  if (event) {
    event.stopPropagation()
  }
  
  console.log("Toggle item:", id)
  if (isItemSelected(id)) {
    selectedItemIds.value = selectedItemIds.value.filter(itemId => itemId !== id)
  } else {
    selectedItemIds.value.push(id)
  }
}

const toggleSelectAll = (): void => {
  console.log("Toggle select all")
  if (isAllItemsSelected.value) {
    selectedItemIds.value = []
  } else {
    selectedItemIds.value = cartItems.value.map(item => item.id)
  }
}

const isAllItemsSelected = computed(() => {
  return cartItems.value.length > 0 && 
         cartItems.value.every(item => isItemSelected(item.id))
})

const decreaseQuantity = (item: CartItem, event: Event): void => {
  event.stopPropagation()
  if (item.quantity > 1) {
    item.quantity--
    cartService.updateQuantity(item.id, item.quantity)
  }
}

const increaseQuantity = (item: CartItem, event: Event): void => {
  event.stopPropagation()
  item.quantity++
  cartService.updateQuantity(item.id, item.quantity)
}

const removeItem = (itemId: number, event: Event): void => {
  event.stopPropagation()
  cartItems.value = cartItems.value.filter(item => item.id !== itemId)
  selectedItemIds.value = selectedItemIds.value.filter(id => id !== itemId)
  cartService.removeItem(itemId)
}

const totalPrice = computed(() => {
  let total = 0
  for (const item of cartItems.value) {
    if (isItemSelected(item.id)) {
      total += item.price * item.quantity
    }
  }
  return total
})

const formatPrice = (price: number) => {
  return '$' + Number(price).toFixed(2)
}

const selectedItemsCount = computed(() => {
  return selectedItemIds.value.length
})

const shippingFee = ref(0.12)

const processCheckout = (): void => {
  const itemsForCheckout = cartItems.value.filter(item => isItemSelected(item.id))
  if (itemsForCheckout.length === 0) {
    alert('Please select at least one item to checkout')
    return
  }
  const checkoutCart = JSON.stringify(itemsForCheckout)
  if (import.meta.client) {
    localStorage.setItem('checkout_cart', checkoutCart)
  }
  router.push('/checkout')
}

const continueShopping = (): void => {
  router.push('/products')
}

</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12 relative overflow-hidden">
    <!-- Decorative circles -->
    <div class="absolute top-20 left-10 w-64 h-64 bg-orange-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"/>
    <div class="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"/>
    <div class="absolute -bottom-8 left-40 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000"/>
    
    <div class="container mx-auto px-4">
      <!-- Page Header -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold">
          <span class="bg-gradient-to-r from-blue-500 to-indigo-600 bg-clip-text text-transparent">Your</span>
          <span class="relative">
            Cart
            <span class="absolute -bottom-1 left-0 w-full h-1 bg-orange-400 rounded-full"/>
          </span>
        </h1>
        <p class="mt-2 text-gray-600">Review your items before checkout</p>
      </div>
      
      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center py-12">
        <div class="loading loading-spinner loading-lg text-orange-500"/>
      </div>
      
      <!-- Cart Content -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Cart Items -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow-xl p-6">
            <h2 class="text-xl font-semibold mb-4">Your Items</h2>
            
            <!-- Select all toggle -->
            <div class="flex justify-between items-center mb-4 pb-2 border-b border-gray-200" style="z-index: 10; position: relative;">
              <div
                class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-full cursor-pointer hover:bg-orange-500 transition duration-300 ease-in-out"
                :class="{'bg-primary text-white border-primary hover:bg-primary-focus': isAllItemsSelected}"
                @click="toggleSelectAll"
              >
                <div class="w-5 h-5 mr-2 flex items-center justify-center">
                  <div v-if="isAllItemsSelected" class="w-5 h-5 bg-white rounded-full flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4 text-primary">
                      <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <div v-else class="w-5 h-5 border-2 border-gray-300 rounded-full"/>
                </div>
                <span>{{ isAllItemsSelected ? 'Deselect All' : 'Select All Items' }}</span>
              </div>
              <span class="text-gray-700">{{ selectedItemsCount }} items selected</span>
            </div>
            
            <!-- Empty Cart State -->
            <div v-if="cartItems.length === 0" class="text-center py-12">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <h3 class="text-lg font-medium text-gray-800 mb-2">Your cart is empty</h3>
              <p class="text-gray-600 mb-4">Looks like you haven't added any products to your cart yet.</p>
              <button 
                class="btn btn-primary"
                @click="continueShopping"
              >
                Continue Shopping
              </button>
            </div>
            
            <!-- Cart Items List -->
            <div v-else class="divide-y divide-gray-100">
              <div 
                v-for="item in cartItems" 
                :key="item.id" 
                class="p-4 flex items-center cursor-pointer"
                :class="{'bg-blue-50 rounded-lg': isItemSelected(item.id)}"
                @click="(event) => toggleItem(item.id, event)"
              >
                <!-- Selection indicator with explicit z-index -->
                <div class="mr-4 z-10" @click.stop="(event) => toggleItem(item.id, event)">
                  <div 
                    class="w-6 h-6 rounded-full flex items-center justify-center transition-colors duration-200"
                    :class="isItemSelected(item.id) ? 'bg-primary text-white' : 'bg-gray-200'"
                  >
                    <svg 
                      v-if="isItemSelected(item.id)"
                      xmlns="http://www.w3.org/2000/svg" 
                      class="h-4 w-4" 
                      viewBox="0 0 20 20" 
                      fill="currentColor"
                    >
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </div>
                </div>
                
                <!-- Item image -->
                <div class="w-16 h-16 bg-gray-100 rounded-md mr-4">
                  <img 
                    v-if="item.image" 
                    :src="item.image" 
                    :alt="item.name"
                    class="w-full h-full object-cover rounded-md"
                  >
                </div>
                
                <!-- Item details - no click handler to avoid conflicts -->
                <div class="flex-grow">
                  <h3 class="font-medium text-gray-800">{{ item.name }}</h3>
                  <p class="text-sm text-gray-500">{{ item.category }}</p>
                  <p class="font-semibold text-gray-900 mt-1">{{ formatPrice(item.price) }}</p>
                </div>
                
                <!-- Quantity controls with explicit stop propagation -->
                <div class="join border border-gray-300 mr-6" @click.stop>
                  <button 
                    class="join-item btn btn-sm btn-ghost"
                    @click.stop="(event) => decreaseQuantity(item, event)"
                  >
                    -
                  </button>
                  <div class="join-item px-3 flex items-center justify-center">
                    {{ item.quantity }}
                  </div>
                  <button 
                    class="join-item btn btn-sm btn-ghost"
                    @click.stop="(event) => increaseQuantity(item, event)"
                  >
                    +
                  </button>
                </div>
                
                <!-- Total price -->
                <div class="text-right" @click.stop>
                  <p class="font-semibold text-orange-500">{{ formatPrice(item.price * item.quantity) }}</p>
                  <button 
                    class="text-sm text-red-500 hover:text-red-700"
                    @click.stop="(event) => removeItem(item.id, event)"
                  >
                    Remove
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Order Summary -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-xl p-6 sticky top-24">
            <h2 class="text-xl font-semibold mb-4">Order Summary</h2>
            
            <div v-if="cartItems.length > 0" class="space-y-4">
              <!-- Summary Details -->
              <div class="space-y-3 mb-4">
                <div class="flex justify-between text-gray-700">
                  <span>Subtotal ({{ selectedItemsCount }} items)</span>
                  <span>{{ formatPrice(totalPrice) }}</span>
                </div>
                <div class="flex justify-between text-gray-700">
                  <span>Shipping Fee</span>
                  <span>{{ formatPrice(shippingFee) }}</span>
                </div>
                <div class="border-t border-gray-200 pt-3 mt-3">
                  <div class="flex justify-between font-bold text-lg text-gray-900">
                    <span>Total</span>
                    <span>{{ formatPrice(totalPrice + shippingFee) }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Checkout Button -->
              <button 
                class="btn btn-primary btn-block hover:bg-orange-500 transition ease-out duration-200"
                :disabled="selectedItemsCount === 0"
                @click="processCheckout"
              >
                Proceed to Checkout
              </button>
              
              <!-- Continue Shopping -->
              <button 
                class="btn btn-outline btn-block"
                @click="continueShopping"
              >
                Continue Shopping
              </button>
            </div>
            
            <div v-else class="text-center py-4">
              <p class="text-gray-500">Add items to your cart to see the order summary</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Animation keyframes */
.animate-blob {
  animation: blob-bounce 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes blob-bounce {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}
</style>