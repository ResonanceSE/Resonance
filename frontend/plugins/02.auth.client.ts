import { useAuthStore } from '~/stores/useAuth';

export default defineNuxtPlugin(() => {
  if (import.meta.client) {
    try {
      const authStore = useAuthStore();
      authStore.initialize();
    } catch (error) {
      console.error('Auth initialization error:', error);
    }
  }
});