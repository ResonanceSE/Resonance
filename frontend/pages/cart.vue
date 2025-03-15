<script setup>
definePageMeta({
  layout: 'default'
})

// Cart data
const cartItems = ref([
  {
    id: 1,
    name: 'Campfire Trifecta Astral Plane',
    category: 'Astral Plane',
    price: 3375,
    quantity: 2,
    image: '/images/product-placeholder.jpg'
  }
]);

const selectedItems = reactive({});

// Initialize selectedItems with all items selected
onMounted(() => {
  cartItems.value.forEach(item => {
    selectedItems[item.id] = true;
  });
});


// Toggle individual item selection
const toggleItemSelection = (itemId) => {
  selectedItems[itemId] = !selectedItems[itemId];
};

// Computed property for select all functionality
const selectAll = computed({
  get: () => {
    return cartItems.value.length > 0 && 
           cartItems.value.every(item => selectedItems[item.id]);
  },
  set: (value) => {
    cartItems.value.forEach(item => {
      selectedItems[item.id] = value;
    });
  }
});

const decreaseQuantity = (item) => {
  if (item.quantity > 1) {
    item.quantity--;
  }
};

const increaseQuantity = (item) => {
  item.quantity++;
};

const removeItem = (itemId) => {
  const index = cartItems.value.findIndex(item => item.id === itemId);
  if (index !== -1) {
    cartItems.value.splice(index, 1);
    selectedItems[itemId] = false;
  }
};
const removeSelectedItems = () => {
  cartItems.value = cartItems.value.filter(item => !selectedItems[item.id]);
  
  const selectedIds = Object.keys(selectedItems).filter(id => !selectedItems[id]);
  
  Object.keys(selectedItems).forEach(key => {
    selectedItems[key] = false;
  });
  
  selectedIds.forEach(id => {
    selectedItems[id] = true;
  });
};
const getTotalPrice = computed(() => {
  let total = 0;
  for (const item of cartItems.value) {
    if (selectedItems[item.id]) {
      total += item.price * item.quantity;
    }
  }
  return total;
});

const formatPrice = (price) => {
  return '$' + (price / 100).toFixed(2);
};

const getSelectedItemsCount = computed(() => {
  return Object.values(selectedItems).filter(Boolean).length;
});

const shippingFee = ref(999); 
const voucher = ref('');
const discount = ref(0);

const addresses = ref([
  {
    id: 1,
    default: true,
    line1: 'xxx/xxx, xxxx Village, xxxx Rd.',
    line2: 'xxxx District, xxxx Province, 10xxx'
  }
]);

const selectedAddress = ref(addresses.value[0]);
const showAddressModal = ref(false);

const applyVoucher = () => {
  if (voucher.value === 'RESONANCE20') {
    discount.value = Math.round(getTotalPrice.value * 0.2); 
  } else {
    discount.value = 0; 
  }
};

const processCheckout = () => {
  console.log('Processing checkout...');
};
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 relative overflow-hidden py-6">
    <!-- Decorative background elements -->
    <div class="absolute top-20 left-10 w-64 h-64 bg-orange-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"/>
    <div class="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"/>
    <div class="absolute -bottom-8 left-40 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000"/>
    
    <!-- Main container -->
    <div class="container mx-auto max-w-6xl px-4">
      
      <!-- Heading -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold">
          <span class="bg-gradient-to-r from-blue-500 to-indigo-600 bg-clip-text text-transparent">Checkout</span>
          <span class="relative">
            Page
            <span class="absolute -bottom-1 left-0 w-full h-1 bg-orange-400 rounded-full"/>
          </span>
        </h1>
      </div>
      
      <!-- Checkout Container -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Left Column - Cart -->
        <div class="lg:col-span-2">
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title text-2xl">Your Cart</h2>
              
              <!-- Select all -->
              <div class="flex justify-between items-center mb-4 pb-2 border-b border-gray-200">
                <div class="form-control">
                  <label class="label cursor-pointer">
                    <input 
                      v-model="selectAll" 
                      type="checkbox" 
                      class="checkbox checkbox-primary"
                    >
                    <span class="label-text ml-2">Select All ({{ getSelectedItemsCount }} items)</span>
                  </label>
                </div>
                <button class="btn btn-ghost btn-sm text-error" @click="removeSelectedItems">
                    Remove
                </button>
              </div>
              
              <!-- Cart Items -->
              <div v-if="cartItems.length > 0" class="space-y-4">
                <div 
                  v-for="item in cartItems" 
                  :key="item.id"
                  class="flex flex-col sm:flex-row items-start sm:items-center py-4 border-b border-gray-200 gap-4"
                >
                  <div class="form-control">
                    <input 
                      type="checkbox" 
                      class="checkbox checkbox-primary" 
                      :checked="selectedItems[item.id]"
                      @change="toggleItemSelection(item.id)"
                    >
                  </div>
                  
                  <!-- Product image -->
                  <div class="w-20 h-20 bg-gray-200 rounded-lg flex-shrink-0"/>
                  
                  <!-- Product details -->
                  <div class="flex-grow">
                    <h3 class="font-medium text-gray-900">{{ item.name }}</h3>
                    <p class="text-sm text-gray-500">{{ item.category }}</p>
                    <p class="font-semibold text-gray-900 mt-1">{{ formatPrice(item.price) }}</p>
                  </div>
                  
                  <!-- Quantity control -->
                  <div class="join flex">
                    <button 
                      class="btn btn-sm join-item" 
                      @click="decreaseQuantity(item)"
                    >
                      -
                    </button>
                    <span class="join-item px-3 py-1 border-y flex items-center">{{ item.quantity }}</span>
                    <button 
                      class="btn btn-sm join-item" 
                      @click="increaseQuantity(item)"
                    >
                      +
                    </button>
                  </div>
                  
                  <!-- Total price -->
                  <div class="text-right">
                    <p class="font-semibold text-lg text-primary">{{ formatPrice(item.price * item.quantity) }}</p>
                    <button 
                      class="btn btn-ghost btn-xs text-error"
                      @click="removeItem(item.id)"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- Empty cart state -->
              <div v-else class="text-center py-12">
                <p class="text-gray-500">Your cart is empty</p>
                <NuxtLink to="/products" class="btn btn-primary mt-4">
                  Continue Shopping
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right Column - Checkout -->
        <div class="lg:col-span-1">
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title text-2xl">Check Out</h2>
              
              <!-- Address Section -->
              <div class="mb-6">
                <h3 class="text-lg font-medium mb-3">Address</h3>
                <div v-if="selectedAddress" class="p-4 bg-base-200 rounded-lg">
                  <p>{{ selectedAddress.line1 }}</p>
                  <p>{{ selectedAddress.line2 }}</p>
                </div>
                
                <div class="flex gap-2 mt-4">
                  <button 
                    class="btn btn-primary flex-1"
                    @click="showAddressModal = true"
                  >
                    Select Address
                  </button>
                  <button class="btn btn-outline flex-1">
                    Add new address
                  </button>
                </div>
              </div>
              
              <!-- Order Summary -->
              <div class="mb-6">
                <h3 class="text-lg font-medium mb-3">Order Summary</h3>
                <div class="space-y-3">
                  <div class="flex justify-between">
                    <span>Items Price ({{ getSelectedItemsCount }} Items)</span>
                    <span>{{ formatPrice(getTotalPrice) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Shipping Fee</span>
                    <span>{{ formatPrice(shippingFee) }}</span>
                  </div>
                  <div v-if="discount > 0" class="flex justify-between text-success">
                    <span>Discount</span>
                    <span>-{{ formatPrice(discount) }}</span>
                  </div>
                  <div class="divider my-2"/>
                  <div class="flex justify-between font-bold text-lg text-primary">
                    <span>Total Price</span>
                    <span>{{ formatPrice(getTotalPrice + shippingFee - discount) }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Voucher -->
              <div class="mb-6">
                <div class="join w-full">
                  <input 
                    v-model="voucher" 
                    type="text"
                    placeholder="Enter Voucher Code" 
                    class="input input-bordered join-item flex-1"
                  >
                  <button 
                    class="btn btn-primary join-item"
                    @click="applyVoucher"
                  >
                    Apply
                  </button>
                </div>
              </div>
              
              <!-- Checkout Button -->
              <button 
                class="btn btn-primary btn-block btn-lg"
                @click="processCheckout"
              >
                Check Out
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Address Modal -->
    <input id="address-modal" v-model="showAddressModal" type="checkbox" class="modal-toggle" >
    <div class="modal" :class="{'modal-open': showAddressModal}">
      <div class="modal-box">
        <h3 class="font-bold text-lg">Select Delivery Address</h3>
        <div class="py-4">
          <div v-for="address in addresses" :key="address.id" class="mb-4">
            <div class="form-control">
              <label class="label cursor-pointer justify-start gap-3">
                <input 
                  type="radio" 
                  name="addressRadio" 
                  class="radio radio-primary" 
                  :checked="selectedAddress.id === address.id"
                  @change="selectedAddress = address"
                >
                <div>
                  <p>{{ address.line1 }}</p>
                  <p>{{ address.line2 }}</p>
                </div>
              </label>
            </div>
          </div>
        </div>
        <div class="modal-action">
          <button class="btn btn-primary" @click="showAddressModal = false">Confirm</button>
          <button class="btn" @click="showAddressModal = false">Close</button>
        </div>
      </div>
      <label class="modal-backdrop" @click="showAddressModal = false"/>
    </div>
  </div>
</template>

<style scoped>
/* Animation keyframes */
.animate-blob {
  animation: blob-bounce 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes blob-bounce {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}

:deep(.btn-primary) {
  background-color: #f97316;
  border-color: #f97316;
}

:deep(.btn-primary:hover) {
  background-color: #ea580c;
  border-color: #ea580c;
}

:deep(.checkbox-primary), :deep(.radio-primary) {
  --chkbg: #f97316;
  --chkfg: white;
}

:deep(.text-primary) {
  color: #f97316;
}
</style>