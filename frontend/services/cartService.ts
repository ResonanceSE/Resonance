import { useAuthStore } from '~/stores/useAuth'



export interface CartItem {
  id: number
  product_id?: number
  name: string
  category: string
  price: number
  quantity: number
  image?: string
  stock?: number
}


export const cartService = {
  async getCart(): Promise<CartItem[]> {
    const authStore = useAuthStore();
    const config = useRuntimeConfig();
    const apiUrl = config.public.apiUrl || 'http://localhost:8000';
    
    if (!authStore.isAuthenticated) {
      // For non-authenticated users, use local storage
      return this.getLocalCart();
    }
    
    try {
      // Fetch cart from server
      const response = await fetch(`${apiUrl}/api/cart/`, {
        headers: {
          'Authorization': `Token ${authStore.token}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to fetch cart: ${response.statusText}`);
      }
      
      const result = await response.json();
      
      if (result.status === 'success') {
        // Transform server cart items to match our interface
        return result.data.map((item: any) => ({
          id: item.product_id,
          product_id: item.product_id,
          name: item.name,
          category: item.category || '',
          price: item.price,
          quantity: item.quantity,
          image: item.image_url,
          stock: item.stock
        }));
      } else {
        throw new Error(result.message || 'Failed to get cart');
      }
    } catch (error) {
      console.error('Error fetching cart from server:', error);
      // Fallback to local cart in case of error
      return this.getLocalCart();
    }
  },
  
  getLocalCart(): CartItem[] {
    if (import.meta.client) {
      const authStore = useAuthStore();
      const currentUser = authStore.user?.username || 'guest';
      
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
  
  // Sync local cart with server
  async syncCart(): Promise<CartItem[]> {
    const authStore = useAuthStore();
    const config = useRuntimeConfig();
    const apiUrl = config.public.apiUrl || 'http://localhost:8000';
    
    if (!authStore.isAuthenticated) {
      return this.getLocalCart();
    }
    
    // Get local cart items
    const localCart = this.getLocalCart();
    
    if (localCart.length === 0) {
      return this.getCart();
    }
    
    try {
      // Send local cart to server for syncing
      const response = await fetch(`${apiUrl}/api/cart/sync/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${authStore.token}`
        },
        body: JSON.stringify({ items: localCart })
      });
      
      if (!response.ok) {
        throw new Error(`Failed to sync cart: ${response.statusText}`);
      }
      
      const result = await response.json();
      
      if (result.status === 'success') {
        // Clear local cart after successful sync
        if (import.meta.client) {
          localStorage.removeItem(`cart_${authStore.user?.username || 'guest'}`);
        }
        
        // Return synchronized cart
        return result.data.map((item: any) => ({
          id: item.product_id,
          product_id: item.product_id,
          name: item.name,
          category: item.category || '',
          price: item.price,
          quantity: item.quantity,
          image: item.image_url,
          stock: item.stock
        }));
      } else {
        throw new Error(result.message || 'Failed to sync cart');
      }
    } catch (error) {
      console.error('Error syncing cart:', error);
      return localCart;
    }
  },

  async saveCart(cart: CartItem[]): Promise<void> {
    const authStore = useAuthStore();
    const config = useRuntimeConfig();
    const apiUrl = config.public.apiUrl || 'http://localhost:8000';
    
    if (!authStore.isAuthenticated) {
      // For non-authenticated users, save to local storage
      this.saveLocalCart(cart);
      return;
    }
    
    try {
      // First, clear existing cart
      await fetch(`${apiUrl}/api/cart/clear/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Token ${authStore.token}`
        }
      });
      
      // Then, add all items to server cart
      for (const item of cart) {
        await fetch(`${apiUrl}/api/cart/add/`, {
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
      }
    } catch (error) {
      console.error('Error saving cart to server:', error);
      // Fallback to local storage in case of error
      this.saveLocalCart(cart);
    }
  },
  
  saveLocalCart(cart: CartItem[]): void {
    if (import.meta.client) {
      const authStore = useAuthStore();
      const currentUser = authStore.user?.username || 'guest';
      
      try {
        localStorage.setItem(`cart_${currentUser}`, JSON.stringify(cart));
      } catch (error) {
        console.error('Error saving local cart:', error);
      }
    }
  },

  async addToCart(item: CartItem): Promise<CartItem[]> {
    const authStore = useAuthStore();
    const config = useRuntimeConfig();
    const apiUrl = config.public.apiUrl || 'http://localhost:8000';
    
    if (!authStore.isAuthenticated) {
      // For non-authenticated users, use local storage
      return this.addToLocalCart(item);
    }
    
    try {
      // Add item to server cart
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
      
      if (!response.ok) {
        throw new Error(`Failed to add item to cart: ${response.statusText}`);
      }
      
      // Get updated cart after addition
      return this.getCart();
    } catch (error) {
      console.error('Error adding to server cart:', error);
      // Fallback to local cart in case of error
      return this.addToLocalCart(item);
    }
  },
  
  addToLocalCart(item: CartItem): CartItem[] {
    const cart = this.getLocalCart();
    const existingItemIndex = cart.findIndex(cartItem => cartItem.id === item.id);
    
    if (existingItemIndex >= 0) {
      cart[existingItemIndex].quantity += item.quantity;
    } else {
      cart.push(item);
    }
    
    this.saveLocalCart(cart);
    return cart;
  },

  async updateQuantity(itemId: number, quantity: number): Promise<CartItem[]> {
    const authStore = useAuthStore();
    const config = useRuntimeConfig();
    const apiUrl = config.public.apiUrl || 'http://localhost:8000';
    
    if (!authStore.isAuthenticated) {
      // For non-authenticated users, use local storage
      return this.updateLocalQuantity(itemId, quantity);
    }
    
    try {
      // First, need to get the cart to find the cart item id
      const cart = await this.getCart();
      // Find the cart item that contains this product
      const cartItem = cart.find(item => item.id === itemId);
      
      if (!cartItem) {
        throw new Error(`Item with id ${itemId} not found in cart`);
      }
      
      // Update item quantity on server
      const response = await fetch(`${apiUrl}/api/cart/update/${cartItem.product_id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${authStore.token}`
        },
        body: JSON.stringify({ quantity })
      });
      
      if (!response.ok) {
        throw new Error(`Failed to update item quantity: ${response.statusText}`);
      }
      
      // Get updated cart after update
      return this.getCart();
    } catch (error) {
      console.error('Error updating quantity in server cart:', error);
      // Fallback to local cart in case of error
      return this.updateLocalQuantity(itemId, quantity);
    }
  },
  
  updateLocalQuantity(itemId: number, quantity: number): CartItem[] {
    const cart = this.getLocalCart();
    const itemIndex = cart.findIndex(item => item.id === itemId);
    
    if (itemIndex >= 0) {
      cart[itemIndex].quantity = quantity;
      this.saveLocalCart(cart);
    }
    
    return cart;
  },

  async removeItem(itemId: number): Promise<CartItem[]> {
    const authStore = useAuthStore();
    const config = useRuntimeConfig();
    const apiUrl = config.public.apiUrl || 'http://localhost:8000';
    
    if (!authStore.isAuthenticated) {
      // For non-authenticated users, use local storage
      return this.removeLocalItem(itemId);
    }
    
    try {
      // First, need to get the cart to find the cart item id
      const cart = await this.getCart();
      // Find the cart item that contains this product
      const cartItem = cart.find(item => item.id === itemId);
      
      if (!cartItem) {
        throw new Error(`Item with id ${itemId} not found in cart`);
      }
      
      // Remove item from server cart
      const response = await fetch(`${apiUrl}/api/cart/remove/${cartItem.product_id}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Token ${authStore.token}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to remove item from cart: ${response.statusText}`);
      }
      
      // Get updated cart after removal
      return this.getCart();
    } catch (error) {
      console.error('Error removing item from server cart:', error);
      // Fallback to local cart in case of error
      return this.removeLocalItem(itemId);
    }
  },
  
  removeLocalItem(itemId: number): CartItem[] {
    const cart = this.getLocalCart();
    const updatedCart = cart.filter(item => item.id !== itemId);
    this.saveLocalCart(updatedCart);
    return updatedCart;
  },

  async clearCart(): Promise<void> {
    const authStore = useAuthStore();
    const config = useRuntimeConfig();
    const apiUrl = config.public.apiUrl || 'http://localhost:8000';
    
    if (!authStore.isAuthenticated) {
      // For non-authenticated users, use local storage
      this.clearLocalCart();
      return;
    }
    
    try {
      // Clear server cart
      const response = await fetch(`${apiUrl}/api/cart/clear/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Token ${authStore.token}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to clear cart: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Error clearing server cart:', error);
      // Fallback to local cart in case of error
      this.clearLocalCart();
    }
  },
  
  clearLocalCart(): void {
    if (import.meta.client) {
      const authStore = useAuthStore();
      const currentUser = authStore.user?.username || 'guest';
      localStorage.removeItem(`cart_${currentUser}`);
    }
  },

  async getCartTotal(): Promise<number> {
    const cart = await this.getCart();
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  },

  async getCartItemCount(): Promise<number> {
    const cart = await this.getCart();
    return cart.reduce((count, item) => count + item.quantity, 0);
  }
};