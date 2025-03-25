<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Orders Management</h1>

    <!-- Orders Table -->
    <div class="bg-white rounded-lg shadow overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Order #</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="order in orders" :key="order.id">
            <td class="px-6 py-4">{{ order.order_number }}</td>
            <td class="px-6 py-4">{{ formatDate(order.created_at) }}</td>
            <td class="px-6 py-4">${{ order.total_amount }}</td>
            <td class="px-6 py-4">
              <span :class="getStatusClass(order.status)">
                {{ order.status }}
              </span>
            </td>
            <td class="px-6 py-4">
              <button
                @click="viewOrderDetails(order)"
                class="text-blue-600 hover:text-blue-800"
              >
                View Details
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Order Details Modal -->
    <div v-if="selectedOrder" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg w-full max-w-2xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">
            Order #{{ selectedOrder.order_number }}
          </h2>
          <button @click="selectedOrder = null" class="text-gray-500 hover:text-gray-700">
            Close
          </button>
        </div>

        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <h3 class="font-medium text-gray-700">Order Status</h3>
              <select
                v-model="selectedOrder.status"
                @change="updateOrderStatus(selectedOrder)"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              >
                <option value="pending">Pending</option>
                <option value="processing">Processing</option>
                <option value="shipped">Shipped</option>
                <option value="delivered">Delivered</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div>
              <h3 class="font-medium text-gray-700">Order Date</h3>
              <p>{{ formatDate(selectedOrder.created_at) }}</p>
            </div>
          </div>

          <div>
            <h3 class="font-medium text-gray-700">Shipping Address</h3>
            <p>{{ selectedOrder.shipping_address }}</p>
          </div>

          <div>
            <h3 class="font-medium text-gray-700 mb-2">Order Items</h3>
            <div class="space-y-2">
              <div
                v-for="item in selectedOrder.items"
                :key="item.id"
                class="flex justify-between items-center"
              >
                <span>{{ item.product }} (x{{ item.quantity }})</span>
                <span>${{ item.price }}</span>
              </div>
            </div>
          </div>

          <div class="border-t pt-4">
            <div class="flex justify-between items-center font-medium">
              <span>Total Amount</span>
              <span>${{ selectedOrder.total_amount }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '~/stores/auth';

definePageMeta({
  layout: 'admin'
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
  status: string;
  total_amount: number;
  shipping_address: string;
  created_at: string;
  items: OrderItem[];
}

const orders = ref<Order[]>([]);
const selectedOrder = ref<Order | null>(null);

// Fetch orders
const fetchOrders = async () => {
  try {
    const response = await fetch('/api/staff/orders/', {
      headers: {
        'Authorization': `Token ${useAuthStore().token}`
      }
    });
    
    if (response.ok) {
      orders.value = await response.json();
    }
  } catch (error) {
    console.error('Error fetching orders:', error);
  }
};

// Update order status
const updateOrderStatus = async (order: Order) => {
  try {
    const response = await fetch(`/api/staff/orders/${order.id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${useAuthStore().token}`
      },
      body: JSON.stringify({ status: order.status })
    });
    
    if (response.ok) {
      await fetchOrders();
    }
  } catch (error) {
    console.error('Error updating order status:', error);
  }
};

// View order details
const viewOrderDetails = async (order: Order) => {
  try {
    const response = await fetch(`/api/staff/orders/${order.id}/`, {
      headers: {
        'Authorization': `Token ${useAuthStore().token}`
      }
    });
    
    if (response.ok) {
      selectedOrder.value = await response.json();
    }
  } catch (error) {
    console.error('Error fetching order details:', error);
  }
};

// Format date
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

// Get status class for styling
const getStatusClass = (status: string) => {
  const classes = {
    pending: 'text-yellow-600',
    processing: 'text-blue-600',
    shipped: 'text-purple-600',
    delivered: 'text-green-600',
    cancelled: 'text-red-600'
  };
  return classes[status as keyof typeof classes] || '';
};

onMounted(fetchOrders);
</script> 