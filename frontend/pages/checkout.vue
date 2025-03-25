<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

definePageMeta({
    layout: 'default'
})

const router = useRouter()

// Checkout steps
const currentStep = ref('cart') // 'cart', 'shipping', 'payment', 'confirmation'
const isLoading = ref(false)

// Cart data
const cartItems = ref([
    {
        id: 1,
        name: 'Campfire Trifecta Astral Plane',
        category: 'Astral Plane',
        price: 3375,
        quantity: 1,
        image: '/images/product-placeholder.jpg'
    }
])

const selectedItems = reactive({})

// Initialize selectedItems with all items selected
onMounted(() => {
    cartItems.value.forEach(item => {
        selectedItems[item.id] = true
    })
})

// Toggle individual item selection
const toggleItemSelection = (itemId) => {
    selectedItems[itemId] = !selectedItems[itemId]
}

// Computed property for select all functionality
const selectAll = computed({
    get: () => {
        return cartItems.value.length > 0 &&
            cartItems.value.every(item => selectedItems[item.id])
    },
    set: (value) => {
        cartItems.value.forEach(item => {
            selectedItems[item.id] = value
        })
    }
})

const decreaseQuantity = (item) => {
    if (item.quantity > 1) {
        item.quantity--
    }
}

const increaseQuantity = (item) => {
    item.quantity++
}

const removeItem = (itemId) => {
    const index = cartItems.value.findIndex(item => item.id === itemId)
    if (index !== -1) {
        cartItems.value.splice(index, 1)
        // Fix for @typescript-eslint/no-dynamic-delete
        selectedItems[itemId] = undefined
    }
}

const removeSelectedItems = () => {
    cartItems.value = cartItems.value.filter(item => !selectedItems[item.id])

    Object.keys(selectedItems).forEach(key => {
        if (selectedItems[key]) {
            // Fix for @typescript-eslint/no-dynamic-delete
            selectedItems[key] = undefined
        }
    })
}

// Price calculations
const getItemsPrice = computed(() => {
    let total = 0
    for (const item of cartItems.value) {
        if (selectedItems[item.id]) {
            total += item.price * item.quantity
        }
    }
    return total
})

// Using this function throughout the template to fix unused variable warning
const formatPrice = (price) => {
    return '$' + (price / 100).toFixed(2)
}

const getSelectedItemsCount = computed(() => {
    return Object.values(selectedItems).filter(Boolean).length
})

// Shipping and payment
const shippingFee = ref(999)
const voucher = ref('')
const discount = ref(0)

// Order Summary calculations
const totalPrice = computed(() => {
    return getItemsPrice.value + shippingFee.value - discount.value
})

// Customer information
const customerInfo = reactive({
    firstName: '',
    lastName: '',
    email: '',
    phone: ''
})

// Address management
const addresses = ref([
    {
        id: 1,
        default: true,
        recipient: 'John Doe',
        line1: 'xxx/xxx, xxxx Village, xxxx Rd.',
        line2: 'xxxx District, xxxx Province, 10xxx'
    }
])

const selectedAddress = ref(addresses.value[0])
const showAddressModal = ref(false)
const showNewAddressForm = ref(false)
const newAddress = reactive({
    recipient: '',
    line1: '',
    line2: ''
})

// Payment methods
const paymentMethods = ref([
    { id: 1, name: 'Credit/Debit Card', icon: 'credit-card' },
    { id: 2, name: 'PayPal', icon: 'paypal' },
    { id: 3, name: 'Bank Transfer', icon: 'building' }
])
const selectedPaymentMethod = ref(paymentMethods.value[0])

// Payment details
const cardDetails = reactive({
    number: '',
    name: '',
    expiry: '',
    cvv: ''
})

// Apply voucher code
const applyVoucher = () => {
    isLoading.value = true

    // Simulate API request
    setTimeout(() => {
        if (voucher.value.toUpperCase() === 'RESONANCE20') {
            discount.value = Math.round(getItemsPrice.value * 0.2)
            // Success notification would go here
        } else {
            discount.value = 0
            // Error notification would go here
        }
        isLoading.value = false
    }, 800)
}

// Add new address
const addNewAddress = () => {
    // Basic validation
    if (!newAddress.recipient || !newAddress.line1) {
        return
    }

    const newId = addresses.value.length > 0
        ? Math.max(...addresses.value.map(a => a.id)) + 1
        : 1

    addresses.value.push({
        id: newId,
        default: addresses.value.length === 0,
        ...newAddress
    })

    selectedAddress.value = addresses.value.find(a => a.id === newId)
    showNewAddressForm.value = false
    showAddressModal.value = false

    // Reset form
    Object.keys(newAddress).forEach(key => {
        newAddress[key] = ''
    })
}

// Process checkout
const processCheckout = () => {
    if (currentStep.value === 'cart') {
        currentStep.value = 'shipping'
    } else if (currentStep.value === 'shipping') {
        // Validate shipping info
        if (!customerInfo.email || !selectedAddress.value) {
            // Show validation error
            return
        }
        currentStep.value = 'payment'
    } else if (currentStep.value === 'payment') {
        // Validate payment info
        if (selectedPaymentMethod.value.id === 1 &&
            (!cardDetails.number || !cardDetails.name || !cardDetails.expiry || !cardDetails.cvv)) {
            // Show validation error
            return
        }

        // Submit order
        submitOrder()
    }
}

const previousStep = () => {
    if (currentStep.value === 'shipping') {
        currentStep.value = 'cart'
    } else if (currentStep.value === 'payment') {
        currentStep.value = 'shipping'
    }
}

const submitOrder = () => {
    isLoading.value = true

    // Simulate API request
    setTimeout(() => {
        // Order successful
        currentStep.value = 'confirmation'
        isLoading.value = false

        // In a real app, you would store the order ID and details
    }, 1500)
}

const goToProductPage = () => {
    router.push('/products')
}
</script>

<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header and progress indicator would go here -->

        <div class="container max-w-6xl mx-auto px-4 py-8">
            <!-- Page title -->
            <div class="mb-8">
                <h1 class="text-3xl font-bold">
                    <span class="text-blue-600">Checkout</span>
                    <span class="text-gray-800"> Page</span>
                </h1>
                <div class="h-1 w-24 bg-orange-500 mt-2" />
            </div>

            <!-- Checkout steps -->
            <div v-if="currentStep !== 'confirmation'" class="mb-8">
                <div class="flex items-center justify-between max-w-2xl mx-auto">
                    <div class="flex flex-col items-center">
                        <div class="w-10 h-10 rounded-full flex items-center justify-center mb-2"
                            :class="currentStep === 'cart' ? 'bg-orange-500 text-white' : 'bg-gray-200 text-gray-600'">
                            1
                        </div>
                        <span class="text-sm">Cart</span>
                    </div>

                    <div class="flex-1 h-1 mx-4" :class="currentStep === 'cart' ? 'bg-gray-200' : 'bg-orange-500'" />

                    <div class="flex flex-col items-center">
                        <div class="w-10 h-10 rounded-full flex items-center justify-center mb-2"
                            :class="currentStep === 'shipping' ? 'bg-orange-500 text-white' : (currentStep === 'cart' ? 'bg-gray-200 text-gray-600' : 'bg-orange-500 text-white')">
                            2
                        </div>
                        <span class="text-sm">Shipping</span>
                    </div>

                    <div class="flex-1 h-1 mx-4" :class="currentStep === 'payment' ? 'bg-orange-500' : 'bg-gray-200'" />

                    <div class="flex flex-col items-center">
                        <div class="w-10 h-10 rounded-full flex items-center justify-center mb-2"
                            :class="currentStep === 'payment' ? 'bg-orange-500 text-white' : 'bg-gray-200 text-gray-600'">
                            3
                        </div>
                        <span class="text-sm">Payment</span>
                    </div>
                </div>
            </div>

            <!-- Cart Step -->
            <div v-if="currentStep === 'cart'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Cart Items -->
                <div class="lg:col-span-2">
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <h2 class="text-xl font-semibold mb-4">Your Cart</h2>

                        <!-- Select all -->
                        <div class="flex justify-between items-center mb-4 pb-2 border-b border-gray-200">
                            <div class="flex items-center">
                                <input v-model="selectAll" type="checkbox"
                                    class="w-5 h-5 rounded text-orange-500 focus:ring-orange-500 border-gray-400">
                                <span class="ml-2 text-gray-700">Select All ({{ getSelectedItemsCount }} items)</span>
                            </div>
                            <button class="text-red-500 hover:text-red-700 text-sm font-medium"
                                @click="removeSelectedItems">
                                Remove
                            </button>
                        </div>

                        <!-- Cart Items -->
                        <div v-if="cartItems.length > 0" class="divide-y divide-gray-100">
                            <div v-for="item in cartItems" :key="item.id" class="py-4 flex items-center">
                                <div class="mr-4">
                                    <input type="checkbox"
                                        class="w-5 h-5 rounded text-orange-500 focus:ring-orange-500 border-gray-400"
                                        :checked="selectedItems[item.id]" @change="toggleItemSelection(item.id)">
                                </div>

                                <!-- Product image -->
                                <div class="w-16 h-16 bg-gray-100 rounded-md mr-4" />

                                <!-- Product details -->
                                <div class="flex-grow">
                                    <h3 class="font-medium text-gray-800">{{ item.name }}</h3>
                                    <p class="text-sm text-gray-500">{{ item.category }}</p>
                                    <p class="font-semibold text-gray-900 mt-1">{{ formatPrice(item.price) }}</p>
                                </div>

                                <!-- Quantity control -->
                                <div class="flex items-center border rounded-md mr-6 border-gray-400">
                                    <button class="px-3 py-1 text-gray-600 hover:bg-gray-100"
                                        @click="decreaseQuantity(item)">
                                        -
                                    </button>
                                    <span class="px-4 py-1 text-gray-800">{{ item.quantity }}</span>
                                    <button class="px-3 py-1 text-gray-600 hover:bg-gray-100"
                                        @click="increaseQuantity(item)">
                                        +
                                    </button>
                                </div>

                                <!-- Total price -->
                                <div class="text-right">
                                    <p class="font-semibold text-orange-500">{{ formatPrice(item.price * item.quantity)
                                    }}</p>
                                    <button class="text-sm text-red-500 hover:text-red-700"
                                        @click="removeItem(item.id)">
                                        Remove
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Empty cart state -->
                        <div v-if="cartItems.length === 0" class="text-center py-12">
                            <p class="text-gray-500 mb-4">Your cart is empty</p>
                            <button class="px-4 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600"
                                @click="goToProductPage">
                                Continue Shopping
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Order Summary -->
                <div class="lg:col-span-1">
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <h2 class="text-xl font-semibold mb-4">Order Summary</h2>

                        <!-- Summary Details -->
                        <div class="space-y-3 mb-4">
                            <div class="flex justify-between text-gray-700">
                                <span>Items Price ({{ getSelectedItemsCount }} Items)</span>
                                <span>{{ formatPrice(getItemsPrice) }}</span>
                            </div>
                            <div class="flex justify-between text-gray-700">
                                <span>Shipping Fee</span>
                                <span>{{ formatPrice(shippingFee) }}</span>
                            </div>
                            <div v-if="discount > 0" class="flex justify-between text-green-600">
                                <span>Discount</span>
                                <span>-{{ formatPrice(discount) }}</span>
                            </div>
                            <div class="border-t border-gray-200 pt-3 mt-3">
                                <div class="flex justify-between font-bold text-gray-900">
                                    <span>Total Price</span>
                                    <span>{{ formatPrice(totalPrice) }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Voucher -->
                        <div class="mb-6">
                            <div class="flex">
                                <input v-model="voucher" type="text" placeholder="Enter Voucher Code"
                                    class="flex-1 rounded-l-md border border-gray-400 focus:ring-orange-500 focus:border-orange-500">
                                <button class="px-4 py-2 bg-orange-500 text-white rounded-r-md hover:bg-orange-600"
                                    @click="applyVoucher">
                                    Apply
                                </button>
                            </div>
                        </div>

                        <!-- Proceed to Checkout -->
                        <button class="w-full py-3 bg-orange-500 text-white rounded-md hover:bg-orange-600 font-medium"
                            :disabled="cartItems.length === 0 || getSelectedItemsCount === 0"
                            :class="{ 'opacity-50 cursor-not-allowed': cartItems.length === 0 || getSelectedItemsCount === 0 }"
                            @click="processCheckout">
                            Proceed to Checkout
                        </button>
                    </div>
                </div>
            </div>

            <!-- Shipping Step -->
            <div v-if="currentStep === 'shipping'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Shipping Information -->
                <div class="lg:col-span-2">
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <h2 class="text-xl font-semibold mb-4">Shipping Information</h2>

                        <!-- Customer Information Form -->
                        <div class="mb-6">
                            <h3 class="text-lg font-medium mb-3">Customer Information</h3>

                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="form-control">
                                    <label class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                                    <input v-model="customerInfo.firstName" type="text"
                                        class="w-full rounded-md border border-gray-400 focus:ring-orange-500 focus:border-orange-500"
                                        required>
                                </div>

                                <div class="form-control">
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                                    <input v-model="customerInfo.lastName" type="text"
                                        class="w-full rounded-md border border-gray-400 focus:ring-orange-500 focus:border-orange-500"
                                        required>
                                </div>
                            </div>

                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                                <div class="form-control">
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                                    <input v-model="customerInfo.email" type="email"
                                        class="w-full rounded-md border border-gray-400 focus:ring-orange-500 focus:border-orange-500"
                                        required>
                                </div>

                                <div class="form-control">
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                                    <input v-model="customerInfo.phone" type="tel"
                                        class="w-full rounded-md border border-gray-400 focus:ring-orange-500 focus:border-orange-500">
                                </div>
                            </div>
                        </div>

                        <!-- Shipping Address -->
                        <div class="mb-6">
                            <h3 class="text-lg font-medium mb-3">Shipping Address</h3>

                            <div v-if="selectedAddress" class="p-4 bg-gray-50 rounded-md mb-4 border border-gray-300">
                                <div class="flex justify-between">
                                    <div>
                                        <p class="font-medium text-gray-800">{{ selectedAddress.recipient }}</p>
                                        <p class="text-gray-600">{{ selectedAddress.line1 }}</p>
                                        <p class="text-gray-600">{{ selectedAddress.line2 }}</p>
                                    </div>
                                    <span v-if="selectedAddress.default"
                                        class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">Default</span>
                                </div>
                            </div>

                            <div class="flex gap-3">
                                <button class="px-4 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 flex-1"
                                    @click="showAddressModal = true">
                                    Select Address
                                </button>
                                <button
                                    class="px-4 py-2 border border-gray-400 text-gray-700 rounded-md hover:bg-gray-50 flex-1"
                                    @click="showNewAddressForm = true; showAddressModal = true">
                                    Add New Address
                                </button>
                            </div>
                        </div>

                        <!-- Navigation buttons -->
                        <div class="flex justify-between mt-8">
                            <button class="px-6 py-2 border border-gray-400 text-gray-700 rounded-md hover:bg-gray-50"
                                @click="previousStep">
                                Back to Cart
                            </button>

                            <button class="px-6 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600"
                                :disabled="!customerInfo.email || !selectedAddress"
                                :class="{ 'opacity-50 cursor-not-allowed': !customerInfo.email || !selectedAddress }"
                                @click="processCheckout">
                                Continue to Payment
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Order Summary -->
                <div class="lg:col-span-1">
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <h2 class="text-xl font-semibold mb-4">Order Summary</h2>

                        <!-- Cart Items Summary -->
                        <div class="space-y-4 mb-6">
                            <div v-for="item in cartItems.filter(i => selectedItems[i.id])" :key="item.id"
                                class="flex items-center">
                                <div class="w-12 h-12 bg-gray-100 rounded-md mr-3 flex-shrink-0" />
                                <div class="flex-grow">
                                    <p class="text-sm font-medium text-gray-800">{{ item.name }}</p>
                                    <p class="text-xs text-gray-500">Qty: {{ item.quantity }}</p>
                                </div>
                                <div class="text-right">
                                    <p class="text-sm font-semibold">{{ formatPrice(item.price * item.quantity) }}</p>
                                </div>
                            </div>
                        </div>

                        <!-- Summary Details -->
                        <div class="space-y-3 border-t border-gray-200 pt-4">
                            <div class="flex justify-between text-gray-700">
                                <span>Subtotal</span>
                                <span>{{ formatPrice(getItemsPrice) }}</span>
                            </div>
                            <div class="flex justify-between text-gray-700">
                                <span>Shipping</span>
                                <span>{{ formatPrice(shippingFee) }}</span>
                            </div>
                            <div v-if="discount > 0" class="flex justify-between text-green-600">
                                <span>Discount</span>
                                <span>-{{ formatPrice(discount) }}</span>
                            </div>
                            <div class="border-t border-gray-200 pt-3 mt-3">
                                <div class="flex justify-between font-bold text-gray-900">
                                    <span>Total</span>
                                    <span>{{ formatPrice(totalPrice) }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Payment Step -->
            <div v-if="currentStep === 'payment'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Payment Information -->
                <div class="lg:col-span-2">
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <h2 class="text-xl font-semibold mb-4">Payment Method</h2>

                        <!-- Payment Options -->
                        <div class="space-y-3 mb-6">
                            <div v-for="method in paymentMethods" :key="method.id"
                                class="border border-gray-400 rounded-md p-4 cursor-pointer"
                                :class="{ 'border-orange-500 bg-orange-50': selectedPaymentMethod.id === method.id }"
                                @click="selectedPaymentMethod = method">
                                <div class="flex items-center">
                                    <input type="radio" :checked="selectedPaymentMethod.id === method.id"
                                        class="w-4 h-4 text-orange-500 focus:ring-orange-500 border-gray-400">
                                    <span class="ml-2 font-medium text-gray-800">{{ method.name }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Credit Card Form (shown when credit card is selected) -->
                        <div v-if="selectedPaymentMethod.id === 1" class="mt-6 border-t border-gray-200 pt-6">
                            <h3 class="text-lg font-medium mb-4">Card Details</h3>

                            <div class="space-y-4">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Card Number</label>
                                    <input v-model="cardDetails.number" type="text"
                                        class="w-full rounded-md border border-gray-400 focus:ring-orange-500 focus:border-orange-500"
                                        placeholder="1234 5678 9012 3456">
                                </div>

                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Cardholder Name</label>
                                    <input v-model="cardDetails.name" type="text"
                                        class="w-full rounded-md border border-gray-400 focus:ring-orange-500 focus:border-orange-500"
                                        placeholder="John Doe">
                                </div>

                                <div class="grid grid-cols-2 gap-4">
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">Expiry Date</label>
                                        <input v-model="cardDetails.expiry" type="text"
                                            class="w-full rounded-md border border-gray-400 focus:ring-orange-500 focus:border-orange-500"
                                            placeholder="MM/YY">
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">CVV</label>
                                        <input v-model="cardDetails.cvv" type="text"
                                            class="w-full rounded-md border border-gray-400 focus:ring-orange-500 focus:border-orange-500"
                                            placeholder="123">
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- PayPal instructions -->
                        <div v-if="selectedPaymentMethod.id === 2" class="mt-6 border-t border-gray-200 pt-6">
                            <p class="text-gray-600">
                                You will be redirected to PayPal to complete your payment after reviewing your order.
                            </p>
                        </div>

                        <!-- Bank Transfer instructions -->
                        <div v-if="selectedPaymentMethod.id === 3" class="mt-6 border-t border-gray-200 pt-6">
                            <p class="text-gray-600">
                                After placing your order, you will receive bank details to complete the transfer.
                                Your order will be processed once payment is confirmed.
                            </p>
                        </div>

                        <!-- Navigation buttons -->
                        <div class="flex justify-between mt-8">
                            <button class="px-6 py-2 border border-gray-400 text-gray-700 rounded-md hover:bg-gray-50"
                                @click="previousStep">
                                Back to Shipping
                            </button>

                            <button class="px-6 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600"
                                :disabled="selectedPaymentMethod.id === 1 && (!cardDetails.number || !cardDetails.name || !cardDetails.expiry || !cardDetails.cvv)"
                                :class="{ 'opacity-50 cursor-not-allowed': selectedPaymentMethod.id === 1 && (!cardDetails.number || !cardDetails.name || !cardDetails.expiry || !cardDetails.cvv) }"
                                @click="processCheckout">
                                Place Order
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Order Summary -->
                <div class="lg:col-span-1">
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <h2 class="text-xl font-semibold mb-4">Order Summary</h2>

                        <!-- Order Details Summary -->
                        <div class="mb-4">
                            <h3 class="font-medium text-gray-700 mb-2">Customer</h3>
                            <p class="text-gray-600">{{ customerInfo.firstName }} {{ customerInfo.lastName }}</p>
                            <p class="text-gray-600">{{ customerInfo.email }}</p>
                            <p v-if="customerInfo.phone" class="text-gray-600">{{ customerInfo.phone }}</p>
                        </div>

                        <div class="mb-4">
                            <h3 class="font-medium text-gray-700 mb-2">Shipping Address</h3>
                            <p class="text-gray-600">{{ selectedAddress.recipient }}</p>
                            <p class="text-gray-600">{{ selectedAddress.line1 }}</p>
                            <p class="text-gray-600">{{ selectedAddress.line2 }}</p>
                        </div>

                        <!-- Cart Items Summary -->
                        <div class="space-y-3 mb-4 border-t border-gray-200 pt-4">
                            <h3 class="font-medium text-gray-700 mb-2">Items</h3>
                            <div v-for="item in cartItems.filter(i => selectedItems[i.id])" :key="item.id"
                                class="flex justify-between text-sm">
                                <span class="text-gray-600">{{ item.name }} (x{{ item.quantity }})</span>
                                <span class="font-medium">{{ formatPrice(item.price * item.quantity) }}</span>
                            </div>
                        </div>

                        <!-- Summary Details -->
                        <div class="space-y-3 border-t border-gray-200 pt-4">
                            <div class="flex justify-between text-gray-700">
                                <span>Subtotal</span>
                                <span>{{ formatPrice(getItemsPrice) }}</span>
                            </div>
                            <div class="flex justify-between text-gray-700">
                                <span>Shipping</span>
                                <span>{{ formatPrice(shippingFee) }}</span>
                            </div>
                            <div v-if="discount > 0" class="flex justify-between text-green-600">
                                <span>Discount</span>
                                <span>-{{ formatPrice(discount) }}</span>
                            </div>
                            <div class="border-t border-gray-200 pt-3 mt-3">
                                <div class="flex justify-between font-bold text-gray-900">
                                    <span>Total</span>
                                    <span>{{ formatPrice(totalPrice) }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Order Confirmation -->
            <div v-if="currentStep === 'confirmation'" class="max-w-2xl mx-auto">
                <div class="bg-white rounded-lg shadow-sm p-8 text-center">
                    <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                    </div>

                    <h2 class="text-2xl font-bold text-gray-800 mb-2">Thank You For Your Order!</h2>
                    <p class="text-gray-600 mb-6">Your order has been placed successfully.</p>

                    <div class="bg-gray-50 rounded-md p-6 mb-6 border border-gray-300">
                        <div class="flex justify-between mb-2">
                            <span class="font-medium text-gray-700">Order Number:</span>
                            <span>ORD-{{ Math.floor(Math.random() * 10000).toString().padStart(4, '0') }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="font-medium text-gray-700">Order Date:</span>
                            <span>{{ new Date().toLocaleDateString() }}</span>
                        </div>
                    </div>

                    <div class="space-y-3 mb-6">
                        <h3 class="text-lg font-medium text-gray-800 text-left">Order Summary</h3>
                        <div class="space-y-3 border-t border-gray-200 pt-4">
                            <div v-for="item in cartItems.filter(i => selectedItems[i.id])" :key="item.id"
                                class="flex justify-between">
                                <span>{{ item.name }} (x{{ item.quantity }})</span>
                                <span>{{ formatPrice(item.price * item.quantity) }}</span>
                            </div>
                            <div class="border-t border-gray-200 pt-3 mt-3">
                                <div class="flex justify-between font-bold">
                                    <span>Total</span>
                                    <span>{{ formatPrice(totalPrice) }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="space-y-3 mb-8 text-left">
                        <h3 class="text-lg font-medium text-gray-800">Shipping Details</h3>
                        <div class="bg-gray-50 rounded-md p-4 border border-gray-300">
                            <p class="font-medium">{{ customerInfo.firstName }} {{ customerInfo.lastName }}</p>
                            <p class="text-gray-600">{{ selectedAddress.line1 }}</p>
                            <p class="text-gray-600">{{ selectedAddress.line2 }}</p>
                            <p class="text-gray-600">Email: {{ customerInfo.email }}</p>
                            <p v-if="customerInfo.phone" class="text-gray-600">Phone: {{ customerInfo.phone }}</p>
                        </div>
                    </div>

                    <div class="flex gap-4 justify-center">
                        <button class="px-6 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600"
                            @click="goToProductPage">
                            Continue Shopping
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <!-- Address Modal -->
        <div v-if="showAddressModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg p-6 max-w-md w-full">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-xl font-bold">Select Delivery Address</h3>
                    <button class="text-gray-500 hover:text-gray-700" @click="showAddressModal = false">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <div v-if="!showNewAddressForm">
                    <div v-for="address in addresses" :key="address.id" class="mb-3">
                        <div class="p-3 border border-gray-400 rounded-md cursor-pointer hover:bg-gray-50"
                            :class="{ 'border-orange-500 bg-orange-50': selectedAddress.id === address.id }"
                            @click="selectedAddress = address; showAddressModal = false">
                            <div class="flex items-start gap-3">
                                <input type="radio" name="addressRadio"
                                    class="mt-1 h-4 w-4 text-orange-500 border-gray-400 focus:ring-orange-500"
                                    :checked="selectedAddress.id === address.id">
                                <div>
                                    <p class="font-medium">{{ address.recipient }}</p>
                                    <p class="text-gray-600 text-sm">{{ address.line1 }}</p>
                                    <p class="text-gray-600 text-sm">{{ address.line2 }}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="flex justify-end gap-2 mt-4">
                        <button class="px-4 py-2 border border-gray-400 rounded-md hover:bg-gray-50"
                            @click="showNewAddressForm = true">
                            Add New
                        </button>
                        <button class="px-4 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600"
                            @click="showAddressModal = false">
                            Confirm
                        </button>
                    </div>
                </div>

                <div v-else>
                    <!-- New Address Form -->
                    <form class="space-y-4" @submit.prevent="addNewAddress">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Recipient's Full Name</label>
                            <input v-model="newAddress.recipient" type="text"
                                class="w-full rounded-md border border-gray-400 focus:ring-orange-500 focus:border-orange-500"
                                required>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Address Line 1</label>
                            <input v-model="newAddress.line1" type="text"
                                class="w-full rounded-md border border-gray-400 focus:ring-orange-500 focus:border-orange-500"
                                placeholder="Street address, apartment, etc." required>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Address Line 2</label>
                            <input v-model="newAddress.line2" type="text"
                                class="w-full rounded-md border border-gray-400 focus:ring-orange-500 focus:border-orange-500"
                                placeholder="City, state, postal code">
                        </div>

                        <div class="flex justify-end gap-2 mt-6">
                            <button type="button" class="px-4 py-2 border border-gray-400 rounded-md hover:bg-gray-50"
                                @click="showNewAddressForm = false">
                                Cancel
                            </button>
                            <button type="submit"
                                class="px-4 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600">
                                Save Address
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Custom styles for better UI */
input[type="checkbox"],
input[type="radio"] {
    color: #f97316;
}

/* Enhanced visible borders for all inputs */
input,
select,
textarea {
    border-color: #9ca3af;
    /* border-gray-400 */
    border-width: 1px;
}

input:focus,
select:focus,
textarea:focus {
    --tw-ring-color: rgba(249, 115, 22, 0.6);
    border-color: #f97316;
    border-width: 1px;
    outline: none;
}

.focus\:ring-orange-500:focus {
    --tw-ring-color: rgba(249, 115, 22, 0.6);
    box-shadow: 0 0 0 2px var(--tw-ring-color);
}

.focus\:border-orange-500:focus {
    border-color: #f97316;
}

.hover\:bg-orange-600:hover {
    background-color: #ea580c;
}

/* Optional animation for transitions */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
