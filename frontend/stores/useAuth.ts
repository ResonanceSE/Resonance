import { defineStore } from 'pinia'
import { 
  login as apiLogin, 
  logout as apiLogout, 
  register as apiRegister,
  getUser,
  getToken 
} from '~/services/authService'

import type { User } from '~/middleware/auth'

interface LoginCredentials {
  username: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    token: null as string | null,
    isLoggedIn: false,
    loading: false,
    error: null as string | null,
    loginTime: null as Date | null
  }),
  
  getters: {
    currentUser: (state) => state.user,
    isAuthenticated: (state) => state.isLoggedIn,
    isAdmin: (state) => state.user?.is_admin === true,
    loginDuration: (state) => {
      if (!state.loginTime) return 0;
      return new Date().getTime() - state.loginTime.getTime();
    }
  },
  
  actions: {
    async login(credentials: LoginCredentials) {
      this.loading = true;
      this.error = null;
      
      try {
        const user = await apiLogin(credentials);
        
        this.loginTime = new Date();
      
        this.user = user;
        this.token = user.token;
        this.isLoggedIn = true;
        
        if (import.meta.client && user.username) {
          const savedCart = localStorage.getItem(`savedCart_${user.username}`);
          if (savedCart) {
            localStorage.setItem('cart', savedCart);
            localStorage.removeItem(`savedCart_${user.username}`);
            window.dispatchEvent(new Event('cart-updated'));
          }
        }
        
        return user;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Login failed';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async register(userData: RegisterData) {
      this.loading = true;
      this.error = null;
      
      try {
        const user = await apiRegister(userData);
        this.user = user;
        this.token = user.token;
        this.isLoggedIn = true;
        
        return this.login({
          username: userData.username,
          password: userData.password
        });
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Registration failed';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async logout() {
      this.loading = true;
      
      try {
        if (import.meta.client && this.user?.username) {
          const currentCart = localStorage.getItem('cart');
          if (currentCart) {
            localStorage.setItem(`savedCart_${this.user.username}`, currentCart);
          }
        }
        
        await apiLogout();
        if (import.meta.client) {
          localStorage.removeItem('cart');
        }
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        this.clearSession();
      }
    },
    
    clearSession() {
      this.user = null;
      this.token = null;
      this.isLoggedIn = false;
      this.loginTime = null;
      this.loading = false;
    },
    
    initialize() {
      if (import.meta.client) {
        try {
          const user = getUser();
          const token = getToken();
          
          if (user && token) {
            this.user = user;
            this.token = token;
            this.isLoggedIn = true;
            this.loginTime = new Date();
            
            if (user.username) {
              const savedCart = localStorage.getItem(`savedCart_${user.username}`);
              if (savedCart && !localStorage.getItem('cart')) {
                localStorage.setItem('cart', savedCart);
                localStorage.removeItem(`savedCart_${user.username}`);
                window.dispatchEvent(new Event('cart-updated'));
              }
            }
          }
        } catch (error) {
          console.error('Failed to initialize auth store:', error);
        }
      }
    }
  }
});