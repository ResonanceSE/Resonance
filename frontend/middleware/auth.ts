// /frontend/middleware/auth.ts
import { useAuthStore } from '~/stores/useAuth'

export interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  token: string;
  is_admin: boolean;
  user_type: 'admin' | 'customer';
  is_superuser?: boolean;
}

export default defineNuxtRouteMiddleware((to) => {
  const currentUser = useAuthStore();
  if (import.meta.server) {
    if (to.path.startsWith('/admin') && !currentUser.user?.is_admin) {
      return navigateTo('/login')
    }
    return
  }
  
  const authStore = useAuthStore()
  const protectedRoutes = ['/admin']
  const isProtected = protectedRoutes.some(route => to.path.startsWith(route))
  
  if (isProtected) {
    try {
      // Check if auth store is initialized
      if (!authStore || typeof authStore.isAuthenticated === 'undefined') {
        console.log("Auth store not initialized, redirecting to login")
        return navigateTo(`/login?redirect=${to.fullPath}`)
      }
      
      // Check if user is authenticated
      if (!authStore.isAuthenticated) {
        console.log("User not authenticated, redirecting to login")
        return navigateTo(`/login?redirect=${to.fullPath}`)
      }
      
      // For admin routes, check if user is admin
      if (to.path.startsWith('/admin') && !authStore.isAdmin) {
        console.log("User is not admin, redirecting to home")
        return navigateTo('/')
      }
    } catch (error) {
      console.error('Error in auth middleware:', error)
      return navigateTo('/login')
    }
  }
})