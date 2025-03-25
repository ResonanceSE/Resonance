import { useAuthStore } from '~/stores/useAuth'

interface Product {
  id: number
  name: string
  slug: string
  description: string
  category: number
  brand: string
  connections: string
  price: number
  sale_price?: number
  stock: number
  sku: string
  weight?: number
  dimensions?: string
  is_active: boolean
  is_featured: boolean
  is_new: boolean
  image_url?: string
  created_at: string
  updated_at: string
}

interface ProductFilters {
  category?: string
  brand?: string
  min_price?: number
  max_price?: number
  is_featured?: boolean
  is_new?: boolean
  search?: string
}

export const productService = {
  async getProducts(filters?: ProductFilters): Promise<Product[]> {
    try {
      const queryParams = new URLSearchParams()
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined) {
            queryParams.append(key, value.toString())
          }
        })
      }

      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/products/?${queryParams.toString()}`,
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
      console.error('Get products error:', error)
      throw error
    }
  },

  async getProductById(id: number): Promise<Product> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/products/${id}/`,
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
      console.error('Get product error:', error)
      throw error
    }
  },

  async getProductFilters(): Promise<{
    categories: string[]
    brands: string[]
    price_range: { min: number; max: number }
  }> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/products/filters/`,
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
      console.error('Get filters error:', error)
      throw error
    }
  },

  async getProductsByCategory(category: string): Promise<Product[]> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/products/${category}/`,
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
      console.error('Get products by category error:', error)
      throw error
    }
  },

  async getFeaturedProducts(): Promise<Product[]> {
    return this.getProducts({ is_featured: true })
  },

  async getNewProducts(): Promise<Product[]> {
    return this.getProducts({ is_new: true })
  },

  async searchProducts(query: string): Promise<Product[]> {
    return this.getProducts({ search: query })
  }
} 