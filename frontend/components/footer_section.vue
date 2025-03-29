<script setup>
const currentYear = new Date().getFullYear();
</script>


<template>
  <footer class="footer footer-horizontal footer-center bg-neutral text-base-content rounded p-10 relative bottom-0">
    <div class="flex flex-col items-center">
      <h2 class="text-xl font-bold text-white mb-2">Resonance Sound Shop</h2>
      <p class="text-white text-sm">Your destination for premium audio equipment and accessories</p>
    </div>
    <aside>
      <p class="text-white">Copyright © {{ currentYear }} - All rights reserved by Resonance Sound Shop</p>
    </aside>
  </footer>
</template>