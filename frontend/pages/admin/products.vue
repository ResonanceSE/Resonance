//frontend/pages/admin/products.vue
<script setup lang="ts">
import { useAuthStore } from '~/stores/useAuth';

definePageMeta({
  layout: 'admin'
});


interface Product {
  id: number;
  name: string;
  category: number;
  brand: string;
  price: number;
  sale_price?: number;
  stock: number;
  sku: string;
  description: string;
  image_url?: string;
  connections: string;
  is_active: boolean;
  is_featured: boolean;
  is_new: boolean;
  slug?: string;
}

interface Category {
  id: number;
  name: string;
  slug: string;
}

const authStore = useAuthStore();
const config = useRuntimeConfig();
const apiUrl = config.public.apiUrl || 'http://localhost:8000';

// State variables
const products = ref<Product[]>([]);
const categories = ref<Category[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const submitting = ref(false);
const deleting = ref(false);

// UI control
const showAddModal = ref(false);
const showEditModal = ref(false);
const showDeleteModal = ref(false);
const productToDelete = ref<Product | null>(null);

// Form data for adding/editing
const formData = ref<Partial<Product>>({
  name: '',
  category: 0,
  brand: '',
  price: 0,
  sale_price: undefined,
  stock: 0,
  sku: '',
  description: '',
  image_url: '',
  connections: '',
  is_active: true,
  is_featured: false,
  is_new: false
});

// Fetch products and categories on component mount
const fetchProducts = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await fetch(`${apiUrl}/api/staff/products/`, {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch products: ${response.statusText}`);
    }
    
    const data = await response.json();
    products.value = data;
    
    // Also fetch categories
    await fetchCategories();
  } catch (err) {
    console.error('Error fetching products:', err);
    error.value = err instanceof Error ? err.message : 'Failed to load products data';
  } finally {
    loading.value = false;
  }
};

const fetchCategories = async () => {
  try {
    // We're using a simplified approach here - just hardcoding categories
    // In a real implementation, you'd fetch these from an API endpoint
    categories.value = [
      { id: 1, name: 'Headphones', slug: 'headphones' },
      { id: 2, name: 'Speakers', slug: 'speakers' },
      { id: 3, name: 'Earbuds', slug: 'earbuds' },
      { id: 4, name: 'Accessories', slug: 'accessories' },
      { id: 5, name: 'Microphones', slug: 'microphones' }
    ];
  } catch (err) {
    console.error('Error fetching categories:', err);
    // Not stopping the show for categories
  }
};

// CRUD operations
const handleSubmit = async () => {
  submitting.value = true;
  
  try {
    const url = showEditModal.value 
      ? `${apiUrl}/api/staff/products/${formData.value.id}/` 
      : `${apiUrl}/api/staff/products/`;
    
    const method = showEditModal.value ? 'PUT' : 'POST';
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${authStore.token}`
      },
      body: JSON.stringify(formData.value)
    });
    
    if (!response.ok) {
      throw new Error(`Failed to ${showEditModal.value ? 'update' : 'create'} product: ${response.statusText}`);
    }
    
    await fetchProducts();
    closeModal();
  } catch (err) {
    console.error('Error saving product:', err);
    alert(err instanceof Error ? err.message : 'Failed to save product');
  } finally {
    submitting.value = false;
  }
};

const editProduct = (product: Product) => {
  formData.value = { ...product };
  showEditModal.value = true;
};

const confirmDelete = (product: Product) => {
  productToDelete.value = product;
  showDeleteModal.value = true;
};

const deleteProduct = async () => {
  if (!productToDelete.value) return;
  
  deleting.value = true;
  
  try {
    const response = await fetch(`${apiUrl}/api/staff/products/${productToDelete.value.id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to delete product: ${response.statusText}`);
    }
    
    await fetchProducts();
    showDeleteModal.value = false;
    productToDelete.value = null;
  } catch (err) {
    console.error('Error deleting product:', err);
    alert(err instanceof Error ? err.message : 'Failed to delete product');
  } finally {
    deleting.value = false;
  }
};

const getCategoryName = (categoryId: number): string => {
  const category = categories.value.find(c => c.id === categoryId);
  return category ? category.name : 'Uncategorized';
};

const getStockClass = (stock: number): string => {
  if (stock <= 0) return 'text-red-600 font-bold';
  if (stock < 10) return 'text-orange-600 font-medium';
  return 'text-green-600';
};

const getStatusBadgeClass = (isActive: boolean): string => {
  return isActive
    ? 'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800'
    : 'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800';
};

const closeModal = () => {
  showAddModal.value = false;
  showEditModal.value = false;
  formData.value = {
    name: '',
    category: 0,
    brand: '',
    price: 0,
    sale_price: undefined,
    stock: 0,
    sku: '',
    description: '',
    image_url: '',
    connections: '',
    is_active: true,
    is_featured: false,
    is_new: false
  };
};

onMounted(fetchProducts);
</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Products Management</h1>
      <button
        @click="showAddModal = true"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Add Product
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center my-12">
      <div class="loader animate-spin h-12 w-12 border-4 border-gray-300 rounded-full border-t-blue-600"></div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 p-4 rounded-lg mb-6">
      <p class="text-red-700">{{ error }}</p>
      <button @click="fetchProducts" class="mt-2 text-blue-600 hover:text-blue-800">Try again</button>
    </div>

    <!-- Empty state -->
    <div v-else-if="products.length === 0" class="bg-gray-50 p-8 rounded-lg text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
      </svg>
      <h3 class="text-lg font-medium text-gray-900 mb-2">No products found</h3>
      <p class="text-gray-500 mb-4">Get started by adding your first product.</p>
      <button 
        @click="showAddModal = true" 
        class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
      >
        <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Add a Product
      </button>
    </div>

    <!-- Products Table -->
    <div v-else class="bg-white rounded-lg shadow overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Price</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stock</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="product in products" :key="product.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="h-10 w-10 flex-shrink-0 mr-3">
                  <img v-if="product.image_url" :src="product.image_url" class="h-10 w-10 rounded-full object-cover" alt="" />
                  <div v-else class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>
                <div>
                  <div class="text-sm font-medium text-gray-900">{{ product.name }}</div>
                  <div class="text-sm text-gray-500">SKU: {{ product.sku || 'N/A' }}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ getCategoryName(product.category) }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">${{ product.price }}</div>
              <div v-if="product.sale_price" class="text-xs text-red-500">Sale: ${{ product.sale_price }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <span :class="getStockClass(product.stock)">{{ product.stock }}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="getStatusBadgeClass(product.is_active)">
                {{ product.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button
                @click="editProduct(product)"
                class="text-blue-600 hover:text-blue-900 mr-3"
              >
                Edit
              </button>
              <button
                @click="confirmDelete(product)"
                class="text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Product Modal -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">
            {{ showEditModal ? 'Edit Product' : 'Add New Product' }}
          </h2>
          <button 
            @click="closeModal" 
            class="text-gray-500 hover:text-gray-700"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="col-span-2">
              <label class="block text-sm font-medium text-gray-700">Name</label>
              <input
                v-model="formData.name"
                type="text"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Category</label>
              <select
                v-model="formData.category"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              >
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Brand</label>
              <input
                v-model="formData.brand"
                type="text"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Price ($)</label>
              <input
                v-model="formData.price"
                type="number"
                step="0.01"
                min="0"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Sale Price ($)</label>
              <input
                v-model="formData.sale_price"
                type="number"
                step="0.01"
                min="0"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Stock</label>
              <input
                v-model="formData.stock"
                type="number"
                min="0"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">SKU</label>
              <input
                v-model="formData.sku"
                type="text"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>

            <div class="col-span-2">
              <label class="block text-sm font-medium text-gray-700">Image URL</label>
              <input
                v-model="formData.image_url"
                type="url"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>

            <div class="col-span-2">
              <label class="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                v-model="formData.description"
                rows="3"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Connections</label>
              <input
                v-model="formData.connections"
                type="text"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
              <p class="mt-1 text-xs text-gray-500">E.g., "Bluetooth 5.0, 3.5mm"</p>
            </div>

            <div class="flex flex-col justify-end">
              <div class="flex items-center mt-4 space-x-4">
                <div class="form-control">
                  <label class="cursor-pointer label">
                    <span class="label-text mr-2">Active</span> 
                    <input v-model="formData.is_active" type="checkbox" class="toggle toggle-primary" />
                  </label>
                </div>
                <div class="form-control">
                  <label class="cursor-pointer label">
                    <span class="label-text mr-2">Featured</span> 
                    <input v-model="formData.is_featured" type="checkbox" class="toggle toggle-primary" />
                  </label>
                </div>
                <div class="form-control">
                  <label class="cursor-pointer label">
                    <span class="label-text mr-2">New</span> 
                    <input v-model="formData.is_new" type="checkbox" class="toggle toggle-primary" />
                  </label>
                </div>
              </div>
            </div>
          </div>

          <div class="flex justify-end mt-6 space-x-3">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              :disabled="submitting"
            >
              <span v-if="submitting">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
              <span v-else>{{ showEditModal ? 'Update Product' : 'Create Product' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Confirm Delete Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg w-full max-w-md">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Confirm Delete</h3>
        <p class="text-gray-700 mb-4">
          Are you sure you want to delete the product "{{ productToDelete?.name }}"? This action cannot be undone.
        </p>
        <div class="flex justify-end space-x-3">
          <button
            @click="showDeleteModal = false"
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200"
          >
            Cancel
          </button>
          <button
            @click="deleteProduct"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
            :disabled="deleting"
          >
            <span v-if="deleting">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Deleting...
            </span>
            <span v-else>Delete</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped>
/* You can add any specific styles here */
</style>