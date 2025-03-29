<script setup>
import { useAuthStore } from '~/stores/useAuth'
import { useRouter } from 'vue-router'

definePageMeta({
    layout: 'default'
})

const router = useRouter()
const authStore = useAuthStore()
const config = useRuntimeConfig()
const apiUrl = config.public.apiUrl || 'http://localhost:8000'

// Payment state
const isLoading = ref(false)
const paymentError = ref('')
const processingPayment = ref(false)
const paymentSuccess = ref(false)
const orderNumber = ref('')
const countdown = ref(5)

// Get order details from localStorage (passed from checkout page)
const orderDetails = ref(null)

onMounted(() => {
    loadOrderDetails()
})

const loadOrderDetails = () => {
    try {
        if (!import.meta.client) return
        
        const orderDetailsString = localStorage.getItem('pending_order')
        if (!orderDetailsString) {
            router.push('/checkout')
            return
        }
        
        orderDetails.value = JSON.parse(orderDetailsString)
        orderNumber.value = orderDetails.value.order_number || ''
    } catch (error) {
        console.error('Error loading order details:', error)
        paymentError.value = 'Error loading order details. Please try again.'
        router.push('/checkout')
    }
}

const formatPrice = (price) => {
    return '$' + Number(price).toFixed(2)
}

const processPayment = async () => {
    if (!orderDetails.value) {
        paymentError.value = 'No order details found'
        return
    }
    
    processingPayment.value = true
    paymentError.value = ''
    
    try {
        // Simulate payment processing delay
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        // Mock API call to update order payment status
        const response = await fetch(`${apiUrl}/api/orders/${orderDetails.value.order_id}/payment/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${authStore.token}`
            },
            body: JSON.stringify({
                payment_status: true,
                payment_method: 'credit_card'
            })
        })
        
        if (!response.ok) {
            throw new Error('Payment processing failed')
        }
        
        // Payment successful
        paymentSuccess.value = true
        
        // Clear the cart and pending order from localStorage
        if (import.meta.client) {
            localStorage.removeItem('cart_' + (authStore.user?.username || 'guest'))
            localStorage.removeItem('pending_order')
        }
        
        // Start countdown for redirect
        startCountdown()
    } catch (error) {
        console.error('Payment error:', error)
        paymentError.value = 'Payment processing failed. Please try again.'
    } finally {
        processingPayment.value = false
    }
}

const startCountdown = () => {
    const timer = setInterval(() => {
        countdown.value--
        if (countdown.value <= 0) {
            clearInterval(timer)
            router.push('/orders')
        }
    }, 1000)
}

const cancelPayment = () => {
    if (import.meta.client) {
        localStorage.removeItem('pending_order')
    }
    router.push('/checkout')
}
</script>

<template>
    <div class="min-h-screen bg-gray-50 py-10">
        <div class="container max-w-3xl mx-auto px-4">
            <!-- Page header -->
            <div class="mb-8 text-center">
                <h1 class="text-3xl font-bold text-gray-800">Payment</h1>
                <div class="w-24 h-1 bg-orange-500 mx-auto mt-2"/>
            </div>
            
            <!-- Loading state -->
            <div v-if="isLoading" class="flex justify-center items-center py-12">
                <div class="loading loading-spinner loading-lg text-orange-500"/>
            </div>
            
            <!-- Error state -->
            <div v-else-if="paymentError" class="mb-6 bg-red-100 border-l-4 border-red-500 text-red-700 p-4">
                <p>{{ paymentError }}</p>
                <button class="btn btn-primary mt-4" @click="cancelPayment">Return to Checkout</button>
            </div>
            
            <!-- Payment Success -->
            <div v-else-if="paymentSuccess" class="bg-white rounded-lg shadow-lg p-8 text-center">
                <div class="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    </svg>
                </div>
                
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Payment Successful!</h2>
                <p class="mb-2">Your order number is: <span class="font-bold">{{ orderNumber }}</span></p>
                <p class="text-gray-600 mb-6">Thank you for your purchase. We'll process your order right away.</p>
                
                <p class="text-sm text-gray-500 mb-4">Redirecting to orders page in {{ countdown }} seconds...</p>
                
                <button class="btn btn-primary" @click="router.push('/orders')">
                    View My Orders
                </button>
            </div>
            
            <!-- Payment Form -->
            <div v-else class="bg-white rounded-lg shadow-lg overflow-hidden">
                <!-- Order Summary -->
                <div v-if="orderDetails" class="p-6 bg-gray-50 border-b">
                    <h2 class="text-xl font-bold mb-4">Order Summary</h2>
                    <div class="flex justify-between text-sm mb-2">
                        <span>Order Number:</span>
                        <span class="font-medium">{{ orderNumber }}</span>
                    </div>
                    <div class="flex justify-between font-bold text-lg border-t border-gray-200 pt-2 mt-2">
                        <span>Total:</span>
                        <span>{{ formatPrice(orderDetails.total_amount) }}</span>
                    </div>
                </div>
                
                <!-- Credit Card Form -->
                <div class="p-6">
                    <h2 class="text-xl font-bold mb-4">Payment Details</h2>
                    
                    <div class="space-y-4">
                        <div class="form-control">
                            <label class="label">
                                <span class="label-text">Card Number</span>
                            </label>
                            <input 
                                type="text" 
                                class="input input-bordered" 
                                placeholder="1234 5678 9012 3456"
                                value="4242 4242 4242 4242"
                                disabled
                            >
                            <label class="label">
                                <span class="label-text-alt text-gray-500">Use this test card number</span>
                            </label>
                        </div>
                        
                        <div class="grid grid-cols-2 gap-4">
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text">Expiration Date</span>
                                </label>
                                <input 
                                    type="text" 
                                    class="input input-bordered" 
                                    placeholder="MM/YY"
                                    value="12/25"
                                    disabled
                                >
                            </div>
                            
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text">CVC</span>
                                </label>
                                <input 
                                    type="text" 
                                    class="input input-bordered" 
                                    placeholder="123"
                                    value="123"
                                    disabled
                                >
                            </div>
                        </div>
                        
                        <div class="form-control">
                            <label class="label">
                                <span class="label-text">Name on Card</span>
                            </label>
                            <input 
                                type="text" 
                                class="input input-bordered" 
                                placeholder="John Doe"
                                value="Test User"
                                disabled
                            >
                        </div>
                    </div>
                    
                    <div class="mt-6 flex justify-between">
                        <button 
                            class="btn btn-outline" 
                            @click="cancelPayment"
                            :disabled="processingPayment"
                        >
                            Cancel
                        </button>
                        
                        <button 
                            class="btn btn-primary" 
                            @click="processPayment"
                            :disabled="processingPayment"
                        >
                            <span v-if="processingPayment">
                                <span class="loading loading-spinner loading-xs mr-2"/>
                                Processing...
                            </span>
                            <span v-else>Complete Payment</span>
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
</style>