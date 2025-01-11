<script setup lang="ts">
import { ref } from 'vue'

const navbar_left_placeholder = ref<string[]>([
  'Home',
  'Catalog',
  'Products',
  'Contact'
])
const navbar_right_placeholder = ref<string[]>([
  "Log In",
])
const catalog_placeholder = ref<string[]>([
  'Headphones',
  'Speakers',
  'Earphones',
  'Accessories'
])

const isMenuOpen = ref(false)

const closeMenu = () => {
  isMenuOpen.value = false
}
</script>

<template>
  <div class="sticky top-0 z-50">
    <!-- Backdrop -->
    <div 
      v-if="isMenuOpen" 
      class="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden" 
      @click="closeMenu"
      />

    <div class="navbar bg-base-100 px-4 md:px-10 shadow-md">
      <!-- Logo Section -->
      <div class="flex-0">
        <NuxtLink to="/" class="text-2xl md:text-3xl font-semibold px-2 md:px-5">
          Resonance
        </NuxtLink>
      </div>

      <!-- Mobile Menu Button -->
      <div class="flex-1 justify-end lg:hidden">
        <button 
          class="btn btn-ghost btn-circle"
          aria-label="Toggle menu"
          @click="isMenuOpen = !isMenuOpen" 
        >
          <Icon 
            :name="isMenuOpen ? 'heroicons:x-mark' : 'heroicons:bars-3'" 
            class="h-6 w-6"
          />
        </button>
      </div>

      <!-- Desktop Navigation -->
      <div class="hidden lg:flex lg:flex-1 lg:justify-between lg:items-center">
        <!-- Left Menu Items -->
        <ul class="menu menu-horizontal px-1 text-lg">
          <li v-for="item in navbar_left_placeholder" :key="item">
            <div v-if="item === 'Catalog'" class="dropdown dropdown-hover dropdown-bottom">
              <label tabindex="0" class="cursor-pointer">
                <span class="flex items-center gap-1">
                  {{ item }}
                  <Icon name="heroicons:chevron-down" class="h-4 w-4" />
                </span>
              </label>
              <ul class="dropdown-content menu bg-base-100 rounded-box z-[1] w-52 p-2 shadow">
                <li v-for="catalog_item in catalog_placeholder" :key="catalog_item">
                  <NuxtLink class="text-base hover:bg-base-200">
                    {{ catalog_item }}
                  </NuxtLink>
                </li>
              </ul>
            </div>
            <NuxtLink v-else class="hover:bg-base-200">
              {{ item }}
            </NuxtLink>
          </li>
        </ul>

        <!-- Right Menu Items -->
        <div class="flex items-center gap-4">
          <ul class="menu menu-horizontal px-1">
            <li v-for="item in navbar_right_placeholder" :key="item">
              <NuxtLink class="text-lg hover:bg-base-200">
                {{ item }}
              </NuxtLink>
            </li>
          </ul>
          <NuxtLink class="btn btn-ghost btn-rectangle">
            <div class="indicator">
              <Icon name="heroicons:shopping-cart" class="h-6 w-6" />
              <span class="badge badge-sm indicator-item">0</span>
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- Mobile Sidebar Menu -->
    <div 
      class="fixed top-0 right-0 h-full w-80 bg-base-100 z-50 lg:hidden transform transition-transform duration-300 ease-in-out shadow-xl"
      :class="isMenuOpen ? 'translate-x-0' : 'translate-x-full'"
    >
      <!-- Sidebar Header -->
      <div class="p-4 border-b">
        <button 
          class="btn btn-ghost btn-circle float-right"
          @click="closeMenu"
        >
          <Icon name="heroicons:x-mark" class="h-6 w-6" />
        </button>
        <h2 class="text-xl font-semibold">Resonance</h2>
      </div>

      <!-- Sidebar Content -->
      <div class="overflow-y-auto h-[calc(100%-4rem)]">
        <div class="p-4 space-y-4">
          <!-- Mobile Menu Items -->
          <div class="space-y-2">
            <div v-for="item in navbar_left_placeholder" :key="item">
              <div v-if="item === 'Catalog'" class="collapse collapse-arrow">
                <input type="checkbox" />
                <div class="collapse-title text-xl font-medium">Catalog</div>
                <div class="collapse-content">
                  <ul class="menu">
                    <li v-for="catalog_item in catalog_placeholder" :key="catalog_item">
                      <NuxtLink class="text-lg" @click="closeMenu">
                        {{ catalog_item }}
                      </NuxtLink>
                    </li>
                  </ul>
                </div>
              </div>
              <NuxtLink 
                v-else
                class="block text-xl p-2 hover:bg-base-200 rounded-lg"
                @click="closeMenu"
              >
                {{ item }}
              </NuxtLink>
            </div>
          </div>

          <div class="divider"/>

          <!-- Mobile Right Menu Items -->
          <div class="space-y-2">
            <div v-for="item in navbar_right_placeholder" :key="item">
              <NuxtLink 
                class="block text-xl p-2 hover:bg-base-200 rounded-lg"
                @click="closeMenu"
        
              >
                {{ item }}
              </NuxtLink>
            </div>
            <NuxtLink 
              class="flex items-center gap-2 text-xl p-2 hover:bg-base-200 rounded-lg"
              @click="closeMenu"
            >
              <Icon name="heroicons:shopping-cart" class="h-6 w-6" />
              Cart
              <span class="badge badge-sm">0</span>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>