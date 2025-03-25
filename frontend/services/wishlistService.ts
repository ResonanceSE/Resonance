import { useAuthStore } from '~/stores/useAuth'

interface WishlistItem {
  id: number
  product: number
  added_at: string
}

interface Wishlist {
  id: number
  items: WishlistItem[]
  created_at: string
  updated_at: string
}

export const wishlistService = {
  async getWishlist(): Promise<Wishlist> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/wishlist/`,
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
      console.error('Get wishlist error:', error)
      throw error
    }
  },

  async addToWishlist(productId: number): Promise<Wishlist> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/wishlist/add/`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Token ${useAuthStore().token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            product: productId,
          }),
        }
      )

      const result = await response.json()
      if (result.status === 'success') {
        return result.data
      }
      throw new Error(result.message)
    } catch (error) {
      console.error('Add to wishlist error:', error)
      throw error
    }
  },

  async removeFromWishlist(productId: number): Promise<Wishlist> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/wishlist/remove/${productId}/`,
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
      console.error('Remove from wishlist error:', error)
      throw error
    }
  },

  async clearWishlist(): Promise<Wishlist> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/wishlist/clear/`,
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
      console.error('Clear wishlist error:', error)
      throw error
    }
  },

  async isInWishlist(productId: number): Promise<boolean> {
    try {
      const wishlist = await this.getWishlist()
      return wishlist.items.some(item => item.product === productId)
    } catch (error) {
      console.error('Check wishlist error:', error)
      return false
    }
  }
} 