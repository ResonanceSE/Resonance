<template>
  <div class="min-h-screen bg-gray-100">

    <!-- Hero Section -->
    <section class="hero bg-blue-600 text-white py-16 text-center">
      <div class="container mx-auto flex flex-col items-center">
        <h1 class="text-4xl font-bold">Premium Headphones for Every Sound</h1>
        <p class="mt-4 text-xl">Experience the best in sound quality, comfort, and design.</p>
        <a href="#products" class="btn btn-primary mt-8">Shop Now</a>
      </div>
    </section>

    <!-- Featured Products Section -->
    <section id="products" class="py-16">
      <div class="container mx-auto text-center">
        <h2 class="text-3xl font-bold mb-8">Our Best Sellers</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          
          <!-- Product Card 1 -->
          <div class="card card-compact w-full bg-white shadow-xl">
            <figure><img src="https://via.placeholder.com/300" alt="Headphone 1" class="w-full h-48 object-cover"></figure>
            <div class="card-body">
              <h3 class="card-title">Premium Sound Pro</h3>
              <p class="text-xl font-semibold">$299.99</p>
              <div class="card-actions justify-end">
                <a href="#" class="btn btn-primary">Add to Cart</a>
              </div>
            </div>
          </div>

          <!-- Product Card 2 -->
          <div class="card card-compact w-full bg-white shadow-xl">
            <figure><img src="https://via.placeholder.com/300" alt="Headphone 2" class="w-full h-48 object-cover"></figure>
            <div class="card-body">
              <h3 class="card-title">Noise Cancelling X</h3>
              <p class="text-xl font-semibold">$199.99</p>
              <div class="card-actions justify-end">
                <a href="#" class="btn btn-primary">Add to Cart</a>
              </div>
            </div>
          </div>

          <!-- Product Card 3 -->
          <div class="card card-compact w-full bg-white shadow-xl">
            <figure><img src="https://via.placeholder.com/300" alt="Headphone 3" class="w-full h-48 object-cover"></figure>
            <div class="card-body">
              <h3 class="card-title">Wireless SoundMax</h3>
              <p class="text-xl font-semibold">$149.99</p>
              <div class="card-actions justify-end">
                <a href="#" class="btn btn-primary">Add to Cart</a>
              </div>
            </div>
          </div>

          <!-- Product Card 4 -->
          <div class="card card-compact w-full bg-white shadow-xl">
            <figure><img src="https://via.placeholder.com/300" alt="Headphone 4" class="w-full h-48 object-cover"></figure>
            <div class="card-body">
              <h3 class="card-title">Sporty Beats</h3>
              <p class="text-xl font-semibold">$129.99</p>
              <div class="card-actions justify-end">
                <a href="#" class="btn btn-primary">Add to Cart</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer Section -->
    <footer class="bg-gray-800 text-white py-8 text-center">
      <p>&copy; 2025 Headphone Store. All rights reserved.</p>
      <div class="flex justify-center space-x-4 mt-4">
        <a href="#" class="text-lg">Facebook</a>
        <a href="#" class="text-lg">Twitter</a>
        <a href="#" class="text-lg">Instagram</a>
      </div>
    </footer>

  </div>
</template>

<script setup>

</script>

<style scoped>

</style>
