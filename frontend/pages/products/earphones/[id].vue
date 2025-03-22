// frontend/pages/products/earphones/[id].vue
<script setup>
definePageMeta({
    layout: 'product-detail-layout'
})

// Get the product data from the layout
const product = inject('product', ref(null));

// All the core functionality is now in the layout
// You can add earphones-specific logic here if needed
</script>

<template>
    <!-- Additional earphones-specific content can go here -->
    <div v-if="product" class="mt-12 bg-gray-50 p-6 rounded-lg">
        <h2 class="text-2xl font-bold mb-4">About {{ product.brand }} Earphones</h2>
        <p class="mb-4">
            {{ product.brand }} earphones deliver premium sound in a compact, portable design.
            Ideal for active lifestyles and on-the-go listening without compromising on audio quality.
        </p>
        
        <!-- Earphones-specific content -->
        <div class="mt-8">
            <h3 class="text-xl font-semibold mb-3">Perfect For</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                    <div class="font-medium text-lg mb-2">Active Lifestyles</div>
                    <p class="text-sm text-gray-600">Stay motivated with your favorite tracks during workouts and runs.</p>
                </div>
                <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                    <div class="font-medium text-lg mb-2">Commuters</div>
                    <p class="text-sm text-gray-600">Enjoy a compact audio solution for your daily commute without bulk.</p>
                </div>
                <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                    <div class="font-medium text-lg mb-2">Everyday Use</div>
                    <p class="text-sm text-gray-600">Convenient for calls, podcasts, and music throughout your day.</p>
                </div>
            </div>
        </div>
    </div>
</template>