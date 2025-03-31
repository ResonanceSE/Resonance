import { useAuthStore } from '~/stores/useAuth'

export interface CartItem {
  id: number
  name: string
  category: string
  price: number
  quantity: number
  image?: string
  stock?: number
  sale_price?: number 
}

export const cartService = {
  async getCart(): Promise<CartItem[]> {
    const authStore = useAuthStore();
    const currentUser = authStore.user?.username || 'guest';
    
    // If the user is authenticated, try to get the cart from the server
    if (authStore.isAuthenticated) {
      try {
        const config = useRuntimeConfig();
        const apiUrl = config.public.apiUrl || 'http://localhost:8000';
        
        const response = await fetch(`${apiUrl}/api/cart/`, {
          headers: {
            'Authorization': `Token ${authStore.token}`
          }
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.status === 'success' && Array.isArray(result.data)) {
            // Save the server cart to localStorage as a backup
            if (import.meta.client) {
              localStorage.setItem(`cart_${currentUser}`, JSON.stringify(result.data));
            }
            return result.data;
          } else if (result.status === 'error') {
            console.error('Server error:', result.message);
            return this.getLocalCart();
          }
        }
        
        // If server request fails, fallback to localStorage
        return this.getLocalCart();
      } catch (error) {
        console.error('Error getting cart from server:', error);
        return this.getLocalCart();
      }
    }
    
    // For unauthenticated users, just use localStorage
    return this.getLocalCart();
  },
  
  getLocalCart(): CartItem[] {
    const authStore = useAuthStore();
    const currentUser = authStore.user?.username || 'guest';
    
    if (import.meta.client) {
      try {
        const cartData = localStorage.getItem(`cart_${currentUser}`);
        return cartData ? JSON.parse(cartData) : [];
      } catch (error) {
        console.error('Error getting local cart:', error);
        return [];
      }
    }
    return [];
  },

  saveLocalCart(cart: CartItem[]): void {
    const authStore = useAuthStore();
    const currentUser = authStore.user?.username || 'guest';
    
    if (import.meta.client) {
      try {
        localStorage.setItem(`cart_${currentUser}`, JSON.stringify(cart));
      } catch (error) {
        console.error('Error saving local cart:', error);
      }
    }
  },

  async addToCart(item: CartItem): Promise<CartItem[]> {
    const authStore = useAuthStore();
    
    // Always update local cart first for immediate feedback
    const localCart = this.getLocalCart();
    const existingItemIndex = localCart.findIndex(cartItem => cartItem.id === item.id);
    
    if (existingItemIndex >= 0) {
      localCart[existingItemIndex].quantity += item.quantity;
    } else {
      localCart.push(item);
    }
    
    this.saveLocalCart(localCart);
    
    // If authenticated, sync with server
    if (authStore.isAuthenticated) {
      try {
        const config = useRuntimeConfig();
        const apiUrl = config.public.apiUrl || 'http://localhost:8000';
        
        const response = await fetch(`${apiUrl}/api/cart/add/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${authStore.token}`
          },
          body: JSON.stringify({
            product_id: item.id,
            quantity: item.quantity
          })
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.status === 'success' && Array.isArray(result.data)) {
            // Update local cart with server response
            this.saveLocalCart(result.data);
            return result.data;
          } else if (result.status === 'error') {
            console.error('Server error:', result.message);
            return localCart;
          }
        }
      } catch (error) {
        console.error('Error adding to cart on server:', error);
      }
    }
    
    return localCart;
  },

  async updateQuantity(itemId: number, quantity: number): Promise<CartItem[]> {
    const authStore = useAuthStore();
    
    // Update local cart first
    const localCart = this.getLocalCart();
    const itemIndex = localCart.findIndex(item => item.id === itemId);
    
    if (itemIndex >= 0) {
      if (quantity <= 0) {
        // Remove item if quantity is 0 or negative
        localCart.splice(itemIndex, 1);
      } else {
        localCart[itemIndex].quantity = quantity;
      }
      this.saveLocalCart(localCart);
    }
    
    // If authenticated, sync with server
    if (authStore.isAuthenticated) {
      try {
        const config = useRuntimeConfig();
        const apiUrl = config.public.apiUrl || 'http://localhost:8000';
        
        const response = await fetch(`${apiUrl}/api/cart/update/${itemId}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${authStore.token}`
          },
          body: JSON.stringify({
            quantity: quantity
          })
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.status === 'success' && Array.isArray(result.data)) {
            // Update local cart with server response
            this.saveLocalCart(result.data);
            return result.data;
          } else if (result.status === 'error') {
            console.error('Server error:', result.message);
            return localCart;
          }
        }
      } catch (error) {
        console.error('Error updating cart quantity on server:', error);
      }
    }
    
    return localCart;
  },

  async removeItem(itemId: number): Promise<CartItem[]> {
    const authStore = useAuthStore();
    
    // Update local cart first
    const localCart = this.getLocalCart();
    const updatedCart = localCart.filter(item => item.id !== itemId);
    this.saveLocalCart(updatedCart);
    
    // If authenticated, sync with server
    if (authStore.isAuthenticated) {
      try {
        const config = useRuntimeConfig();
        const apiUrl = config.public.apiUrl || 'http://localhost:8000';
        
        const response = await fetch(`${apiUrl}/api/cart/remove/${itemId}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Token ${authStore.token}`
          }
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.status === 'success' && Array.isArray(result.data)) {
            // Update local cart with server response
            this.saveLocalCart(result.data);
            return result.data;
          } else if (result.status === 'error') {
            console.error('Server error:', result.message);
            return updatedCart;
          }
        }
      } catch (error) {
        console.error('Error removing item from cart on server:', error);
      }
    }
    
    return updatedCart;
  },

  async clearCart(): Promise<void> {
    const authStore = useAuthStore();
    const currentUser = authStore.user?.username || 'guest';
    
    // Clear local cart
    if (import.meta.client) {
      localStorage.removeItem(`cart_${currentUser}`);
    }
    
    // If authenticated, clear server cart
    if (authStore.isAuthenticated) {
      try {
        const config = useRuntimeConfig();
        const apiUrl = config.public.apiUrl || 'http://localhost:8000';
        
        const response = await fetch(`${apiUrl}/api/cart/clear/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Token ${authStore.token}`
          }
        });
        
        if (!response.ok) {
          const result = await response.json();
          console.error('Error clearing cart on server:', result.message);
        }
      } catch (error) {
        console.error('Error clearing cart on server:', error);
      }
    }
  },

  async syncCart(): Promise<CartItem[]> {
    const authStore = useAuthStore();
    
    // Only sync if authenticated
    if (!authStore.isAuthenticated) {
      return this.getLocalCart();
    }
    
    try {
      const config = useRuntimeConfig();
      const apiUrl = config.public.apiUrl || 'http://localhost:8000';
      const localCart = this.getLocalCart();
      
      const response = await fetch(`${apiUrl}/api/cart/sync/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${authStore.token}`
        },
        body: JSON.stringify({
          items: localCart.map(item => ({
            id: item.id,
            quantity: item.quantity
          })),
          replace_all: true
        })
      });
      
      if (response.ok) {
        const result = await response.json();
        if (result.status === 'success' && Array.isArray(result.data)) {
          // Update local cart with server response
          this.saveLocalCart(result.data);
          return result.data;
        } else if (result.status === 'error') {
          console.error('Server error:', result.message);
          return localCart;
        }
      }
      
      return localCart;
    } catch (error) {
      console.error('Error syncing cart with server:', error);
      return this.getLocalCart();
    }
  },

  getCartTotal(): number {
    const cart = this.getLocalCart();
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  },

  getCartItemCount(): number {
    const cart = this.getLocalCart();
    return cart.reduce((count, item) => count + item.quantity, 0);
  }
}