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

export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore();
  
  if (to.path === '/reset_password') {
    const token = to.query.token as string;
    
    if (!token) {
      return navigateTo('/forgot_password');
    }
    
    if (authStore.resetToken !== token) {
      try {

        const isValid = await authStore.setResetToken(token);
        if (!isValid) {
          console.log("Invalid reset token, redirecting to forgot_password");
          return navigateTo('/forgot_password?error=invalid_token');
        }
      } catch (error) {
        return navigateTo('/forgot_password?error=validation_error');
      }
    }
    
    return;
  }
  
  if (import.meta.server) {
    if (to.path.startsWith('/admin') && !authStore.user?.is_admin) {
      return navigateTo('/login')
    }
    return
  }
  
  const protectedRoutes = ['/admin', '/setting', '/orders', '/checkout']
  const isProtected = protectedRoutes.some(route => to.path.startsWith(route))
  
  if (isProtected) {
    try {
      if (!authStore || typeof authStore.isAuthenticated === 'undefined') {
        return navigateTo(`/login?redirect=${to.fullPath}`)
      }
      
      if (!authStore.isAuthenticated) {
        return navigateTo(`/login?redirect=${to.fullPath}`)
      }
      
      if (to.path.startsWith('/admin') && !authStore.isAdmin) {
        return navigateTo('/')
      }
    } catch (error) {
      return navigateTo('/login')
    }
  }
})