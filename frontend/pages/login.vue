<script setup>
const email = ref('');
const password = ref('');
const router = useRouter();

const handleLogin = () => {
  if (email.value && password.value) {
    console.log('Logging in:', email.value);
    router.push('/');
  }
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-8 grid place-items-center">
    <div class="relative w-full max-w-6xl rounded-3xl overflow-hidden shadow-xl bg-blue-50">
      <!-- Grid container -->
      <div class="grid grid-cols-1 md:grid-cols-12">
        
        <!-- Left side - Decorative content (7/12 columns on desktop) -->
        <div class="hidden md:block md:col-span-7 relative p-6 lg:p-16">
          <!-- Decorative shapes -->
          <div class="absolute right-0 top-1/4 w-32 h-32 bg-teal-500 rounded-l-full"/>
          <div class="absolute left-0 top-0 w-48 h-48 bg-teal-500 rounded-r-full"/>
          <div class="absolute right-16 bottom-40 w-16 h-16 bg-orange-500 rotate-45"/>
          <div class="absolute left-16 bottom-24 w-32 h-32 bg-pink-500 rounded-full"/>
          
          <!-- Main text -->
          <div class="z-10 absolute flex items-center justify-center">
            <h2 class="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
              Explore the world of sounds<br>
              ...at Resonance
            </h2>
          </div>
          
          <!-- Registration CTA -->
          <div class="absolute inset-0 flex flex-col items-center justify-center">
            <p class="text-gray-600 text-2xl mb-2 font-semibold">New to Resonance ?</p>
            <a href="#" class="btn btn-lg px-24 bg-orange-500 hover:bg-orange-600 text-white border-none rounded-lg shadow-sm">
              Register Here!
            </a>
          </div>
        </div>
        
        <!-- Right side-->
        <div class="col-span-1 md:col-span-5 bg-white p-8 md:p-12 rounded-3xl md:rounded-l-none">
          <!-- Grid layout for the vertical sections -->
          <div class="grid grid-rows-[auto_1fr_auto] gap-8 h-full">
            <!-- Header section -->
            <div>
              <div class="mb-8">
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-gray-800 mr-1"/>
                  <span class="font-semibold text-gray-800">Resonance</span>
                </div>
              </div>
              
              <div class="mb-10">
                <h1 class="text-2xl font-bold mb-1">
                  Welcome to
                </h1>
                <h1 class="text-2xl font-bold"><span class="text-blue-500">Resonance</span> Website</h1>
              </div>
            </div>
            
            <!-- Main form section -->
            <div class="grid gap-8">
              <!-- Input fields -->
              <div class="grid gap-4">
                <div>
                  <input 
                    v-model="email" 
                    type="email" 
                    placeholder="Email or Username" 
                    class="w-full px-4 py-3 rounded-md border border-gray-200 focus:outline-none focus:ring-1 focus:ring-gray-400"
                  >
                </div>
                <div>
                  <input 
                    v-model="password" 
                    type="password" 
                    placeholder="Password" 
                    class="w-full px-4 py-3 rounded-md border border-gray-200 focus:outline-none focus:ring-1 focus:ring-gray-400"
                  >
                </div>
                <div>
                  <button 
                    class="w-full py-3 bg-orange-500 hover:bg-orange-600 text-white font-medium rounded-md transition-colors" 
                    @click="handleLogin"
                  >
                    LOG IN
                  </button>
                </div>
              </div>
              
              <!-- Social login section -->
              <div class="grid gap-2">
                <div class="divider">Or login by</div>
                <div class="grid grid-cols-3 gap-4 place-items-center max-w-xs mx-auto">
                  <Icon name="logos:google-icon" class="h-10 w-10" aria-hidden="true"/>
                  <Icon name="logos:facebook" class="h-10 w-10" aria-hidden="true"/>
                  <Icon name="logos:x" class="h-10 w-10" aria-hidden="true"/>
                </div>
              </div>
            </div>
            
            <!-- Footer section -->
            <div class="grid place-items-center">
              <div class="flex space-x-6 text-sm">
                <a href="#" class="text-gray-600 hover:underline">Terms of Use</a>
                <a href="#" class="text-gray-600 hover:underline">Privacy policy</a>
              </div>
            </div>
            <div class="grid lg:hidden text-gray-600">
                <div class="flex flex-row gap-2 justify-center">
                  <span class="text-gray-600">New to Resonance?</span>
                    <NuxtLink class="link link-warning">Sign up here</NuxtLink>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* DaisyUI divider styling */
.divider {
  display: flex;
  align-items: center;
  text-align: center;
  font-weight: 500;
  color: #9ca3af;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background-color: #e5e7eb;
  margin: 0 1rem;
}
</style>