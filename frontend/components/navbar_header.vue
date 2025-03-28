\<script setup lang="ts">
import { useAuthStore } from '~/stores/useAuth';

const navbar_left_placeholder = ref<string[]>([
  'Home',
  'Products',
  'Contact'
]);

const catalog_placeholder = reactive<{ slug: string; name: string; icon: string }[]>([
  {
    slug: "headphones",
    name: "Headphones",
    icon: "ic:baseline-headset"
  },
  {
    slug: "speakers",
    name: "Speakers",
    icon: "heroicons:speaker-wave"
  },
  {
    slug: "earbuds",
    name: "Earbuds",
    icon: "heroicons:musical-note"
  }
]);

interface CartItem {
  id: number;
  price: number;
  quantity: number;
}

const cartItems = ref<CartItem[]>([]);
const isMenuOpen = ref(false);
const cartCount = computed(() => {
  return cartItems.value.reduce((total, item) => total + item.quantity, 0);
});

const route = useRoute();
const router = useRouter();
const config = useRuntimeConfig();
const apiUrl = config.public.apiUrl || 'http://localhost:8000';

const authStore = useAuthStore();
const isLogin = computed(() => authStore.isLoggedIn);
const username = computed(() => authStore.user?.username || "User Log In");

const showLogoutModal = ref(false);
const isLoggingOut = ref(false);
const showLogoutSuccessModal = ref(false);

const loadCart = () => {
  try {
    const username = authStore.user?.username || 'guest';
    const cartData = localStorage.getItem(`cart_${username}`);
    
    if (cartData) {
      cartItems.value = JSON.parse(cartData);
    } else {
      cartItems.value = [];
    }
  } catch (error) {
    console.error('Error loading cart:', error);
    cartItems.value = [];
  }
};
watch(() => authStore.user?.username, (newUsername) => {
  if (newUsername) {
    loadCart();
  } else {
    cartItems.value = [];
  }
});

const subtotal = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + (item.price * item.quantity), 0);
});


const formatPrice = (price : number) => {
  const dollars = price / 100;
  return '$' + dollars.toFixed(2);
};

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const closeMenu = () => {
  isMenuOpen.value = false;
};

const shouldShowDropdown = (item: string): boolean => {
  return item === 'Products';
};

const isActive = (path: string): boolean => {
  if (path === '') {
    return route.path === '/';
  }
  return route.path.includes(path.toLowerCase());
};

const openLogoutModal = () => {
  showLogoutModal.value = true;
  closeMenu();
};

const closeProductsDropdown = () => {
  const desktopDropdowns = document.querySelectorAll('.desktop-dropdown');
  desktopDropdowns.forEach(dropdown => {
    dropdown.removeAttribute('open');
  });
  
  const mobileDropdowns = document.querySelectorAll('.mobile-dropdown');
  mobileDropdowns.forEach(dropdown => {
    dropdown.removeAttribute('open');
  });
};

onMounted(() => {
  loadCart();
  
  window.addEventListener('click', function(e) {
    document.querySelectorAll('.dropdown').forEach(function(dropdown) {
      const target = e.target as HTMLElement;
      
      if (!dropdown.contains(target)) {
        dropdown.removeAttribute('open');
      }
    });
  });
  
  window.addEventListener('storage', (event) => {
    if (event.key === 'cart') {
      loadCart();
    }
  });
});

watch(() => authStore.isLoggedIn, (newValue) => {
  loadCart();
});

const closeLogoutModal = () => {
  showLogoutModal.value = false;
};

const handleLogout = async () => {
  try {
    isLoggingOut.value = true;
    
    showLogoutModal.value = false;
    await new Promise(resolve => setTimeout(resolve, 300));
    
    await authStore.logout();
  
    showLogoutSuccessModal.value = true;
    setTimeout(() => {
      showLogoutSuccessModal.value = false;
      
      setTimeout(() => {
        router.push('/');
      }, 300);
    }, 1500);
  } catch (error) {
    console.error('Logout failed:', error);
  } finally {
    isLoggingOut.value = false;
  }
};
</script>

<template>
  <div class="sticky top-0 z-50">
    <!-- Backdrop for mobile menu -->
    <div 
      v-if="isMenuOpen" 
      class="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden" 
      @click="closeMenu"
    />
    
    <!-- Main Navbar -->
    <div class="navbar bg-base-100 shadow-md">
      <!-- Logo Section -->
      <div class="flex flex-grow lg:flex-grow-0">
        <NuxtLink to="/" class="text-2xl md:text-3xl font-semibold px-2 md:px-5">
          <span class="text-primary hidden sm:inline">♪</span> Resonance
        </NuxtLink>
      </div>
      
      <!-- Desktop Navigation -->
      <div class="hidden lg:flex flex-1 lg:min-w-screen">
        <div class="flex">
          <ul class="menu menu-horizontal px-1 text-lg items-center">
            <li v-for="item in navbar_left_placeholder" :key="item">
              <!-- Products Dropdown -->
              <details 
                v-if="shouldShowDropdown(item)" 
                class="dropdown dropdown-bottom desktop-dropdown"
              >
                <summary
                  class="m-1 btn btn-ghost items-center"
                  :class="isActive(item === 'Home' ? '' : item.toLowerCase()) ? 'bg-orange-400 text-white border-orange-500' : ''">
                  <div class="my-auto py-2">{{ item }}</div>
                </summary>
                <ul class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52 mt-4">
                  <li v-for="catalog_item in catalog_placeholder" :key="catalog_item.slug">
                    <NuxtLink 
                      :to="`/products/${catalog_item.slug}`"
                      @click="closeProductsDropdown"
                    >
                      <Icon :name="catalog_item.icon" class="h-5 w-5" />
                      {{ catalog_item.name }}
                    </NuxtLink>
                  </li>
                  <div class="divider my-0"/>
                  <li>
                    <NuxtLink 
                      to="/products"
                      @click="closeProductsDropdown"
                    >
                      <Icon name="heroicons:squares-2x2" class="h-5 w-5" />
                      All Categories
                    </NuxtLink>
                  </li>
                </ul>
              </details>
          
              <!-- Other Menu Items -->
              <NuxtLink
                v-else
                class="m-1 btn btn-ghost"
                :class="isActive(item === 'Home' ? '' : item.toLowerCase()) ? 'bg-orange-400 text-white border-orange-500' : ''"
                :to="`/${item !== 'Home' ? item.toLowerCase() : ''}`"
              >
                {{ item }}
              </NuxtLink>
            </li>
          </ul>
        </div>
      </div>
        
      <!-- Desktop Right Menu -->
      <div class="hidden lg:flex gap-2 ml-2">
        <!-- User Menu -->
        <div v-if="isLogin" class="text-neutral">{{ username }}</div>
        <div class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost btn-circle avatar">
            <div class="w-10 rounded-full bg-neutral-content flex items-center justify-center">
              <Icon name="heroicons:user-circle" class="h-10 w-10 text-neutral" />
            </div>
          </label>
          <ul tabindex="0" class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
            <li v-if="!isLogin"><NuxtLink to="/login">Log In</NuxtLink></li>
            <li v-if="isLogin"><a>Settings</a></li>
            <li v-if="isLogin"><a @click="openLogoutModal">Logout</a></li>
          </ul>
        </div>
          
        <!-- Cart -->
        <div class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost btn-circle">
            <div class="indicator">
              <Icon name="heroicons:shopping-cart" class="h-5 w-5" />
              <span v-if="cartCount > 0" class="badge badge-sm badge-primary indicator-item">{{ cartCount }}</span>
            </div>
          </label>
          <div tabindex="0" class="mt-3 card card-compact dropdown-content w-52 bg-base-100 shadow-lg z-[1]">
            <div class="card-body">
              <span class="font-bold text-lg">{{ cartCount }} Item{{ cartCount !== 1 ? 's' : '' }}</span>
              <span class="text-info">Subtotal: {{ formatPrice(subtotal) }}</span>
              <div class="card-actions">
                <NuxtLink to="/cart" class="btn btn-primary btn-block">View cart</NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Mobile Controls -->
      <div class="flex lg:hidden gap-2">
        <!-- Mobile Cart Button -->
        <NuxtLink to="/cart" class="btn btn-ghost btn-circle">
          <div class="indicator">
            <Icon name="heroicons:shopping-cart" class="h-5 w-5" />
            <span v-if="cartCount > 0" class="badge badge-sm badge-primary indicator-item">{{ cartCount }}</span>
          </div>
        </NuxtLink>
        
        <!-- Mobile Menu Toggle -->
        <button class="btn btn-ghost btn-circle" @click="toggleMenu">
          <Icon name="heroicons:bars-3" class="h-5 w-5" />
        </button>
      </div>
    </div>
    
    <!-- Mobile Sidebar Menu -->
    <div
      class="fixed top-0 right-0 h-full w-80 bg-base-100 z-50 lg:hidden transform transition-transform duration-300 ease-in-out shadow-xl"
      :class="isMenuOpen ? 'translate-x-0' : 'translate-x-full'"
    >
      <!-- Sidebar Header -->
      <div class="flex justify-between items-center p-4 border-b">
        <h2 class="text-xl font-semibold">Resonance</h2>
        <button class="btn btn-sm btn-circle btn-ghost" @click="closeMenu">
          <Icon name="heroicons:x-mark" class="h-5 w-5" />
        </button>
      </div>
      
      <!-- Sidebar Content -->
      <div class="overflow-y-auto h-[calc(100%-4rem)]">
        <ul class="menu p-4 text-base-content">
          <!-- Mobile Menu Items -->
          <li v-for="item in navbar_left_placeholder" :key="item">
            <!-- Products in Mobile -->
            <details 
              v-if="shouldShowDropdown(item)" 
              class="collapse collapse-arrow bg-base-200 rounded-box mobile-dropdown"
            >
              <summary class="collapse-title flex flex-row items-center gap-2">
                <div class="flex items-center space-x-2">
                  <Icon name="heroicons:shopping-bag" class="h-5 w-5" />
                  <span class="text-center items-center">{{ item }} </span>
                </div>
              </summary>
              <div class="collapse-content">
                <ul class="menu menu-sm">
                  <li v-for="catalog_item in catalog_placeholder" :key="catalog_item.slug">
                    <NuxtLink 
                      :to="`/products/${catalog_item.slug}`" 
                      @click="closeMenu"
                    >
                      <Icon :name="catalog_item.icon" class="h-5 w-5" />
                      {{ catalog_item.name }}
                    </NuxtLink>
                  </li>
                  <li>
                    <NuxtLink 
                      to="/products" 
                      @click="closeMenu"
                    >
                      <Icon name="heroicons:squares-2x2" class="h-5 w-5" />
                      All Categories
                    </NuxtLink>
                  </li>
                </ul>
              </div>
            </details>
            
            <!-- Other Menu Items -->
            <NuxtLink
              v-else
              :to="`/${item !== 'Home' ? item.toLowerCase() : ''}`" 
              class="flex items-center gap-2 my-2 py-2"
              @click="closeMenu"
            >
              <Icon 
                :name="
                  item === 'Home' ? 'heroicons:home' : 
                  item === 'Contact' ? 'heroicons:envelope' : 'heroicons:document-text'
                " 
                class="h-5 w-5" 
              />
              {{ item }}
            </NuxtLink>
          </li>
          
          <div class="divider">Account</div>
          
          <!-- Mobile Account Items -->
          <li v-if="!isLogin">
            <NuxtLink to="/login" class="flex items-center gap-2 py-2" @click="closeMenu">
              <Icon name="heroicons:user-circle" class="h-5 w-5" />
              Log In
            </NuxtLink>
          </li>
          <li v-if="isLogin">
            <a class="flex items-center gap-2 py-2" @click="openLogoutModal">
              <Icon name="heroicons:arrow-right-on-rectangle" class="h-5 w-5" />
              Logout
            </a>
          </li>
          <li>
            <NuxtLink to="/cart" class="flex items-center gap-2 py-2" @click="closeMenu">
              <Icon name="heroicons:shopping-cart" class="h-5 w-5" />
              Cart
              <span v-if="cartCount > 0" class="badge badge-sm badge-primary ml-2">{{ cartCount }}</span>
            </NuxtLink>
          </li>
        </ul>
      </div>
    </div>
    
    <!-- Logout Confirmation Modal -->
    <div v-if="showLogoutModal" class="fixed inset-0 flex items-center justify-center z-50">
      <div
class="absolute inset-0 bg-black bg-opacity-50 transition-opacity duration-200" 
           @click="closeLogoutModal"/>
      
      <div class="bg-white rounded-lg shadow-xl w-80 p-6 transform transition-all duration-300 scale-100 opacity-100">
        <div class="text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-orange-100 mb-4">
            <Icon name="heroicons:question-mark-circle" class="h-6 w-6 text-orange-600" />
          </div>
          
          <h3 class="text-lg font-medium text-gray-900 mb-4">Confirm Logout</h3>
          
          <p class="text-sm text-gray-500 mb-6">
            Are you sure you want to logout of your account?
          </p>
          
          <div class="flex justify-between gap-4">
            <button 
              class="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
              @click="closeLogoutModal"
            >
              Cancel
            </button>
            <button 
              class="flex-1 px-4 py-2 text-sm font-medium text-white bg-orange-600 rounded-md hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
              :disabled="isLoggingOut"
              @click="handleLogout"
            >
              <span v-if="isLoggingOut" class="flex items-center justify-center">
                <span class="spinner-white mr-2"/>
                <span>Logging Out...</span>
              </span>
              <span v-else>Yes, Logout</span>
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Logout Success Modal -->
    <LogoutModal :show="showLogoutSuccessModal" />
  </div>
</template>

<style scoped>
.translate-x-full {
  transform: translateX(100%);
}

.translate-x-0 {
  transform: translateX(0);
}

.spinner-white {
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>