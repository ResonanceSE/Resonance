import { useAuthStore } from '~/stores/useAuth'

interface OrderItem {
  id: number
  product: number
  quantity: number
  price: number
}

interface Order {
  id: number
  items: OrderItem[]
  total: number
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
  shipping_address: string
  payment_method: string
  created_at: string
  updated_at: string
}

export const orderService = {
  async createOrder(shippingAddress: string, paymentMethod: string): Promise<Order> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/orders/create/`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Token ${useAuthStore().token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            shipping_address: shippingAddress,
            payment_method: paymentMethod,
          }),
        }
      )

      const result = await response.json()
      if (result.status === 'success') {
        return result.data
      }
      throw new Error(result.message)
    } catch (error) {
      console.error('Create order error:', error)
      throw error
    }
  },

  async getOrders(): Promise<Order[]> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/orders/`,
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
      console.error('Get orders error:', error)
      throw error
    }
  },

  async getOrderById(id: number): Promise<Order> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/orders/${id}/`,
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
      console.error('Get order error:', error)
      throw error
    }
  },

  async cancelOrder(id: number): Promise<Order> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/orders/${id}/cancel/`,
        {
          method: 'POST',
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
      console.error('Cancel order error:', error)
      throw error
    }
  },

  async getOrderHistory(): Promise<Order[]> {
    try {
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/orders/history/`,
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
      console.error('Get order history error:', error)
      throw error
    }
  }
} 