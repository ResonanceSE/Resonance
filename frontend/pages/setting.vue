<script setup>
import { useAuthStore } from '~/stores/useAuth';
import { ref, reactive, onMounted } from 'vue';

definePageMeta({
    layout: 'default',
    middleware: ['auth']
});

const authStore = useAuthStore();
const isLoading = ref(true);
const isSaving = ref(false);
const userLoaded = ref(false);
const generalError = ref('');
const successMessage = ref('');
const currentTab = ref('profile');

// Form validation state
const usernameChanged = ref(false);
const addressChanged = ref(false);
const isEditingAddress = ref(false);
const hasAddress = ref(false);

// Profile form
const profileForm = reactive({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    originalUsername: '',
    usernameError: ''
});

// Address form
const addressForm = reactive({
    recipient_name: '',
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    postal_code: '',
    country: '',
    is_default: true,
    addressError: ''
});

// Load user data
const loadUserData = async () => {
    isLoading.value = true;
    generalError.value = '';

    try {
        // If we already have user data in authStore, use it
        if (authStore.user) {
            profileForm.username = authStore.user.username || '';
            profileForm.originalUsername = authStore.user.username || '';
            profileForm.email = authStore.user.email || '';
            profileForm.first_name = authStore.user.first_name || '';
            profileForm.last_name = authStore.user.last_name || '';

            // Load shipping address if available in user data
            if (authStore.user.address) {
                const addressParts = authStore.user.address.split('\n');
                if (addressParts.length >= 1) addressForm.recipient_name = addressParts[0];
                if (addressParts.length >= 2) addressForm.address_line1 = addressParts[1];
                if (addressParts.length >= 3) addressForm.address_line2 = addressParts[2];

                // The city, state, postal code might be in one line
                if (addressParts.length >= 4) {
                    const cityStateParts = addressParts[3].split(',');
                    if (cityStateParts.length >= 1) addressForm.city = cityStateParts[0].trim();

                    if (cityStateParts.length >= 2) {
                        const stateZipParts = cityStateParts[1].trim().split(' ');
                        addressForm.state = stateZipParts[0] || '';
                        if (stateZipParts.length >= 2) {
                            addressForm.postal_code = stateZipParts.slice(1).join(' ');
                        }
                    }
                }

                if (addressParts.length >= 5) addressForm.country = addressParts[4];

                // Mark that we have an address
                hasAddress.value = true;
            }

            userLoaded.value = true;
        } else {
            // If not, fetch user data from API
            const config = useRuntimeConfig();
            const apiUrl = config.public.apiUrl || 'http://127.0.0.1:8000';

            const response = await fetch(`${apiUrl}/api/auth/user/`, {
                headers: {
                    'Authorization': `Token ${authStore.token}`
                }
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch user data: ${response.statusText}`);
            }

            const userData = await response.json();

            if (userData.status === 'success' && userData.data) {
                profileForm.username = userData.data.username || '';
                profileForm.originalUsername = userData.data.username || '';
                profileForm.email = userData.data.email || '';
                profileForm.first_name = userData.data.first_name || '';
                profileForm.last_name = userData.data.last_name || '';

                // Parse address if available
                if (userData.data.address) {
                    const addressParts = userData.data.address.split('\n');
                    if (addressParts.length >= 1) addressForm.recipient_name = addressParts[0];
                    if (addressParts.length >= 2) addressForm.address_line1 = addressParts[1];
                    if (addressParts.length >= 3) addressForm.address_line2 = addressParts[2];

                    // The city, state, postal code might be in one line
                    if (addressParts.length >= 4) {
                        const cityStateParts = addressParts[3].split(',');
                        if (cityStateParts.length >= 1) addressForm.city = cityStateParts[0].trim();

                        if (cityStateParts.length >= 2) {
                            const stateZipParts = cityStateParts[1].trim().split(' ');
                            addressForm.state = stateZipParts[0] || '';
                            if (stateZipParts.length >= 2) {
                                addressForm.postal_code = stateZipParts.slice(1).join(' ');
                            }
                        }
                    }

                    if (addressParts.length >= 5) addressForm.country = addressParts[4];
                }

                userLoaded.value = true;
            }
        }
    } catch (error) {
        console.error('Error loading user data:', error);
        generalError.value = 'Failed to load user data. Please try refreshing the page.';
    } finally {
        isLoading.value = false;
    }
};

// Update username
const updateUsername = async () => {
    if (!usernameChanged.value) return true;

    profileForm.usernameError = '';

    // Validate username
    if (!profileForm.username) {
        profileForm.usernameError = 'Username is required';
        return false;
    }

    if (profileForm.username === profileForm.originalUsername) {
        // No changes, skip update
        return true;
    }

    isSaving.value = true;

    try {
        const config = useRuntimeConfig();
        const apiUrl = config.public.apiUrl || 'http://127.0.0.1:8000';

        const response = await fetch(`${apiUrl}/api/auth/update-username/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${authStore.token}`
            },
            body: JSON.stringify({
                username: profileForm.username
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `Failed to update username: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.status === 'success') {
            // Update local user data
            if (authStore.user) {
                authStore.user.username = profileForm.username;
            }

            profileForm.originalUsername = profileForm.username;
            usernameChanged.value = false;
            return true;
        } else {
            throw new Error(result.message || 'Failed to update username');
        }
    } catch (error) {
        console.error('Error updating username:', error);
        profileForm.usernameError = error.message || 'Failed to update username';
        return false;
    } finally {
        isSaving.value = false;
    }
};

// Update address
const updateAddress = async () => {
    if (!addressChanged.value) return true;

    addressForm.addressError = '';

    // Validate required address fields
    if (!addressForm.recipient_name || !addressForm.address_line1 || !addressForm.city || !addressForm.postal_code || !addressForm.country) {
        addressForm.addressError = 'Please fill in all required address fields';
        return false;
    }

    isSaving.value = true;

    try {
        const config = useRuntimeConfig();
        const apiUrl = config.public.apiUrl || 'http://127.0.0.1:8000';

        // Format address for API
        const formattedAddress = [
            addressForm.recipient_name,
            addressForm.address_line1,
            addressForm.address_line2,
            `${addressForm.city}, ${addressForm.state} ${addressForm.postal_code}`,
            addressForm.country
        ].filter(Boolean).join('\n');

        const response = await fetch(`${apiUrl}/api/auth/update-address/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${authStore.token}`
            },
            body: JSON.stringify({
                address: formattedAddress,
                is_default: addressForm.is_default
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `Failed to update address: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.status === 'success') {
            // Update local user data if available
            if (authStore.user) {
                authStore.user.address = formattedAddress;
            }

            addressChanged.value = false;
            return true;
        } else {
            throw new Error(result.message || 'Failed to update address');
        }
    } catch (error) {
        console.error('Error updating address:', error);
        addressForm.addressError = error.message || 'Failed to update address';
        return false;
    } finally {
        isSaving.value = false;
    }
};

// Save settings
const saveSettings = async () => {
    generalError.value = '';
    successMessage.value = '';

    try {
        let success = true;

        if (currentTab.value === 'profile') {
            success = await updateUsername();
        } else if (currentTab.value === 'address') {
            success = await updateAddress();
        }

        if (success) {
            successMessage.value = 'Your settings have been updated successfully!';

            // Clear success message after 5 seconds
            setTimeout(() => {
                successMessage.value = '';
            }, 5000);
        }
    } catch (error) {
        console.error('Error saving settings:', error);
        generalError.value = 'Failed to save settings. Please try again.';
    }
};

// Watch for username changes
watch(() => profileForm.username, (newValue) => {
    if (newValue !== profileForm.originalUsername) {
        usernameChanged.value = true;
    } else {
        usernameChanged.value = false;
    }
});

// Watch for address form changes
watch([
    () => addressForm.recipient_name,
    () => addressForm.address_line1,
    () => addressForm.address_line2,
    () => addressForm.city,
    () => addressForm.state,
    () => addressForm.postal_code,
    () => addressForm.country
], () => {
    addressChanged.value = true;
});

// Load user data when component mounts
onMounted(loadUserData);
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12 relative overflow-hidden">
        <!-- Decorative circles -->
        <div
            class="absolute top-20 left-10 w-64 h-64 bg-orange-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob" />
        <div
            class="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000" />
        <div
            class="absolute -bottom-8 left-40 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000" />

        <div class="container mx-auto px-4">
            <!-- Page Header -->
            <div class="mb-8 text-center">
                <h1 class="text-3xl font-bold">
                    <span
                        class="bg-gradient-to-r from-blue-500 to-indigo-600 bg-clip-text text-transparent">Account</span>
                    <span class="relative">
                        Settings
                        <span class="absolute -bottom-1 left-0 w-full h-1 bg-orange-400 rounded-full" />
                    </span>
                </h1>
                <p class="mt-2 text-gray-600">Manage your account preferences</p>
            </div>

            <!-- Loading State -->
            <div v-if="isLoading" class="flex justify-center py-12">
                <div class="loading loading-spinner loading-lg text-orange-500" />
            </div>

            <!-- Not logged in state -->
            <div
v-else-if="!authStore.isAuthenticated"
                class="bg-white rounded-lg shadow-xl p-8 max-w-md mx-auto text-center">
                <div class="w-16 h-16 mx-auto bg-orange-100 rounded-full flex items-center justify-center mb-4">
                    <svg
xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-orange-500" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                </div>
                <h2 class="text-2xl font-bold mb-4">Please Sign In</h2>
                <p class="text-gray-600 mb-6">You need to be logged in to access your settings</p>
                <NuxtLink to="/login" class="btn btn-primary">
                    Go to Login
                </NuxtLink>
            </div>

            <!-- Settings Content -->
            <div v-else-if="userLoaded" class="grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
                <!-- Left sidebar with tabs -->
                <div class="lg:col-span-1">
                    <div class="bg-white rounded-lg shadow-md overflow-hidden">
                        <div class="p-4 bg-gray-50 border-b border-gray-200">
                            <div class="flex items-center space-x-3">
                                <div class="avatar placeholder">
                                    <div class="bg-primary text-neutral-content rounded-full w-12">
                                        <span>{{ profileForm.username.charAt(0).toUpperCase() }}</span>
                                    </div>
                                </div>
                                <div>
                                    <h3 class="font-medium text-gray-800">{{ profileForm.username }}</h3>
                                    <p class="text-xs text-gray-500">{{ profileForm.email }}</p>
                                </div>
                            </div>
                        </div>
                        <div class="p-2">
                            <ul class="menu menu-lg p-0">
                                <li>
                                    <a
:class="{ 'active bg-primary/10 text-primary': currentTab === 'profile' }"
                                        @click="currentTab = 'profile'">
                                        <svg
xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                            viewBox="0 0 24 24" stroke="currentColor">
                                            <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                        </svg>
                                        Account Profile
                                    </a>
                                </li>
                                <li>
                                    <a
:class="{ 'active bg-primary/10 text-primary': currentTab === 'address' }"
                                        @click="currentTab = 'address'">
                                        <svg
xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                            viewBox="0 0 24 24" stroke="currentColor">
                                            <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                            <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                        </svg>
                                        Shipping Address
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- Right content panel -->
                <div class="lg:col-span-2">
                    <div class="bg-white rounded-lg shadow-md overflow-hidden">
                        <!-- Error/Success messages -->
                        <div v-if="generalError" class="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
                            <div class="flex">
                                <div class="flex-shrink-0">
                                    <svg
class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 20 20" fill="currentColor">
                                        <path
fill-rule="evenodd"
                                            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                            clip-rule="evenodd" />
                                    </svg>
                                </div>
                                <div class="ml-3">
                                    <p class="text-sm text-red-700">{{ generalError }}</p>
                                </div>
                            </div>
                        </div>

                        <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
                            <div class="flex">
                                <div class="flex-shrink-0">
                                    <svg
class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 20 20" fill="currentColor">
                                        <path
fill-rule="evenodd"
                                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                            clip-rule="evenodd" />
                                    </svg>
                                </div>
                                <div class="ml-3">
                                    <p class="text-sm text-green-700">{{ successMessage }}</p>
                                </div>
                            </div>
                        </div>

                        <!-- Profile Tab -->
                        <div v-if="currentTab === 'profile'" class="p-6">
                            <h2 class="text-xl font-semibold mb-6">Account Profile</h2>

                            <div class="space-y-6">
                                <!-- Username field -->
                                <div class="form-control">
                                    <label class="label">
                                        <span class="label-text font-medium">Username</span>
                                    </label>
                                    <input
v-model="profileForm.username" type="text" placeholder="Enter username"
                                        class="input input-bordered w-full"
                                        :class="{ 'input-error': profileForm.usernameError }">
                                    <label v-if="profileForm.usernameError" class="label">
                                        <span class="label-text-alt text-error">{{ profileForm.usernameError }}</span>
                                    </label>
                                </div>

                                <!-- Email field (readonly) -->
                                <div class="form-control">
                                    <label class="label">
                                        <span class="label-text font-medium">Email Address</span>
                                    </label>
                                    <input
v-model="profileForm.email" type="email" readonly disabled
                                        class="input input-bordered w-full bg-gray-50 opacity-70">
                                    <label class="label">
                                        <span class="label-text-alt text-gray-500">Email cannot be changed</span>
                                    </label>
                                </div>

                                <!-- First Name field (optional, disabled for simplicity) -->
                                <div class="form-control">
                                    <label class="label">
                                        <span class="label-text font-medium">First Name</span>
                                    </label>
                                    <input
v-model="profileForm.first_name" type="text" disabled readonly
                                        class="input input-bordered w-full bg-gray-50 opacity-70">
                                </div>

                                <!-- Last Name field (optional, disabled for simplicity) -->
                                <div class="form-control">
                                    <label class="label">
                                        <span class="label-text font-medium">Last Name</span>
                                    </label>
                                    <input
v-model="profileForm.last_name" type="text" disabled readonly
                                        class="input input-bordered w-full bg-gray-50 opacity-70">
                                </div>

                                <!-- Save Button -->
                                <div class="mt-8">
                                    <button
class="btn btn-primary w-full sm:w-auto"
                                        :disabled="isSaving || !usernameChanged" @click="saveSettings">
                                        <span v-if="isSaving">
                                            <span class="loading loading-spinner loading-xs mr-2" />
                                            Saving...
                                        </span>
                                        <span v-else>Save Changes</span>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Address Tab -->
                        <div v-if="currentTab === 'address'" class="p-6">
                            <h2 class="text-xl font-semibold mb-6">Shipping Address</h2>

                            <div v-if="addressForm.addressError" class="alert alert-error mb-4">
                                <svg
xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6"
                                    fill="none" viewBox="0 0 24 24">
                                    <path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <span>{{ addressForm.addressError }}</span>
                            </div>

                            <div class="grid grid-cols-1 gap-6">
                                <!-- Recipient Name -->
                                <div class="form-control">
                                    <label class="label">
                                        <span class="label-text font-medium">Full Name*</span>
                                    </label>
                                    <input
v-model="addressForm.recipient_name" type="text" placeholder="John Doe"
                                        class="input input-bordered w-full" required>
                                </div>

                                <!-- Address Line 1 -->
                                <div class="form-control">
                                    <label class="label">
                                        <span class="label-text font-medium">Address Line 1*</span>
                                    </label>
                                    <input
v-model="addressForm.address_line1" type="text" placeholder="123 Main St"
                                        class="input input-bordered w-full" required>
                                </div>

                                <!-- Address Line 2 -->
                                <div class="form-control">
                                    <label class="label">
                                        <span class="label-text font-medium">Address Line 2</span>
                                    </label>
                                    <input
v-model="addressForm.address_line2" type="text" placeholder="Apt 4B"
                                        class="input input-bordered w-full">
                                </div>

                                <!-- City, State, ZIP grid -->
                                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    <div class="form-control md:col-span-1">
                                        <label class="label">
                                            <span class="label-text font-medium">City*</span>
                                        </label>
                                        <input
v-model="addressForm.city" type="text" placeholder="New York"
                                            class="input input-bordered w-full" required>
                                    </div>

                                    <div class="form-control md:col-span-1">
                                        <label class="label">
                                            <span class="label-text font-medium">State/Province</span>
                                        </label>
                                        <input
v-model="addressForm.state" type="text" placeholder="NY"
                                            class="input input-bordered w-full">
                                    </div>

                                    <div class="form-control md:col-span-1">
                                        <label class="label">
                                            <span class="label-text font-medium">ZIP/Postal Code*</span>
                                        </label>
                                        <input
v-model="addressForm.postal_code" type="text" placeholder="10001"
                                            class="input input-bordered w-full" required>
                                    </div>
                                </div>

                                <!-- Country -->
                                <div class="form-control">
                                    <label class="label">
                                        <span class="label-text font-medium">Country*</span>
                                    </label>
                                    <input
v-model="addressForm.country" type="text" placeholder="United States"
                                        class="input input-bordered w-full" required>
                                </div>

                                <!-- Default Address Checkbox -->
                                <div class="form-control">
                                    <label class="cursor-pointer flex items-center gap-3">
                                        <input
v-model="addressForm.is_default" type="checkbox" checked="checked"
                                            class="checkbox checkbox-primary">
                                        <span class="label-text">Set as default shipping address</span>
                                    </label>
                                </div>

                                <!-- Save Button -->
                                <div class="mt-4">
                                    <button
class="btn btn-primary w-full sm:w-auto"
                                        :disabled="isSaving || !addressChanged" @click="saveSettings">
                                        <span v-if="isSaving">
                                            <span class="loading loading-spinner loading-xs mr-2" />
                                            Saving...
                                        </span>
                                        <span v-else>Save Address</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
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

.menu li .active {
    position: relative;
    font-weight: 600;
}

.menu li .active::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 4px;
    height: 60%;
    background-color: hsl(var(--p));
    border-radius: 0 4px 4px 0;
}

.form-control {
    width: 100%;
}

.btn-primary {
    @apply bg-orange-500 hover:bg-orange-600 border-orange-500 text-white;
}
</style>