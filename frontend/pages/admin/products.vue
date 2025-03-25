<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Products Management</h1>
      <button
        @click="showAddModal = true"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Add Product
      </button>
    </div>

    <!-- Products Table -->
    <div class="bg-white rounded-lg shadow overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Price</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stock</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="product in products" :key="product.id">
            <td class="px-6 py-4">{{ product.name }}</td>
            <td class="px-6 py-4">{{ product.category }}</td>
            <td class="px-6 py-4">${{ product.price }}</td>
            <td class="px-6 py-4">{{ product.stock }}</td>
            <td class="px-6 py-4">
              <button
                @click="editProduct(product)"
                class="text-blue-600 hover:text-blue-800 mr-3"
              >
                Edit
              </button>
              <button
                @click="deleteProduct(product.id)"
                class="text-red-600 hover:text-red-800"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Product Modal -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg w-full max-w-lg">
        <h2 class="text-xl font-semibold mb-4">
          {{ showEditModal ? 'Edit Product' : 'Add New Product' }}
        </h2>
        
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Name</label>
            <input
              v-model="formData.name"
              type="text"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Category</label>
            <select
              v-model="formData.category"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              required
            >
              <option value="Speakers">Speakers</option>
              <option value="Earbuds">Earbuds</option>
              <option value="Accessories">Accessories</option>
              <option value="Microphones">Microphones</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Price</label>
            <input
              v-model="formData.price"
              type="number"
              step="0.01"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Stock</label>
            <input
              v-model="formData.stock"
              type="number"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Description</label>
            <textarea
              v-model="formData.description"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              rows="3"
              required
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Image URL</label>
            <input
              v-model="formData.image"
              type="url"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              required
            />
          </div>

          <div class="flex justify-end space-x-3 mt-6">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 border rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {{ showEditModal ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '~/stores/auth';

definePageMeta({
  layout: 'admin'
});

interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  stock: number;
  description: string;
  image: string;
}

const products = ref<Product[]>([]);
const showAddModal = ref(false);
const showEditModal = ref(false);
const formData = ref({
  id: null as number | null,
  name: '',
  category: '',
  price: 0,
  stock: 0,
  description: '',
  image: ''
});

// Fetch products
const fetchProducts = async () => {
  try {
    const response = await fetch('/api/staff/products/', {
      headers: {
        'Authorization': `Token ${useAuthStore().token}`
      }
    });
    
    if (response.ok) {
      products.value = await response.json();
    }
  } catch (error) {
    console.error('Error fetching products:', error);
  }
};

// Add/Edit product
const handleSubmit = async () => {
  const url = formData.value.id
    ? `/api/staff/products/${formData.value.id}/`
    : '/api/staff/products/';
    
  const method = formData.value.id ? 'PUT' : 'POST';
  
  try {
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${useAuthStore().token}`
      },
      body: JSON.stringify(formData.value)
    });
    
    if (response.ok) {
      await fetchProducts();
      closeModal();
    }
  } catch (error) {
    console.error('Error saving product:', error);
  }
};

// Delete product
const deleteProduct = async (id: number) => {
  if (!confirm('Are you sure you want to delete this product?')) return;
  
  try {
    const response = await fetch(`/api/staff/products/${id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Token ${useAuthStore().token}`
      }
    });
    
    if (response.ok) {
      await fetchProducts();
    }
  } catch (error) {
    console.error('Error deleting product:', error);
  }
};

// Edit product
const editProduct = (product: Product) => {
  formData.value = { ...product };
  showEditModal.value = true;
};

// Close modal
const closeModal = () => {
  showAddModal.value = false;
  showEditModal.value = false;
  formData.value = {
    id: null,
    name: '',
    category: '',
    price: 0,
    stock: 0,
    description: '',
    image: ''
  };
};

onMounted(fetchProducts);
</script> 