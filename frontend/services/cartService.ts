import { useAuthStore } from '~/stores/useAuth'


export interface CartItem {
  id: number
  name: string
  category: string
  price: number
  quantity: number
  image?: string
}

export const cartService = {
  getCart(): CartItem[] {
    const authStore = useAuthStore();
    const currentUser = authStore.user?.username || 'guest';
    
    if (import.meta.client) {
      try {
        const cartData = localStorage.getItem(`cart_${currentUser}`);
        return cartData ? JSON.parse(cartData) : [];
      } catch (error) {
        console.error('Error getting cart:', error);
        return [];
      }
    }
    return [];
  },

  saveCart(cart: CartItem[]): void {
    const authStore = useAuthStore();
    const currentUser = authStore.user?.username || 'guest';
    
    if (import.meta.client) {
      try {
        localStorage.setItem(`cart_${currentUser}`, JSON.stringify(cart));
      } catch (error) {
        console.error('Error saving cart:', error);
      }
    }
  },

  addToCart(item: CartItem): CartItem[] {
    const cart = this.getCart()
    const existingItemIndex = cart.findIndex(cartItem => cartItem.id === item.id)
    
    if (existingItemIndex >= 0) {
      cart[existingItemIndex].quantity += item.quantity
    } else {
      cart.push(item)
    }
    
    this.saveCart(cart)
    return cart
  },

  updateQuantity(itemId: number, quantity: number): CartItem[] {
    const cart = this.getCart()
    const itemIndex = cart.findIndex(item => item.id === itemId)
    
    if (itemIndex >= 0) {
      cart[itemIndex].quantity = quantity
      this.saveCart(cart)
    }
    
    return cart
  },

  removeItem(itemId: number): CartItem[] {
    const cart = this.getCart()
    const updatedCart = cart.filter(item => item.id !== itemId)
    this.saveCart(updatedCart)
    return updatedCart
  },

  clearCart(): void {
    if (import.meta.client) {
      localStorage.removeItem('cart')
    }
  },

  getCartTotal(): number {
    const cart = this.getCart()
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0)
  },

  getCartItemCount(): number {
    const cart = this.getCart()
    return cart.reduce((count, item) => count + item.quantity, 0)
  }
}