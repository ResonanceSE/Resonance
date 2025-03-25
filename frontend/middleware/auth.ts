// /frontend/middleware/auth.ts
import { defineNuxtRouteMiddleware, navigateTo } from 'nuxt/app'
import { useAuthStore } from '~/stores/useAuth'

export interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  token: string;
  is_admin: boolean;
}

export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.server) {
    return
  }
  const authStore = useAuthStore()
  const protectedRoutes = ['/admin']
  const isProtected = protectedRoutes.some(route => to.path.startsWith(route))
  
  if (isProtected) {
    try {
      const token = localStorage.getItem('auth_token')
      if (!token) {
        return navigateTo(`/login?redirect=${to.fullPath}`)
      }
      
      if (to.path.startsWith('/admin') && !authStore.currentUser?.is_admin) {
        return navigateTo('/')
      }
    } catch (error) {
      console.error('Error in auth middleware:', error)
      return navigateTo('/login')
    }
  }
})