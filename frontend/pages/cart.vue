<script setup lang="ts">

import { cartService} from '~/services/cartService'

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
const selectedItems = ref<Record<number, boolean>>({})
const isLoading = ref(true)

// Load cart on component mount
onMounted(() => {
  loadCart()
})

const loadCart = () => {
  isLoading.value = true
  try {
    cartItems.value = cartService.getCart()
    const newSelectedItems: Record<number, boolean> = {}
    cartItems.value.forEach(item => {
      newSelectedItems[item.id] = true
    })
    selectedItems.value = newSelectedItems
  } catch (error) {
    console.error('Error loading cart:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleItemSelection = (itemId: number) => {
  selectedItems[itemId] = !selectedItems[itemId];
};


const selectAll = computed({
  get: () => {
    return cartItems.value.length > 0 && 
           cartItems.value.every(item => selectedItems.value[item.id] === true)
  },
  set: (value: boolean) => {
    const updatedSelection: Record<number, boolean> = { ...selectedItems.value }
    cartItems.value.forEach(item => {
      updatedSelection[item.id] = value
    })
    selectedItems.value = updatedSelection
  }
})


const decreaseQuantity = (item : CartItem) => {
  if (item.quantity > 1) {
    item.quantity--
    cartService.updateQuantity(item.id, item.quantity)
  }
}

const increaseQuantity = (item : CartItem) => {
  item.quantity++
  cartService.updateQuantity(item.id, item.quantity)
}

const removeItem = (itemId: number) => {
  cartItems.value = cartItems.value.filter(item => item.id !== itemId);
  selectedItems[itemId] = false;
};


const getTotalPrice = computed(() => {
  let total = 0
  for (const item of cartItems.value) {
    if (selectedItems[item.id]) {
      total += item.price * item.quantity
    }
  }
  return total
})

const formatPrice = (price : number) => {
  return '$' + (price / 100).toFixed(2)
}

const getSelectedItemsCount = computed(() => {
  return Object.values(selectedItems).filter(Boolean).length
})

const shippingFee = ref(100)

const processCheckout = () => {
  const itemsForCheckout = cartItems.value.filter(item => selectedItems[item.id])
  
  if (itemsForCheckout.length === 0) {
    alert('Please select at least one item to checkout')
    return
  }
  
  const checkoutCart = JSON.stringify(itemsForCheckout)
  localStorage.setItem('checkout_cart', checkoutCart)
  router.push('/checkout')
}

const continueShopping = () => {
  router.push('/products')
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12 relative overflow-hidden">
    <!-- Decorative circles using CSS only -->
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
        <div class="loader border-4 rounded-full border-t-orange-500 border-gray-200 h-12 w-12 animate-spin"/>
      </div>
      
      <!-- Cart Content -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Cart Items -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow-xl p-6">
            <h2 class="text-xl font-semibold mb-4">Your Items</h2>
            
            <!-- Select all -->
            <div class="flex justify-between items-center mb-4 pb-2 border-b border-gray-200">
              <div class="flex items-center">
                <input
v-model="selectAll" type="checkbox"
                  class="w-5 h-5 rounded text-orange-500 focus:ring-orange-500 border-gray-400">
                <span class="ml-2 text-gray-700">Select All ({{ getSelectedItemsCount }} items)</span>
              </div>
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
              <div v-for="item in cartItems" :key="item.id" class="py-4 flex items-center">
                <div class="mr-4">
                  <input
type="checkbox"
                    class="w-5 h-5 rounded text-orange-500 focus:ring-orange-500 border-gray-400"
                    :checked="selectedItems[item.id]" 
                    @change="toggleItemSelection(item.id)">
                </div>
                
                <!-- Product image -->
                <div class="w-16 h-16 bg-gray-100 rounded-md mr-4">
                  <img 
                    v-if="item.image" 
                    :src="item.image" 
                    :alt="item.name"
                    class="w-full h-full object-cover rounded-md"
                  >
                </div>
                
                <!-- Product details -->
                <div class="flex-grow">
                  <h3 class="font-medium text-gray-800">{{ item.name }}</h3>
                  <p class="text-sm text-gray-500">{{ item.category }}</p>
                  <p class="font-semibold text-gray-900 mt-1">{{ formatPrice(item.price) }}</p>
                </div>
                
                <!-- Quantity control -->
                <div class="flex items-center border rounded-md mr-6 border-gray-300">
                  <button 
                    class="px-3 py-1 text-gray-600 hover:bg-gray-100"
                    @click="decreaseQuantity(item)"
                  >
                    -
                  </button>
                  <span class="px-4 py-1 text-gray-800">{{ item.quantity }}</span>
                  <button 
                    class="px-3 py-1 text-gray-600 hover:bg-gray-100"
                    @click="increaseQuantity(item)"
                  >
                    +
                  </button>
                </div>
                
                <!-- Total price -->
                <div class="text-right">
                  <p class="font-semibold text-orange-500">{{ formatPrice(item.price * item.quantity) }}</p>
                  <button 
                    class="text-sm text-red-500 hover:text-red-700"
                    @click="removeItem(item.id)"
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
                  <span>Subtotal ({{ getSelectedItemsCount }} items)</span>
                  <span>{{ formatPrice(getTotalPrice) }}</span>
                </div>
                <div class="flex justify-between text-gray-700">
                  <span>Shipping Fee</span>
                  <span>{{ formatPrice(shippingFee) }}</span>
                </div>
                <div class="border-t border-gray-200 pt-3 mt-3">
                  <div class="flex justify-between font-bold text-lg text-gray-900">
                    <span>Total</span>
                    <span>{{ formatPrice(getTotalPrice + shippingFee) }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Checkout Button -->
              <button 
                class="w-full py-3 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white font-medium rounded-lg transition-all shadow-md hover:shadow-lg active:shadow-sm transform hover:-translate-y-0.5 active:translate-y-0 duration-150"
                :disabled="getSelectedItemsCount === 0"
                :class="{ 'opacity-50 cursor-not-allowed': getSelectedItemsCount === 0 }"
                @click="processCheckout"
              >
                Proceed to Checkout
              </button>
              
              <!-- Continue Shopping -->
              <button 
                class="w-full py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium transition-colors duration-150"
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

.btn-primary {
  background-color: #f97316;
  color: white;
}

.btn-primary:hover {
  background-color: #ea580c;
}
</style>