// /frontend/middleware/auth.ts
import { defineNuxtRouteMiddleware, useRouter } from 'nuxt/app'

export interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  token: string;
}

export default defineNuxtRouteMiddleware((to) => {
  const router = useRouter()
  const protectedRoutes = ['/admin']
  const isProtected = protectedRoutes.some(route => to.path.startsWith(route))
  
  if (isProtected) {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      return router.push(`/login?redirect=${to.fullPath}`)
    }
  }
})