<script setup>
import { useAuthStore } from '~/stores/useAuth'

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

// Selected payment method
const paymentMethod = ref(null) // 'qr' or 'cod'
const showQrCode = ref(false)

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
    return '฿' + Number(price).toFixed(2)
}

const selectPaymentMethod = (method) => {
    paymentMethod.value = method
    if (method === 'qr') {
        showQrCode.value = true
    } else {
        showQrCode.value = false
    }
}

const processPayment = async () => {
    if (!orderDetails.value) {
        paymentError.value = 'No order details found'
        return
    }
    
    if (!paymentMethod.value) {
        paymentError.value = 'Please select a payment method'
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
                payment_status: paymentMethod.value === 'qr', // true for QR payment, false for COD
                payment_method: paymentMethod.value
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
                <h1 class="text-3xl font-bold text-gray-800">การชำระเงิน</h1>
                <div class="w-24 h-1 bg-orange-500 mx-auto mt-2"/>
            </div>
            
            <!-- Loading state -->
            <div v-if="isLoading" class="flex justify-center items-center py-12">
                <div class="loading loading-spinner loading-lg text-orange-500"/>
            </div>
            
            <!-- Error state -->
            <div v-else-if="paymentError" class="mb-6 bg-red-100 border-l-4 border-red-500 text-red-700 p-4">
                <p>{{ paymentError }}</p>
                <button class="btn btn-primary mt-4" @click="cancelPayment">กลับสู่ตะกร้าสินค้า</button>
            </div>
            
            <!-- Payment Success -->
            <div v-else-if="paymentSuccess" class="bg-white rounded-lg shadow-lg p-8 text-center">
                <div class="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    </svg>
                </div>
                
                <h2 class="text-2xl font-bold text-gray-800 mb-4">การชำระเงินสำเร็จ!</h2>
                <p class="mb-2">หมายเลขคำสั่งซื้อของคุณคือ: <span class="font-bold">{{ orderNumber }}</span></p>
                <p v-if="paymentMethod === 'qr'" class="text-gray-600 mb-2">ขอบคุณสำหรับการชำระเงิน เราจะดำเนินการตามคำสั่งซื้อของคุณทันที</p>
                <p v-else class="text-gray-600 mb-2">คุณได้เลือกการชำระเงินปลายทาง คำสั่งซื้อของคุณกำลังถูกดำเนินการ</p>
                <p class="text-gray-600 mb-6">คุณสามารถติดตามสถานะคำสั่งซื้อได้ที่หน้าคำสั่งซื้อของฉัน</p>
                
                <p class="text-sm text-gray-500 mb-4">กำลังนำคุณไปยังหน้าคำสั่งซื้อในอีก {{ countdown }} วินาที...</p>
                
                <button class="btn btn-primary" @click="router.push('/orders')">
                    ดูคำสั่งซื้อ
                </button>
            </div>
            
            <!-- Payment Method Selection -->
            <div v-else-if="orderDetails && !paymentMethod" class="bg-white rounded-lg shadow-lg overflow-hidden">
                <!-- Order Summary -->
                <div class="p-6 bg-gray-50 border-b">
                    <h2 class="text-xl font-bold mb-4">สรุปคำสั่งซื้อ</h2>
                    <div class="flex justify-between text-sm mb-2">
                        <span>หมายเลขคำสั่งซื้อ:</span>
                        <span class="font-medium">{{ orderNumber }}</span>
                    </div>
                    <div class="flex justify-between font-bold text-lg border-t border-gray-200 pt-2 mt-2">
                        <span>ยอดรวมทั้งหมด:</span>
                        <span>{{ formatPrice(orderDetails.total_amount) }}</span>
                    </div>
                </div>
                
                <!-- Payment Methods -->
                <div class="p-6">
                    <h2 class="text-xl font-bold mb-4">เลือกวิธีการชำระเงิน</h2>
                    
                    <div class="space-y-4">
                        <!-- QR Payment Option -->
                        <div 
                            class="border rounded-lg p-4 hover:border-orange-500 cursor-pointer transition-all hover:bg-orange-50"
                            @click="selectPaymentMethod('qr')"
                        >
                            <div class="flex items-center space-x-4">
                                <div class="bg-blue-50 rounded-full p-3">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-blue-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                                        <path d="M8 8h2v2H8z"/>
                                        <path d="M14 8h2v2h-2z"/>
                                        <path d="M8 14h2v2H8z"/>
                                        <path d="M14 14h2v2h-2z"/>
                                    </svg>
                                </div>
                                <div class="flex-1">
                                    <h3 class="font-semibold text-lg">QR Payment</h3>
                                    <p class="text-gray-600">สแกนจ่ายผ่าน QR Code</p>
                                </div>
                                <div class="flex-shrink-0">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Cash on Delivery Option -->
                        <div 
                            class="border rounded-lg p-4 hover:border-orange-500 cursor-pointer transition-all hover:bg-orange-50"
                            @click="selectPaymentMethod('cod')"
                        >
                            <div class="flex items-center space-x-4">
                                <div class="bg-orange-50 rounded-full p-3">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <div class="flex-1">
                                    <h3 class="font-semibold text-lg">จ่ายปลายทาง</h3>
                                    <p class="text-gray-600">ชำระเงินเมื่อได้รับสินค้า</p>
                                </div>
                                <div class="flex-shrink-0">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- QR Code Payment Display -->
            <div v-else-if="showQrCode" class="bg-white rounded-lg shadow-lg overflow-hidden">
                <!-- Order Summary -->
                <div class="p-6 bg-gray-50 border-b">
                    <h2 class="text-xl font-bold mb-4">สแกน QR เพื่อชำระเงิน</h2>
                    <div class="flex justify-between text-sm mb-2">
                        <span>หมายเลขคำสั่งซื้อ:</span>
                        <span class="font-medium">{{ orderNumber }}</span>
                    </div>
                    <div class="flex justify-between font-bold text-lg border-t border-gray-200 pt-2 mt-2">
                        <span>ยอดที่ต้องชำระ:</span>
                        <span>{{ formatPrice(orderDetails.total_amount) }}</span>
                    </div>
                </div>
                
                <!-- QR Code Display -->
                <div class="p-6 flex flex-col items-center">
                    <div class="mb-6 max-w-xs">
                        <!-- QR Payment Header Removed -->
                        
                        <!-- Thai QR Payment Banner -->
                        <div class="bg-blue-900 p-3 flex justify-center rounded-t-lg">
                            <div class="text-white font-bold text-lg">THAI QR PAYMENT</div>
                        </div>
                        
                        <!-- PromptPay Label -->
                        <div class="bg-white p-3 border-b flex justify-center">
                            <div class="font-bold text-blue-900">พร้อมเพย์</div>
                        </div>
                        
                        <!-- QR Code -->
                        <div class="bg-white p-4 flex justify-center rounded-b-lg">
                            <img src="https://i.ibb.co/Vc240585/image-2025-03-29-203931507.png" alt="Payment QR Code" class="w-64 h-64" >
                        </div>
                        
                        <!-- Account Info -->
                        <div class="mt-4 text-center">
                            <p class="text-gray-700">ชื่อบัญชี</p>
                            <p class="font-semibold text-xl">นาย กฤษกร ขามวิเศษ</p>
                        </div>
                    </div>
                    
                    <p class="text-gray-600 mb-6 text-center max-w-lg">
                        กรุณาสแกน QR Code เพื่อชำระเงิน หลังจากชำระเงินเรียบร้อยแล้ว กดปุ่ม "ยืนยันการชำระเงิน" ด้านล่าง
                    </p>
                    
                    <div class="flex space-x-4">
                        <button 
                            class="btn btn-outline" 
                            :disabled="processingPayment"
                            @click="selectPaymentMethod(null)"
                        >
                            เปลี่ยนวิธีชำระเงิน
                        </button>
                        
                        <button 
                            class="btn btn-primary" 
                            :disabled="processingPayment"
                            @click="processPayment"
                        >
                            <span v-if="processingPayment">
                                <span class="loading loading-spinner loading-xs mr-2"/>
                                กำลังประมวลผล...
                            </span>
                            <span v-else>ยืนยันการชำระเงิน</span>
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Cash on Delivery Confirmation -->
            <div v-else-if="paymentMethod === 'cod'" class="bg-white rounded-lg shadow-lg overflow-hidden">
                <!-- Order Summary -->
                <div class="p-6 bg-gray-50 border-b">
                    <h2 class="text-xl font-bold mb-4">ยืนยันการชำระเงินปลายทาง</h2>
                    <div class="flex justify-between text-sm mb-2">
                        <span>หมายเลขคำสั่งซื้อ:</span>
                        <span class="font-medium">{{ orderNumber }}</span>
                    </div>
                    <div class="flex justify-between font-bold text-lg border-t border-gray-200 pt-2 mt-2">
                        <span>ยอดที่ต้องชำระ:</span>
                        <span>{{ formatPrice(orderDetails.total_amount) }}</span>
                    </div>
                </div>
                
                <!-- COD Confirmation -->
                <div class="p-6">
                    <div class="bg-orange-50 p-4 rounded-lg mb-6">
                        <div class="flex items-start">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-orange-500 mt-0.5 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <div>
                                <h3 class="font-medium text-orange-800 mb-2">รายละเอียดการชำระเงินปลายทาง</h3>
                                <p class="text-orange-700">คุณจะต้องชำระเงินจำนวน {{ formatPrice(orderDetails.total_amount) }} เมื่อได้รับสินค้า</p>
                                <p class="text-orange-700 mt-2">การชำระเงินสามารถทำได้โดยเงินสดหรือโอนเงินให้พนักงานส่งสินค้า</p>
                            </div>
                        </div>
                    </div>
                    
                    <p class="text-gray-600 mb-6 text-center">
                        กรุณากดปุ่ม "ยืนยันคำสั่งซื้อ" เพื่อดำเนินการต่อ
                    </p>
                    
                    <div class="flex space-x-4 justify-center">
                        <button 
                            class="btn btn-outline" 
                            :disabled="processingPayment"
                            @click="selectPaymentMethod(null)"
                        >
                            เปลี่ยนวิธีชำระเงิน
                        </button>
                        
                        <button 
                            class="btn btn-primary" 
                            :disabled="processingPayment"
                            @click="processPayment"
                        >
                            <span v-if="processingPayment">
                                <span class="loading loading-spinner loading-xs mr-2"/>
                                กำลังประมวลผล...
                            </span>
                            <span v-else>ยืนยันคำสั่งซื้อ</span>
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