<script>
// Registration form logic
import { register } from '~/services/authService';

export default {
    data() {
        return {
            firstName: '',
            lastName: '',
            username: '',
            email: '',
            password: '',
            confirmPassword: '',
            agreeTerms: false,
            newsletterOpt: false,
            errorMessage: '',
            successMessage: '',
            passwordVisible: false,
            confirmPasswordVisible: false,
            formSubmitted: false
        }
    },
    methods: {
        async handleRegister() {

            this.errorMessage = '';
            this.successMessage = '';
            this.formSubmitted = true;

            if (!this.firstName || !this.lastName || !this.email || !this.password || !this.confirmPassword) {
                this.errorMessage = 'Please fill in all required fields';
                return;
            }

            if (this.password !== this.confirmPassword) {
                this.errorMessage = 'Passwords do not match';
                return;
            }

            if (!this.agreeTerms) {
                this.errorMessage = 'You must agree to the Terms of Service';
                return;
            }

            const userData = {
                username: this.username || this.email, 
                email: this.email,
                password: this.password,
                first_name: this.firstName,
                last_name: this.lastName
            };

            try {
                const user = await register(userData);
                this.successMessage = 'Registration successful! Redirecting to login...';

                setTimeout(() => {
                    this.$router.push('/login'); 
                }, 2000);

            } catch (error) {
                this.errorMessage = error.message || 'Registration failed. Please try again.';
            }
        },
        togglePasswordVisibility() {
            this.passwordVisible = !this.passwordVisible;
        },
        toggleConfirmPasswordVisibility() {
            this.confirmPasswordVisible = !this.confirmPasswordVisible;
        }
    }
}

</script>

<template>
    <!-- Adding decorative background elements -->
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12 relative overflow-hidden">
        <!-- Decorative circles -->
        <div
            class="absolute top-20 left-10 w-64 h-64 bg-orange-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob" />
        <div
            class="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000" />
        <div
            class="absolute -bottom-8 left-40 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000" />

        <div class="flex flex-col justify-center items-center my-10 relative z-10">
            <!-- Enhanced header with icon -->
            <div class="flex items-center gap-2 mb-6">
                <div
                    class="w-8 h-8 bg-gradient-to-r from-orange-500 to-orange-400 rounded-full flex items-center justify-center">
                    <div class="w-4 h-4 bg-white rounded-sm transform rotate-45" />
                </div>
                <h4 class="text-3xl font-bold">Create your account!</h4>
            </div>

            <!-- Main card with enhanced styling -->
            <div
                class="relative mx-auto w-full max-w-4xl rounded-3xl overflow-hidden shadow-2xl bg-white/80 backdrop-blur-sm">
                <!-- Optional decorative side pattern -->
                <div
                    class="absolute left-0 top-0 h-full w-3 bg-gradient-to-b from-orange-400 via-orange-500 to-orange-600" />

                <div class="col-span-1 md:col-span-5 p-8 md:p-12 pl-10 rounded-3xl md:rounded-l-none">
                    <!-- Grid layout for the vertical sections -->
                    <div class="grid grid-rows-[auto_1fr_auto] gap-8 h-full">
                        <!-- Enhanced header section -->
                        <div>
                            <div class="mb-8">
                                <div class="flex items-center">
                                    <div class="w-5 h-5 bg-gradient-to-r from-blue-500 to-purple-500 rounded-md mr-2" />
                                    <span class="font-semibold text-gray-800 text-lg tracking-wide">Resonance</span>
                                </div>
                            </div>
                            <div class="mb-10">
                                <h1
                                    class="text-3xl font-bold mb-1 bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
                                    Register for
                                </h1>
                                <h1 class="text-3xl font-bold">
                                    <span
                                        class="bg-gradient-to-r from-blue-500 to-indigo-600 bg-clip-text text-transparent">Resonance</span>
                                    <span class="relative">
                                        Website
                                        <span class="absolute -bottom-1 left-0 w-full h-1 bg-orange-400 rounded-full" />
                                    </span>
                                </h1>
                            </div>
                        </div>

                        <!-- Main form section-->
                        <div class="grid gap-6">
                            <!-- Enhanced Error/Success Messages -->
                            <div v-if="errorMessage"
                                class="bg-red-50 border-l-4 border-red-400 text-red-700 p-4 rounded-r-md flex items-start">
                                <span class="text-xl mr-2">ⓘ</span>
                                {{ errorMessage }}
                            </div>
                            <div v-if="successMessage"
                                class="bg-green-50 border-l-4 border-green-400 text-green-700 p-4 rounded-r-md flex items-start">
                                <span class="text-xl mr-2">✓</span>
                                {{ successMessage }}
                            </div>

                            <!-- Enhanced input fields -->
                            <div class="grid gap-5">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                                    <div>
                                        <label for="firstName"
                                            class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                                        <div class="relative">
                                            <span
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                                                👤
                                            </span>
                                            <input id="firstName" v-model="firstName" type="text"
                                                placeholder="First Name"
                                                class="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                                                :class="{ 'border-red-300 focus:ring-red-400': formSubmitted && !firstName }">
                                        </div>
                                    </div>
                                    <div>
                                        <label for="lastName" class="block text-sm font-medium text-gray-700 mb-1">Last
                                            Name</label>
                                        <div class="relative">
                                            <span
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                                                👤
                                            </span>
                                            <input id="lastName" v-model="lastName" type="text" placeholder="Last Name"
                                                class="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                                                :class="{ 'border-red-300 focus:ring-red-400': formSubmitted && !lastName }">
                                        </div>
                                    </div>
                                    <div class="lg:col-span-2">
                                        <label for="Username"
                                            class="block text-sm font-medium text-gray-700 mb-1">Username</label>
                                        <div class="relative">
                                            <span
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                                                👤
                                            </span>
                                            <input id="username" v-model="username" type="text" placeholder="Username"
                                                class="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                                                :class="{ 'border-red-300 focus:ring-red-400': formSubmitted && !username }">
                                        </div>
                                    </div>
                                    <div class="lg:col-span-2">
                                        <label for="email"
                                            class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                                        <div class="relative">
                                            <span
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                                                ✉
                                            </span>
                                            <input id="email" v-model="email" type="email" placeholder="Email address"
                                                class="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                                                :class="{ 'border-red-300 focus:ring-red-400': formSubmitted && !email }">
                                        </div>
                                    </div>
                                    <div>
                                        <label for="password"
                                            class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                                        <div class="relative">
                                            <span
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                                                🔒
                                            </span>
                                            <input id="password" v-model="password"
                                                :type="passwordVisible ? 'text' : 'password'"
                                                placeholder="Create password"
                                                class="w-full pl-10 pr-10 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                                                :class="{ 'border-red-300 focus:ring-red-400': formSubmitted && !password }">
                                            <button type="button"
                                                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                                                @click="togglePasswordVisibility">
                                                <span v-if="!passwordVisible">👁</span>
                                                <span v-else>👁‍🗨</span>
                                            </button>
                                        </div>
                                    </div>

                                    <div>
                                        <label for="confirmPassword"
                                            class="block text-sm font-medium text-gray-700 mb-1">Confirm
                                            Password</label>
                                        <div class="relative">
                                            <span
                                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                                                🔒
                                            </span>
                                            <input id="confirmPassword" v-model="confirmPassword"
                                                :type="confirmPasswordVisible ? 'text' : 'password'"
                                                placeholder="Confirm password"
                                                class="w-full pl-10 pr-10 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all"
                                                :class="{ 'border-red-300 focus:ring-red-400': formSubmitted && !confirmPassword }">
                                            <button type="button"
                                                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                                                @click="toggleConfirmPasswordVisibility">
                                                <span v-if="!confirmPasswordVisible">👁</span>
                                                <span v-else>👁‍🗨</span>
                                            </button>
                                        </div>
                                    </div>

                                    <!-- Enhanced checkboxes -->
                                    <div class="flex flex-col gap-4 lg:col-span-2">
                                        <div class="flex items-center">
                                            <div class="relative flex items-start">
                                                <div class="flex items-center h-5">
                                                    <input id="agreeTerms" v-model="agreeTerms" type="checkbox"
                                                        class="h-5 w-5 rounded border-gray-300 text-orange-500 focus:ring-orange-500 transition-colors"
                                                        :class="{ 'border-red-300': formSubmitted && !agreeTerms }">
                                                </div>
                                                <label for="agreeTerms" class="ml-3 text-sm">
                                                    <span class="text-gray-700">I agree to the </span>
                                                    <a href="#"
                                                        class="text-orange-500 hover:text-orange-600 font-medium hover:underline">Terms
                                                        of Service</a>
                                                    <span class="text-gray-700"> and </span>
                                                    <a href="#"
                                                        class="text-orange-500 hover:text-orange-600 font-medium hover:underline">Privacy
                                                        Policy</a>
                                                </label>
                                            </div>
                                        </div>
                                    </div>
                                    <!-- Enhanced button -->
                                    <div class="lg:col-span-2 pt-2 flex justify-center">
                                        <button
                                            class="w-3/4 py-3.5 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white font-medium rounded-xl transition-all shadow-md hover:shadow-lg active:shadow-sm transform hover:-translate-y-0.5 active:translate-y-0 duration-150"
                                            @click="handleRegister">
                                            <div class="flex items-center justify-center">
                                                <span>CREATE ACCOUNT</span>
                                                <span class="arrow-right ml-2" />
                                            </div>
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <!-- Enhanced footer section -->
                            <div class="grid gap-4 pt-4">
                                <div class="grid place-items-center">
                                    <div class="flex space-x-8 text-sm">
                                        <a href="#"
                                            class="text-gray-600 hover:text-gray-800 hover:underline transition-colors">Terms
                                            of Use</a>
                                        <a href="#"
                                            class="text-gray-600 hover:text-gray-800 hover:underline transition-colors">Privacy
                                            Policy</a>
                                        <a href="#"
                                            class="text-gray-600 hover:text-gray-800 hover:underline transition-colors">Help
                                            Center</a>
                                    </div>
                                </div>
                                <div class="text-gray-600 mt-2">
                                    <div class="flex flex-row gap-2 justify-center">
                                        <span class="text-gray-600">Already have an account?</span>
                                        <NuxtLink
                                            class="text-orange-500 hover:text-orange-600 font-medium hover:underline"
                                            :to="'/login'">Log in here</NuxtLink>
                                    </div>
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

.arrow-right {
    position: relative;
    display: inline-block;
    width: 14px;
    height: 2px;
    background-color: currentColor;
}

.arrow-right:after {
    content: '';
    position: absolute;
    right: 0;
    top: -3px;
    width: 8px;
    height: 8px;
    border-top: 2px solid currentColor;
    border-right: 2px solid currentColor;
    transform: rotate(45deg);
}

.divider {
    display: flex;
    align-items: center;
    text-align: center;
    color: #9ca3af;
}

.divider::before,
.divider::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #e5e7eb;
}

.divider::before {
    margin-right: 0.5em;
}

.divider::after {
    margin-left: 0.5em;
}
</style>