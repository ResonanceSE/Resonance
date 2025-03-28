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

const CURRENT_USER_KEY = 'currentUsername';

const getBaseUrl = (): string => {
  const config = useRuntimeConfig();
  return config.public.apiUrl || 'http://127.0.0.1:8000';
};

export async function login(credentials: LoginCredentials): Promise<User> {
  try {
    const response = await fetch(`${getBaseUrl()}/api/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials),
      credentials: 'include',
    });
    console.log("Response:", response);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || errorData.detail || `Login failed with status ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Login response:', data); 
    
    let user: User;
    
    if (data.status === 'success' && data.data) {
      user = data.data;
    } else if (data.token || data.key) {
      user = {
        token: data.token || data.key,
        username: credentials.username,
        ...data.user,
      };
    } else {
      user = {
        ...data,
        token: data.token,
      };
    }
    
    if (!user.token) {
      throw new Error('No authentication token received');
    }
    
    sessionStorage.setItem(CURRENT_USER_KEY, credentials.username);
    localStorage.setItem(`auth_token_${credentials.username}`, user.token);
    localStorage.setItem(`user_${credentials.username}`, JSON.stringify(user));
    
    return user;
  } catch (error) {
    console.error('Login error:', error);
    if (error instanceof Error) {
      throw new Error(error.message);
    }
    throw new Error('Login failed');
  }
}

export async function register(userData: RegisterData): Promise<User> {
  try {
    console.error('Attempting registration for:', userData.username);
    
    const response = await fetch(`${getBaseUrl()}/api/auth/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData),
      credentials: 'include',
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || errorData.detail || `Registration failed with status ${response.status}`);
    }
    
    const data = await response.json();
    console.error('Registration response:', data);
    
    let user: User;
    
    if (data.status === 'success' && data.data) {
      user = data.data;
    } else if (data.token || data.key) {
      user = {
        token: data.token || data.key,
        username: userData.username,
        ...data.user,
      };
    } else {
      user = {
        ...data,
        token: data.token,
      };
    }
    
    if (!user.token) {
      throw new Error('No authentication token received');
    }
    

    sessionStorage.setItem(CURRENT_USER_KEY, userData.username);
    localStorage.setItem(`auth_token_${userData.username}`, user.token);
    localStorage.setItem(`user_${userData.username}`, JSON.stringify(user));
    
    return user;
  } catch (error) {
    console.error('Registration error:', error);
    if (error instanceof Error) {
      throw new Error(error.message);
    }
    throw new Error('Registration failed');
  }
}

export async function logout(): Promise<void> {
  const currentUsername = sessionStorage.getItem(CURRENT_USER_KEY);
  
  if (!currentUsername) {
    console.error('No current user found for logout');
    return;
  }
  
  const token = localStorage.getItem(`auth_token_${currentUsername}`);
  
  if (token) {
    try {
      await fetch(`${getBaseUrl()}/api/auth/logout/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`
        },
        credentials: 'include',
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
  }
  
  // Clear only the current tab's session
  sessionStorage.removeItem(CURRENT_USER_KEY);
}

export function getUser(): User | null {
  if (import.meta.client) {
    const currentUsername = sessionStorage.getItem(CURRENT_USER_KEY);
    if (!currentUsername) return null;
    
    const userJson = localStorage.getItem(`user_${currentUsername}`);
    return userJson ? JSON.parse(userJson) : null;
  }
  return null;
}

export function getToken(): string | null {
  if (import.meta.client) {
    const currentUsername = sessionStorage.getItem(CURRENT_USER_KEY);
    if (!currentUsername) return null;
    
    return localStorage.getItem(`auth_token_${currentUsername}`);
  }
  return null;
}

export function isAuthenticated(): boolean {
  if (import.meta.client) {
    const currentUsername = sessionStorage.getItem(CURRENT_USER_KEY);
    if (!currentUsername) return false;
    
    return !!localStorage.getItem(`auth_token_${currentUsername}`);
  }
  return false;
}

export function switchUser(username: string): boolean {
  if (import.meta.client) {
    // Check if this user exists in localStorage
    const userToken = localStorage.getItem(`auth_token_${username}`);
    if (!userToken) return false;
    
    // Switch to this user in current tab only
    sessionStorage.setItem(CURRENT_USER_KEY, username);
    return true;
  }
  return false;
}

export function getStoredUsers(): string[] {
  if (import.meta.client) {
    const users: string[] = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key?.startsWith('user_')) {
        users.push(key.replace('user_', ''));
      }
    }
    return users;
  }
  return [];
}

export async function validatePassword(password: string) {
  try {
    const response = await fetch(`${getBaseUrl()}/api/auth/validate-password/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ password }),
      credentials: 'include',
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      console.error('Password validation failed:', errorData);
      return { 
        status: 'error', 
        message: Array.isArray(errorData.message) ? errorData.message : [errorData.message || 'Invalid password'] 
      };
    }
    
    const data = await response.json();
    console.log('Password validation response:', data);
    return data;
  } catch (error) {
    console.error('Password validation error:', error);
    return { 
      status: 'error', 
      message: ['Failed to validate password. Please check your connection.']
    };
  }
}