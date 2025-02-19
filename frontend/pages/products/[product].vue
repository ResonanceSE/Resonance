<script setup>
  const route = useRoute();
  const productName = ref(route.params.product);
  console.log(route.params.product)
  watch(() => route.params.product, (newValue) => {
    productName.value = newValue;
  });
</script>

<template>
  <div>
    <navbar_header/>
    <div class="container mx-auto py-10">
          <h1 class="text-2xl font-bold text-center mb-8">{{ productName.charAt(0).toUpperCase() + productName.slice(1)}}</h1>
    </div>
  </div>  
</template>
