<script setup lang="ts">
const navbar_left_placeholder = ref<string[]>([
  'Home',
  'Products',
  'Contact'
]);

const navbar_right_placeholder = ref<string[]>([
  "Log In",
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
    slug: "earphones",
    name: "Earphones",
    icon: "heroicons:musical-note"
  }
]);

// State management
const isMenuOpen = ref(false);
const cartCount = ref(2);


const route = useRoute();

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const closeMenu = () => {
  isMenuOpen.value = false;
};


const closeProductsDropdown = () => {
  // desktop dropdown
  const desktopDropdowns = document.querySelectorAll('.desktop-dropdown');
  desktopDropdowns.forEach(dropdown => {
    dropdown.removeAttribute('open');
  });
  
  // mobile dropdown
  const mobileDropdowns = document.querySelectorAll('.mobile-dropdown');
  mobileDropdowns.forEach(dropdown => {
    dropdown.removeAttribute('open');
  });
};

// Handle outside clicks for dropdowns
onMounted(() => {
  window.addEventListener('click', function(e) {
    document.querySelectorAll('.dropdown').forEach(function(dropdown) {
      const target = e.target as HTMLElement;
      
      if (!dropdown.contains(target)) {
        dropdown.removeAttribute('open');
      }
    });
  });
});


const shouldShowDropdown = (item: string): boolean => {
  return item === 'Products';
};


const isActive = (path: string): boolean => {
  if (path === '') {
    return route.path === '/';
  }
  return route.path.includes(path.toLowerCase());
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
        <div class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost btn-circle avatar">
            <div class="w-10 rounded-full bg-neutral-content flex items-center justify-center">
              <Icon name="heroicons:user-circle" class="h-10 w-10 text-neutral" />
            </div>
          </label>
          <ul tabindex="0" class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
            <li v-for="item in navbar_right_placeholder" :key="item">
              <NuxtLink to="/login">{{ item }}</NuxtLink>
            </li>
            <li><a>Settings</a></li>
            <li><a>Logout</a></li>
          </ul>
        </div>
          
        <!-- Cart -->
        <div class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost btn-circle">
            <div class="indicator">
              <Icon name="heroicons:shopping-cart" class="h-5 w-5" />
              <span class="badge badge-sm badge-primary indicator-item">{{ cartCount }}</span>
            </div>
          </label>
          <div tabindex="0" class="mt-3 card card-compact dropdown-content w-52 bg-base-100 shadow-lg z-[1]">
            <div class="card-body">
              <span class="font-bold text-lg">{{ cartCount }} Items</span>
              <span class="text-info">Subtotal: $999</span>
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
                      @click="() => { closeMenu(); closeProductsDropdown(); }"
                    >
                      <Icon :name="catalog_item.icon" class="h-5 w-5" />
                      {{ catalog_item.name }}
                    </NuxtLink>
                  </li>
                  <li>
                    <NuxtLink 
                      to="/products" 
                      @click="() => { closeMenu(); closeProductsDropdown(); }"
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
          <li v-for="item in navbar_right_placeholder" :key="item">
            <NuxtLink to="/login" class="flex items-center gap-2 py-2" @click="closeMenu">
              <Icon name="heroicons:user-circle" class="h-5 w-5" />
              {{ item }}
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/cart" class="flex items-center gap-2 py-2" @click="closeMenu">
              <Icon name="heroicons:shopping-cart" class="h-5 w-5" />
              Cart
              <span v-if="cartCount > 0" class="badge badge-sm badge-primary ml-2">{{ cartCount }}</span>
            </NuxtLink>
          </li>
          
          <!-- Contact Info in Mobile Menu -->
          <div class="mt-auto pt-6">
            <div class="text-sm opacity-50 mb-2">Contact Us</div>
            <a href="tel:+1234567890" class="flex items-center gap-2 py-1">
              <Icon name="heroicons:phone" class="h-4 w-4" />
              (123) 456-7890
            </a>
            <a href="mailto:info@resonance.com" class="flex items-center gap-2 py-1">
              <Icon name="heroicons:envelope" class="h-4 w-4" />
              info@resonance.com
            </a>
          </div>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>

.translate-x-full {
  transform: translateX(100%);
}

.translate-x-0 {
  transform: translateX(0);
}
</style>