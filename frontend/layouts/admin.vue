<script setup lang="ts">
import { useAuthStore } from '~/stores/useAuth';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const isLoading = ref(true);

const userName = computed(() => authStore.user?.username || 'Admin User');
const userEmail = computed(() => authStore.user?.email || 'admin@example.com');

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
    '/admin/manage_staff': 'Manage Staff',
  };

  return routeMap[route.path] || 'Admin Panel';
});

const getActiveClass = (path: string) => {
  if (path === '/admin') {
    return route.path === path ? 'active bg-primary text-primary-content' : '';
  }
  return route.path.startsWith(path) ? 'active bg-primary/10 text-primary' : '';
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
  checkAuth();
});

onMounted(() => {
  checkAuth();
});

definePageMeta({
  middleware: ['auth']
});
</script>

<template>
  <div class="drawer lg:drawer-open min-h-screen bg-base-100">
    <!-- Mobile drawer toggle -->
    <input id="admin-drawer" type="checkbox" class="drawer-toggle">
    <!-- Page content -->
    <div class="drawer-content flex flex-col">
      <!-- Top header -->
      <header class="bg-base-100 shadow sticky top-0 z-10">
        <div class="navbar px-4">
          <!-- Mobile menu button -->
          <div class="flex-none lg:hidden">
            <label for="admin-drawer" class="btn btn-square btn-ghost">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                class="inline-block w-6 h-6 stroke-current">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </label>
          </div>

          <!-- Title -->
          <div class="flex-1">
            <h2 class="text-xl font-semibold">{{ pageTitle }}</h2>
          </div>

          <!-- Logout button -->
        </div>

        <!-- Breadcrumbs -->
        <div class="text-sm breadcrumbs px-4 py-2 bg-base-200 border-t border-base-300">
          <ul>
            <li>
              <NuxtLink to="/admin">Admin</NuxtLink>
            </li>
            <li v-if="currentRoute !== '/admin'">{{ formattedRouteName }}</li>
          </ul>
        </div>
      </header>

      <!-- Main content -->
      <main class="p-6 flex-grow">
        <slot />
      </main>

      <!-- Footer -->
      <footer class="footer footer-center p-4 bg-base-100 text-base-content border-t">
        <div>
          <p>© {{ new Date().getFullYear() }} Resonance - All rights reserved</p>
        </div>
      </footer>
    </div>

    <div class="drawer-side z-20">
      <label for="admin-drawer" class="drawer-overlay" />
      <aside class="w-80 bg-gradient-to-b from-base-100 to-base-200 min-h-screen border-r border-base-300">
        <div
          class="relative h-24 bg-gradient-to-r from-primary to-secondary flex items-center justify-center overflow-hidden">
          <!-- Decorative circles -->
          <div class="absolute -left-6 -top-6 w-16 h-16 bg-primary/30 rounded-full blur-sm" />
          <div class="absolute right-12 bottom-4 w-8 h-8 bg-secondary/30 rounded-full blur-sm" />

          <!-- Logo -->
          <div class="relative z-10 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-white flex items-center justify-center shadow-lg">
              <span class="text-2xl font-bold text-primary">R</span>
            </div>
            <h1 class="text-white text-2xl font-bold tracking-wider">Resonance</h1>
          </div>
        </div>

        <!-- User profile section -->
        <div class="p-4 border-b border-base-300">
          <div class="flex items-center space-x-3">
            <div class="avatar placeholder">
              <div class="bg-neutral text-neutral-content rounded-full w-12">
                <span>{{ userName.charAt(0).toUpperCase() }}</span>
              </div>
            </div>
            <div>
              <div class="font-bold">{{ userName }}</div>
              <div class="text-xs opacity-70">{{ userEmail }}</div>
            </div>
          </div>
        </div>

        <!-- Navigation-->
        <div class="px-3 py-4">
          <div class="mb-2 px-4 text-xs font-semibold uppercase text-base-content/50">Navigation</div>
          <ul class="menu menu-md rounded-box w-full">
            <li>
              <NuxtLink to="/"
                class="flex items-center gap-3 font-medium hover:bg-base-300 transition-all duration-200">
                <div class="w-8 h-8 flex items-center justify-center rounded-lg bg-base-300/50">
                  <Icon name="heroicons:home" class="h-5 w-5" />
                </div>
                <span>Home Page</span>
              </NuxtLink>
            </li>
          </ul>

          <div class="divider">Management</div>

          <ul class="menu menu-md rounded-box w-full">
            <li>
              <NuxtLink to="/admin" :class="getActiveClass('/admin')"
                class="flex items-center gap-3 font-medium hover:bg-base-300 transition-all duration-200">
                <div class="w-8 h-8 flex items-center justify-center rounded-lg bg-base-300/50">
                  <Icon name="material-symbols:capture-outline" class="w-6 h-6 text-black" />
                </div>
                <span>Dashboard</span>
              </NuxtLink>
            </li>
            <li v-if="authStore.isSuperuser">
              <NuxtLink to="/admin/manage_staff" :class="getActiveClass('/admin/manage_staff')"
                class="flex items-center gap-3 font-medium hover:bg-base-300 transition-all duration-200">
                <div class="w-8 h-8 flex items-center justify-center rounded-lg bg-base-300/50">
                  <Icon name="heroicons:users" class="h-5 w-5" />
                </div>
                <span>Staffs</span>
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/admin/products" :class="getActiveClass('/admin/products')"
                class="flex items-center gap-3 font-medium hover:bg-base-300 transition-all duration-200">
                <div class="w-8 h-8 flex items-center justify-center rounded-lg bg-base-300/50">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                </div>
                <span>Products</span>
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/admin/orders" :class="getActiveClass('/admin/orders')"
                class="flex items-center gap-3 font-medium hover:bg-base-300 transition-all duration-200">
                <div class="w-8 h-8 flex items-center justify-center rounded-lg bg-base-300/50">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                  </svg>
                </div>
                <span>Orders</span>
              </NuxtLink>
            </li>
          </ul>

          <div class="divider">Others</div>

          <ul class="menu menu-md rounded-box w-full">
            <li>
              <button
                class="flex items-center gap-3 font-medium hover:bg-error/10 text-error hover:text-error transition-all duration-200"
                @click="logout">
                <div class="w-8 h-8 flex items-center justify-center rounded-lg bg-error/10">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                </div>
                <span>Logout</span>
              </button>
            </li>
          </ul>
        </div>

      </aside>
    </div>
  </div>
</template>

<style scoped>
.menu li .active {
  position: relative;
  font-weight: 600;
}

.menu li .active::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 60%;
  background-color: hsl(var(--p));
  border-radius: 0 4px 4px 0;
}

@keyframes pulse {
  0% {
    opacity: 0.6;
  }

  50% {
    opacity: 1;
  }

  100% {
    opacity: 0.6;
  }
}

.radial-progress {
  animation: pulse 2s infinite;
}
</style>