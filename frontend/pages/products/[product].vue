<script setup>
  const route = useRoute();
  const productName = computed(() => {
    return route.params.product
      ? route.params.product.charAt(0).toUpperCase() + route.params.product.slice(1)
      : "";
  });
</script>

<template>
  <div>
    <navbar_header />
    <div class="container mx-auto py-10">
      <h1 class="text-2xl font-bold text-center mb-8">{{ productName }}</h1>
    </div>
  </div>  
</template>
