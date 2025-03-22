// frontend/pages/products/headphones/[id].vue
<script setup>
definePageMeta({
    layout: 'product-detail-layout'
})

// Get the product data from the layout
const product = inject('product', ref(null));

// All the core functionality is now in the layout
// You can add headphones-specific logic here if needed
</script>

<template>
    <!-- Additional headphones-specific content can go here -->
    <div v-if="product" class="mt-12 bg-gray-50 p-6 rounded-lg">
        <h2 class="text-2xl font-bold mb-4">About {{ product.brand }} Headphones</h2>
        <p class="mb-4">
            {{ product.brand }} headphones are known for their exceptional sound quality and comfort.
            Perfect for immersive listening experiences whether you're at home, commuting, or working.
        </p>
        
        <!-- Headphones-specific content -->
        <div class="mt-8">
            <h3 class="text-xl font-semibold mb-3">Perfect For</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                    <div class="font-medium text-lg mb-2">Music Enthusiasts</div>
                    <p class="text-sm text-gray-600">Experience your music with incredible detail and clarity.</p>
                </div>
                <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                    <div class="font-medium text-lg mb-2">Remote Workers</div>
                    <p class="text-sm text-gray-600">Stay focused with noise cancellation during video calls and work sessions.</p>
                </div>
                <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                    <div class="font-medium text-lg mb-2">Travelers</div>
                    <p class="text-sm text-gray-600">Block out ambient noise on planes, trains, and in busy environments.</p>
                </div>
            </div>
        </div>
    </div>
</template>