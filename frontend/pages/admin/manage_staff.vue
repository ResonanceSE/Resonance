<script setup lang="ts">
import { useAuthStore } from '~/stores/useAuth';

// Define proper interface for User data
interface StaffUser {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  password?: string;
  is_admin?: boolean;
  is_superuser?: boolean;
  user_type?: string;
  token?: string;
}

interface StaffForm extends Partial<StaffUser> {
  is_submitting: boolean;
  error: string;
}

definePageMeta({
  layout: 'admin',
  middleware: ['auth']
});

const authStore = useAuthStore();
const config = useRuntimeConfig();
const apiUrl = config.public.apiUrl || 'http://localhost:8000';

// State variables
const staffList = ref<StaffUser[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const successMessage = ref<string | null>(null);

// Staff form
const newStaffForm = reactive<StaffForm>({
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  is_superuser: false,
  is_submitting: false,
  error: ''
});

// Edit staff modal state
const showEditModal = ref(false);
const editStaffForm = reactive<StaffForm>({
  id: null as unknown as number,
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  is_superuser: false,
  is_submitting: false,
  error: ''
});

// Confirmation modal for deletion
const showDeleteModal = ref(false);
const staffToDelete = ref<StaffUser | null>(null);
const isDeleting = ref(false);

// Form validation
const validateStaffForm = (form: StaffForm): string => {
  if (!form.username || !form.email) {
    return 'Username and email are required';
  }

  if (form.password && form.password.length < 8) {
    return 'Password must be at least 8 characters';
  }

  // Email format validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(form.email)) {
    return 'Invalid email format';
  }

  return '';
};
watch(() => newStaffForm.is_superuser, (newVal) => {
  console.log("is_superuser changed:", newVal);
});
// Fetch all staff members
const fetchStaff = async () => {
  loading.value = true;
  error.value = null;

  try {
    const response = await fetch(`${apiUrl}/api/admin/staff/`, {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch staff: ${response.statusText}`);
    }

    const data = await response.json();
    staffList.value = data.data || [];
  } catch (err) {
    console.error('Error fetching staff:', err);
    error.value = err instanceof Error ? err.message : 'Failed to load staff data';
  } finally {
    loading.value = false;
  }
};

// Add new staff member
const addStaff = async () => {
  newStaffForm.error = validateStaffForm(newStaffForm);
  if (newStaffForm.error) return;

  newStaffForm.is_submitting = true;
  try {
    console.log("Data to be sent:", newStaffForm);
    const response = await fetch(`${apiUrl}/api/auth/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${authStore.token}`
      },
      body: JSON.stringify({
        username: newStaffForm.username,
        email: newStaffForm.email,
        password: newStaffForm.password,
        first_name: newStaffForm.first_name,
        last_name: newStaffForm.last_name,
        user_type: 'admin',
        is_superuser: newStaffForm.is_superuser
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || `Registration failed: ${response.statusText}`);
    }

    // Clear form and show success message
    successMessage.value = `Staff member ${newStaffForm.username} added successfully!`;
    console.log('Successfully added staff member:', data);
    resetNewStaffForm();
    fetchStaff();
    setTimeout(() => {
      successMessage.value = null;
    }, 3000);
  } catch (err) {
    console.error('Error adding staff:', err);
    newStaffForm.error = err instanceof Error ? err.message : 'Failed to add staff member';
  } finally {
    newStaffForm.is_submitting = false;
  }
};

// Edit staff member
const editStaff = (staff: StaffUser) => {
  editStaffForm.id = staff.id;
  editStaffForm.username = staff.username;
  editStaffForm.email = staff.email;
  editStaffForm.first_name = staff.first_name || '';
  editStaffForm.last_name = staff.last_name || '';
  editStaffForm.is_superuser = staff.is_superuser || false;
  showEditModal.value = true;
};


// Save edited staff
const saveStaffChanges = async () => {
  editStaffForm.error = validateStaffForm(editStaffForm);
  if (editStaffForm.error) return;

  editStaffForm.is_submitting = true;
  try {
    const response = await fetch(`${apiUrl}/api/admin/staff/${editStaffForm.id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${authStore.token}`
      },
      body: JSON.stringify({
        username: editStaffForm.username,
        email: editStaffForm.email,
        first_name: editStaffForm.first_name,
        last_name: editStaffForm.last_name,
        is_superuser: editStaffForm.is_superuser
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `Failed to update staff: ${response.statusText}`);
    }

    // Close modal and refresh list
    showEditModal.value = false;
    fetchStaff();

    // Show success message
    successMessage.value = `Staff member updated successfully!`;
    setTimeout(() => {
      successMessage.value = null;
    }, 3000);
  } catch (err) {
    console.error('Error updating staff:', err);
    editStaffForm.error = err instanceof Error ? err.message : 'Failed to update staff member';
  } finally {
    editStaffForm.is_submitting = false;
  }
};

// Delete staff member confirmation
const confirmDeleteStaff = (staff: StaffUser) => {
  staffToDelete.value = staff;
  showDeleteModal.value = true;
};

// Delete staff member
const deleteStaff = async () => {
  if (!staffToDelete.value) return;

  isDeleting.value = true;
  try {
    const response = await fetch(`${apiUrl}/api/admin/staff/${staffToDelete.value.id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    });

    if (!response.ok) {
      throw new Error(`Failed to delete staff: ${response.statusText}`);
    }

    // Close modal and refresh list
    showDeleteModal.value = false;
    fetchStaff();

    // Show success message
    successMessage.value = `Staff member ${staffToDelete.value.username} removed successfully!`;
    setTimeout(() => {
      successMessage.value = null;
    }, 3000);
  } catch (err) {
    console.error('Error deleting staff:', err);
    error.value = err instanceof Error ? err.message : 'Failed to delete staff member';
  } finally {
    isDeleting.value = false;
    staffToDelete.value = null;
  }
};

// Reset forms
const resetNewStaffForm = () => {
  newStaffForm.username = '';
  newStaffForm.email = '';
  newStaffForm.password = '';
  newStaffForm.first_name = '';
  newStaffForm.last_name = '';
  newStaffForm.error = '';
};

const closeEditModal = () => {
  showEditModal.value = false;
  editStaffForm.error = '';
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  staffToDelete.value = null;
};

// Fetch staff on component mount
onMounted(fetchStaff);
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <svg
xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mr-3 text-primary" fill="none" viewBox="0 0 24 24"
        stroke="currentColor">
        <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
      Manage Staff
    </h1>

    <!-- Success Message -->
    <div v-if="successMessage" class="alert alert-success mb-6">
      <svg
xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
        stroke="currentColor">
        <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>{{ successMessage }}</span>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="alert alert-error mb-6">
      <svg
xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
        stroke="currentColor">
        <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>{{ error }}</span>
      <button class="btn btn-sm btn-ghost ml-4" @click="fetchStaff">Retry</button>
    </div>

    <!-- Add New Staff Form -->
    <div class="card bg-base-100 shadow-xl mb-6">
      <div class="card-body">
        <h2 class="card-title text-lg mb-4">Add New Staff Member</h2>

        <div v-if="newStaffForm.error" class="alert alert-error mb-4">
          <svg
xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ newStaffForm.error }}</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="form-control">
            <label class="label">
              <span class="label-text">Username</span>
            </label>
            <input v-model="newStaffForm.username" type="text" class="input input-bordered" required>
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text">Email</span>
            </label>
            <input v-model="newStaffForm.email" type="email" class="input input-bordered" required>
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text">First Name</span>
            </label>
            <input v-model="newStaffForm.first_name" type="text" class="input input-bordered">
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text">Last Name</span>
            </label>
            <input v-model="newStaffForm.last_name" type="text" class="input input-bordered">
          </div>

          <div class="form-control md:col-span-2">
            <label class="label">
              <span class="label-text">Password</span>
            </label>
            <input v-model="newStaffForm.password" type="password" class="input input-bordered" required>
          </div>
          <div class="form-control mb-4">
            <div class="flex gap-4 cursor-pointer">
              <span class="bold-text">Superuser?</span>
              <input
v-model="newStaffForm.is_superuser" type="checkbox"
                class="checkbox checkbox-primary small-checkbox">
            </div>
          </div>
        </div>

        <div class="card-actions mt-4">
          <button class="btn btn-primary" :disabled="newStaffForm.is_submitting" @click="addStaff">
            <span v-if="newStaffForm.is_submitting">
              <span class="loading loading-spinner loading-xs mr-2" />
              Adding...
            </span>
            <span v-else>Add Staff Member</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Staff List -->
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-lg mb-4">Staff Members</h2>

        <!-- Loading state -->
        <div v-if="loading" class="flex justify-center py-8">
          <div class="loading loading-spinner loading-lg text-primary" />
        </div>

        <!-- Empty state -->
        <div v-else-if="staffList.length === 0" class="text-center py-8 text-gray-500">
          <svg
xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-4 text-gray-400" fill="none"
            viewBox="0 0 24 24" stroke="currentColor">
            <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <p>No staff members found</p>
        </div>

        <!-- Staff table -->
        <div v-else class="overflow-x-auto">
          <table class="table w-full">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Name</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="staff in staffList" :key="staff.id" class="hover">
                <td>{{ staff.username }}</td>
                <td>{{ staff.email }}</td>
                <td>{{ [staff.first_name, staff.last_name].filter(Boolean).join(' ') || 'N/A' }}</td>
                <td>
                  <div class="flex space-x-2">
                    <button class="btn btn-sm btn-info" @click="editStaff(staff)">
                      Edit
                    </button>
                    <button
class="btn btn-sm btn-error"
                      :disabled="staff.id === authStore.user?.id || staff.is_superuser"
                      @click="confirmDeleteStaff(staff)">
                      Remove
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Edit Staff Modal -->
    <div v-if="showEditModal" class="modal modal-open">
      <div class="modal-box max-w-md">
        <h3 class="font-bold text-lg mb-4">Edit Staff Member</h3>

        <div v-if="editStaffForm.error" class="alert alert-error mb-4">
          <svg
xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ editStaffForm.error }}</span>
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text">Username</span>
          </label>
          <input v-model="editStaffForm.username" type="text" class="input input-bordered" required>
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text">Email</span>
          </label>
          <input v-model="editStaffForm.email" type="email" class="input input-bordered" required>
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text">First Name</span>
          </label>
          <input v-model="editStaffForm.first_name" type="text" class="input input-bordered">
        </div>

        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text">Last Name</span>
          </label>
          <input v-model="editStaffForm.last_name" type="text" class="input input-bordered">
        </div>
        <div v-if="editStaffForm.id !== authStore.user?.id" class="form-control mb-4">
          <div class="flex gap-4 cursor-pointer">
            <span class="bold-text">Superuser?</span>
            <input
v-model="editStaffForm.is_superuser" type="checkbox"
              class="checkbox checkbox-primary small-checkbox">
          </div>
        </div>


        <div class="modal-action">
          <button class="btn btn-outline" @click="closeEditModal">
            Cancel
          </button>
          <button class="btn btn-primary" :disabled="editStaffForm.is_submitting" @click="saveStaffChanges">
            <span v-if="editStaffForm.is_submitting">
              <span class="loading loading-spinner loading-xs mr-2" />
              Saving...
            </span>
            <span v-else>Save Changes</span>
          </button>
        </div>
      </div>
      <div class="modal-backdrop bg-neutral bg-opacity-50" @click="closeEditModal" />
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal modal-open">
      <div class="modal-box max-w-md">
        <h3 class="font-bold text-lg mb-4">Confirm Staff Removal</h3>

        <p class="mb-4">
          Are you sure you want to remove <span class="font-semibold">{{ staffToDelete?.username }}</span> from staff?
        </p>

        <div class="modal-action">
          <button class="btn btn-outline" @click="closeDeleteModal">
            Cancel
          </button>
          <button class="btn btn-error" :disabled="isDeleting" @click="deleteStaff">
            <span v-if="isDeleting">
              <span class="loading loading-spinner loading-xs mr-2" />
              Removing...
            </span>
            <span v-else>Remove Staff</span>
          </button>
        </div>
      </div>
      <div class="modal-backdrop bg-neutral bg-opacity-50" @click="closeDeleteModal" />
    </div>
  </div>
</template>

<style scoped></style>