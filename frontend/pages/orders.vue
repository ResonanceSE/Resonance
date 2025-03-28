<script setup>
import { useAuthStore } from '~/stores/useAuth';
import { orderService } from '~/services/orderService';

definePageMeta({
    layout: 'default',
    middleware: ['auth']
});

const authStore = useAuthStore();
const orders = ref([]);
const isLoading = ref(false);
const error = ref(null);
const expandedOrderId = ref(null);
const statusFilter = ref('');
const sortOrder = ref('newest');
const showTrackingModal = ref(false);
const selectedOrder = ref(null);
const showCancelModal = ref(false);
const orderToCancel = ref(null);
const isCancelling = ref(false);

// Tracking steps for the order progress visualization
const trackingSteps = [
    { status: 'pending', label: 'Order Placed' },
    { status: 'processing', label: 'Processing' },
    { status: 'shipped', label: 'Shipped' },
    { status: 'delivered', label: 'Delivered' }
];

// Computed properties
const filteredOrders = computed(() => {
    let result = [...orders.value];

    // Apply status filter
    if (statusFilter.value) {
        result = result.filter(order => order.status === statusFilter.value);
    }

    result.sort((a, b) => {
        const dateA = new Date(a.created_at).getTime();
        const dateB = new Date(b.created_at).getTime();

        return sortOrder.value === 'newest' ? dateB - dateA : dateA - dateB;
    });

    return result;
});

const fetchOrders = async () => {
    if (!authStore.isAuthenticated) {
        return;
    }

    isLoading.value = true;
    error.value = null;

    try {
        const data = await orderService.getOrders();
        orders.value = data;
    } catch (err) {
        console.error('Error fetching orders:', err);
        error.value = 'Failed to load your orders. Please try again.';
    } finally {
        isLoading.value = false;
    }
};

const toggleOrderDetails = (orderId) => {
    if (expandedOrderId.value === orderId) {
        expandedOrderId.value = null;
    } else {
        expandedOrderId.value = orderId;
    }
};

const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
};

const formatPrice = (price) => {
    if (typeof price === 'string') {
        price = parseFloat(price);
    }
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
};

// Format status for display
const formatStatus = (status) => {
    const statusMap = {
        pending: 'Pending',
        processing: 'Processing',
        shipped: 'Shipped',
        delivered: 'Delivered',
        cancelled: 'Cancelled'
    };

    return statusMap[status] || status;
};

// Get CSS class for status badge
const getStatusBadgeClass = (status) => {
    const statusClasses = {
        pending: 'bg-yellow-100 text-yellow-800',
        processing: 'bg-blue-100 text-blue-800',
        shipped: 'bg-indigo-100 text-indigo-800',
        delivered: 'bg-green-100 text-green-800',
        cancelled: 'bg-red-100 text-red-800'
    };

    return statusClasses[status] || 'bg-gray-100 text-gray-800';
};

// Apply filters to the orders
const applyFilters = () => {
    // No additional logic needed as we're using computed properties
};

// Track order - open tracking modal
const trackOrder = (order) => {
    selectedOrder.value = order;
    showTrackingModal.value = true;
};

// Get CSS class for tracking step
const getTrackingStepClass = (stepStatus, orderStatus) => {
    const stepIndex = trackingSteps.findIndex(step => step.status === stepStatus);
    const orderIndex = trackingSteps.findIndex(step => step.status === orderStatus);

    if (orderStatus === 'cancelled') {
        return stepStatus === 'pending' ? 'bg-red-500' : 'bg-gray-200';
    }

    if (stepIndex <= orderIndex) {
        return 'bg-green-500';
    }

    return 'bg-gray-200';
};

// Check if step is complete based on current order status
const isStepComplete = (stepStatus, orderStatus) => {
    const statusOrder = ['pending', 'processing', 'shipped', 'delivered'];
    const stepIndex = statusOrder.indexOf(stepStatus);
    const orderIndex = statusOrder.indexOf(orderStatus);

    if (orderStatus === 'cancelled') {
        return stepStatus === 'pending';
    }

    return stepIndex <= orderIndex;
};

// Get estimated delivery date (mocked function)
const getEstimatedDelivery = (order) => {
    if (order.status === 'delivered') {
        return 'Delivered';
    }

    if (order.status === 'cancelled') {
        return 'Order Cancelled';
    }

    // Mock delivery estimate calculation
    const orderDate = new Date(order.created_at);
    const deliveryDays = {
        pending: 7,
        processing: 5,
        shipped: 2
    };

    const days = deliveryDays[order.status] || 7;
    const estimatedDate = new Date(orderDate);
    estimatedDate.setDate(orderDate.getDate() + days);

    return formatDate(estimatedDate);
};

// Cancel order flow
const cancelOrder = (orderId) => {
    orderToCancel.value = orderId;
    showCancelModal.value = true;
};

// Confirm order cancellation 
const confirmCancelOrder = async () => {
    if (!orderToCancel.value) return;

    isCancelling.value = true;

    try {
        await orderService.cancelOrder(orderToCancel.value);

        // Update order status in the local state
        const index = orders.value.findIndex(o => o.id === orderToCancel.value);
        if (index !== -1) {
            orders.value[index].status = 'cancelled';
        }

        showCancelModal.value = false;
    } catch (err) {
        console.error('Error cancelling order:', err);
        alert('Failed to cancel order. Please try again.');
    } finally {
        isCancelling.value = false;
        orderToCancel.value = null;
    }
};

// Handle invoice download
const downloadInvoice = (order) => {
    const filename = `invoice-${order.order_number}.pdf`;
    alert(`In a production environment, this would download an invoice named "${filename}"`);
};

// Fetch orders on component mount
onMounted(() => {
    if (authStore.isAuthenticated) {
        fetchOrders();
    }
});

// Watch for auth state changes
watch(() => authStore.isAuthenticated, (newValue) => {
    if (newValue) {
        fetchOrders();
    }
});
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12 relative overflow-hidden">
        <!-- Decorative circles -->
        <div
            class="absolute top-20 left-10 w-64 h-64 bg-orange-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob" />
        <div
            class="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000" />
        <div
            class="absolute -bottom-8 left-40 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000" />

        <div class="container mx-auto px-4">
            <!-- Page Header -->
            <div class="mb-8 text-center">
                <h1 class="text-3xl font-bold">
                    <span
                        class="bg-gradient-to-r from-blue-500 to-indigo-600 bg-clip-text text-transparent">Order</span>
                    <span class="relative">
                        History
                        <span class="absolute -bottom-1 left-0 w-full h-1 bg-orange-400 rounded-full" />
                    </span>
                </h1>
                <p class="mt-2 text-gray-600">View and track your past orders</p>
            </div>

            <!-- Login Prompt (if not authenticated) -->
            <div
v-if="!authStore.isAuthenticated"
                class="bg-white rounded-lg shadow-xl p-8 max-w-md mx-auto text-center">
                <div class="w-16 h-16 mx-auto bg-orange-100 rounded-full flex items-center justify-center mb-4">
                    <svg
xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-orange-500" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                </div>
                <h2 class="text-2xl font-bold mb-4">Please Sign In</h2>
                <p class="text-gray-600 mb-6">You need to be logged in to view your order history</p>
                <NuxtLink to="/login" class="btn btn-primary">
                    Go to Login
                </NuxtLink>
            </div>

            <!-- Loading State -->
            <div v-else-if="isLoading" class="flex justify-center py-12">
                <div class="loading loading-spinner loading-lg text-orange-500" />
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="bg-white rounded-lg shadow-xl p-8 max-w-md mx-auto">
                <div class="flex items-center text-red-500 mb-4">
                    <svg
xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <h2 class="text-xl font-bold">Error Loading Orders</h2>
                </div>
                <p class="text-gray-600 mb-6">{{ error }}</p>
                <button class="btn btn-primary" @click="fetchOrders">
                    <svg
xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Try Again
                </button>
            </div>

            <!-- Empty Orders State -->
            <div v-else-if="orders.length === 0" class="bg-white rounded-lg shadow-xl p-8 max-w-md mx-auto text-center">
                <div class="w-16 h-16 mx-auto bg-blue-100 rounded-full flex items-center justify-center mb-4">
                    <svg
xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                </div>
                <h2 class="text-2xl font-bold mb-4">No Orders Found</h2>
                <p class="text-gray-600 mb-6">You haven't placed any orders yet.</p>
                <NuxtLink to="/products" class="btn btn-primary">
                    Start Shopping
                </NuxtLink>
            </div>

            <!-- Orders List -->
            <div v-else class="space-y-6">
                <!-- Filter & Sort Controls -->
                <div class="bg-white rounded-lg shadow-md p-4">
                    <div class="flex flex-col md:flex-row gap-4">
                        <div class="flex-1">
                            <select v-model="statusFilter" class="select select-bordered w-full" @change="applyFilters">
                                <option value="">All Statuses</option>
                                <option value="pending">Pending</option>
                                <option value="processing">Processing</option>
                                <option value="shipped">Shipped</option>
                                <option value="delivered">Delivered</option>
                                <option value="cancelled">Cancelled</option>
                            </select>
                        </div>
                        <div class="flex-1">
                            <select v-model="sortOrder" class="select select-bordered w-full" @change="applyFilters">
                                <option value="newest">Newest First</option>
                                <option value="oldest">Oldest First</option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- Orders Cards -->
                <div
v-for="order in filteredOrders" :key="order.id"
                    class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
                    <div class="p-6">
                        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                            <div>
                                <h3 class="text-lg font-semibold">Order #{{ order.order_number }}</h3>
                                <p class="text-sm text-gray-500">{{ formatDate(order.created_at) }}</p>
                            </div>

                            <div class="flex items-center gap-4">
                                <span
:class="getStatusBadgeClass(order.status)"
                                    class="px-3 py-1 rounded-full text-xs font-medium">
                                    {{ formatStatus(order.status) }}
                                </span>
                                <button class="btn btn-sm btn-ghost" @click="toggleOrderDetails(order.id)">
                                    {{ expandedOrderId === order.id ? 'Hide Details' : 'View Details' }}
                                </button>
                            </div>
                        </div>

                        <!-- Order Summary (always visible) -->
                        <div class="flex justify-between items-center mt-2">
                            <span class="text-gray-600">Total: <span class="font-semibold">{{
                                    formatPrice(order.total_amount) }}</span></span>
                            <button class="btn btn-sm btn-outline" @click="trackOrder(order)">
                                Track Order
                            </button>
                        </div>

                        <!-- Order Details (expandable) -->
                        <div v-if="expandedOrderId === order.id" class="mt-6 border-t pt-4">
                            <!-- Shipping Address -->
                            <div class="mb-4">
                                <h4 class="text-sm font-semibold text-gray-700 mb-2">Shipping Address</h4>
                                <p class="text-sm text-gray-600 whitespace-pre-line">{{ order.shipping_address }}</p>
                            </div>

                            <!-- Order Items -->
                            <div>
                                <h4 class="text-sm font-semibold text-gray-700 mb-2">Items</h4>
                                <div class="bg-gray-50 rounded-lg p-4">
                                    <div
v-for="(item, index) in order.items" :key="index"
                                        class="flex justify-between items-center py-2 border-b border-gray-200 last:border-0">
                                        <div class="flex-1">
                                            <p class="font-medium">{{ item.product }}</p>
                                            <p class="text-sm text-gray-500">Qty: {{ item.quantity }} × {{
                                                formatPrice(item.price) }}</p>
                                        </div>
                                        <div class="text-right">
                                            <p class="font-semibold">{{ formatPrice(item.subtotal) }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Order Actions -->
                            <div class="flex justify-between mt-4">
                                <button
v-if="order.status === 'pending'" class="btn btn-sm btn-error"
                                    @click="cancelOrder(order.id)">
                                    Cancel Order
                                </button>
                                <button class="btn btn-sm btn-outline" @click="downloadInvoice(order)">
                                    <svg
xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none"
                                        viewBox="0 0 24 24" stroke="currentColor">
                                        <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                    Download Invoice
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Track Order Modal -->
        <div
v-if="showTrackingModal && selectedOrder"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg shadow-xl w-full max-w-lg p-6 mx-4">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-xl font-semibold">Track Order #{{ selectedOrder.order_number }}</h2>
                    <button class="btn btn-sm btn-circle btn-ghost" @click="showTrackingModal = false">✕</button>
                </div>

                <div class="mb-8">
                    <h3 class="text-sm font-medium text-gray-500 mb-2">Current Status</h3>
                    <div class="flex items-center">
                        <span
:class="getStatusBadgeClass(selectedOrder.status)"
                            class="px-3 py-1 rounded-full text-xs font-medium">
                            {{ formatStatus(selectedOrder.status) }}
                        </span>
                        <span class="ml-3 text-gray-600">Updated {{ formatDate(selectedOrder.created_at) }}</span>
                    </div>
                </div>

                <!-- Shipping Progress -->
                <div class="mb-6">
                    <div class="relative">
                        <div class="absolute left-0 top-1/2 transform -translate-y-1/2 w-full h-1 bg-gray-200"/>

                        <div class="relative flex justify-between">
                            <div v-for="(step, index) in trackingSteps" :key="index" class="flex flex-col items-center">
                                <div
class="rounded-full w-8 h-8 flex items-center justify-center z-10 mb-2"
                                    :class="getTrackingStepClass(step.status, selectedOrder.status)">
                                    <svg
v-if="isStepComplete(step.status, selectedOrder.status)"
                                        xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white"
                                        viewBox="0 0 20 20" fill="currentColor">
                                        <path
fill-rule="evenodd"
                                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                            clip-rule="evenodd" />
                                    </svg>
                                    <span v-else class="text-xs font-medium">{{ index + 1 }}</span>
                                </div>
                                <div
class="text-xs font-medium text-center"
                                    :class="isStepComplete(step.status, selectedOrder.status) ? 'text-green-600' : 'text-gray-500'">
                                    {{ step.label }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Estimated Delivery -->
                <div class="bg-gray-50 p-4 rounded-lg">
                    <h3 class="text-sm font-medium text-gray-700 mb-2">Estimated Delivery</h3>
                    <p class="text-lg font-semibold">{{ getEstimatedDelivery(selectedOrder) }}</p>
                </div>

                <div class="text-center mt-8">
                    <button class="btn btn-primary" @click="showTrackingModal = false">Close</button>
                </div>
            </div>
        </div>

        <!-- Cancel Order Confirmation Modal -->
        <div v-if="showCancelModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg shadow-xl w-full max-w-md p-6 mx-4">
                <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
                    <svg
xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                </div>

                <h3 class="text-xl font-medium text-center mb-4">Cancel Order</h3>
                <p class="text-gray-600 mb-6 text-center">Are you sure you want to cancel this order? This action cannot
                    be undone.</p>

                <div class="flex justify-center space-x-4">
                    <button class="btn btn-outline" @click="showCancelModal = false">
                        Keep Order
                    </button>
                    <button class="btn btn-error" :disabled="isCancelling" @click="confirmCancelOrder">
                        <span v-if="isCancelling">
                            <span class="loading loading-spinner loading-xs mr-2" />
                            Cancelling...
                        </span>
                        <span v-else>Yes, Cancel Order</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
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
    @apply bg-orange-500 hover:bg-orange-600 border-orange-500 text-white;
}
</style>