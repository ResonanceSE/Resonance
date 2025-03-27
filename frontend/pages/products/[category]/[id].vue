// frontend/pages/products/[category]/[id].vue
<script setup>
definePageMeta({
  layout: 'product-detail-layout'
});
const route = useRoute();
const category = route.params.category;

const categoryContent = computed(() => {
  switch(category) {
    case 'earphones':
      return {
        title: "About Earphones",
        description: "Earphones deliver premium sound in a compact, portable design. Ideal for active lifestyles and on-the-go listening without compromising on audio quality.",
        useCases: [
          { title: "Active Lifestyles", description: "Stay motivated with your favorite tracks during workouts and runs." },
          { title: "Commuters", description: "Enjoy a compact audio solution for your daily commute without bulk." },
          { title: "Everyday Use", description: "Convenient for calls, podcasts, and music throughout your day." }
        ]
      };
    case 'headphones':
      return {
        title: "About Headphones",
        description: "Headphones provide an immersive listening experience with superior sound isolation and comfort for extended use.",
        useCases: [
          { title: "Audiophiles", description: "Experience your music with rich, detailed sound quality." },
          { title: "Work Focus", description: "Block out distractions and create your perfect work environment." },
          { title: "Home Entertainment", description: "Immerse yourself in movies, games, and music without disturbing others." }
        ]
      };
    case 'speakers':
      return {
        title: "About Speakers",
        description: "Our speakers fill your room with amazing sound, bringing your music, movies, and games to life with powerful, balanced audio.",
        useCases: [
          { title: "Home Audio", description: "Transform your living space with rich, room-filling sound." },
          { title: "Parties & Gatherings", description: "Create the perfect atmosphere for social events." },
          { title: "Smart Home", description: "Connect with voice assistants and smart home technology." }
        ]
      };
    default:
      return null;
  }
});

const product = inject('product', ref(null));

</script>

<template>
  <div v-if="product && categoryContent" class="mt-12 bg-gray-50 p-6 rounded-lg">
    <h2 class="text-2xl font-bold mb-4">{{ categoryContent.title }}</h2>
    <p class="mb-6 text-gray-700">{{ categoryContent.description }}</p>
    
    <div v-if="categoryContent.useCases" class="mt-8">
      <h3 class="text-xl font-semibold mb-4">Perfect For</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div
v-for="(useCase, index) in categoryContent.useCases" :key="index" 
            class="bg-white p-5 rounded-lg shadow-sm border border-gray-100">
          <div class="font-medium text-lg mb-2">{{ useCase.title }}</div>
          <p class="text-sm text-gray-600">{{ useCase.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>