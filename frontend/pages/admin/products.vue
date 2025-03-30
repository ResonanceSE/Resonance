<script setup lang="ts">
import { useAuthStore } from '~/stores/useAuth';

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
  description: string;
  image_url?: string;
  connections: string;
  is_active: boolean;
  is_featured: boolean;
  is_new: boolean;
  slug?: string;
}

// State variables for image handling
const isUploading = ref(false);
const imagePreview = ref('');
const uploadError = ref('');
const uploadSuccess = ref(false);

const authStore = useAuthStore();
const config = useRuntimeConfig();
const apiUrl = config.public.apiUrl || 'http://localhost:8000';
const imgApi = config.public.imgApiKey;

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
  description: '',
  image_url: '',
  connections: '',
  is_active: true,
  is_featured: false,
  is_new: false
});

const handleImageUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  
  if (!file) {
    console.error('No file selected');
    return;
  }

  uploadError.value = '';
  uploadSuccess.value = false;
  
  const validImageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
  if (!validImageTypes.includes(file.type)) {
    uploadError.value = 'Please select a valid image file (JPEG, PNG, GIF, WEBP)';
    return;
  }
  

  if (file.size > 5 * 1024 * 1024) {
    uploadError.value = 'Image size must be less than 5MB';
    return;
  }

  const reader = new FileReader();
  reader.onload = (e: ProgressEvent<FileReader>) => {
    imagePreview.value = e.target?.result as string;
  };
  reader.readAsDataURL(file);

  if (!imgApi) {
    console.error('Image API key is not configured');
    uploadError.value = 'Image upload is not configured. Please contact administrator.';
    return;
  }

  const imageFormData = new FormData();
  imageFormData.append('image', file);

  try {
    isUploading.value = true;
    const response = await fetch(`https://api.imgbb.com/1/upload?key=${imgApi}`, {
      method: 'POST',
      body: imageFormData
    });

    if (!response.ok) {
      throw new Error(`Upload failed with status: ${response.status}`);
    }

    const result = await response.json();
    console.log('ImgBB API response:', result);

    if (result.success) {
      formData.value.image_url = result.data.display_url;
      uploadSuccess.value = true;
      console.log('Image uploaded successfully:', result.data.display_url);
    } else {
      throw new Error(result.error?.message || 'Failed to upload image');
    }
  } catch (error) {
    console.error('Error uploading image:', error);
    uploadError.value = error instanceof Error ? error.message : 'Failed to upload image. Please try again.';
  } finally {
    isUploading.value = false;
  }
};

// Function to remove image
const removeImage = () => {
  imagePreview.value = '';
  formData.value.image_url = '';
  uploadSuccess.value = false;
};

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
    
    console.log('Sending product data:', formData.value);

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
  formData.value = JSON.parse(JSON.stringify(product));
  if (product.image_url) {
    imagePreview.value = product.image_url;
  } else {
    imagePreview.value = '';
  }
  
  // Reset upload states
  uploadError.value = '';
  uploadSuccess.value = false;
  
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
  
  imagePreview.value = '';
  uploadError.value = '';
  uploadSuccess.value = false;
  
  // Reset form data
  formData.value = {
    name: '',
    category: 0,
    brand: '',
    price: 0,
    sale_price: undefined,
    stock: 0,
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
      <button class="btn btn-primary" @click="showAddModal = true">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Add Product
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center my-12">
      <div class="loading loading-spinner loading-lg text-primary"/>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="alert alert-error mb-6">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <div>
        <h3 class="font-bold">Error</h3>
        <div class="text-sm">{{ error }}</div>
      </div>
      <button class="btn btn-sm btn-outline" @click="fetchProducts">Try again</button>
    </div>

    <!-- Product list -->
    <div v-else class="bg-white shadow rounded-lg overflow-hidden">
      <ul class="divide-y divide-gray-200">
        <li v-for="product in products" :key="product.id" class="px-6 py-4 hover:bg-gray-50 transition-colors duration-150">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <div class="flex-shrink-0 h-16 w-16 bg-gray-100 rounded-md overflow-hidden">
                <img
                  v-if="product.image_url" 
                  :src="product.image_url" 
                  :alt="product.name"
                  class="h-full w-full object-cover"
                >
                <div v-else class="h-full w-full flex items-center justify-center text-gray-400">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900">{{ product.name }}</h3>
                <div class="mt-1 text-sm text-gray-500 grid grid-cols-2 gap-x-4 gap-y-1">
                  <p>Category: <span class="font-medium">{{ getCategoryName(product.category).toLowerCase() === 'earbuds' ? 'Earbuds / IEMS' : getCategoryName(product.category) }}</span></p>
                  <p>Brand: <span class="font-medium">{{ product.brand }}</span></p>
                  <p>Price: <span class="font-medium">${{ product.price }}</span></p>
                  <p>
                    Stock: <span :class="getStockClass(product.stock)" class="font-medium">{{ product.stock }}</span>
                  </p>
                </div>
              </div>
            </div>
            <div class="flex items-center space-x-3">
              <span :class="getStatusBadgeClass(product.is_active)">
                {{ product.is_active ? 'Active' : 'Inactive' }}
              </span>
              <button 
                class="btn btn-sm btn-outline btn-info" 
                @click="editProduct(product)"
              >
                Edit
              </button>
              <button 
                class="btn btn-sm btn-outline btn-error" 
                @click="confirmDelete(product)"
              >
                Delete
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Add/Edit Product Modal -->
    <div v-if="showAddModal || showEditModal" class="modal modal-open">
      <div class="modal-box max-w-3xl">
        <h3 class="font-bold text-lg mb-6 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          {{ showEditModal ? 'Edit Product' : 'Add New Product' }}
        </h3>
        
        <form class="space-y-6" @submit.prevent="handleSubmit">
          <!-- Two-column layout for form -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Left column: Basic info -->
            <div class="space-y-4">
              <div class="form-control">
                <label class="label">
                  <span class="label-text font-semibold">Product Name*</span>
                </label>
                <input
                  v-model="formData.name" 
                  type="text" 
                  required
                  placeholder="Enter product name"
                  class="input input-bordered w-full"
                >
              </div>

              <div class="form-control">
                <label class="label">
                  <span class="label-text font-semibold">Category*</span>
                </label>
                <select
                  v-model="formData.category" 
                  required
                  class="select select-bordered w-full"
                >
                  <option disabled value="0">Select a category</option>
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name.toLowerCase() === "earbuds" ? "Earbuds / IEMS" : category.name }}
                  </option>
                </select>
              </div>

              <div class="form-control">
                <label class="label">
                  <span class="label-text font-semibold">Brand*</span>
                </label>
                <input
                  v-model="formData.brand" 
                  type="text" 
                  required
                  placeholder="Enter brand name"
                  class="input input-bordered w-full"
                >
              </div>

              <div class="form-control">
                <label class="label">
                  <span class="label-text font-semibold">Connections*</span>
                </label>
                <input
                  v-model="formData.connections" 
                  type="text" 
                  required
                  placeholder="e.g. Bluetooth 5.0, 3.5mm"
                  class="input input-bordered w-full"
                >
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Price*</span>
                  </label>
                  <div class="input-group">
                    <span>$</span>
                    <input
                      v-model.number="formData.price" 
                      type="number" 
                      step="0.01" 
                      required
                      min="0.01"
                      placeholder="0.00"
                      class="input input-bordered w-full"
                    >
                  </div>
                </div>

                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Sale Price</span>
                  </label>
                  <div class="input-group">
                    <span>$</span>
                    <input
                      v-model.number="formData.sale_price" 
                      type="number" 
                      step="0.01"
                      min="0"
                      placeholder="0.00"
                      class="input input-bordered w-full"
                    >
                  </div>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Stock*</span>
                  </label>
                  <input
                    v-model.number="formData.stock" 
                    type="number" 
                    required
                    min="0"
                    placeholder="0"
                    class="input input-bordered w-full"
                  >
                </div>
              </div>
            </div>

            <!-- Right column: Image, description, flags -->
            <div class="space-y-4">
              <!-- Image upload area with preview -->
              <div class="form-control">
                <label class="label">
                  <span class="label-text font-semibold">Product Image</span>
                </label>
                <div class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-4">
                  <!-- Image preview -->
                  <div v-if="formData.image_url && imagePreview" class="mb-4 flex justify-center">
                    <div class="relative rounded-lg border overflow-hidden" style="width: 200px; height: 150px;">
                      <img :src="imagePreview" alt="Product image" class="w-full h-full object-contain">
                      <button
                        type="button"
                        class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
                        title="Remove image"
                        @click="removeImage"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                        </svg>
                      </button>
                    </div>
                  </div>

                  <!-- Upload button -->
                  <div v-if="!formData.image_url || !imagePreview" class="flex flex-col items-center justify-center">
                    <label class="w-full flex flex-col items-center px-4 py-6 bg-white text-blue rounded-lg shadow-lg tracking-wide border border-blue cursor-pointer hover:bg-blue-50 transition">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      <span class="mt-2 text-base leading-normal">Select an image</span>
                      <input 
                        type="file" 
                        class="hidden" 
                        accept="image/*"
                        @change="handleImageUpload"
                      >
                    </label>
                  </div>
                  
                  <!-- Change image button when image exists -->
                  <div v-else class="flex justify-center mt-2">
                    <label class="cursor-pointer inline-flex items-center px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span>Change Image</span>
                      <input 
                        type="file" 
                        class="hidden" 
                        accept="image/*"
                        @change="handleImageUpload"
                      >
                    </label>
                  </div>
                  
                  <!-- Loading indicator -->
                  <div v-if="isUploading" class="flex justify-center mt-4">
                    <div class="flex items-center space-x-2">
                      <div class="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"/>
                      <span class="text-sm text-gray-600">Uploading...</span>
                    </div>
                  </div>
                  
                  <!-- Error message -->
                  <p v-if="uploadError" class="mt-2 text-sm text-red-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                    {{ uploadError }}
                  </p>
                  
                  <!-- Success message -->
                  <p v-if="uploadSuccess" class="mt-2 text-sm text-green-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                    Image uploaded successfully
                  </p>
                </div>
              </div>

              <div class="form-control">
                <label class="label">
                  <span class="label-text font-semibold">Description*</span>
                </label>
                <textarea
                  v-model="formData.description" 
                  rows="5"
                  required
                  placeholder="Enter product description"
                  class="textarea textarea-bordered w-full h-32"
                />
              </div>

              <div class="form-control">
                <label class="label">
                  <span class="label-text font-semibold">Product Status</span>
                </label>
                <div class="bg-gray-50 p-4 rounded-lg space-y-3">
                  <label class="cursor-pointer flex items-center gap-3">
                    <input v-model="formData.is_active" type="checkbox" class="toggle toggle-primary" >
                    <span>Active</span>
                    <span class="text-xs text-gray-500">— Product is available for purchase</span>
                  </label>

                  <label class="cursor-pointer flex items-center gap-3">
                    <input v-model="formData.is_featured" type="checkbox" class="toggle toggle-accent" >
                    <span>Featured</span>
                    <span class="text-xs text-gray-500">— Highlight product on homepage</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
          
          <div class="modal-action border-t pt-4">
            <button
              type="button" 
              class="btn btn-outline"
              @click="closeModal"
            >
              Cancel
            </button>
            <button
              type="submit" 
              class="btn btn-primary"
              :disabled="submitting"
            >
              <div v-if="submitting" class="flex items-center">
                <span class="loading loading-spinner loading-xs mr-2"/>
                Saving...
              </div>
              <span v-else>{{ showEditModal ? 'Update Product' : 'Create Product' }}</span>
            </button>
          </div>
        </form>
      </div>
      
      <label class="modal-backdrop" @click="closeModal"/>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal modal-open">
      <div class="modal-box">
        <h3 class="font-bold text-lg text-error flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Delete Product
        </h3>
        <p class="py-4">
          Are you sure you want to delete "<span class="font-semibold">{{ productToDelete?.name }}</span>"? This action cannot be undone.
        </p>
        <div class="modal-action">
          <button
            class="btn btn-outline"
            @click="showDeleteModal = false"
          >
            Cancel
          </button>
          <button
            class="btn btn-error"
            :disabled="deleting"
            @click="deleteProduct"
          >
            <div v-if="deleting" class="flex items-center">
              <span class="loading loading-spinner loading-xs mr-2"/>
              Deleting...
            </div>
            <span v-else>Delete</span>
          </button>
        </div>
      </div>
      <label class="modal-backdrop" @click="showDeleteModal = false"/>
    </div>
  </div>
</template>

<style scoped>
/* Add any additional styles here */
</style>