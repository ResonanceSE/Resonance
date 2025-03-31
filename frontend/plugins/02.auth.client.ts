import { useAuthStore } from '~/stores/useAuth';
import { cartService } from '~/services/cartService';

export default defineNuxtPlugin(() => {
  if (import.meta.client) {
    try {
      const authStore = useAuthStore();
      
      authStore.initialize();
      
      if (authStore.isAuthenticated) {
        syncCartWithServer();
      }
      
      watch(() => authStore.isAuthenticated, (isAuthenticated) => {
        if (isAuthenticated) {
          syncCartWithServer();
        }
      });
      
      async function syncCartWithServer() {
        try {
          await cartService.syncCart();
        } catch (error) {
          console.error('Error syncing cart with server:', error);
        }
      }
    } catch (error) {
      console.error('Auth initialization error:', error);
    }
  }
});