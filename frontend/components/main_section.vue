<script setup>
// Product data with minimal enhancements
const items = [
  {
    id: 1,
    name: "Noise Cancelling Headphones",
    description: "Experience the ultimate sound clarity and noise isolation.",
    price: 299.99,
    rating: 4.8,
    image: "https://via.placeholder.com/300x200",
  },
  {
    id: 2,
    name: "Wireless Bluetooth Headphones",
    description: "Enjoy tangle-free audio with high-quality sound.",
    price: 199.99,
    rating: 4.5,
    image: "https://via.placeholder.com/300x200",
  },
  {
    id: 3,
    name: "Over-Ear Studio Headphones",
    description: "Perfect for music production and professional use.",
    price: 249.99,
    rating: 4.7,
    image: "https://via.placeholder.com/300x200",
  },
  {
    id: 4,
    name: "Sports Headphones",
    description: "Sweat-proof and designed for an active lifestyle.",
    price: 149.99,
    rating: 4.3,
    image: "https://via.placeholder.com/300x200",
  },
];

// Simple star display function
function getStars(rating) {
  return "★".repeat(Math.round(rating)) + "☆".repeat(5 - Math.round(rating));
}
</script>

<template>
  <main class="container mx-auto py-10 px-4">
    <!-- Section Header -->
    <div class="text-center mb-8">
      <h1 class="text-2xl font-bold mb-2">Our Best-Selling Headphones</h1>
      <div class="w-16 h-1 bg-primary mx-auto"/>
    </div>
    
    <!-- Product Grid -->
    <div class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div 
        v-for="item in items" 
        :key="item.id" 
        class="card bg-base-100 shadow-md hover:shadow-xl transition-all duration-300"
      >
        <!-- Image -->
        <figure class="relative overflow-hidden">
          <img 
            :src="item.image" 
            :alt="item.name" 
            class="w-full h-48 object-cover transition-transform duration-500 hover:scale-105" 
          >
          <!-- Price badge -->
          <div class="absolute top-2 right-2 badge badge-primary">
            ${{ item.price }}
          </div>
        </figure>
        
        <!-- Content -->
        <div class="card-body">
          <h2 class="card-title text-lg font-semibold">{{ item.name }}</h2>
          
          <!-- Star Rating -->
          <div class="text-yellow-400 text-sm mb-2">
            {{ getStars(item.rating) }}
          </div>
          
          <p class="text-sm text-gray-600">{{ item.description }}</p>
          
          <div class="card-actions justify-end mt-4">
            <button class="btn btn-primary btn-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}
</style>