<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  username: {
    type: String,
    default: ''
  }
});

const isVisible = ref(false);
const isAnimating = ref(false);

watch(() => props.show, (value) => {
  if (value) {
    isVisible.value = true;
    nextTick(() => {
      isAnimating.value = true;
    });
  } else {
    isAnimating.value = false;
    setTimeout(() => {
      isVisible.value = false;
    }, 300);
  }
});
</script>

<template>
  <div v-if="isVisible" class="fixed inset-0 flex items-center justify-center z-50">
    <div
class="absolute inset-0 bg-black bg-opacity-30 transition-opacity duration-300" 
         :class="isAnimating ? 'opacity-100' : 'opacity-0'"/>
    
    <div
class="bg-white rounded-lg shadow-xl w-80 p-6 transform transition-all duration-300"
         :class="isAnimating ? 'scale-100 opacity-100' : 'scale-95 opacity-0'">
      
      <div class="text-center">
        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 mb-4">
          <Icon name="heroicons:check" class="h-6 w-6 text-green-600" />
        </div>
        
        <h3 class="text-lg font-medium text-gray-900 mb-2">Login Successful!</h3>
        
        <p class="text-sm text-gray-500 mb-5">
          Welcome back, {{ username }}!
        </p>
        
        <div class="flex items-center justify-center">
          <div class="spinner mr-3"/>
          <p class="text-sm text-gray-500">
            Redirecting to homepage...
          </p>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #4ade80;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>