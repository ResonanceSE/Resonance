<script setup>
  </script>
<template>
    <footer class="bg-neutral text-neutral-content">
      <div class="container mx-auto p-10 grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Brand and About -->
        <div>
          <h2 class="text-lg font-bold">Resonance</h2>
          <p class="text-sm mt-2">
            Discover the best sound quality with our exclusive range of headphones. Designed for music enthusiasts.
          </p>
        </div>
  
        <!-- Navigation Links -->
        <div>
          <h3 class="text-lg font-semibold">Quick Links</h3>
          <ul class="mt-2 space-y-1">
            <li><a class="link link-hover" href="/shop">Shop</a></li>
            <li><a class="link link-hover" href="/about">About Us</a></li>
            <li><a class="link link-hover" href="/support">Support</a></li>
            <li><a class="link link-hover" href="/contact">Contact</a></li>
          </ul>
        </div>
  
        <!-- Social Links -->
        <div>
          <h3 class="text-lg font-semibold">Follow Us</h3>
          <div class="flex mt-2 space-x-4">
            <a
              href="https://facebook.com"
              target="_blank"
              class="link link-hover text-xl"
            >
              <span class="iconify" data-icon="mdi:facebook" aria-hidden="true"/>
            </a>
            <a
              href="https://twitter.com"
              target="_blank"
              class="link link-hover text-xl"
            >
              <span class="iconify" data-icon="mdi:twitter" aria-hidden="true"/>
            </a>
            <a
              href="https://instagram.com"
              target="_blank"
              class="link link-hover text-xl"
            >
              <span class="iconify" data-icon="mdi:instagram" aria-hidden="true"/>
            </a>
            <a
              href="https://youtube.com"
              target="_blank"
              class="link link-hover text-xl"
            >
              <span class="iconify" data-icon="mdi:youtube" aria-hidden="true"/>
            </a>
          </div>
        </div>
      </div>
      <div class="bg-neutral-focus py-4 text-center">
        <p>&copy; {{ new Date().getFullYear() }} Resonance. All Rights Reserved.</p>
      </div>
    </footer>
  </template>
  
  
  <style>

  </style>
  