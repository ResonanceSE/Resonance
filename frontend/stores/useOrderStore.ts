import { defineStore } from 'pinia';
import { useAuthStore } from '~/stores/useAuth';


export type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';

export interface Order {
  id: number;
  order_number: string;
  user: string;
  status: OrderStatus;
  total_amount: string;
  created_at: string;
  customer_email?: string;
  shipping_address?: string;
  items?: OrderItem[];
}

export interface OrderItem {
  id: number;
  product_id: number;
  product_name: string;
  quantity: number;
  price: number;
  subtotal: number;
}

export interface OrderFilters {
  status?: OrderStatus;
  startDate?: string;
  endDate?: string;
  search?: string;
}

export const useOrderStore = defineStore('orders', {
  state: () => ({
    orders: [] as Order[],
    currentOrder: null as Order | null,
  
    loading: false,
    error: null as string | null,
  
    page: 1,
    limit: 10,
    total: 0,
    
    filters: {
      status: undefined,
      startDate: undefined,
      endDate: undefined,
      search: '',
    } as OrderFilters,
    
    sortBy: 'created_at',
    sortDir: 'desc',
  }),
  
  getters: {
    recentOrders: (state) => {
      return [...state.orders]
        .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        .slice(0, 5);
    },
    ordersByStatus: (state) => (status: OrderStatus) => {
      return state.orders.filter(order => order.status === status);
    },
    countByStatus: (state) => {
      const counts = {
        pending: 0,
        processing: 0,
        shipped: 0,
        delivered: 0,
        cancelled: 0,
      };
      
      state.orders.forEach(order => {
        counts[order.status as keyof typeof counts]++;
      });
      
      return counts;
    },
    totalSales: (state) => {
      return state.orders.reduce((sum, order) => {
        return sum + parseFloat(order.total_amount);
      }, 0);
    },
    filteredOrders: (state) => {
      let result = [...state.orders];
      if (state.filters.status) {
        result = result.filter(order => order.status === state.filters.status);
      }
      if (state.filters.startDate) {
        const startDate = new Date(state.filters.startDate);
        result = result.filter(order => new Date(order.created_at) >= startDate);
      }
      
      if (state.filters.endDate) {
        const endDate = new Date(state.filters.endDate);
        result = result.filter(order => new Date(order.created_at) <= endDate);
      }
      if (state.filters.search) {
        const searchTerm = state.filters.search.toLowerCase();
        result = result.filter(order => 
          order.order_number.toLowerCase().includes(searchTerm) ||
          order.user.toLowerCase().includes(searchTerm)
        );
      }
      
      result.sort((a, b) => {
        let aValue , bValue;

        switch (state.sortBy) {
          case 'total_amount':
            aValue = parseFloat(a.total_amount);
            bValue = parseFloat(b.total_amount);
            break;
          case 'created_at':
            aValue = new Date(a.created_at).getTime();
            bValue = new Date(b.created_at).getTime();
            break;
          default:
            aValue = a[state.sortBy as keyof Order];
            bValue = b[state.sortBy as keyof Order];
        }
        if (state.sortDir === 'asc') {
          return aValue > bValue ? 1 : -1;
        } else {
          return aValue < bValue ? 1 : -1;
        }
      });
      
      return result;
    },
    
    paginatedOrders: (state) => {
      const start = (state.page - 1) * state.limit;
      const end = start + state.limit;
      return state.orders.slice(start, end);
    },
  },
  
  actions: {
    // Set loading state
    setLoading(isLoading: boolean) {
      this.loading = isLoading;
    },
    
    // Set error state
    setError(error: string | null) {
      this.error = error;
    },
    
    // Set filters
    setFilters(filters: Partial<OrderFilters>) {
      this.filters = { ...this.filters, ...filters };
      this.page = 1; // Reset to first page when filters change
    },
    
    // Reset filters
    resetFilters() {
      this.filters = {
        status: undefined,
        startDate: undefined,
        endDate: undefined,
        search: '',
      };
      this.page = 1;
    },
    
    // Set sorting
    setSorting(sortBy: string, sortDir: 'asc' | 'desc' = 'desc') {
      this.sortBy = sortBy;
      this.sortDir = sortDir;
    },
    
    // Set pagination
    setPage(page: number) {
      this.page = page;
    },
    
    // Set items per page
    setLimit(limit: number) {
      this.limit = limit;
      this.page = 1; // Reset to first page when limit changes
    },
    
    // Fetch all orders
    async fetchOrders() {
      this.setLoading(true);
      this.setError(null);
      
      try {
        const authStore = useAuthStore();
        const config = useRuntimeConfig();
        const apiUrl = config.public.apiUrl || 'http://localhost:8000';
        
        // Build the query parameters for filtering and pagination
        const queryParams = new URLSearchParams();
        
        if (this.filters.status) {
          queryParams.append('status', this.filters.status);
        }
        
        if (this.filters.startDate) {
          queryParams.append('start_date', this.filters.startDate);
        }
        
        if (this.filters.endDate) {
          queryParams.append('end_date', this.filters.endDate);
        }
        
        if (this.filters.search) {
          queryParams.append('search', this.filters.search);
        }
        
        queryParams.append('page', this.page.toString());
        queryParams.append('limit', this.limit.toString());
        
        queryParams.append('sort_by', this.sortBy);
        queryParams.append('sort_dir', this.sortDir);
        
        const response = await fetch(`${apiUrl}/api/staff/orders/?${queryParams.toString()}`, {
          headers: {
            'Authorization': `Token ${authStore.token}`
          }
        });
        
        if (!response.ok) {
          throw new Error(`Failed to fetch orders: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (Array.isArray(data)) {
          this.orders = data;
          this.total = data.length;
        } else if (data.results && Array.isArray(data.results)) {
          this.orders = data.results;
          this.total = data.count || data.results.length;
        } else {
          this.orders = [];
          this.total = 0;
        }
      } catch (error) {
        console.error('Error fetching orders:', error);
        this.setError(error instanceof Error ? error.message : 'Failed to load orders');
        this.orders = [];
        this.total = 0;
      } finally {
        this.setLoading(false);
      }
    },
    
    async fetchOrder(orderId: number) {
      this.setLoading(true);
      this.setError(null);
      
      try {
        const authStore = useAuthStore();
        const config = useRuntimeConfig();
        const apiUrl = config.public.apiUrl || 'http://localhost:8000';
        
        const response = await fetch(`${apiUrl}/api/staff/orders/${orderId}/`, {
          headers: {
            'Authorization': `Token ${authStore.token}`
          }
        });
        
        if (!response.ok) {
          throw new Error(`Failed to fetch order: ${response.statusText}`);
        }
        
        const data = await response.json();
        this.currentOrder = data;
      } catch (error) {
        console.error(`Error fetching order ${orderId}:`, error);
        this.setError(error instanceof Error ? error.message : 'Failed to load order details');
        this.currentOrder = null;
      } finally {
        this.setLoading(false);
      }
    },
    async updateOrderStatus(orderId: number, status: OrderStatus) {
      this.setLoading(true);
      this.setError(null);
      
      try {
        const authStore = useAuthStore();
        const config = useRuntimeConfig();
        const apiUrl = config.public.apiUrl || 'http://localhost:8000';
        
        const response = await fetch(`${apiUrl}/api/staff/orders/${orderId}/status/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${authStore.token}`
          },
          body: JSON.stringify({ status })
        });
        
        if (!response.ok) {
          throw new Error(`Failed to update order status: ${response.statusText}`);
        }
        
        const updatedOrder = await response.json();
        const index = this.orders.findIndex(order => order.id === orderId);
        if (index !== -1) {
          this.orders[index] = updatedOrder;
        }
        
        if (this.currentOrder && this.currentOrder.id === orderId) {
          this.currentOrder = updatedOrder;
        }
        
        return true;
      } catch (error) {
        console.error(`Error updating order ${orderId} status:`, error);
        this.setError(error instanceof Error ? error.message : 'Failed to update order status');
        return false;
      } finally {
        this.setLoading(false);
      }
    },
    
    async deleteOrder(orderId: number) {
      this.setLoading(true);
      this.setError(null);
      
      try {
        const authStore = useAuthStore();
        const config = useRuntimeConfig();
        const apiUrl = config.public.apiUrl || 'http://localhost:8000';
        
        const response = await fetch(`${apiUrl}/api/staff/orders/${orderId}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Token ${authStore.token}`
          }
        });
        
        if (!response.ok) {
          throw new Error(`Failed to delete order: ${response.statusText}`);
        }
        
        this.orders = this.orders.filter(order => order.id !== orderId);
        
        if (this.currentOrder && this.currentOrder.id === orderId) {
          this.currentOrder = null;
        }
        
        return true;
      } catch (error) {
        console.error(`Error deleting order ${orderId}:`, error);
        this.setError(error instanceof Error ? error.message : 'Failed to delete order');
        return false;
      } finally {
        this.setLoading(false);
      }
    }
  }
});