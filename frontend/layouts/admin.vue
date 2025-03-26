<script setup lang="ts">
import { useAuthStore } from '~/stores/useAuth';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

// Add loading state
const isLoading = ref(true);

const userName = ref('Admin User');
// Current route information
const currentRoute = computed(() => route.path);
const formattedRouteName = computed(() => {
  const parts = route.path.split('/');
  const lastPart = parts[parts.length - 1];
  return lastPart.charAt(0).toUpperCase() + lastPart.slice(1);
});

// Page title based on route
const pageTitle = computed(() => {
  const routeMap: Record<string, string> = {
    '/admin': 'Dashboard',
    '/admin/products': 'Product Management',
    '/admin/orders': 'Order Management',
    '/admin/support': 'Customer Support'
  };
  
  return routeMap[route.path] || 'Admin Panel';
});

const getActiveClass = (path: string) => {
  if (path === '/admin') {
    return route.path === path ? 'active bg-orange-600' : '';
  }
  return route.path.startsWith(path) ? 'active bg-gray-700' : '';
};

const logout = async () => {
  try {
    await authStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

// Improved auth check that runs immediately
const checkAuth = () => {
  isLoading.value = true;
  
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return false;
  }
  
  if (!authStore.isAdmin) {
    router.push('/');
    return false;
  }
  
  isLoading.value = false;
  return true;
};

onBeforeMount(() => {
  // Run immediately to prevent flash
  checkAuth();
});

// Double-check on mounted for extra security
onMounted(() => {
  checkAuth();
});

definePageMeta({
  middleware: ['auth']
});
</script>

<template>
  <div class="drawer lg:drawer-open min-h-screen bg-gray-100">
    <!-- Mobile drawer toggle -->
    <input id="admin-drawer" type="checkbox" class="drawer-toggle" >
    
    <!-- Page content -->
    <div class="drawer-content flex flex-col">
      <!-- Top header -->
      <header class="bg-white shadow sticky top-0 z-10">
        <div class="navbar px-4">
          <!-- Mobile menu button -->
          <div class="flex-none lg:hidden">
            <label for="admin-drawer" class="btn btn-square btn-ghost">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-6 h-6 stroke-current">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
            </label>
          </div>
          
          <!-- Title -->
          <div class="flex-1">
            <h2 class="text-xl font-semibold text-gray-800">{{ pageTitle }}</h2>
          </div>
          
          <!-- Logout button -->
          <div class="flex-none">
            <button class="btn btn-ghost text-red-600 hover:text-red-800" @click="logout">
              Logout
            </button>
          </div>
        </div>
        
        <!-- Breadcrumbs -->
        <div class="text-sm breadcrumbs px-4 py-2 bg-gray-50 border-t border-gray-200">
          <ul>
            <li><NuxtLink to="/admin">Admin</NuxtLink></li>
            <li v-if="currentRoute !== '/admin'">{{ formattedRouteName }}</li>
          </ul>
        </div>
      </header>

      <!-- Main content -->
      <main class="p-6 flex-grow">
        <slot />
      </main>
      
      <!-- Footer -->
      <footer class="footer footer-center p-4 bg-white text-base-content border-t">
        <div>
          <p>© {{ new Date().getFullYear() }} Resonance - All rights reserved</p>
        </div>
      </footer>
    </div>
    
    <!-- Sidebar -->
    <div class="drawer-side z-20">
      <label for="admin-drawer" class="drawer-overlay"/>
      <aside class="w-64 bg-slate-200 min-h-screen">
        <!-- Logo -->
        <div class="flex items-center justify-center h-16 bg-gray-900">
          <h1 class="text-white text-xl font-semibold">Resonance System</h1>
        </div>
        
        <!-- Navigation -->
        <nav class="mt-5">
          <ul class="menu menu-md p-0 [&_li>*]:rounded-none">
            <li>
              <NuxtLink to="/admin" :class="getActiveClass('/admin')" exact>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                Dashboard
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/admin/products" :class="getActiveClass('/admin/products')">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
                Products
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/admin/orders" :class="getActiveClass('/admin/orders')">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                Orders
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/admin/support" :class="getActiveClass('/admin/support')">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                Support
              </NuxtLink>
            </li>
          </ul>
        </nav>
        
        <!-- Logout button (mobile only) -->
        <div class="absolute bottom-0 w-full p-4 bg-gray-900 lg:hidden">
          <button class="btn btn-block btn-sm text-red-400 hover:text-red-300" @click="logout">
            Logout
          </button>
        </div>
      </aside>
    </div>
  </div>
</template>



<style scoped>
.loader {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #f97316;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>