<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Dashboard</h1>
    
    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-gray-500 text-sm">Total Sales</h3>
        <p class="text-2xl font-semibold">${{ stats.total_sales }}</p>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-gray-500 text-sm">Total Orders</h3>
        <p class="text-2xl font-semibold">{{ stats.total_orders }}</p>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-gray-500 text-sm">Pending Orders</h3>
        <p class="text-2xl font-semibold">{{ stats.pending_orders }}</p>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-gray-500 text-sm">Low Stock Products</h3>
        <p class="text-2xl font-semibold">{{ stats.low_stock_products }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin'
});

interface Stats {
  total_sales: number;
  total_orders: number;
  pending_orders: number;
  low_stock_products: number;
}

const stats = ref<Stats>({
  total_sales: 0,
  total_orders: 0,
  pending_orders: 0,
  low_stock_products: 0
});

// Fetch stats on component mount
onMounted(async () => {
  try {
    const response = await fetch('/api/staff/stats/', {
      headers: {
        'Authorization': `Token ${useAuthStore().token}`
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      stats.value = data.data;
    }
  } catch (error) {
    console.error('Error fetching stats:', error);
  }
});
</script> 