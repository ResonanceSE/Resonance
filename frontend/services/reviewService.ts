import { useAuthStore } from '~/stores/useAuth'

interface Review {
  id: number
  product: number
  user: number
  rating: number
  comment: string
  created_at: string
  updated_at: string
}

export const reviewService = {
  async getProductReviews(productId: number): Promise<Review[]> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/products/${productId}/reviews/`,
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
      console.error('Get product reviews error:', error)
      throw error
    }
  },

  async createReview(productId: number, rating: number, comment: string): Promise<Review> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/products/${productId}/reviews/create/`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Token ${useAuthStore().token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            rating,
            comment,
          }),
        }
      )

      const result = await response.json()
      if (result.status === 'success') {
        return result.data
      }
      throw new Error(result.message)
    } catch (error) {
      console.error('Create review error:', error)
      throw error
    }
  },

  async updateReview(reviewId: number, rating: number, comment: string): Promise<Review> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/reviews/${reviewId}/update/`,
        {
          method: 'PUT',
          headers: {
            'Authorization': `Token ${useAuthStore().token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            rating,
            comment,
          }),
        }
      )

      const result = await response.json()
      if (result.status === 'success') {
        return result.data
      }
      throw new Error(result.message)
    } catch (error) {
      console.error('Update review error:', error)
      throw error
    }
  },

  async deleteReview(reviewId: number): Promise<void> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/reviews/${reviewId}/delete/`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Token ${useAuthStore().token}`,
          },
        }
      )

      const result = await response.json()
      if (result.status !== 'success') {
        throw new Error(result.message)
      }
    } catch (error) {
      console.error('Delete review error:', error)
      throw error
    }
  },

  async getUserReviews(): Promise<Review[]> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/reviews/user/`,
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
      console.error('Get user reviews error:', error)
      throw error
    }
  }
} 