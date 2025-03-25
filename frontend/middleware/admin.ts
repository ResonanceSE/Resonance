import { defineNuxtRouteMiddleware, navigateTo } from '#app';
import { useAuthStore } from '~/stores/useAuth';

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  
  // Check if user is authenticated and is admin
  if (!authStore.isAuthenticated || !authStore.isAdmin) {
    return navigateTo('/login');
  }
}); 