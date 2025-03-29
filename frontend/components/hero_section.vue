<script setup lang="ts">

onMounted(() => {
  const heroContent = document.querySelector('.hero-content');
  heroContent?.classList.add('animate-fadeIn');
});
</script>

<template>
  <div class="h-3/4">
    <div 
      class="hero h-full relative"
      style="background-image: url(https://i.ibb.co/LfPzXWy/semeon-hrozian-y-DC3-NXxrtyc-unsplash.jpg);">
      
      <!-- Improved overlay with gradient -->
      <div class="hero-overlay bg-gradient-to-r from-black via-black/70 to-transparent"/>
      
      <!-- Decorative elements -->
      <div class="absolute top-10 left-10 w-16 h-16 border-4 border-orange-400/20 rounded-full"/>
      <div class="absolute bottom-10 left-20 w-24 h-24 border-4 border-orange-400/20 rounded-full"/>
      
      <!-- Main content with improved layout -->
      <div class="hero-content text-left p-10 sm:p-18 lg:p-48 lg:mr-auto relative z-10">
        <div class="max-w-md">
          <!-- Spotlight effect around headings -->
          <div class="relative mb-8">
            <div class="absolute -inset-1 bg-orange-400/20 blur-xl rounded-lg opacity-75"/>
            <h1 class="relative font-bold text-white text-3xl lg:text-5xl">
              Fine quality,<br>   
              <span class="text-orange-400">Affordable</span>
            </h1>
          </div>
          
          <p class="mb-8 text-neutral-300 lg:text-lg text-wrap border-l-4 border-orange-400 pl-4">
            Experience the difference with fine quality headphones at the best price. Whether you're a music lover or an audio professional, our headphones deliver crisp, clear sound and lasting comfort for every ear.
          </p>
          
          <div class="flex items-center gap-4">
            <NuxtLink to="/products" class="btn bg-orange-400 hover:bg-orange-500 text-white border-none shadow-lg shadow-orange-400/50 transition-all hover:translate-y-[-2px]">
              Shop Now
              <Icon name="heroicons:arrow-right" class="h-5 w-5" />
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>