//frontend/pages/admin/products.vue
<script setup lang="ts">
import { useAuthStore } from '~/stores/useAuth';
import { definePageMeta } from '#imports'

definePageMeta({
  layout: 'admin',
  middleware: ['auth']
});

interface Category {
  id: number;
  name: string;
  slug: string;
}

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
// pics upload handelers
const isUploading = ref(false);
const imagePreview = ref('');

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


const showAddModal = ref(false);
const showEditModal = ref(false);
const showDeleteModal = ref(false);
const productToDelete = ref<Product | null>(null);


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
  } catch (err) {
    console.error('Error fetching products:', err);
    error.value = err instanceof Error ? err.message : 'Failed to load products data';
  } finally {
    loading.value = false;
  }
};


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
      const errorData = await response.json();
      throw new Error(errorData.message || `Failed to ${showEditModal.value ? 'update' : 'create'} product: ${response.statusText}`);
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
const handleImageUpload = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (!file) return;

  // แสดง Preview ในหน้า UI
  const reader = new FileReader();
  reader.onload = (e: ProgressEvent<FileReader>) => {
    imagePreview.value = e.target?.result as string;
  };
  reader.readAsDataURL(file);

  // อัปโหลดรูปภาพไปยังบริการภายนอก
  const imageFormData = new FormData();
  imageFormData.append('image', file);
  imageFormData.append('key', 'YOUR_API_KEY'); // ใส่ API Key ของคุณที่นี่

  try {
    isUploading.value = true;
    const response = await fetch('https://api.imgbb.com/1/upload', {
      method: 'POST',
      body: imageFormData
    });

    const result = await response.json();

    if (result.success) {
      // เก็บ URL ของรูปภาพลงในฟอร์ม
      formData.value.image_url = result.data.url;
    } else {
      throw new Error('Failed to upload image');
    }
  } catch (error) {
    console.error('Error uploading image:', error);
    alert('Failed to upload image. Please try again.');
  } finally {
    isUploading.value = false;
  }
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
const fetchCategories = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/categories/`, {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch categories: ${response.statusText}`);
    }
    
    const data = await response.json();
    categories.value = data;
  } catch (err) {
    console.error('Error fetching categories:', err);
  }
};

const getCategoryName = (categoryId: number): string => {
  const category = categories.value.find(c => c.id === categoryId);
  if (category) return category.name;
  if (categories.value.length === 0 && categoryId > 0) {
    return `Category ID: ${categoryId}`;
  }
  return 'Uncategorized';
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

onMounted(() => {
  fetchProducts();
  fetchCategories();
});

</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Products Management</h1>
      <button class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700" @click="showAddModal = true">
        Add Product
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center my-12">
      <div class="loader animate-spin h-12 w-12 border-4 border-gray-300 rounded-full border-t-blue-600" />
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 p-4 rounded-lg mb-6">
      <p class="text-red-700">{{ error }}</p>
      <button class="mt-2 text-blue-600 hover:text-blue-800" @click="fetchProducts">Try again</button>
    </div>

    <!-- Product list -->
    <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul class="divide-y divide-gray-200">
        <li v-for="product in products" :key="product.id" class="px-6 py-4 flex items-center justify-between">
          <div class="flex items-center">
            <img v-if="product.image_url" :src="product.image_url" :alt="product.name"
              class="h-16 w-16 object-cover rounded">
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">{{ product.name }}</h3>
              <div class="mt-1 text-sm text-gray-500">
                <p>Category: {{ getCategoryName(product.category) }}</p>
                <p>Brand: {{ product.brand }}</p>
                <p>Price: ${{ product.price }}</p>
                <p class="mt-1">
                  Stock: <span :class="getStockClass(product.stock)">{{ product.stock }}</span>
                </p>
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span :class="getStatusBadgeClass(product.is_active)">
              {{ product.is_active ? 'Active' : 'Inactive' }}
            </span>
            <button class="text-blue-600 hover:text-blue-900" @click="editProduct(product)">
              Edit
            </button>
            <button class="text-red-600 hover:text-red-900" @click="confirmDelete(product)">
              Delete
            </button>
          </div>
        </li>
      </ul>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || showEditModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900">
            {{ showEditModal ? 'Edit Product' : 'Add New Product' }}
          </h3>
          <form class="mt-4" @submit.prevent="handleSubmit">
            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-bold mb-2">Name</label>
              <input v-model="formData.name" type="text" required
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            </div>

            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-bold mb-2">Category</label>
              <select v-model="formData.category" required
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-bold mb-2">Brand</label>
              <input v-model="formData.brand" type="text" required
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            </div>

            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-bold mb-2">Price</label>
              <input v-model.number="formData.price" type="number" step="0.01" required
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            </div>

            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-bold mb-2">Sale Price</label>
              <input v-model.number="formData.sale_price" type="number" step="0.01"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            </div>

            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-bold mb-2">Stock</label>
              <input v-model.number="formData.stock" type="number" required
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            </div>

            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-bold mb-2">SKU</label>
              <input v-model="formData.sku" type="text"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            </div>

            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-bold mb-2">Description</label>
              <textarea v-model="formData.description" required rows="3"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
            </div>
            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-bold mb-2">Product Image</label>
              <div class="flex items-center space-x-4">
                <input type="file" @change="handleImageUpload" accept="image/*"
                  class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                <span v-if="isUploading">Uploading...</span>
              </div>
              <div v-if="imagePreview" class="mt-2">
                <img :src="imagePreview" alt="Preview" class="h-24 w-auto object-contain">
              </div>
            </div>
            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-bold mb-2">Connections</label>
              <input v-model="formData.connections" type="text" required
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            </div>

            <div class="mb-4 space-y-2">
              <label class="flex items-center">
                <input v-model="formData.is_active" type="checkbox" class="form-checkbox h-4 w-4 text-blue-600">
                <span class="ml-2">Active</span>
              </label>

              <label class="flex items-center">
                <input v-model="formData.is_featured" type="checkbox" class="form-checkbox h-4 w-4 text-blue-600">
                <span class="ml-2">Featured</span>
              </label>

              <label class="flex items-center">
                <input v-model="formData.is_new" type="checkbox" class="form-checkbox h-4 w-4 text-blue-600">
                <span class="ml-2">New</span>
              </label>
            </div>

            <div class="flex justify-end space-x-4">
              <button type="button" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
                @click="closeModal">
                Cancel
              </button>
              <button type="submit" :disabled="submitting"
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
                {{ submitting ? 'Saving...' : 'Save' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <h3 class="text-lg font-medium text-gray-900">Confirm Delete</h3>
        <p class="mt-2 text-sm text-gray-500">
          Are you sure you want to delete "{{ productToDelete?.name }}"? This action cannot be undone.
        </p>
        <div class="mt-4 flex justify-end space-x-4">
          <button class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
            @click="showDeleteModal = false">
            Cancel
          </button>
          <button :disabled="deleting"
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 disabled:opacity-50" @click="deleteProduct">
            {{ deleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>