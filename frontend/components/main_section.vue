<script setup>
const items = [
  {
    id: 1,
    name: "Noise Cancelling Headphones",
    description: "Experience the ultimate sound clarity and noise isolation.",
    price: 299.99,
    image: "https://via.placeholder.com/300x200",
  },
  {
    id: 2,
    name: "Wireless Bluetooth Headphones",
    description: "Enjoy tangle-free audio with high-quality sound.",
    price: 199.99,
    image: "https://via.placeholder.com/300x200",
  },
  {
    id: 3,
    name: "Over-Ear Studio Headphones",
    description: "Perfect for music production and professional use.",
    price: 249.99,
    image: "https://via.placeholder.com/300x200",
  },
  {
    id: 4,
    name: "Sports Headphones",
    description: "Sweat-proof and designed for an active lifestyle.",
    price: 149.99,
    image: "https://via.placeholder.com/3 00x200",
  },
];
</script>



<template>
    <main class="container mx-auto py-10">
      <h1 class="text-2xl font-bold text-center mb-8">Our Best-Selling Headphones</h1>
      <div class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <div 
          v-for="item in items" 
          :key="item.id" 
          class="card bg-base-100 shadow-md hover:shadow-lg transition-shadow duration-300"
        >
          <!-- Image -->
          <figure>
            <img :src="item.image" :alt="item.name" class="w-full h-48 object-cover" />
          </figure>
          <!-- Content -->
          <div class="card-body">
            <h2 class="card-title text-lg font-semibold">{{ item.name }}</h2>
            <p class="text-sm text-gray-600">{{ item.description }}</p>
            <div class="mt-4 flex items-center justify-between">
              <span class="text-xl font-bold text-primary">${{ item.price }}</span>
              <button class="btn btn-primary btn-sm">Buy Now</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </template>
  
  <style scoped>
  .card:hover {
    transform: scale(1.02);
  }
  </style>
  