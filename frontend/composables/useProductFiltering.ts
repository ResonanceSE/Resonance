interface Product {
    id: number;
    name: string;
    description?: string;
    slug?: string;
    category?: string;
    brand?: string;
    connections?: string;
    price: number | string;
    sale_price?: number | string | null;
    stock?: number;
    is_active?: boolean;
    is_new?: boolean;
    is_featured?: boolean;
    image_url?: string;
    tags?: string[];
  }
  
  interface ApiFilterResponse {
    brands?: Array<{brand?: string; name?: string; count?: number}>;
    connections?: Array<{connections?: string; name?: string; count?: number}>;
    types?: Array<{name: string; count?: number}>;
    price_ranges?: Array<{name: string; min: number; max: number|null; count?: number}>;
  }
  
  interface FilterState {
    category: string;
    searchQuery: string;
    brands: string[];
    priceRanges: string[];
    connections: string[];
    sortBy: string;
  }
  
  export function useProductFiltering() {
    const config = useRuntimeConfig();
    const apiUrl = config.public.apiUrl || 'http://localhost:8000';
    const products = ref<Product[]>([]);
    const filteredProducts = ref<Product[]>([]);
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);
    
    const filters = reactive<FilterState>({
      category: '',
      searchQuery: '',
      brands: [],
      priceRanges: [],
      connections: [],
      sortBy: 'default'
    });
    
    const fetchFilters = async (): Promise<ApiFilterResponse> => {
      try {
        const response = await fetch(`${apiUrl}/api/products/filters/`);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch filters: ${response.status}`);
        }
        
        return await response.json();
      } catch (err) {
        console.error('Error fetching filters:', err);
        return {
          brands: [],
          connections: [],
          price_ranges: []
        };
      }
    };
    
    const fetchProducts = async (category: string = ''): Promise<Product[]> => {
      isLoading.value = true;
      error.value = null;
      console.log("Fetching products for category:", category);
      try {
        const url = category 
          ? `${apiUrl}/api/products/${category}/` 
          : `${apiUrl}/api/products/`;
          
        const response = await fetch(url);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch products: ${response.status}`);
        }
        
        const data = await response.json();
        products.value = data;
        filters.category = category;
        applyFilters();
        
        return data;
      } catch (err) {
        console.error('Error fetching products:', err);
        error.value = err instanceof Error ? err.message : 'Failed to load products data';
        products.value = [];
        filteredProducts.value = [];
        return [];
      } finally {
        isLoading.value = false;
      }
    };
    
    const applyFilters = (): Product[] => {
      let result = [...products.value];
      if (filters.searchQuery) {
        const query = filters.searchQuery.toLowerCase();
        result = result.filter(product => 
          product.name?.toLowerCase().includes(query) || 
          product.description?.toLowerCase().includes(query)
        );
      }
      
      if (filters.brands.length > 0) {
        result = result.filter(product => 
          product.brand && filters.brands.includes(product.brand)
        );
      }
      
      if (filters.connections.length > 0) {
        result = result.filter(product => {
          const productConnections = product.connections?.split(',').map(c => c.trim());
          return productConnections && filters.connections.some(conn => 
            productConnections.includes(conn)
          );
        });
      }
      
      if (filters.priceRanges.length > 0) {
        result = result.filter(product => {
          const price = parseFloat(typeof product.price === 'string' ? product.price : product.price.toString());
          
          return filters.priceRanges.some(range => {
            if (range === 'Under $100' && price < 100) return true;
            if (range === '$100 - $300' && price >= 100 && price < 300) return true;
            if (range === '$300 - $500' && price >= 300 && price < 500) return true;
            if (range === 'Over $500' && price >= 500) return true;
            return false;
          });
        });
      }
      
      if (filters.sortBy !== 'default') {
        result = [...result];
        
        switch (filters.sortBy) {
          case 'price-low':
            result.sort((a, b) => {
              const aPrice = parseFloat(typeof a.price === 'string' ? a.price : a.price.toString());
              const bPrice = parseFloat(typeof b.price === 'string' ? b.price : b.price.toString());
              return aPrice - bPrice;
            });
            break;
          case 'price-high':
            result.sort((a, b) => {
              const aPrice = parseFloat(typeof a.price === 'string' ? a.price : a.price.toString());
              const bPrice = parseFloat(typeof b.price === 'string' ? b.price : b.price.toString());
              return bPrice - aPrice;
            });
            break;
          case 'name':
            result.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
            break;
        }
      }
      
      filteredProducts.value = result;
      return result;
    };
    
    const updateFilters = (newFilters: Partial<FilterState>): Product[] => {
      Object.assign(filters, newFilters);
      return applyFilters();
    };
    
    return {
      products,
      filteredProducts,
      filters,
      isLoading,
      error,
      fetchProducts,
      fetchFilters,
      updateFilters
    };
  }