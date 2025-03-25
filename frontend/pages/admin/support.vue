<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Support Queries</h1>

    <!-- Support Queries Table -->
    <div class="bg-white rounded-lg shadow overflow-x-auto">
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
          <tr v-for="query in queries" :key="query.id">
            <td class="px-6 py-4">#{{ query.id }}</td>
            <td class="px-6 py-4">{{ query.customer_name }}</td>
            <td class="px-6 py-4">{{ query.subject }}</td>
            <td class="px-6 py-4">
              <span :class="getStatusClass(query.status)">
                {{ query.status }}
              </span>
            </td>
            <td class="px-6 py-4">{{ formatDate(query.created_at) }}</td>
            <td class="px-6 py-4">
              <button
                @click="viewQueryDetails(query)"
                class="text-blue-600 hover:text-blue-800"
              >
                View Details
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Query Details Modal -->
    <div v-if="selectedQuery" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg w-full max-w-2xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">
            Support Query #{{ selectedQuery.id }}
          </h2>
          <button @click="selectedQuery = null" class="text-gray-500 hover:text-gray-700">
            Close
          </button>
        </div>

        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <h3 class="font-medium text-gray-700">Status</h3>
              <select
                v-model="selectedQuery.status"
                @change="updateQueryStatus(selectedQuery)"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
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

          <div>
            <h3 class="font-medium text-gray-700">Customer</h3>
            <p>{{ selectedQuery.customer_name }}</p>
            <p class="text-sm text-gray-500">{{ selectedQuery.customer_email }}</p>
          </div>

          <div>
            <h3 class="font-medium text-gray-700">Subject</h3>
            <p>{{ selectedQuery.subject }}</p>
          </div>

          <div>
            <h3 class="font-medium text-gray-700">Message</h3>
            <p class="whitespace-pre-wrap">{{ selectedQuery.message }}</p>
          </div>

          <div class="border-t pt-4">
            <h3 class="font-medium text-gray-700 mb-2">Reply</h3>
            <textarea
              v-model="replyMessage"
              rows="4"
              class="block w-full rounded-md border-gray-300 shadow-sm"
              placeholder="Type your reply..."
            ></textarea>
            <div class="mt-2 flex justify-end">
              <button
                @click="sendReply"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
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

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '~/stores/auth';

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

const queries = ref<SupportQuery[]>([]);
const selectedQuery = ref<SupportQuery | null>(null);
const replyMessage = ref('');

// Fetch support queries
const fetchQueries = async () => {
  try {
    const response = await fetch('/api/staff/support/', {
      headers: {
        'Authorization': `Token ${useAuthStore().token}`
      }
    });
    
    if (response.ok) {
      queries.value = await response.json();
    }
  } catch (error) {
    console.error('Error fetching support queries:', error);
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
      await fetchQueries();
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
    }
  } catch (error) {
    console.error('Error fetching query details:', error);
  }
};

// Send reply
const sendReply = async () => {
  if (!selectedQuery.value || !replyMessage.value.trim()) return;
  
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
      replyMessage.value = '';
      await viewQueryDetails(selectedQuery.value);
    }
  } catch (error) {
    console.error('Error sending reply:', error);
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
    open: 'text-yellow-600',
    in_progress: 'text-blue-600',
    resolved: 'text-green-600',
    closed: 'text-gray-600'
  };
  return classes[status as keyof typeof classes] || '';
};

onMounted(fetchQueries);
</script> 