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
        
        // Store login time for analytics/tracking
        this.loginTime = new Date();
        
        // Update state
        this.user = user;
        this.token = user.token;
        this.isLoggedIn = true;
        
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
        await apiLogout();
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        this.clearSession();
      }
    },
    
    // Helper methods
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
          }
        } catch (error) {
          console.error('Failed to initialize auth store:', error);
        }
      }
    }
  }
});