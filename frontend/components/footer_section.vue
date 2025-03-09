<script setup>
const currentYear = new Date().getFullYear();
</script>


<template>
  <footer class="footer footer-horizontal footer-center bg-neutral text-base-content rounded p-10 relative bottom-0 ">
    <nav class="grid grid-flow-col gap-4">
      <a class="link link-hover text-white">About us</a>
      <a class="link link-hover text-white">Contact</a>
      <a class="link link-hover text-white">Jobs</a>
      <a class="link link-hover text-white">Press kit</a>
    </nav>
    <nav>
      <div class="grid grid-flow-col gap-6">
        <a class="link link-hover"><Icon name="logos:x" class="h-10 w-10" aria-hidden="true"/></a>
        <a class="link link-hover"><Icon name="logos:facebook" class="h-10 w-10" aria-hidden="true"/></a>
        <a class="link link-hover"><Icon name="logos:youtube-icon" class="h-10 w-10" aria-hidden="true"/></a>
        <a class="link link-hover"><Icon name="logos:google-icon" class="h-10 w-10" aria-hidden="true"/></a>
      </div>
    </nav>
    <aside>
      <p class="text-white">Copyright © {{ currentYear }} - All right reserved by Resonance</p>
    </aside>
  </footer>
</template>
