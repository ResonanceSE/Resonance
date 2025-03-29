import { useAuthStore } from '~/stores/useAuth'


interface OrderItem {
  id: number
  product: number
  quantity: number
  price: number
}

interface Order {
  user : string
  id: number
  items: OrderItem[]
  total: number
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
  shipping_address: string
  payment_method: string
  created_at: string
  updated_at: string
}

interface CartItem {
  id: number      
  quantity: number
  name?: string
  price?: number
  category?: string
  image?: string
}

export const orderService = {
  async createOrder(shippingAddress: string, cartItems?: CartItem[]): Promise<Order> {
    try {
      const requestBody: {
        shipping_address: string;
        cart_items?: string;
      } = {
        shipping_address: shippingAddress,
      }
      
      if (cartItems && cartItems.length > 0) {
        const simplifiedCartItems = cartItems.map(item => ({
          id: item.id,    
          quantity: item.quantity
        }));
        
        requestBody.cart_items = JSON.stringify(simplifiedCartItems)
      }
      
      const response = await fetch(
        `${useRuntimeConfig().public.apiUrl}/api/orders/create/`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Token ${useAuthStore().token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        }
      )

      const result = await response.json()
      if (result.status === 'success') {
        return result.data
      }
      throw new Error(result.message || "Failed to create order")
    } catch (error) {
      console.error('Create order error:', error)
      throw error instanceof Error ? error : new Error('Unknown error occurred')
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
      throw new Error(result.message || "Failed to get orders")
    } catch (error) {
      console.error('Get orders error:', error)
      throw error instanceof Error ? error : new Error('Unknown error occurred')
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
      throw new Error(result.message || "Failed to get order details")
    } catch (error) {
      console.error('Get order error:', error)
      throw error instanceof Error ? error : new Error('Unknown error occurred')
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
      throw new Error(result.message || "Failed to get order history")
    } catch (error) {
      console.error('Get order history error:', error)
      throw error instanceof Error ? error : new Error('Unknown error occurred')
    }
  }
}