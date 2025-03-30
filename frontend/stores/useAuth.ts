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
  user_type?: 'customer' | 'admin';
  is_superuser?: boolean
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    username : null as string | null,
    token: null as string | null,
    isLoggedIn: false,
    loading: false,
    error: null as string | null,
    loginTime: null as Date | null,
    resetToken: null as string | null,
    resetTokenValid: false
  }),

  getters: {
    currentUser: (state) => state.user,
    isAuthenticated: (state) => state.isLoggedIn,
    isSuperuser: (state) => state.user?.is_superuser === true,
    isAdmin: (state) => state.user?.is_admin === true,
    userType: (state) => state.user?.user_type || 'customer',
    userName: (state) => state.user?.username || state.username,
    loginDuration: (state) => {
      if (!state.loginTime) return 0;
      return new Date().getTime() - state.loginTime.getTime();
    },
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
        this.username = user.username
        this.isLoggedIn = true;

        if (import.meta.client && user.username) {
          const savedCart = localStorage.getItem(`savedCart_${user.username}`);
          if (savedCart) {
            localStorage.setItem('cart', savedCart);
            localStorage.removeItem(`savedCart_${user.username}`);
            window.dispatchEvent(new Event('cart-updated'));
          }
        }
        if (this.resetToken){
          this.clearResetToken();
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
        this.username = user.username
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
    async setResetToken(token: string) {
      this.resetToken = token;
      this.resetTokenValid = false;
      if (!token) return false;
      try {
        const config = useRuntimeConfig();
        const apiUrl = config.public.apiUrl;

        const response = await fetch(`${apiUrl}/api/auth/validate-reset-token/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ token })
        });

        if (!response.ok) {
          throw new Error('Invalid or expired token');
        }

        const data = await response.json();

        if (data.status === 'success') {
          this.resetTokenValid = true;
          this.username = data.username;
          return true;
        } else {
          throw new Error(data.message || 'Invalid token');
        }
      } catch (error) {
        console.error('Error validating reset token:', error);
        this.resetToken = null;
        this.resetTokenValid = false;
        return false;
      }
    },

    clearResetToken() {
      this.resetToken = null;
      this.resetTokenValid = false;
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