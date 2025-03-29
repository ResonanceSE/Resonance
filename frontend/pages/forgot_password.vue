<script setup>

definePageMeta({
  layout: 'false'
});

const email = ref('');
const isSubmitting = ref(false);
const emailSent = ref(false);
const errorMessage = ref('');
const config = useRuntimeConfig();
const apiUrl = config.public.apiUrl || 'http://localhost:8000';

const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

const handleSubmit = async () => {
  // Reset state
  errorMessage.value = '';
  
  // Validate email
  if (!email.value) {
    errorMessage.value = 'Please enter your email address';
    return;
  }
  
  if (!validateEmail(email.value)) {
    errorMessage.value = 'Please enter a valid email address';
    return;
  }
  
  isSubmitting.value = true;
  
  try {
    const response = await fetch(`${apiUrl}/api/auth/forgot-password/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email: email.value })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      emailSent.value = true;
    } else {
      errorMessage.value = data.message || 'An error occurred. Please try again.';
    }
  } catch (error) {
    console.error('Error sending password reset request:', error);
    errorMessage.value = 'Failed to connect to the server. Please try again later.';
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <!-- Decorative background -->
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12 relative overflow-hidden">
    <!-- Decorative circles -->
    <div class="absolute top-20 left-10 w-64 h-64 bg-orange-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"/>
    <div class="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"/>
    <div class="absolute -bottom-8 left-40 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000"/>

    <!-- Card container -->
    <div class="max-w-md mx-auto bg-white rounded-xl shadow-lg overflow-hidden md:max-w-2xl m-6">
      <div class="p-8">
        <!-- Logo/Branding -->
        <div class="flex items-center gap-2 mb-8">
          <div class="w-8 h-8 bg-gradient-to-r from-orange-500 to-orange-400 rounded-full flex items-center justify-center">
            <div class="w-4 h-4 bg-white rounded-sm transform rotate-45"/>
          </div>
          <h3 class="text-xl font-bold">Resonance Sound Shop</h3>
        </div>

        <!-- Success State -->
        <div v-if="emailSent" class="text-center py-8">
          <div class="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 class="text-2xl font-semibold mb-2">Check Your Email</h2>
          <p class="text-gray-600 mb-6">
            We've sent password reset instructions to:<br>
            <span class="font-medium">{{ email }}</span>
          </p>
          <p class="text-gray-500 text-sm mb-6">
            If you don't see the email, check other places it might be, like your junk, spam, social, or other folders.
          </p>
          <div class="flex flex-col space-y-3">
            <NuxtLink to="/login" class="btn btn-outline hover:bg-orange-500 hover:border-orange-500">
              Back to Login
            </NuxtLink>
            <button 
              class="btn btn-ghost text-orange-500"
              @click="emailSent = false; email = ''"
            >
              Try another email
            </button>
          </div>
        </div>

        <!-- Form State -->
        <div v-else>
          <h2 class="text-2xl font-bold mb-2">Forgot Password</h2>
          <p class="text-gray-600 mb-6">
            Enter your email address and we'll send you instructions to reset your password.
          </p>

          <!-- Error message -->
          <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-400 text-red-700 p-4 mb-6 rounded-r-md">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div class="ml-3">
                <p>{{ errorMessage }}</p>
              </div>
            </div>
          </div>

          <!-- Form -->
          <form @submit.prevent="handleSubmit">
            <div class="mb-6">
              <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
                Email Address
              </label>
              <div class="relative">
                <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                  ✉
                </span>
                <input
                  id="email"
                  v-model="email"
                  type="email"
                  placeholder="Enter your email"
                  class="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                  required
                >
              </div>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              class="w-full py-3.5 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white font-medium rounded-xl transition-all shadow-md hover:shadow-lg active:shadow-sm transform hover:-translate-y-0.5 active:translate-y-0 duration-150"
              :disabled="isSubmitting"
            >
              <div v-if="isSubmitting" class="flex items-center justify-center">
                <div class="spinner-white mr-2"/>
                <span>Sending...</span>
              </div>
              <span v-else>Send Reset Instructions</span>
            </button>
          </form>

          <div class="text-center mt-6">
            <NuxtLink to="/login" class="text-orange-500 hover:text-orange-700 font-medium">
              Back to Login
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
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

.spinner-white {
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>