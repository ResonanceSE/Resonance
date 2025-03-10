// /frontend/services/authService.ts
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

interface ApiResponse {
  status: string;
  message?: string;
  data?: any;
}

export async function login(credentials: LoginCredentials): Promise<User> {
  try {
    const response = await fetch('/api/auth/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    });
    
    const data: ApiResponse = await response.json();
    
    if (data.status === 'error' || !data.data) {
      throw new Error(data.message || 'Login failed');
    }
    
    const user: User = data.data;
    
    // Store token and user data
    localStorage.setItem('auth_token', user.token);
    localStorage.setItem('user', JSON.stringify(user));
    
    return user;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(error.message);
    }
    throw new Error('Login failed');
  }
}

export async function register(userData: RegisterData): Promise<User> {
  try {
    const response = await fetch('/api/auth/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    });
    
    const data: ApiResponse = await response.json();
    
    if (data.status === 'error' || !data.data) {
      throw new Error(data.message || 'Registration failed');
    }
    
    const user: User = data.data;
    
    // Store token and user data
    localStorage.setItem('auth_token', user.token);
    localStorage.setItem('user', JSON.stringify(user));
    
    return user;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(error.message);
    }
    throw new Error('Registration failed');
  }
}

export async function logout(): Promise<void> {
  const token = localStorage.getItem('auth_token');
  
  if (token) {
    try {
      await fetch('/api/auth/logout/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
  }
  
  // Clear storage
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user');
}

export function getUser(): User | null {
  const userJson = localStorage.getItem('user');
  return userJson ? JSON.parse(userJson) : null;
}

export function getToken(): string | null {
  return localStorage.getItem('auth_token');
}

export function isAuthenticated(): boolean {
  return !!localStorage.getItem('auth_token');
}