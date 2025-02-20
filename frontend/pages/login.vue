  
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
    <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div class="flex flex-1 justify-center items-center">
        <div class="bg-white p-8 rounded-lg shadow-lg w-96">
          <h2 class="text-2xl font-semibold text-center mb-6">Login</h2>
          <form @submit.prevent="handleLogin">
            <div class="mb-4">
              <label class="block text-gray-700">Email</label>
              <input v-model="email" type="email" required class="w-full p-2 border rounded-lg focus:outline-none focus:ring focus:ring-blue-300">
            </div>
    
            <div class="mb-4">
              <label class="block text-gray-700">Password</label>
              <input v-model="password" type="password" required class="w-full p-2 border rounded-lg focus:outline-none focus:ring focus:ring-blue-300">
            </div>
    
            <button type="submit" class="w-full bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 transition">
              Login
            </button>
          </form>
        </div>
      </div>
      <div class="w-full mt-auto">
        <footer_section/>
      </div>
    </div>
</template>
  