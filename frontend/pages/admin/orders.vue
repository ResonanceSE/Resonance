//frontend/pages/admin/orders.vue
<script setup lang="ts">
import { useAuthStore } from '~/stores/useAuth';

definePageMeta({
  layout: 'admin',
  middleware: ['auth']
});

interface OrderItem {
  id: number;
  product: string;
  quantity: number;
  price: number;
}

interface Order {
  id: number;
  order_number: string;
  user: string;
  status: string;
  total_amount: string;
  shipping_address: string;
  payment_status: boolean;
  created_at: string;
  items?: OrderItem[];
}

const orders = ref<Order[]>([]);
const selectedOrder = ref<Order | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);
const isUpdatingOrderStatus = ref(false);
const authStore = useAuthStore();
const config = useRuntimeConfig();
const apiUrl = config.public.apiUrl || 'http://localhost:8000';

// Order status options 
const orderStatuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];

// Fetch orders
const fetchOrders = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await fetch(`${apiUrl}/api/staff/orders/`, {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch orders: ${response.statusText}`);
    }
    
    const data = await response.json();
    orders.value = Array.isArray(data) ? data : [];
  } catch (err) {
    console.error('Error fetching orders:', err);
    error.value = err instanceof Error ? err.message : 'Failed to load orders data';
  } finally {
    loading.value = false;
  }
};

// View order details
const viewOrderDetails = async (order: Order) => {
  try {
    const response = await fetch(`${apiUrl}/api/staff/orders/${order.id}/`, {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch order details: ${response.statusText}`);
    }
    
    const data = await response.json();
    selectedOrder.value = data;
  } catch (err) {
    console.error('Error fetching order details:', err);
    alert(err instanceof Error ? err.message : 'Failed to load order details');
  }
};

// Update order status
const updateOrderStatus = async (order: Order) => {
  if (!order) return;
  
  isUpdatingOrderStatus.value = true;
  
  try {
    const response = await fetch(`${apiUrl}/api/staff/orders/${order.id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${authStore.token}`
      },
      body: JSON.stringify({ status: order.status })
    });
    
    if (!response.ok) {
      throw new Error(`Failed to update order status: ${response.statusText}`);
    }
    
    // Update the order in the orders list
    const index = orders.value.findIndex(o => o.id === order.id);
    if (index !== -1) {
      orders.value[index].status = order.status;
    }
  } catch (err) {
    console.error('Error updating order status:', err);
    alert(err instanceof Error ? err.message : 'Failed to update order status');
  } finally {
    isUpdatingOrderStatus.value = false;
  }
};

// Format date
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Get status class for coloring
const getStatusClass = (status: string) => {
  switch (status.toLowerCase()) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    case 'processing':
      return 'bg-blue-100 text-blue-800';
    case 'shipped':
      return 'bg-purple-100 text-purple-800';
    case 'delivered':
      return 'bg-green-100 text-green-800';
    case 'cancelled':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

// Print order details
const printOrderDetails = () => {
  if (!selectedOrder.value) return;
  
  const printWindow = window.open('', '_blank');
  if (!printWindow) {
    alert('Please allow pop-ups to print order details');
    return;
  }
  
  const order = selectedOrder.value;
  
  let printContent = `
    <html>
    <head>
      <title>Order #${order.order_number}</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        .section { margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f4f4f4; }
      </style>
    </head>
    <body>
      <h1>Order #${order.order_number}</h1>
      
      <div class="section">
        <h2>Order Information</h2>
        <p><strong>Date:</strong> ${formatDate(order.created_at)}</p>
        <p><strong>Status:</strong> ${order.status}</p>
        <p><strong>Payment Status:</strong> ${order.payment_status ? 'Paid' : 'Unpaid'}</p>
      </div>
      
      <div class="section">
        <h2>Customer Information</h2>
        <p><strong>Customer:</strong> ${order.user || 'Anonymous'}</p>
        <p><strong>Shipping Address:</strong><br>${order.shipping_address.replace(/\n/g, '<br>')}</p>
      </div>
      
      <div class="section">
        <h2>Order Items</h2>
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Quantity</th>
              <th>Price</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
  `;
  
  if (order.items && order.items.length > 0) {
    order.items.forEach(item => {
      printContent += `
        <tr>
          <td>${item.product}</td>
          <td>${item.quantity}</td>
          <td>${item.price}</td>
          <td>${(item.quantity * item.price).toFixed(2)}</td>
        </tr>
      `;
    });
  } else {
    printContent += `
      <tr>
        <td colspan="4">No items found in this order</td>
      </tr>
    `;
  }
  
  printContent += `
          </tbody>
        </table>
        <p><strong>Total Amount:</strong> ${order.total_amount}</p>
      </div>
    </body>
    </html>
  `;
  
  printWindow.document.open();
  printWindow.document.write(printContent);
  printWindow.document.close();
  
  setTimeout(() => {
    printWindow.print();
  }, 500);
};

onMounted(fetchOrders);
</script>
<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Orders Management</h1>

    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center my-12">
      <div class="loader animate-spin h-12 w-12 border-4 border-gray-300 rounded-full border-t-blue-600"/>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 p-4 rounded-lg mb-6">
      <p class="text-red-700">{{ error }}</p>
      <button class="mt-2 text-blue-600 hover:text-blue-800" @click="fetchOrders">Try again</button>
    </div>

    <!-- Empty state -->
    <div v-else-if="orders.length === 0" class="bg-gray-50 p-8 rounded-lg text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
      </svg>
      <h3 class="text-lg font-medium text-gray-900 mb-2">No orders found</h3>
      <p class="text-gray-500">Orders will appear here when customers make purchases.</p>
    </div>

    <!-- Orders Table -->
    <div v-else class="bg-white rounded-lg shadow overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Order #</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="order in orders" :key="order.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap font-medium">{{ order.order_number }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ order.user || 'Anonymous' }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ formatDate(order.created_at) }}</td>
            <td class="px-6 py-4 whitespace-nowrap">${{ order.total_amount }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="getStatusClass(order.status)" class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full">
                {{ order.status }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <button
                class="text-blue-600 hover:text-blue-900"
                @click="viewOrderDetails(order)"
              >
                View Details
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Order Details Modal -->
    <div v-if="selectedOrder" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">
            Order #{{ selectedOrder.order_number }}
          </h2>
          <button 
            class="text-gray-500 hover:text-gray-700" 
            @click="selectedOrder = null"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Order Information -->
            <div>
              <h3 class="font-medium text-gray-900 mb-2">Order Information</h3>
              <div class="bg-gray-50 p-4 rounded-lg">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <p class="text-sm text-gray-500">Order Date</p>
                    <p class="font-medium">{{ formatDate(selectedOrder.created_at) }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Total Amount</p>
                    <p class="font-medium">${{ selectedOrder.total_amount }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Payment Status</p>
                    <p class="font-medium">{{ selectedOrder.payment_status ? 'Paid' : 'Unpaid' }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Status</p>
                    <div class="mt-1">
                      <select
                        v-model="selectedOrder.status"
                        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
                        @change="updateOrderStatus(selectedOrder)"
                      >
                        <option v-for="status in orderStatuses" :key="status" :value="status">
                          {{ status }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Customer Information -->
            <div>
              <h3 class="font-medium text-gray-900 mb-2">Customer Information</h3>
              <div class="bg-gray-50 p-4 rounded-lg">
                <p class="font-medium">{{ selectedOrder.user || 'Anonymous' }}</p>
                <p class="text-sm text-gray-500 mt-2">Shipping Address</p>
                <p class="whitespace-pre-line">{{ selectedOrder.shipping_address }}</p>
              </div>
            </div>
          </div>

          <!-- Order Items -->
          <div>
            <h3 class="font-medium text-gray-900 mb-2">Order Items</h3>
            <div class="bg-gray-50 rounded-lg overflow-hidden border border-gray-200">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-100">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantity</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Price</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="!selectedOrder.items || selectedOrder.items.length === 0">
                    <td colspan="4" class="px-6 py-4 text-center text-gray-500">No items found in this order</td>
                  </tr>
                  <tr v-for="item in selectedOrder.items" :key="item.id" class="hover:bg-gray-50">
                    <td class="px-6 py-4">{{ item.product }}</td>
                    <td class="px-6 py-4">{{ item.quantity }}</td>
                    <td class="px-6 py-4">${{ item.price }}</td>
                    <td class="px-6 py-4">${{ (item.quantity * item.price).toFixed(2) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Order Actions -->
          <div class="flex justify-end space-x-3">
            <button
              class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200"
              @click="selectedOrder = null"
            >
              Close
            </button>
            <button
              v-if="isUpdatingOrderStatus"
              class="px-4 py-2 bg-blue-600 text-white rounded-md"
              disabled
            >
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              Updating...
            </button>
            <button
              v-else
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              @click="printOrderDetails"
            >
              Print
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped>
.loader {
  border-top-color: #3B82F6;
}
</style>