<template>
  <div class="admin-users-container">
    <h1>User Management</h1>
    
    <div class="filters">
      <div class="filter-group">
        <label>Filter by Status:</label>
        <select v-model="statusFilter">
          <option value="all">All Users</option>
          <option value="pending">Pending Approval</option>
          <option value="active">Active Users</option>
          <option value="inactive">Inactive Users</option>
        </select>
      </div>
      <div class="search-box">
        <input type="text" v-model="searchTerm" placeholder="Search by name or email...">
      </div>
    </div>
    
    <div v-if="loading" class="loading">
      Loading users...
    </div>
    
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    
    <div v-else>
      <table class="users-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Registered</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id" :class="{ 'pending': !user.is_approved, 'inactive': !user.is_active }">
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>
              <span v-if="!user.is_verified" class="status-badge unverified">Unverified</span>
              <span v-else-if="!user.is_approved" class="status-badge pending">Pending Approval</span>
              <span v-else-if="user.is_active" class="status-badge active">Active</span>
              <span v-else class="status-badge inactive">Inactive</span>
            </td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td class="actions">
              <button 
                v-if="!user.is_approved" 
                @click="approveUser(user.id)" 
                class="btn approve"
                :disabled="actionInProgress"
              >
                Approve
              </button>
              
              <button 
                v-if="user.is_approved" 
                @click="toggleUserActive(user.id)" 
                class="btn"
                :class="user.is_active ? 'deactivate' : 'activate'"
                :disabled="actionInProgress"
              >
                {{ user.is_active ? 'Deactivate' : 'Activate' }}
              </button>
              
              <button 
                @click="confirmDelete(user)" 
                class="btn delete"
                :disabled="actionInProgress"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="filteredUsers.length === 0" class="no-results">
        No users found matching your filters
      </div>
    </div>
    
    <!-- Delete Confirmation Dialog -->
    <div v-if="showDeleteDialog" class="modal-overlay" @click="cancelDelete">
      <div class="modal-content" @click.stop>
        <h2>Confirm Delete</h2>
        <p>Are you sure you want to delete user <strong>{{ userToDelete?.name }}</strong> ({{ userToDelete?.email }})?</p>
        <p class="warning">This action cannot be undone!</p>
        <div class="modal-actions">
          <button @click="cancelDelete" class="btn cancel">Cancel</button>
          <button @click="deleteUser" class="btn delete">Delete User</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../utils/axios'

export default {
  name: 'AdminUsersView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    // Check if user is admin, redirect if not
    if (!authStore.isAdmin) {
      router.push('/')
      return {}
    }
    
    const users = ref([])
    const loading = ref(true)
    const error = ref(null)
    const statusFilter = ref('all')
    const searchTerm = ref('')
    const showDeleteDialog = ref(false)
    const userToDelete = ref(null)
    const actionInProgress = ref(false)
    
    // Fetch all users
    const fetchUsers = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await api.get('/api/admin/users')
        users.value = response.data
      } catch (err) {
        console.error('Failed to fetch users:', err)
        error.value = 'Failed to load users. Please try again.'
        
        if (err.response?.status === 403) {
          router.push('/') // Redirect if not authorized
        }
      } finally {
        loading.value = false
      }
    }
    
    // Filter users based on status and search term
    const filteredUsers = computed(() => {
      let filtered = [...users.value]
      
      // Apply status filter
      if (statusFilter.value === 'pending') {
        filtered = filtered.filter(user => !user.is_approved)
      } else if (statusFilter.value === 'active') {
        filtered = filtered.filter(user => user.is_approved && user.is_active)
      } else if (statusFilter.value === 'inactive') {
        filtered = filtered.filter(user => user.is_approved && !user.is_active)
      }
      
      // Apply search term
      if (searchTerm.value.trim()) {
        const term = searchTerm.value.toLowerCase()
        filtered = filtered.filter(user => 
          user.name.toLowerCase().includes(term) || 
          user.email.toLowerCase().includes(term)
        )
      }
      
      return filtered
    })
    
    // Approve a user
    const approveUser = async (userId) => {
      actionInProgress.value = true
      
      try {
        const response = await api.put(`/api/admin/users/${userId}/approve`)
        
        // Update user in the list
        const index = users.value.findIndex(u => u.id === userId)
        if (index !== -1) {
          users.value[index] = response.data.user
        }
        
      } catch (err) {
        console.error('Failed to approve user:', err)
        error.value = 'Failed to approve user. Please try again.'
      } finally {
        actionInProgress.value = false
      }
    }
    
    // Toggle user active status
    const toggleUserActive = async (userId) => {
      actionInProgress.value = true
      
      try {
        const response = await api.put(`/api/admin/users/${userId}/toggle-active`)
        
        // Update user in the list
        const index = users.value.findIndex(u => u.id === userId)
        if (index !== -1) {
          users.value[index] = response.data.user
        }
        
      } catch (err) {
        console.error('Failed to toggle user status:', err)
        error.value = 'Failed to update user status. Please try again.'
      } finally {
        actionInProgress.value = false
      }
    }
    
    // Show delete confirmation dialog
    const confirmDelete = (user) => {
      userToDelete.value = user
      showDeleteDialog.value = true
    }
    
    // Cancel delete
    const cancelDelete = () => {
      showDeleteDialog.value = false
      userToDelete.value = null
    }
    
    // Delete a user
    const deleteUser = async () => {
      if (!userToDelete.value) return
      
      actionInProgress.value = true
      
      try {
        await api.delete(`/api/admin/users/${userToDelete.value.id}`)
        
        // Remove user from the list
        users.value = users.value.filter(u => u.id !== userToDelete.value.id)
        
        // Close dialog
        showDeleteDialog.value = false
        userToDelete.value = null
        
      } catch (err) {
        console.error('Failed to delete user:', err)
        error.value = 'Failed to delete user. Please try again.'
      } finally {
        actionInProgress.value = false
      }
    }
    
    // Format date
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
    
    // Load users when component mounts
    onMounted(fetchUsers)
    
    return {
      users,
      loading,
      error,
      statusFilter,
      searchTerm,
      filteredUsers,
      approveUser,
      toggleUserActive,
      confirmDelete,
      cancelDelete,
      deleteUser,
      showDeleteDialog,
      userToDelete,
      actionInProgress,
      formatDate
    }
  }
}
</script>

<style scoped>
.admin-users-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  margin-bottom: 1.5rem;
  color: #333;
}

.filters {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group select,
.search-box input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-box input {
  min-width: 250px;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
}

.users-table th,
.users-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.users-table th {
  background-color: #f5f5f5;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.status-badge.unverified {
  background-color: #ffccbc;
  color: #d84315;
}

.status-badge.pending {
  background-color: #fff9c4;
  color: #ff8f00;
}

.status-badge.active {
  background-color: #c8e6c9;
  color: #2e7d32;
}

.status-badge.inactive {
  background-color: #e0e0e0;
  color: #616161;
}

tr.pending {
  background-color: #fffde7;
}

tr.inactive {
  background-color: #f5f5f5;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.4rem 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn.approve {
  background-color: #4caf50;
  color: white;
}

.btn.approve:hover:not(:disabled) {
  background-color: #388e3c;
}

.btn.activate {
  background-color: #2196f3;
  color: white;
}

.btn.activate:hover:not(:disabled) {
  background-color: #1976d2;
}

.btn.deactivate {
  background-color: #ff9800;
  color: white;
}

.btn.deactivate:hover:not(:disabled) {
  background-color: #f57c00;
}

.btn.delete {
  background-color: #f44336;
  color: white;
}

.btn.delete:hover:not(:disabled) {
  background-color: #d32f2f;
}

.btn.cancel {
  background-color: #9e9e9e;
  color: white;
}

.btn.cancel:hover:not(:disabled) {
  background-color: #757575;
}

.loading {
  text-align: center;
  font-size: 1.125rem;
  padding: 2rem;
  color: #666;
}

.error-message {
  background-color: #ffcdd2;
  border-left: 4px solid #d32f2f;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.no-results {
  text-align: center;
  padding: 2rem;
  color: #666;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-content {
  background-color: #fff;
  padding: 2rem;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
}

.modal-content h2 {
  margin-top: 0;
  color: #d32f2f;
}

.warning {
  color: #d32f2f;
  font-weight: bold;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}
</style>
