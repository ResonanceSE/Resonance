// frontend/middleware/admin.ts
import { useAuthStore } from '~/stores/useAuth';

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  
  if (!authStore.isLoggedIn) {
    return navigateTo(`/login?redirect=${to.fullPath}`);
  }
  
  if (!authStore.user?.is_admin) {
    console.log('Not an admin user, redirecting');
    return navigateTo('/');
  }
});