import { useAuthStore } from '~/stores/useAuth'

interface CartItem {
  id: number
  product: number
  quantity: number
  price: number
}

interface Cart {
  id: number
  items: CartItem[]
  total: number
  created_at: string
  updated_at: string
}

export const cartService = {
  async getCart(): Promise<Cart> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/cart/`,
        {
          headers: {
            'Authorization': `Token ${useAuthStore().token}`,
          },
        }
      )

      const result = await response.json()
      if (result.status === 'success') {
        return result.data
      }
      throw new Error(result.message)
    } catch (error) {
      console.error('Get cart error:', error)
      throw error
    }
  },

  async addToCart(productId: number, quantity: number = 1): Promise<Cart> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/cart/add/`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Token ${useAuthStore().token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            product: productId,
            quantity,
          }),
        }
      )

      const result = await response.json()
      if (result.status === 'success') {
        return result.data
      }
      throw new Error(result.message)
    } catch (error) {
      console.error('Add to cart error:', error)
      throw error
    }
  },

  async updateCartItem(itemId: number, quantity: number): Promise<Cart> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/cart/update/${itemId}/`,
        {
          method: 'PUT',
          headers: {
            'Authorization': `Token ${useAuthStore().token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            quantity,
          }),
        }
      )

      const result = await response.json()
      if (result.status === 'success') {
        return result.data
      }
      throw new Error(result.message)
    } catch (error) {
      console.error('Update cart item error:', error)
      throw error
    }
  },

  async removeFromCart(itemId: number): Promise<Cart> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/cart/remove/${itemId}/`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Token ${useAuthStore().token}`,
          },
        }
      )

      const result = await response.json()
      if (result.status === 'success') {
        return result.data
      }
      throw new Error(result.message)
    } catch (error) {
      console.error('Remove from cart error:', error)
      throw error
    }
  },

  async clearCart(): Promise<Cart> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/cart/clear/`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Token ${useAuthStore().token}`,
          },
        }
      )

      const result = await response.json()
      if (result.status === 'success') {
        return result.data
      }
      throw new Error(result.message)
    } catch (error) {
      console.error('Clear cart error:', error)
      throw error
    }
  }
} 