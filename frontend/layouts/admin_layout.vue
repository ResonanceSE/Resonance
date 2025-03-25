<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="fixed inset-y-0 left-0 w-64 bg-gray-800">
      <div class="flex items-center justify-center h-16 bg-gray-900">
        <h1 class="text-white text-xl font-semibold">Resonance Admin</h1>
      </div>
      <nav class="mt-5">
        <NuxtLink
          to="/admin"
          class="flex items-center px-6 py-2 text-gray-100 hover:bg-gray-700"
        >
          <span class="mx-3">Dashboard</span>
        </NuxtLink>
        <NuxtLink
          to="/admin/products"
          class="flex items-center px-6 py-2 text-gray-100 hover:bg-gray-700"
        >
          <span class="mx-3">Products</span>
        </NuxtLink>
        <NuxtLink
          to="/admin/orders"
          class="flex items-center px-6 py-2 text-gray-100 hover:bg-gray-700"
        >
          <span class="mx-3">Orders</span>
        </NuxtLink>
        <NuxtLink
          to="/admin/support"
          class="flex items-center px-6 py-2 text-gray-100 hover:bg-gray-700"
        >
          <span class="mx-3">Support</span>
        </NuxtLink>
      </nav>
    </aside>

    <!-- Main content -->
    <div class="ml-64">
      <!-- Top header -->
      <header class="bg-white shadow">
        <div class="flex items-center justify-between px-4 py-4">
          <h2 class="text-xl font-semibold text-gray-800">Admin Panel</h2>
          <button @click="logout" class="text-red-600 hover:text-red-800">
            Logout
          </button>
        </div>
      </header>

      <!-- Page content -->
      <main class="p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'nuxt/app';
import { useAuthStore } from '~/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

// Middleware to check if user is admin
definePageMeta({
  middleware: 'admin'
});

const logout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script> 