<script setup>

definePageMeta({
  layout: 'false'
});

const route = useRoute();
const router = useRouter();
const token = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const passwordVisible = ref(false);
const confirmPasswordVisible = ref(false);
const isSubmitting = ref(false);
const passwordResetSuccess = ref(false);
const errorMessage = ref('');
const config = useRuntimeConfig();
const apiUrl = config.public.apiUrl || 'http://localhost:8000';

onMounted(() => {
  token.value = route.query.token;
  
  if (!token.value) {
    errorMessage.value = 'Invalid password reset link. Please request a new one.';
  }
});

const validatePassword = () => {
  if (!newPassword.value) {
    errorMessage.value = 'Please enter a new password';
    return false;
  }
  
  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match';
    return false;
  }
  
  return true;
};

const togglePasswordVisibility = (field) => {
  if (field === 'password') {
    passwordVisible.value = !passwordVisible.value;
  } else {
    confirmPasswordVisible.value = !confirmPasswordVisible.value;
  }
};

const handleResetPassword = async () => {
  errorMessage.value = '';
  
  if (!validatePassword()) {
    return;
  }
  
  isSubmitting.value = true;
  
  try {
    const response = await fetch(`${apiUrl}/api/auth/reset-password/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        token: token.value,
        password: newPassword.value
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      passwordResetSuccess.value = true;
      // Clear form fields
      newPassword.value = '';
      confirmPassword.value = '';
    } else {
      errorMessage.value = data.message || 'Failed to reset password. Please try again.';
    }
  } catch (error) {
    console.error('Error resetting password:', error);
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
        <div v-if="passwordResetSuccess" class="text-center py-8">
          <div class="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 class="text-2xl font-semibold mb-2">Password Reset Successful</h2>
          <p class="text-gray-600 mb-6">
            Your password has been reset successfully. You can now log in with your new password.
          </p>
          <NuxtLink to="/login" class="btn btn-primary">
            Go to Login
          </NuxtLink>
        </div>

        <!-- Error with no token -->
        <div v-else-if="!token" class="text-center py-8">
          <div class="w-16 h-16 mx-auto bg-red-100 rounded-full flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 class="text-2xl font-semibold mb-2">Invalid Reset Link</h2>
          <p class="text-gray-600 mb-6">
            The password reset link is invalid or has expired. Please request a new one.
          </p>
          <NuxtLink to="/forgot_password" class="btn btn-primary">
            Request New Link
          </NuxtLink>
        </div>

        <!-- Form State -->
        <div v-else>
          <h2 class="text-2xl font-bold mb-2">Reset Password</h2>
          <p class="text-gray-600 mb-6">
            Please enter your new password below.
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
          <form @submit.prevent="handleResetPassword">
            <div class="mb-6">
              <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
                New Password
              </label>
              <div class="relative">
                <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                  🔒
                </span>
                <input
                  id="password"
                  v-model="newPassword"
                  :type="passwordVisible ? 'text' : 'password'"
                  placeholder="Enter new password"
                  class="w-full pl-10 pr-10 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                  required
                >
                <button
                  type="button"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                  @click="togglePasswordVisibility('password')"
                >
                  <span v-if="!passwordVisible">👁</span>
                  <span v-else>👁‍🗨</span>
                </button>
              </div>
            </div>

            <div class="mb-6">
              <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">
                Confirm Password
              </label>
              <div class="relative">
                <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                  🔒
                </span>
                <input
                  id="confirmPassword"
                  v-model="confirmPassword"
                  :type="confirmPasswordVisible ? 'text' : 'password'"
                  placeholder="Confirm new password"
                  class="w-full pl-10 pr-10 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                  required
                >
                <button
                  type="button"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                  @click="togglePasswordVisibility('confirm')"
                >
                  <span v-if="!confirmPasswordVisible">👁</span>
                  <span v-else>👁‍🗨</span>
                </button>
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
                <span>Resetting Password...</span>
              </div>
              <span v-else>Reset Password</span>
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