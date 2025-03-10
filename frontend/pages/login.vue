<script setup >

import { login } from '~/services/authService';

definePageMeta({
  layout: 'false'
})


const username_or_email = ref('')
const password = ref('');
const router = useRouter();
const passwordVisible = ref(false);
const errorMessage = ref('');
const formSubmitted = ref(false);



const handleLogin = async () => {
  formSubmitted.value = true;
  errorMessage.value = '';
  console.log('Form submitted:', { username_or_email: username_or_email.value, password: password.value });
  const credentials = { username : username_or_email.value, password: password.value };
  try {
    await login(credentials);
    console.log('Logging in:', username_or_email.value);
    router.push('/');
  } catch (error) {
    errorMessage.value = error.message || 'Login failed';
    console.error('Login error:', error);
  } finally {
    console.log("Log in attempted")
  }
};
const togglePasswordVisibility = () => {
  passwordVisible.value = !passwordVisible.value;
};

</script>

<template>
  <!-- Adding decorative background elements without SVG -->
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12 relative overflow-hidden">
    <!-- Decorative circles using CSS only -->
    <div class="absolute top-20 left-10 w-64 h-64 bg-orange-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"></div>
    <div class="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"></div>
    <div class="absolute -bottom-8 left-40 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000"></div>
    
    <div class="relative top-[50%] w-full max-w-6xl m-auto rounded-3xl overflow-hidden shadow-2xl bg-white/80 backdrop-blur-sm">
      <!-- Grid container -->
      <div class="grid grid-cols-1 md:grid-cols-12">
        
        <!-- Left side - Decorative content (7/12 columns on desktop) -->
        <div class="hidden md:block md:col-span-7 relative p-6 lg:p-16 bg-gradient-to-br from-blue-500 to-indigo-600">
          <!-- Decorative shapes with enhanced styling -->
          <div class="absolute right-0 top-1/4 w-32 h-32 bg-teal-400 rounded-l-full opacity-75 animate-pulse"></div>
          <div class="absolute left-0 top-0 w-40 h-48 bg-teal-500 rounded-r-full opacity-75 animate-float"></div>
          <div class="absolute right-16 bottom-40 w-16 h-16 bg-orange-400 rotate-45 animate-spin-slow"></div>
          <div class="absolute left-16 bottom-24 w-32 h-32 bg-pink-400 rounded-full opacity-75 animate-float-delay"></div>
          
          <!-- Enhanced main text with better contrast -->
          <div class="z-10 absolute top-20 right-8 lg:right-16">
            <h2 class="text-2xl md:text-3xl lg:text-4xl font-bold leading-tight text-right text-white drop-shadow-md">
              Explore the world of sounds<br>
              <span class="text-orange-300">...at Resonance</span>
            </h2>
          </div>
          
          <!-- Registration CTA with improved styling -->
          <div class="absolute inset-0 flex flex-col items-center justify-center">
            <p class="text-white text-2xl mb-6 font-semibold drop-shadow-md">New to Resonance?</p>
            <NuxtLink 
              to="/register"
              class="px-8 py-3 bg-white hover:bg-orange-50 text-orange-600 font-medium border-none rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-0.5 active:translate-y-0 duration-150"
            >
              <div class="flex items-center justify-center gap-2">
                <span class="text-lg">Register Here!</span>
                <!-- Arrow using CSS triangle instead of SVG -->
                <div class="arrow-right"></div>
              </div>
            </NuxtLink>
          </div>
          
          <!-- Decorative wave pattern using pure CSS instead of SVG -->
          <div class="absolute bottom-0 left-0 right-0 h-24 overflow-hidden">
            <div class="wave"></div>
          </div>
        </div>
        
        <!-- Right side with enhanced styling -->
        <div class="col-span-1 md:col-span-5 p-8 md:p-12 rounded-3xl md:rounded-l-none">
          <!-- Absolute positioned decorative element -->
          <div class="absolute right-0 top-0 h-2 w-full md:w-1/3 bg-gradient-to-r from-orange-400 to-orange-500"></div>
          
          <!-- Grid layout for the vertical sections -->
          <div class="grid grid-rows-[auto_1fr_auto] gap-8 h-full">
            <!-- Enhanced header section -->
            <div>
              <div class="mb-8">
                <div class="flex items-center">
                  <div class="w-5 h-5 bg-gradient-to-r from-blue-500 to-purple-500 rounded-md mr-2"></div>
                  <span class="font-semibold text-gray-800 text-lg tracking-wide">Resonance</span>
                </div>
              </div>
              
              <div class="mb-10">
                <h1 class="text-3xl font-bold mb-1 bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
                  Welcome to
                </h1>
                <h1 class="text-3xl font-bold">
                  <span class="bg-gradient-to-r from-blue-500 to-indigo-600 bg-clip-text text-transparent">Resonance</span> 
                  <span class="relative">
                    Website
                    <span class="absolute -bottom-1 left-0 w-full h-1 bg-orange-400 rounded-full"></span>
                  </span>
                </h1>
              </div>
            </div>
            
            <!-- Enhanced main form section -->
            <div class="grid gap-8">
              <!-- Error message display -->
              <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-400 text-red-700 p-4 rounded-r-md flex items-start">
                <!-- Info icon using Unicode character instead of SVG -->
                <span class="text-xl mr-2">ⓘ</span>
                {{ errorMessage }}
              </div>
              
              <!-- Input fields with enhanced styling -->
              <div class="grid gap-5">
                <div>
                  <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email or Username</label>
                  <div class="relative">
                    <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                      ✉
                    </span>
                    <input 
                      v-model="username_or_email" 
                      id="user_email"
                      type="user_email" 
                      placeholder="Email or Username" 
                      class="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                      :class="{'border-red-300 focus:ring-red-400': formSubmitted && !email}"
                    >
                  </div>
                </div>
                
                <div>
                  <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                  <div class="relative">
                    <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                      🔒
                    </span>
                    <input 
                      v-model="password" 
                      id="password"
                      :type="passwordVisible ? 'text' : 'password'" 
                      placeholder="Password" 
                      class="w-full pl-10 pr-10 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                      :class="{'border-red-300 focus:ring-red-400': formSubmitted && !password}"
                    >
                    <button 
                      type="button" 
                      class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                      @click="togglePasswordVisibility"
                    >
                      <span v-if="!passwordVisible">👁</span>
                      <span v-else>👁‍🗨</span>
                    </button>
                  </div>
                </div>
                
                <!-- Forgot password link -->
                <div class="flex justify-end -mt-2">
                  <a href="#" class="text-sm text-orange-500 hover:text-orange-600 hover:underline">Forgot password?</a>
                </div>
                
                <!-- Enhanced login button -->
                <div class="pt-2">
                  <button
                    class="w-full py-3.5 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white font-medium rounded-xl transition-all shadow-md hover:shadow-lg active:shadow-sm transform hover:-translate-y-0.5 active:translate-y-0 duration-150"
                    @click="handleLogin"
                  >
                    <div class="flex items-center justify-center">
                      <span>LOG IN</span>
                      <!-- Arrow using CSS instead of SVG -->
                      <span class="arrow-login ml-2"></span>
                    </div>
                  </button>
                </div>
              </div>
              
              <!-- Enhanced social login section -->
              <div class="grid gap-4 pt-4">
                <div class="relative flex items-center">
                  <div class="flex-grow border-t border-gray-300"></div>
                  <span class="flex-shrink mx-4 text-gray-500">Or login with</span>
                  <div class="flex-grow border-t border-gray-300"></div>
                </div>
                <div class="grid grid-cols-3 gap-4 max-w-xs mx-auto">
                  <button class="p-3 rounded-lg border border-gray-200 hover:bg-gray-50 hover:border-gray-300 transition-all transform hover:-translate-y-0.5 duration-150">
                    <Icon name="logos:google-icon" class="h-7 w-7 mx-auto" aria-hidden="true" />
                  </button>
                  <button class="p-3 rounded-lg border border-gray-200 hover:bg-gray-50 hover:border-gray-300 transition-all transform hover:-translate-y-0.5 duration-150">
                    <Icon name="logos:facebook" class="h-7 w-7 mx-auto" aria-hidden="true" />
                  </button>
                  <button class="p-3 rounded-lg border border-gray-200 hover:bg-gray-50 hover:border-gray-300 transition-all transform hover:-translate-y-0.5 duration-150">
                    <Icon name="logos:x" class="h-7 w-7 mx-auto" aria-hidden="true" />
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Enhanced footer section -->
            <div class="grid gap-4 pt-4">
              <div class="grid place-items-center">
                <div class="flex space-x-8 text-sm">
                  <a href="#" class="text-gray-600 hover:text-gray-800 hover:underline transition-colors">Terms of Use</a>
                  <a href="#" class="text-gray-600 hover:text-gray-800 hover:underline transition-colors">Privacy Policy</a>
                  <a href="#" class="text-gray-600 hover:text-gray-800 hover:underline transition-colors">Help Center</a>
                </div>
              </div>
              <div class="text-gray-600 mt-2 md:hidden">
                <div class="flex flex-row gap-2 justify-center">
                  <span class="text-gray-600">New to Resonance?</span>
                  <NuxtLink class="text-orange-500 hover:text-orange-600 font-medium hover:underline" to="/register">Sign up here</NuxtLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Animation keyframes */
.animate-blob {
  animation: blob-bounce 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes blob-bounce {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-float-delay {
  animation: float 8s ease-in-out infinite;
  animation-delay: 2s;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0px);
  }
}

.animate-spin-slow {
  animation: spin 15s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(45deg);
  }
  to {
    transform: rotate(405deg);
  }
}

/* Custom CSS for components without SVG */
.arrow-right {
  width: 0;
  height: 0;
  border-top: 6px solid transparent;
  border-bottom: 6px solid transparent;
  border-left: 10px solid currentColor;
  display: inline-block;
}

.arrow-login {
  position: relative;
  display: inline-block;
  width: 14px;
  height: 2px;
  background-color: currentColor;
}

.arrow-login:after {
  content: '';
  position: absolute;
  right: 0;
  top: -3px;
  width: 8px;
  height: 8px;
  border-top: 2px solid currentColor;
  border-right: 2px solid currentColor;
  transform: rotate(45deg);
}

/* CSS wave effect instead of SVG */
.wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px;
  background: linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(255,255,255,0.3) 100%);
  transform: scaleY(0.3);
  border-radius: 100% 100% 0 0;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: #9ca3af;
}

.divider::before, .divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #e5e7eb;
}

.divider::before {
  margin-right: 0.5em;
}

.divider::after {
  margin-left: 0.5em;
}
</style>