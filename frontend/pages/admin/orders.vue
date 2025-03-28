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
  user: string;
  id: number;
  order_number: string;
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

// Helper function to capitalize first letter
const capitalize = (str: string) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

// Get customer initials for avatar
const getInitials = (name: string) => {
  if (!name) return 'A';
  const parts = name.split(' ');
  if (parts.length === 1) return name.charAt(0).toUpperCase();
  return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
};

// Get badge class for status
const getBadgeClass = (status: string) => {
  switch (status.toLowerCase()) {
    case 'pending':
      return 'badge-warning';
    case 'processing':
      return 'badge-info';
    case 'shipped':
      return 'badge-secondary';
    case 'delivered':
      return 'badge-success';
    case 'cancelled':
      return 'badge-error';
    default:
      return 'badge-ghost';
  }
};

// Get select class for status dropdown
const getSelectClass = (status: string) => {
  switch (status.toLowerCase()) {
    case 'pending':
      return 'select-warning';
    case 'processing':
      return 'select-info';
    case 'shipped':
      return 'select-secondary';
    case 'delivered':
      return 'select-success';
    case 'cancelled':
      return 'select-error';
    default:
      return '';
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
        .header { display: flex; justify-content: space-between; align-items: center; }
        .logo { font-weight: bold; font-size: 24px; color: #f97316; }
        .order-id { font-size: 18px; }
        .footer { margin-top: 50px; text-align: center; font-size: 12px; color: #666; }
      </style>
    </head>
    <body>
      <div class="header">
        <div class="logo">Resonance</div>
        <div class="order-id">Order #${order.order_number}</div>
      </div>
      
      <div class="section">
        <h2>Order Information</h2>
        <p><strong>Date:</strong> ${formatDate(order.created_at)}</p>
        <p><strong>Status:</strong> ${capitalize(order.status)}</p>
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
              <th style="text-align: center;">Quantity</th>
              <th style="text-align: right;">Price</th>
              <th style="text-align: right;">Total</th>
            </tr>
          </thead>
          <tbody>
  `;
  
  if (order.items && order.items.length > 0) {
    order.items.forEach(item => {
      const itemTotal = (item.quantity * item.price).toFixed(2);
      printContent += `
        <tr>
          <td>${item.product}</td>
          <td style="text-align: center;">${item.quantity}</td>
          <td style="text-align: right;">$${item.price}</td>
          <td style="text-align: right;">$${itemTotal}</td>
        </tr>
      `;
    });
  } else {
    printContent += `
      <tr>
        <td colspan="4" style="text-align: center;">No items found in this order</td>
      </tr>
    `;
  }
  
  printContent += `
          </tbody>
          <tfoot>
            <tr>
              <td colspan="3" style="text-align: right; font-weight: bold;">Total:</td>
              <td style="text-align: right; font-weight: bold;">$${order.total_amount}</td>
            </tr>
          </tfoot>
        </table>
      </div>
      
      <div class="footer">
        <p>Thank you for your order! If you have any questions, please contact us at support@resonance.com</p>
        <p>© ${new Date().getFullYear()} Resonance - All rights reserved</p>
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
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mr-3 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
      </svg>
      Orders Management
    </h1>

    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center my-12">
      <div class="loading loading-spinner loading-lg text-primary"/>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="alert alert-error mb-6">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <div>
        <h3 class="font-bold">Error</h3>
        <div class="text-sm">{{ error }}</div>
      </div>
      <button class="btn btn-sm" @click="fetchOrders">Try again</button>
    </div>

    <!-- Empty state -->
    <div v-else-if="orders.length === 0" class="card bg-base-100 shadow-lg p-8 text-center">
      <div class="card-body items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
        <h3 class="text-xl font-bold mb-2">No orders found</h3>
        <p class="text-gray-500">Orders will appear here when customers make purchases.</p>
      </div>
    </div>

    <!-- Orders Table -->
    <div v-else class="card bg-base-100 shadow-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="table table-zebra w-full">
          <thead>
            <tr>
              <th>Order #</th>
              <th>Customer</th>
              <th>Date</th>
              <th>Total</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.id" class="hover">
              <td class="font-medium">{{ order.order_number }}</td>
              <td>{{ order.user || 'Anonymous' }}</td>
              <td>{{ formatDate(order.created_at) }}</td>
              <td>${{ order.total_amount }}</td>
              <td>
                <div :class="getBadgeClass(order.status)" class="badge">
                  {{ capitalize(order.status) }}
                </div>
              </td>
              <td>
                <button
                  class="btn btn-sm btn-outline btn-info"
                  @click="viewOrderDetails(order)"
                >
                  View Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Order Details Modal -->
    <div v-if="selectedOrder" class="modal modal-open">
      <div class="modal-box max-w-3xl">
        <div class="flex justify-between items-center mb-6">
          <h3 class="font-bold text-xl flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            Order #{{ selectedOrder.order_number }}
          </h3>
          <button class="btn btn-sm btn-circle" @click="selectedOrder = null">✕</button>
        </div>

        <div class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Order Information -->
            <div>
              <h3 class="font-medium text-gray-900 mb-2 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Order Information
              </h3>
              <div class="card bg-base-200 shadow-sm">
                <div class="card-body p-4">
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <p class="text-sm opacity-70">Order Date</p>
                      <p class="font-medium">{{ formatDate(selectedOrder.created_at) }}</p>
                    </div>
                    <div>
                      <p class="text-sm opacity-70">Total Amount</p>
                      <p class="font-medium text-primary">${{ selectedOrder.total_amount }}</p>
                    </div>
                    <div>
                      <p class="text-sm opacity-70">Payment Status</p>
                      <div class="badge mt-1" :class="selectedOrder.payment_status ? 'badge-success' : 'badge-warning'">
                        {{ selectedOrder.payment_status ? 'Paid' : 'Unpaid' }}
                      </div>
                    </div>
                    <div>
                      <p class="text-sm opacity-70">Status</p>
                      <div class="mt-1">
                        <select
                          v-model="selectedOrder.status"
                          class="select select-bordered select-sm w-full"
                          :class="getSelectClass(selectedOrder.status)"
                          @change="updateOrderStatus(selectedOrder)"
                        >
                          <option v-for="status in orderStatuses" :key="status" :value="status">
                            {{ capitalize(status) }}
                          </option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Customer Information -->
            <div>
              <h3 class="font-medium text-gray-900 mb-2 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                Customer Information
              </h3>
              <div class="card bg-base-200 shadow-sm">
                <div class="card-body p-4">
                  <div class="flex items-center mb-3">
                    <div class="avatar placeholder mr-3">
                      <div class="bg-neutral-focus text-neutral-content rounded-full w-8">
                        <span>{{ getInitials(selectedOrder.user) }}</span>
                      </div>
                    </div>
                    <div>
                      <p class="font-medium">{{ selectedOrder.user || 'Anonymous Customer' }}</p>
                    </div>
                  </div>
                  <div>
                    <p class="text-sm opacity-70 mb-1">Shipping Address</p>
                    <div class="p-3 bg-base-100 rounded-md">
                      <p class="whitespace-pre-line text-sm">{{ selectedOrder.shipping_address }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Order Items -->
          <div>
            <h3 class="font-medium text-gray-900 mb-2 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
              Order Items
            </h3>
            <div class="card bg-base-200 shadow-sm overflow-hidden">
              <div class="overflow-x-auto">
                <table class="table table-compact w-full">
                  <thead>
                    <tr>
                      <th>Product</th>
                      <th class="text-center">Quantity</th>
                      <th class="text-right">Price</th>
                      <th class="text-right">Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="!selectedOrder.items || selectedOrder.items.length === 0">
                      <td colspan="4" class="text-center py-4 text-gray-500">No items found in this order</td>
                    </tr>
                    <tr v-for="item in selectedOrder.items" :key="item.id" class="hover">
                      <td class="font-medium">{{ item.product }}</td>
                      <td class="text-center">{{ item.quantity }}</td>
                      <td class="text-right">${{ item.price }}</td>
                      <td class="text-right font-medium">${{ (item.quantity * item.price).toFixed(2) }}</td>
                    </tr>
                  </tbody>
                  <tfoot>
                    <tr>
                      <td colspan="3" class="text-right font-bold">Total:</td>
                      <td class="text-right font-bold">${{ selectedOrder.total_amount }}</td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>
          </div>

          <!-- Order Actions -->
          <div class="modal-action border-t pt-4">
            <button
              class="btn btn-outline"
              @click="selectedOrder = null"
            >
              Close
            </button>
            <button
              v-if="isUpdatingOrderStatus"
              class="btn btn-primary"
              disabled
            >
              <span class="loading loading-spinner loading-xs mr-2"/>
              Updating...
            </button>
            <button
              v-else
              class="btn btn-primary"
              @click="printOrderDetails"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Print Order
            </button>
          </div>
        </div>
      </div>
      <label class="modal-backdrop" @click="selectedOrder = null"/>
    </div>
  </div>
</template>