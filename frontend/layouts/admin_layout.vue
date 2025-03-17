<script setup>

const isDrawerOpen = ref(false);

const route = useRoute();
const pageTitle = computed(() => {
  const path = route.path;
  if (path === '/admin') return 'Dashboard';
  if (path.includes('/analytics')) return 'Analytics';
  if (path.includes('/users')) return 'User Management';
  if (path.includes('/products')) return 'Products';
  if (path.includes('/orders')) return 'Orders';
  if (path.includes('/settings')) return 'Settings';
  return 'Admin Dashboard';
});

const mainMenuItems = [
  { 
    title: 'Dashboard', 
    path: '/admin', 
    icon: 'dashboard'
  },
  { 
    title: 'Analytics', 
    path: '/admin/analytics', 
    icon: 'analytics'
  },
  { 
    title: 'Users', 
    path: '/admin/users', 
    icon: 'users'
  },
  { 
    title: 'Products', 
    path: '/admin/products', 
    icon: 'products'
// Menu items with simple icon identifiers instead of component references
  },
  { 
    title: 'Orders', 
    path: '/admin/orders', 
    icon: 'orders'
  }
];

const settingsMenuItems = [
  { 
    title: 'General', 
    path: '/admin/settings/general', 
    icon: 'settings'
  },
  { 
    title: 'Appearance', 
    path: '/admin/settings/appearance', 
    icon: 'theme'
  },
  { 
    title: 'Security', 
    path: '/admin/settings/security', 
    icon: 'security'
  }
];
</script>


<template>
    <div class="drawer lg:drawer-open">
      <input id="admin-drawer" v-model="isDrawerOpen" type="checkbox" class="drawer-toggle" >
      
      <div class="drawer-content flex flex-col">
        <!-- Navbar -->
        <div class="navbar bg-base-100 border-b border-base-200 shadow-sm">
          <div class="flex-none">
            <label for="admin-drawer" class="btn btn-square btn-ghost drawer-button lg:hidden">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-5 h-5 stroke-current">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
            </label>
          </div>
          <div class="flex-1">
            <p class="text-xl font-bold">{{ pageTitle }}</p>
          </div>
          <div class="flex-none gap-2">
            <div class="form-control">
              <input type="text" placeholder="Search..." class="input input-bordered w-24 md:w-auto" >
            </div>
            <div class="dropdown dropdown-end">
              <label tabindex="0" class="btn btn-ghost btn-circle avatar">
                <div class="w-10 rounded-full">
                  <img src="https://daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg" >
                </div>
              </label>
              <ul tabindex="0" class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
                <li>
                  <a class="justify-between">
                    Profile
                    <span class="badge">New</span>
                  </a>
                </li>
                <li><a>Settings</a></li>
                <li><a>Logout</a></li>
              </ul>
            </div>
          </div>
        </div>
        
        <main class="flex-1 overflow-y-auto p-4 md:p-6 bg-base-200">
          <slot />
        </main>
        
        <!-- Footer -->
        <footer class="footer footer-center p-4 bg-base-100 text-base-content border-t border-base-200">
          <div>
            <p>Copyright © {{ new Date().getFullYear() }} - All right reserved</p>
          </div>
        </footer>
      </div>
      
      <!-- Sidebar -->
      <div class="drawer-side">
        <label for="admin-drawer" aria-label="close sidebar" class="drawer-overlay"/>
        <aside class="bg-base-100 w-64 min-h-full border-r border-base-200">
          <!-- Logo area -->
          <div class="p-4 flex items-center border-b border-base-200 h-16">
            <h1 class="text-xl font-bold">Admin Dashboard</h1>
          </div>
          
          <!-- Menu items -->
          <ul class="menu p-4 pt-2 text-base-content">
            <li class="font-semibold text-xs uppercase text-base-content/50 pb-2">Main</li>
            <li v-for="(item, index) in mainMenuItems" :key="index">
              <NuxtLink :to="item.path" class="flex items-center">
                <!-- Simply use the inline SVG icons -->
                <svg v-if="item.icon === 'dashboard'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                <svg v-if="item.icon === 'analytics'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <svg v-if="item.icon === 'users'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                <svg v-if="item.icon === 'products'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                <svg v-if="item.icon === 'orders'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                {{ item.title }}
              </NuxtLink>
            </li>
            
            <div class="divider my-2"/>
            
            <li class="font-semibold text-xs uppercase text-base-content/50 pb-2">Settings</li>
            <li v-for="(item, index) in settingsMenuItems" :key="index">
              <NuxtLink :to="item.path" class="flex items-center">
                <svg v-if="item.icon === 'settings'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <svg v-if="item.icon === 'theme'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                </svg>
                <svg v-if="item.icon === 'security'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                {{ item.title }}
              </NuxtLink>
            </li>
          </ul>
        </aside>
      </div>
    </div>
  </template>
