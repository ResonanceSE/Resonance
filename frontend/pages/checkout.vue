<script setup>
import { useAuthStore } from '~/stores/useAuth'

definePageMeta({
    layout: 'default'
})

const router = useRouter()
const authStore = useAuthStore()
const config = useRuntimeConfig()
const apiUrl = config.public.apiUrl || 'http://localhost:8000'

// UI state
const isLoading = ref(false)
const isSubmitting = ref(false)
const errorMessage = ref('')
const orderPlaced = ref(false)
const orderNumber = ref('')

const cartItems = ref([])

const addressForm = reactive({
    recipient: '',
    line1: '',
    line2: '',
    city: '',
    postal_code: '',
    country: ''
})

const useExistingAddress = ref(true)
const addresses = ref([
    {
        id: 1,
        recipient: 'John Doe',
        line1: '123 Main Street',
        line2: 'Apt 4B',
        city: 'New York',
        postal_code: '10001',
        country: 'USA'
    }
])
const selectedAddressId = ref(1)

onMounted(() => {
    loadCart()
})
const loadCart = () => {
    isLoading.value = true
    try {
        const cartString = localStorage.getItem(`cart_${authStore.user.username || 'guest'}`)
        console.log("Raw cart data from localStorage:", cartString)
        
        if (cartString) {
            const parsedCart = JSON.parse(cartString)
            console.log("Parsed cart data:", parsedCart)
            cartItems.value = parsedCart
        } else {
            cartItems.value = []
        }
        
        // Additional logging to see exactly what product IDs you're working with
        console.log("Product IDs in cart:", cartItems.value.map(item => item.id))
        
        if (cartItems.value.length === 0 && !orderPlaced.value) {
            router.push('/cart')
        }
    } catch (error) {
        console.error('Error loading cart:', error)
        cartItems.value = []
    } finally {
        isLoading.value = false
    }
}

const subtotal = computed(() => {
    return cartItems.value.reduce((sum, item) => sum + (item.price * item.quantity), 0)
})

const shippingFee = computed(() => {
    return cartItems.value.length > 0 ? 999 : 0
})

const total = computed(() => {
    return subtotal.value + shippingFee.value
})

const formatPrice = (price) => {
    return '$' + (price / 100).toFixed(2)
}

const selectedAddress = computed(() => {
    return addresses.value.find(addr => addr.id === selectedAddressId.value) || addresses.value[0]
})

const getFormattedAddress = () => {
    if (useExistingAddress.value) {
        const addr = selectedAddress.value
        return `${addr.recipient}\n${addr.line1}\n${addr.line2}\n${addr.city}, ${addr.postal_code}\n${addr.country}`
    } else {
        return `${addressForm.recipient}\n${addressForm.line1}\n${addressForm.line2}\n${addressForm.city}, ${addressForm.postal_code}\n${addressForm.country}`
    }
}

const placeOrder = async () => {
    if (!authStore.isLoggedIn) {
        router.push('/login?redirect=/checkout')
        return
    }
    
    if (!useExistingAddress.value) {
        if (!addressForm.recipient || !addressForm.line1 || !addressForm.city) {
            errorMessage.value = 'Please fill in all required address fields'
            return
        }
    }
    
    if (cartItems.value.length === 0) {
        errorMessage.value = 'Your cart is empty'
        return
    }
    
    isSubmitting.value = true
    errorMessage.value = ''
    
    try {
        const shippingAddress = getFormattedAddress()
        const items = cartItems.value.map(item => ({
            product_id: item.id,
            quantity: item.quantity,
            price: item.price
        }))
        
        console.log("Sending order with items:", items)
        
        const response = await fetch(`${apiUrl}/api/orders/create/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${authStore.token}`
            },
            body: JSON.stringify({
                shipping_address: shippingAddress,
                items: items
            })
        })
        
        const result = await response.json()
        
        if (response.ok && result.status === 'success') {
            orderNumber.value = result.data.order_number
            orderPlaced.value = true
            localStorage.removeItem('cart')
            cartItems.value = []
        } else {
            throw new Error(result.message || 'Failed to create order')
        }
    } catch (error) {
        console.error('Error placing order:', error)
        errorMessage.value = error.message || 'An error occurred while placing your order. Please try again.'
    } finally {
        isSubmitting.value = false
    }
}

const continueShopping = () => {
    router.push('/products')
}
</script>

<template>
    <div class="min-h-screen bg-gray-50 py-10">
        <div class="container max-w-4xl mx-auto px-4">
            <!-- Page header -->
            <div class="mb-8 text-center">
                <h1 class="text-3xl font-bold text-gray-800">Checkout</h1>
                <div class="w-24 h-1 bg-orange-500 mx-auto mt-2"/>
            </div>
            
            <!-- Error message -->
            <div v-if="errorMessage" class="mb-6 bg-red-100 border-l-4 border-red-500 text-red-700 p-4">
                <p>{{ errorMessage }}</p>
            </div>
            
            <!-- Loading indicator -->
            <div v-if="isLoading" class="flex justify-center py-12">
                <div class="loading loading-spinner loading-lg text-orange-500"/>
            </div>
            
            <!-- Order Confirmation -->
            <div v-else-if="orderPlaced" class="bg-white rounded-lg shadow-lg p-8 text-center">
                <div class="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                </div>
                
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Order Placed Successfully!</h2>
                <p class="mb-2">Your order number is: <span class="font-bold">{{ orderNumber }}</span></p>
                <p class="text-gray-600 mb-6">Thank you for your order. We'll process it as soon as possible.</p>
                
                <button 
                    class="btn btn-primary"
                    @click="continueShopping"
                >
                    Continue Shopping
                </button>
            </div>
            
            <!-- Checkout Form -->
            <div v-else class="bg-white rounded-lg shadow-lg overflow-hidden">
                <!-- Cart Summary -->
                <div class="p-6 bg-gray-50 border-b">
                    <h2 class="text-xl font-bold mb-4">Order Summary</h2>
                    
                    <div class="divide-y divide-gray-200">
                        <div v-for="item in cartItems" :key="item.id" class="py-3 flex justify-between">
                            <div>
                                <h3 class="font-medium">{{ item.name }}</h3>
                                <p class="text-sm text-gray-500">Qty: {{ item.quantity }}</p>
                            </div>
                            <div class="text-right">
                                <p class="font-medium">{{ formatPrice(item.price * item.quantity) }}</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-4 pt-4 border-t border-gray-200">
                        <div class="flex justify-between text-sm">
                            <span>Subtotal</span>
                            <span>{{ formatPrice(subtotal) }}</span>
                        </div>
                        <div class="flex justify-between text-sm mt-2">
                            <span>Shipping</span>
                            <span>{{ formatPrice(shippingFee) }}</span>
                        </div>
                        <div class="flex justify-between font-bold text-lg mt-2 pt-2 border-t border-gray-200">
                            <span>Total</span>
                            <span>{{ formatPrice(total) }}</span>
                        </div>
                    </div>
                </div>
                
                <!-- Shipping Address -->
                <div class="p-6">
                    <h2 class="text-xl font-bold mb-4">Shipping Address</h2>
                    
                    <!-- Address selection toggle -->
                    <div class="mb-6 flex space-x-4">
                        <label class="flex items-center">
                            <input v-model="useExistingAddress" type="radio" :value="true" class="radio radio-primary mr-2">
                            <span>Use existing address</span>
                        </label>
                        <label class="flex items-center">
                            <input v-model="useExistingAddress" type="radio" :value="false" class="radio radio-primary mr-2">
                            <span>Enter new address</span>
                        </label>
                    </div>
                    
                    <!-- Existing addresses -->
                    <div v-if="useExistingAddress" class="mb-6">
                        <div
v-for="address in addresses" :key="address.id" 
                            class="border rounded-lg p-4 mb-3 cursor-pointer"
                            :class="{'border-orange-500 bg-orange-50': selectedAddressId === address.id}"
                            @click="selectedAddressId = address.id">
                            <div class="flex items-start">
                                <input type="radio" :checked="selectedAddressId === address.id" class="radio radio-primary mt-1 mr-3">
                                <div>
                                    <p class="font-medium">{{ address.recipient }}</p>
                                    <p>{{ address.line1 }}</p>
                                    <p>{{ address.line2 }}</p>
                                    <p>{{ address.city }}, {{ address.postal_code }}</p>
                                    <p>{{ address.country }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- New address form -->
                    <div v-else class="mb-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text">Full Name</span>
                                </label>
                                <input v-model="addressForm.recipient" type="text" class="input input-bordered" required>
                            </div>
                            
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text">Address Line 1</span>
                                </label>
                                <input v-model="addressForm.line1" type="text" class="input input-bordered" required>
                            </div>
                            
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text">Address Line 2</span>
                                </label>
                                <input v-model="addressForm.line2" type="text" class="input input-bordered">
                            </div>
                            
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text">City</span>
                                </label>
                                <input v-model="addressForm.city" type="text" class="input input-bordered" required>
                            </div>
                            
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text">Postal Code</span>
                                </label>
                                <input v-model="addressForm.postal_code" type="text" class="input input-bordered" required>
                            </div>
                            
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text">Country</span>
                                </label>
                                <input v-model="addressForm.country" type="text" class="input input-bordered" required>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Place Order Button -->
                    <div class="mt-6">
                        <button 
                            class="btn btn-primary btn-block"
                            :disabled="isSubmitting"
                            @click="placeOrder"
                        >
                            <span v-if="isSubmitting">
                                <span class="loading loading-spinner loading-xs mr-2"/>
                                Processing...
                            </span>
                            <span v-else>Place Order</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.btn-primary {
  @apply bg-orange-500 hover:bg-orange-600 border-orange-500;
}
.radio-primary:checked {
  @apply bg-orange-500 border-orange-500;
}
</style>