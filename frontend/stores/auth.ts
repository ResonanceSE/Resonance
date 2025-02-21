import { defineStore } from 'pinia';

export interface AuthState {
  token: string | null;
  user: any;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: useCookie<string | null>('token', { default: () => null }).value,
    user: null,
  }),

  actions: {
    async login(username: string, password: string) {
      try {
        const response = await $fetch<{ access: string; refresh: string }>(
          "http://127.0.0.1:8000/api/auth/login/",
          {
            method: "POST",
            body: { username, password },
          }
        );

        this.token = response.access;
        useCookie('token').value = response.access;
      } catch (error) {
        console.error("Login error:", error);
      }
    },

    async logout() {
      this.token = null;
      useCookie('token').value = null;
    },

    async fetchUser() {
      if (!this.token) return;
      try {
        const response = await $fetch("http://127.0.0.1:8000/api/auth/user/", {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.user = response;
      } catch (error) {
        console.error("Fetch user error:", error);
      }
    },
  },
});
