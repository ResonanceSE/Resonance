// frontend/layouts/product-detail-layout.vue
<script setup>
import { ref, computed, onMounted } from 'vue';

// Get route information
const route = useRoute();
const productId = route.params.id;
const productType = route.path.split('/')[2]; // Gets "headphones", "earphones", etc.
const apiUrl = useRuntimeConfig().public.apiUrl;

// State for product data
const product = ref(null);
const isLoading = ref(true);
const error = ref(null);

// Fetch product data
const fetchProduct = async () => {
    isLoading.value = true;
    error.value = null;
    
    try {
        const response = await fetch(`${apiUrl}/api/products/${productId}/`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch product: ${response.statusText}`);
        }
        
        product.value = await response.json();
    } catch (err) {
        console.error('Error fetching product:', err);
        error.value = err.message || 'Failed to load product details';
        
        // Use mock data during development if API fails
        if (process.env.NODE_ENV !== 'production') {
            product.value = getMockProduct();
        }
    } finally {
        isLoading.value = false;
    }
};

// Mock product data for development
const getMockProduct = () => {
    return {
        id: productId,
        name: `Premium ${productType.charAt(0).toUpperCase() + productType.slice(1, -1)}`,
        brand: "Resonance",
        modelName: `RS-${productType.charAt(0).toUpperCase()}${productId}`,
        productSubtitle: "Premium Audio Experience",
        price: 349.99,
        description: `Experience premium audio quality with our ${productType} line. Designed for comfort and exceptional sound performance.`,
        stock: 35,
        connections: "Bluetooth 5.0, 3.5mm Jack",
        images: [
            `https://via.placeholder.com/500x500?text=${productType}+Main`,
            `https://via.placeholder.com/500x500?text=${productType}+Side`,
            `https://via.placeholder.com/500x500?text=${productType}+Top`,
            `https://via.placeholder.com/500x500?text=${productType}+Detail`
        ],
        colors: [
            { value: "black", label: "Black", hex: "#000000" },
            { value: "silver", label: "Silver", hex: "#C0C0C0" },
            { value: "blue", label: "Midnight Blue", hex: "#191970" }
        ],
        features: [
            "Premium sound quality",
            "30-hour battery life",
            "Quick charging capability",
            "Comfortable design",
            "Touch controls",
            "Built-in microphone"
        ],
        reviewCount: 487,
        reviews: [
            { 
                name: "Michael T.", 
                date: "March 2, 2025", 
                comment: "Excellent quality product. Highly recommended." 
            },
            { 
                name: "Sarah J.", 
                date: "February 15, 2025", 
                comment: "Great sound quality with comfortable fit." 
            }
        ],
        specifications: {
            "Driver Type": "40mm, dynamic",
            "Frequency Response": "20Hz-20,000Hz",
            "Battery Life": "Up to 30 hours",
            "Weight": "250g",
            "Bluetooth Version": "5.0"
        }
    };
};

// Check if we need to handle adding to cart
const handleAddToCart = (productData) => {
    console.log('Adding to cart:', productData);
    // Implement cart functionality here
};

// Format functions
const formatCurrency = (price) => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
};

// Compute props for product page layout
const layoutProps = computed(() => {
    if (!product.value) return {};
    
    return {
        brandName: product.value.brand || '',
        modelName: product.value.modelName || product.value.name || '',
        productSubtitle: product.value.productSubtitle || '',
        productPrice: product.value.price || 0,
        mainImage: product.value.images?.[0] || `https://via.placeholder.com/500x500?text=${product.value.name?.replace(/\s+/g, '+')}`,
        productImages: product.value.images || [],
        productColors: product.value.colors || [],
        productDescription: product.value.description || '',
        productFeatures: product.value.features || [],
        productReviewCount: product.value.reviewCount || 0,
        productReviews: product.value.reviews || [],
        productSpecifications: product.value.specifications || {},
        productName: product.value.name || ''
    };
});

// Initialize
onMounted(() => {
    fetchProduct();
});

// Provide the product data to child components
provide('product', product);
provide('isLoading', isLoading);
provide('error', error);
provide('layoutProps', layoutProps);
provide('handleAddToCart', handleAddToCart);
</script>

<template>
    <div>
        <!-- Loading state -->
        <div v-if="isLoading" class="flex justify-center items-center min-h-[400px]">
            <div class="loading loading-spinner loading-lg text-orange-500"></div>
        </div>
        
        <!-- Error state -->
        <div v-else-if="error" class="alert alert-error my-8 max-w-2xl mx-auto">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ error }}</span>
        </div>
        
        <!-- Product display using the product-page-layout -->
        <div v-else-if="product">
            <ProductPageLayout
                v-bind="layoutProps"
                @add-to-cart="handleAddToCart"
            >
                <!-- Slot for additional product-specific content -->
                <slot></slot>
            </ProductPageLayout>
        </div>
        
        <!-- No product found state -->
        <div v-else class="text-center my-12">
            <h2 class="text-2xl font-bold mb-2">Product Not Found</h2>
            <p class="mb-6">We couldn't find the product you're looking for.</p>
            <NuxtLink :to="`/products/${productType}`" class="btn btn-primary">
                View All {{ productType.charAt(0).toUpperCase() + productType.slice(1) }}
            </NuxtLink>
        </div>
    </div>
</template>