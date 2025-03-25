<script setup lang="ts">
import { useAuthStore } from '~/stores/useAuth';

definePageMeta({
  layout: 'admin'
});


interface SupportQuery {
  id: number;
  customer_name: string;
  customer_email: string;
  subject: string;
  message: string;
  status: string;
  created_at: string;
}

interface Reply {
  id: number;
  message: string;
  created_at: string;
  is_staff: boolean;
}

// State
const queries = ref<SupportQuery[]>([]);
const selectedQuery = ref<SupportQuery | null>(null);
const replyMessage = ref('');
const loading = ref(false);
const error = ref('');
const replies = ref<Reply[]>([]);
const replySending = ref(false);
const replySent = ref(false);

// Pagination
const currentPage = ref(1);
const itemsPerPage = ref(10);

// Filters
const searchTerm = ref('');
const statusFilter = ref('');
const sortBy = ref('created_at_desc');
const debounceTimeout = ref<NodeJS.Timeout | null>(null);

// State variables initialized above

// Computed properties
const filteredQueries = computed(() => {
  let result = [...queries.value];

  // Apply search filter
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase();
    result = result.filter(query => 
      query.customer_name.toLowerCase().includes(term) || 
      query.subject.toLowerCase().includes(term)
    );
  }

  // Apply status filter
  if (statusFilter.value) {
    result = result.filter(query => query.status === statusFilter.value);
  }

  // Apply sorting
  if (sortBy.value === 'created_at_desc') {
    result.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
  } else if (sortBy.value === 'created_at_asc') {
    result.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
  } else if (sortBy.value === 'status') {
    const statusOrder = { open: 1, in_progress: 2, resolved: 3, closed: 4 };
    result.sort((a, b) => statusOrder[a.status as keyof typeof statusOrder] - statusOrder[b.status as keyof typeof statusOrder]);
  }

  return result;
});

const totalPages = computed(() => Math.ceil(filteredQueries.value.length / itemsPerPage.value));

const paginatedQueries = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredQueries.value.slice(start, end);
});

const pagination = computed(() => {
  const total = filteredQueries.value.length;
  const from = total === 0 ? 0 : (currentPage.value - 1) * itemsPerPage.value + 1;
  const to = Math.min(currentPage.value * itemsPerPage.value, total);
  
  return { from, to, total };
});

// Watch for filter changes to reset pagination
watch([searchTerm, statusFilter, sortBy], () => {
  currentPage.value = 1;
});

// Fetch support queries
const fetchQueries = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    const response = await fetch('/api/staff/support/', {
      headers: {
        'Authorization': `Token ${useAuthStore().token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch: ${response.status}`);
    }
    
    queries.value = await response.json();
  } catch (err) {
    console.error('Error fetching support queries:', err);
    error.value = 'Failed to load support queries. Please try again.';
  } finally {
    loading.value = false;
  }
};

// Fetch replies for selected query
const fetchReplies = async (queryId: number) => {
  try {
    const response = await fetch(`/api/staff/support/${queryId}/replies/`, {
      headers: {
        'Authorization': `Token ${useAuthStore().token}`
      }
    });
    
    if (response.ok) {
      replies.value = await response.json();
    } else {
      replies.value = [];
    }
  } catch (error) {
    console.error('Error fetching replies:', error);
    replies.value = [];
  }
};

// Update query status
const updateQueryStatus = async (query: SupportQuery) => {
  try {
    const response = await fetch(`/api/staff/support/${query.id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${useAuthStore().token}`
      },
      body: JSON.stringify({ status: query.status })
    });
    
    if (response.ok) {
      // Update the query in the list
      const index = queries.value.findIndex(q => q.id === query.id);
      if (index !== -1) {
        queries.value[index].status = query.status;
      }
    }
  } catch (error) {
    console.error('Error updating query status:', error);
  }
};

// View query details
const viewQueryDetails = async (query: SupportQuery) => {
  try {
    const response = await fetch(`/api/staff/support/${query.id}/`, {
      headers: {
        'Authorization': `Token ${useAuthStore().token}`
      }
    });
    
    if (response.ok) {
      selectedQuery.value = await response.json();
      replyMessage.value = '';
      replySent.value = false;
      
      // Also fetch replies
      await fetchReplies(query.id);
    }
  } catch (error) {
    console.error('Error fetching query details:', error);
  }
};

// Send reply
const sendReply = async () => {
  if (!selectedQuery.value || !replyMessage.value.trim()) return;
  
  replySending.value = true;
  replySent.value = false;
  
  try {
    const response = await fetch(`/api/staff/support/${selectedQuery.value.id}/reply/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${useAuthStore().token}`
      },
      body: JSON.stringify({ message: replyMessage.value })
    });
    
    if (response.ok) {
      // Add the new reply to the list
      const newReply = await response.json();
      replies.value.push(newReply);
      replyMessage.value = '';
      replySent.value = true;
    }
  } catch (error) {
    console.error('Error sending reply:', error);
  } finally {
    replySending.value = false;
  }
};

// Format date
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Get status class for styling
const getStatusClass = (status: string) => {
  const classes = {
    open: 'bg-yellow-100 text-yellow-800',
    in_progress: 'bg-blue-100 text-blue-800',
    resolved: 'bg-green-100 text-green-800',
    closed: 'bg-gray-100 text-gray-800'
  };
  return classes[status as keyof typeof classes] || '';
};

// Format status display
const formatStatus = (status: string) => {
  const statusMap: Record<string, string> = {
    open: 'Open',
    in_progress: 'In Progress',
    resolved: 'Resolved',
    closed: 'Closed'
  };
  return statusMap[status] || status;
};

// Search handler with debounce
const handleSearch = () => {
  if (debounceTimeout.value) {
    clearTimeout(debounceTimeout.value);
  }
  
  debounceTimeout.value = setTimeout(() => {
    // The computed filteredQueries will update automatically
  }, 300);
};

// Filter change handler
const handleFilterChange = () => {
  // The computed filteredQueries will update automatically
};

// Sort change handler
const handleSortChange = () => {
  // The computed filteredQueries will update automatically
};

// Reset filters
const resetFilters = () => {
  searchTerm.value = '';
  statusFilter.value = '';
  sortBy.value = 'created_at_desc';
  currentPage.value = 1;
};

// Close query details and refresh list
const closeQueryDetails = () => {
  selectedQuery.value = null;
  fetchQueries(); // Refresh the list to reflect any changes
};

// Lifecycle
onMounted(fetchQueries);
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Support Queries</h1>

    <!-- Search and Filters -->
    <div class="mb-6 bg-white rounded-lg shadow p-4">
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-1">
          <input
            v-model="searchTerm"
            type="text"
            placeholder="Search by customer name or subject..."
            class="input input-bordered w-full"
            @input="handleSearch"
          />
        </div>
        <div class="flex-1 flex gap-4">
          <select
            v-model="statusFilter"
            class="select select-bordered flex-1"
            @change="handleFilterChange"
          >
            <option value="">All Statuses</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>
          <select
            v-model="sortBy"
            class="select select-bordered flex-1"
            @change="handleSortChange"
          >
            <option value="created_at_desc">Newest First</option>
            <option value="created_at_asc">Oldest First</option>
            <option value="status">By Status</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center my-8">
      <div class="loading loading-spinner loading-lg text-primary"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-error shadow-lg my-4">
      <div>
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <span>{{ error }}</span>
      </div>
      <div class="flex-none">
        <button @click="fetchQueries" class="btn btn-sm">Retry</button>
      </div>
    </div>

    <!-- Support Queries Table -->
    <div v-else-if="filteredQueries.length > 0" class="bg-white rounded-lg shadow overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Query ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Subject</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="query in paginatedQueries" :key="query.id">
            <td class="px-6 py-4">#{{ query.id }}</td>
            <td class="px-6 py-4">{{ query.customer_name }}</td>
            <td class="px-6 py-4">{{ query.subject }}</td>
            <td class="px-6 py-4">
              <span :class="getStatusClass(query.status)" class="px-2 py-1 rounded-full text-xs">
                {{ formatStatus(query.status) }}
              </span>
            </td>
            <td class="px-6 py-4">{{ formatDate(query.created_at) }}</td>
            <td class="px-6 py-4">
              <button
                @click="viewQueryDetails(query)"
                class="btn btn-sm btn-ghost text-blue-600 hover:text-blue-800"
              >
                View Details
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <!-- Pagination -->
      <div class="px-6 py-4 flex items-center justify-between border-t border-gray-200">
        <div>
          <p class="text-sm text-gray-700">
            Showing <span class="font-medium">{{ pagination.from }}</span> to <span class="font-medium">{{ pagination.to }}</span> of <span class="font-medium">{{ filteredQueries.length }}</span> results
          </p>
        </div>
        <div class="join">
          <button 
            class="join-item btn btn-sm" 
            :disabled="currentPage === 1"
            @click="currentPage--"
          >
            Previous
          </button>
          <button 
            v-for="page in totalPages" 
            :key="page" 
            @click="currentPage = page"
            :class="['join-item btn btn-sm', currentPage === page ? 'btn-active' : '']"
          >
            {{ page }}
          </button>
          <button 
            class="join-item btn btn-sm" 
            :disabled="currentPage === totalPages"
            @click="currentPage++"
          >
            Next
          </button>
        </div>
      </div>
    </div>
    
    <!-- Empty State -->
    <div v-else class="bg-white rounded-lg shadow p-8 text-center">
      <div class="text-gray-500 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900">No support queries found</h3>
      <p class="mt-1 text-sm text-gray-500">
        {{ searchTerm || statusFilter ? 'Try adjusting your filters' : 'All support queries will appear here' }}
      </p>
      <div class="mt-6">
        <button @click="resetFilters" class="btn btn-primary">
          Reset Filters
        </button>
      </div>
    </div>

    <!-- Query Details Modal -->
    <div v-if="selectedQuery" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 overflow-y-auto">
      <div class="bg-white p-6 rounded-lg w-full max-w-3xl mx-4 my-8">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">
            Support Query #{{ selectedQuery.id }}
          </h2>
          <button @click="closeQueryDetails" class="btn btn-sm btn-circle">
            ✕
          </button>
        </div>

        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 class="font-medium text-gray-700">Status</h3>
              <select
                v-model="selectedQuery.status"
                @change="updateQueryStatus(selectedQuery)"
                class="select select-bordered w-full mt-1"
              >
                <option value="open">Open</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="closed">Closed</option>
              </select>
            </div>
            <div>
              <h3 class="font-medium text-gray-700">Date</h3>
              <p>{{ formatDate(selectedQuery.created_at) }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 class="font-medium text-gray-700">Customer</h3>
              <p>{{ selectedQuery.customer_name }}</p>
              <p class="text-sm text-gray-500">{{ selectedQuery.customer_email }}</p>
            </div>
            <div>
              <h3 class="font-medium text-gray-700">Subject</h3>
              <p>{{ selectedQuery.subject }}</p>
            </div>
          </div>

          <div class="card bg-base-100">
            <div class="card-body p-4 bg-gray-50 rounded-lg">
              <h3 class="card-title text-sm font-medium text-gray-700">Original Message</h3>
              <p class="whitespace-pre-wrap">{{ selectedQuery.message }}</p>
            </div>
          </div>

          <!-- Reply History -->
          <div v-if="replies.length > 0">
            <h3 class="font-medium text-gray-700 mb-2">Conversation History</h3>
            <div class="space-y-3">
              <div 
                v-for="(reply, index) in replies" 
                :key="index"
                :class="[
                  'p-3 rounded-lg', 
                  reply.is_staff ? 'bg-blue-50 ml-8' : 'bg-gray-50 mr-8'
                ]"
              >
                <div class="flex justify-between items-start mb-1">
                  <span class="font-medium">
                    {{ reply.is_staff ? 'Support Agent' : selectedQuery.customer_name }}
                  </span>
                  <span class="text-xs text-gray-500">{{ formatDate(reply.created_at) }}</span>
                </div>
                <p class="whitespace-pre-wrap">{{ reply.message }}</p>
              </div>
            </div>
          </div>

          <div class="border-t pt-4">
            <h3 class="font-medium text-gray-700 mb-2">Reply</h3>
            <textarea
              v-model="replyMessage"
              rows="4"
              class="textarea textarea-bordered w-full"
              placeholder="Type your reply..."
            ></textarea>
            <div class="mt-2 flex justify-between">
              <div class="flex items-center">
                <span class="text-sm text-gray-500" v-if="replySending">Sending...</span>
                <span class="text-sm text-green-500" v-if="replySent">Reply sent successfully!</span>
              </div>
              <button
                @click="sendReply"
                class="btn btn-primary"
                :disabled="!replyMessage.trim() || replySending"
              >
                Send Reply
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
/* Add any component-specific styles here */
</style>