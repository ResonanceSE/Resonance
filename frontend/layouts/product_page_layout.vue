<script setup>
// Props for layout
const props = defineProps({
  brandName: {
    type: String,
    default: ''
  },
  modelName: {
    type: String,
    default: ''
  },
  productSubtitle: {
    type: String,
    default: ''
  },
  productPrice: {
    type: [Number, String],
    default: 0
  },
  mainImage: {
    type: String,
    default: ''
  },
  productImages: {
    type: Array,
    default: () => []
  },
  productColors: {
    type: Array,
    default: () => []
  },
  productDescription: {
    type: String,
    default: ''
  },
  productFeatures: {
    type: Array,
    default: () => []
  },
  productReviewCount: {
    type: Number,
    default: 0
  },
  productReviews: {
    type: Array,
    default: () => []
  },
  productSpecifications: {
    type: Object,
    default: () => ({})
  },
  productName: {
    type: String,
    default: ''
  }
});

// Emits
const emit = defineEmits(['add-to-cart', 'select-color', 'select-image']);

// State
const currentImageIndex = ref(0);
const selectedColor = ref('');

onMounted(() => {
  if (props.productColors && props.productColors.length > 0) {
    selectedColor.value = props.productColors[0].value;
  }
});

// Methods
const setCurrentImage = (index) => {
  currentImageIndex.value = index;
  emit('select-image', index);
};

const selectColor = (colorValue) => {
  selectedColor.value = colorValue;
  emit('select-color', colorValue);
};

const addToCart = () => {
  if (props.productColors.length > 0 && !selectedColor.value) {
    alert('Please select a color');
    return;
  }
  
  const colorName = props.productColors.find(c => c.value === selectedColor.value)?.label || selectedColor.value;
  emit('add-to-cart', {
    brandName: props.brandName,
    modelName: props.modelName,
    colorValue: selectedColor.value,
    colorName: colorName
  });
};
</script>
<!-- layouts/headphones.vue -->
<template>
    <div class="container mx-auto px-4 py-8">
      <!-- Main Product Section -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
        <!-- Left: Product Images -->
        <div class="product-images relative">
          <!-- Main Image -->
          <div class="main-image relative">
            <img :src="mainImage" :alt="productName" class="w-full rounded-lg">
            
            <!-- Zoom Button -->
            <button class="btn btn-circle btn-sm bg-base-100 absolute top-4 left-4">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
              </svg>
            </button>
          </div>
          
          <!-- Thumbnail Gallery -->
          <div class="thumbnails grid grid-cols-4 gap-2 mt-4">
            <div
v-for="(image, index) in productImages" :key="index" 
                 class="thumbnail cursor-pointer border-2 rounded-md p-1" 
                 :class="currentImageIndex === index ? 'border-primary' : 'border-transparent'">
              <img
:src="image" :alt="`${productName} - view ${index + 1}`" 
                   class="w-full h-full object-cover" 
                   @click="setCurrentImage(index)">
            </div>
          </div>
        </div>
        
        <!-- Right: Product Details -->
        <div class="product-details flex flex-col">
          <!-- Brand and Model -->
          <div class="mb-2">
            <h1 class="text-3xl font-medium">
              <span class="opacity-70">{{ brandName }}</span> 
              <span class="font-bold">{{ modelName }}</span>
            </h1>
            <h2 class="text-2xl">{{ productSubtitle }}</h2>
          </div>
          
          <!-- Color Selection -->
          <div v-if="productColors.length > 0" class="my-8">
            <div class="flex items-center justify-between mb-4">
              <span class="font-medium">Select Color</span>
            </div>
            
            <div class="flex gap-3 mb-6">
              <button
v-for="color in productColors" :key="color.value"
                     class="w-10 h-10 rounded-full border-2" 
                     :class="selectedColor === color.value ? 'border-primary' : 'border-transparent'"
                     :style="`background-color: ${color.hex}`"
                     @click="selectColor(color.value)"/>
            </div>
          </div>
          
          <!-- Add to Cart Section -->
          <div class="flex items-center gap-4 my-8">
            <button class="btn btn-primary flex-1 rounded-full" @click="addToCart">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
              </svg>
              ADD TO BAG
            </button>
            <div class="text-2xl font-bold">$ {{ productPrice }}</div>
          </div>
          
          <!-- Product Information Accordion -->
          <div class="product-info mt-6">
            <div class="collapse collapse-arrow border-t">
              <input type="checkbox" > 
              <div class="collapse-title font-medium flex items-center">
                Description
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 ml-2 opacity-60">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                </svg>
              </div>
              <div class="collapse-content"> 
                <p>{{ productDescription }}</p>
              </div>
            </div>
            
            <div class="collapse collapse-arrow border-t">
              <input type="checkbox" > 
              <div class="collapse-title font-medium flex items-center">
                Features
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 ml-2 opacity-60">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                </svg>
              </div>
              <div class="collapse-content"> 
                <ul class="list-disc pl-5 space-y-1">
                  <li v-for="(feature, index) in productFeatures" :key="index">
                    {{ feature }}
                  </li>
                </ul>
              </div>
            </div>
            
            <div class="collapse collapse-arrow border-t">
              <input type="checkbox" > 
              <div class="collapse-title font-medium flex items-center">
                Free Shipping & Returns
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 ml-2 opacity-60">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                </svg>
              </div>
              <div class="collapse-content"> 
                <p>Free standard shipping on orders over $50. Free returns within 30 days of delivery.</p>
              </div>
            </div>
            
            <div v-if="productReviews.length > 0" class="collapse collapse-arrow border-t border-b">
              <input type="checkbox" > 
              <div class="collapse-title font-medium flex items-center">
                Reviews ({{ productReviewCount }})
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 ml-2 opacity-60">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                </svg>
              </div>
              <div class="collapse-content"> 
                <div class="reviews space-y-4">
                  <div v-for="(review, index) in productReviews" :key="index" class="review">
                    <div class="font-medium">{{ review.name }}</div>
                    <div class="text-sm opacity-60 mb-1">{{ review.date }}</div>
                    <p>{{ review.comment }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Technical Specifications -->
          <div v-if="Object.keys(productSpecifications).length > 0" class="mt-8">
            <h3 class="font-medium mb-4">Technical Specifications</h3>
            <div class="grid grid-cols-2 gap-y-2 opacity-70">
              <div v-for="(spec, key) in productSpecifications" :key="key" class="col-span-2 md:col-span-1">
                <div class="grid grid-cols-2">
                  <div class="font-medium">{{ key }}</div>
                  <div>{{ spec }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Slot for additional content -->
      <slot/>
    </div>
</template>
  