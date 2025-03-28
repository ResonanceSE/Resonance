<script setup lang="ts">

import { useAuthStore } from '~/stores/useAuth';
import { useOrderStore } from '~/stores/useOrderStore';
import { definePageMeta } from '#imports'

// Set page layout
definePageMeta({
  layout: 'admin',
  middleware: ['auth']
});

interface Stats {
  total_sales: number;
  total_orders: number;
  pending_orders: number;
  low_stock_products: number;
}

// Initialize stores
const authStore = useAuthStore();
const orderStore = useOrderStore();

// State
const stats = ref<Stats>({
  total_sales: 0,
  total_orders: 0,
  pending_orders: 0,
  low_stock_products: 0
});
const loading = ref(true);
const error = ref<string | null>(null);
const config = useRuntimeConfig();
const apiUrl = config.public.apiUrl || 'http://localhost:8000';

// Fetch stats on component mount
const fetchStats = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    // Fetch orders first (this will populate orderStore.orders)
    await orderStore.fetchOrders();
    
    // Fetch additional stats that aren't in the order store
    const response = await fetch(`${apiUrl}/api/staff/stats/`, {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch stats: ${response.statusText}`);
    }
    
    const data = await response.json();
    if (data.status === 'success') {
      stats.value = data.data;
    } else {
      stats.value = data; // Fallback in case your API doesn't wrap in {status, data}
    }
  } catch (err) {
    console.error('Error fetching stats:', err);
    error.value = err instanceof Error ? err.message : 'Failed to load dashboard data';
  } finally {
    loading.value = false;
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

// Format status for display
const formatStatus = (status: string) => {
  return status.charAt(0).toUpperCase() + status.slice(1);
};

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

const getPercentage = (value: number, total: number) => {
  if (total === 0) return 0;
  return Math.round((value / total) * 100);
};

onMounted(fetchStats);
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 flex items-center">
    <Icon name="heroicons:user-circle" class="h-8 w-8 mr-3" />
    Welcome, <span class="text-orange-300 ml-2">{{ authStore.user?.username || 'Staff Member' }}</span>!
  </h1>
  <p class="text-slate-500 my-4">
    Admin Dashboard | Last login: {{ new Date().toLocaleDateString() }}
  </p>
    <div v-if="loading" class="flex justify-center my-8">
      <div class="loading loading-spinner loading-lg text-primary"/>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="alert alert-error shadow-lg mb-6">
      <div>
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <span>{{ error }}</span>
      </div>
      <div class="flex-none">
        <button class="btn btn-sm" @click="fetchStats">Try again</button>
      </div>
    </div>
    
    <!-- Stats Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-white p-6 rounded-lg shadow hover:shadow-md transition-all">
        <h3 class="text-gray-500 text-sm">Total Sales</h3>
        <p class="text-2xl font-semibold">${{ orderStore.totalSales.toFixed(2) }}</p>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow hover:shadow-md transition-all">
        <h3 class="text-gray-500 text-sm">Total Orders</h3>
        <p class="text-2xl font-semibold">{{ stats.total_orders }}</p>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow hover:shadow-md transition-all">
        <h3 class="text-gray-500 text-sm">Pending Orders</h3>
        <p class="text-2xl font-semibold">{{ orderStore.countByStatus.pending }}</p>
      </div>
    </div>
    
    <!-- Recent Orders Section -->
    <div class="mt-8">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Recent Orders</h2>
        <NuxtLink to="/admin/orders" class="btn btn-sm btn-outline">
          View All Orders
        </NuxtLink>
      </div>
      
      <div class="bg-white shadow rounded-lg overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="orderStore.recentOrders.length === 0">
              <td colspan="6" class="px-6 py-4 text-center text-gray-500">No recent orders</td>
            </tr>
            <tr v-for="order in orderStore.recentOrders" :key="order.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">{{ order.order_number }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ order.user }}</td>
              <td class="px-6 py-4 whitespace-nowrap">${{ order.total_amount }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getStatusClass(order.status)" class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full">
                  {{ formatStatus(order.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">{{ formatDate(order.created_at) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <NuxtLink :to="`/admin/orders/`" class="text-blue-600 hover:text-blue-900">
                  View
                </NuxtLink>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Quick Stats Cards -->
    <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Orders by Status -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-gray-800 font-medium mb-4">Orders by Status</h3>
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-sm">Pending</span>
            <div class="flex items-center">
              <span class="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full mr-2">
                {{ orderStore.countByStatus.pending }}
              </span>
              <div class="w-24 bg-gray-200 rounded-full h-2">
                <div
class="bg-yellow-500 h-2 rounded-full" 
                     :style="`width: ${getPercentage(orderStore.countByStatus.pending, stats.total_orders)}%`"/>
              </div>
            </div>
          </div>
          
          <div class="flex justify-between items-center">
            <span class="text-sm">Processing</span>
            <div class="flex items-center">
              <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mr-2">
                {{ orderStore.countByStatus.processing }}
              </span>
              <div class="w-24 bg-gray-200 rounded-full h-2">
                <div
class="bg-blue-500 h-2 rounded-full" 
                     :style="`width: ${getPercentage(orderStore.countByStatus.processing, stats.total_orders)}%`"/>
              </div>
            </div>
          </div>
          
          <div class="flex justify-between items-center">
            <span class="text-sm">Shipped</span>
            <div class="flex items-center">
              <span class="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded-full mr-2">
                {{ orderStore.countByStatus.shipped }}
              </span>
              <div class="w-24 bg-gray-200 rounded-full h-2">
                <div
class="bg-purple-500 h-2 rounded-full" 
                     :style="`width: ${getPercentage(orderStore.countByStatus.shipped, stats.total_orders)}%`"/>
              </div>
            </div>
          </div>
          
          <div class="flex justify-between items-center">
            <span class="text-sm">Delivered</span>
            <div class="flex items-center">
              <span class="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full mr-2">
                {{ orderStore.countByStatus.delivered }}
              </span>
              <div class="w-24 bg-gray-200 rounded-full h-2">
                <div
class="bg-green-500 h-2 rounded-full" 
                     :style="`width: ${getPercentage(orderStore.countByStatus.delivered, stats.total_orders)}%`"/>
              </div>
            </div>
          </div>
          
          <div class="flex justify-between items-center">
            <span class="text-sm">Cancelled</span>
            <div class="flex items-center">
              <span class="bg-red-100 text-red-800 text-xs px-2 py-1 rounded-full mr-2">
                {{ orderStore.countByStatus.cancelled }}
              </span>
              <div class="w-24 bg-gray-200 rounded-full h-2">
                <div
class="bg-red-500 h-2 rounded-full" 
                     :style="`width: ${getPercentage(orderStore.countByStatus.cancelled, stats.total_orders)}%`"/>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-gray-800 font-medium mb-4">Quick Actions</h3>
        <div class="space-y-2">
          <NuxtLink to="/admin/products" class="btn btn-outline btn-primary w-full justify-start">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
            Manage Products
          </NuxtLink>
          
          <NuxtLink to="/admin/orders" class="btn btn-outline btn-secondary w-full justify-start">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            View All Orders
          </NuxtLink>
        </div>
      </div>
      
      <!-- System Status -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-gray-800 font-medium mb-4">System Status</h3>
        
        <div class="space-y-4">
          <div>
            <div class="flex justify-between text-sm mb-1">
              <span>API Status</span>
              <span class="text-green-600">Operational</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div class="bg-green-500 h-2 rounded-full w-full"/>
            </div>
          </div>
          <div class="text-sm text-gray-500 mt-4">
            Last updated: {{ formatDate(new Date().toISOString()) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>