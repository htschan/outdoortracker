<template>
  <div class="profile-container">
    <h1>User Profile</h1>
    
    <div v-if="loading" class="loading">
      Loading profile information...
    </div>
    
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    
    <div v-else class="profile-card">
      <div class="profile-header">
        <div class="profile-avatar">
          {{ userInitials }}
        </div>
        <div class="profile-details">
          <h2>{{ user.name }}</h2>
          <p>{{ user.email }}</p>
          <p class="user-role">Role: {{ user.role }}</p>
        </div>
      </div>
      
      <div class="profile-actions">
        <h3>Tracking Settings</h3>
        <div class="setting-row">
          <label for="tracking-active">Activate Location Tracking</label>
          <div class="toggle-switch">
            <input 
              type="checkbox" 
              id="tracking-active" 
              v-model="trackingActive" 
              @change="toggleTracking"
            />
            <span class="toggle-slider"></span>
          </div>
        </div>
        
        <div v-if="trackingActive" class="tracking-info">
          <p class="success-text">Your location is being tracked and shared with other users.</p>
          <p v-if="currentPosition">
            Current position: {{ formatPosition(currentPosition) }}
          </p>
        </div>
        
        <div class="setting-row">
          <label for="tracking-frequency">Update Frequency</label>
          <select 
            id="tracking-frequency" 
            v-model="trackingFrequency"
            @change="updateFrequency"
            :disabled="!trackingActive"
          >
            <option value="5">Every 5 seconds</option>
            <option value="10">Every 10 seconds</option>
            <option value="30">Every 30 seconds</option>
            <option value="60">Every minute</option>
            <option value="300">Every 5 minutes</option>
          </select>
        </div>
      </div>
      
      <div class="profile-section">
        <h3>Account Information</h3>
        <button @click="changePassword" class="btn secondary">Change Password</button>
      </div>
      
      <div v-if="isAdmin" class="admin-section">
        <h3>Admin Features</h3>
        <p>As an admin, you can approve new users and manage the application.</p>
        <button @click="goToAdminPanel" class="btn">Admin Panel</button>
      </div>
    </div>
    
    <!-- Password Change Dialog -->
    <div v-if="showPasswordDialog" class="dialog-overlay">
      <div class="dialog">
        <h3>Change Password</h3>
        
        <div class="form-group">
          <label for="current-password">Current Password</label>
          <input 
            type="password" 
            id="current-password" 
            v-model="passwordForm.current"
            placeholder="Enter your current password"
          />
        </div>
        
        <div class="form-group">
          <label for="new-password">New Password</label>
          <input 
            type="password" 
            id="new-password" 
            v-model="passwordForm.new"
            placeholder="Enter your new password"
          />
        </div>
        
        <div class="form-group">
          <label for="confirm-password">Confirm New Password</label>
          <input 
            type="password" 
            id="confirm-password" 
            v-model="passwordForm.confirm"
            placeholder="Confirm your new password"
          />
        </div>
        
        <div v-if="passwordError" class="error-message">
          {{ passwordError }}
        </div>
        
        <div class="dialog-actions">
          <button @click="closeDialog" class="btn secondary">Cancel</button>
          <button @click="submitPasswordChange" class="btn">Change Password</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useLocationStore } from '../stores/location'
import api from '../utils/axios'

export default {
  name: 'ProfileView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const locationStore = useLocationStore()
    
    // User data
    const user = ref({})
    const loading = ref(true)
    const error = ref(null)
    
    // Tracking state
    const trackingActive = computed(() => locationStore.isTracking)
    const currentPosition = computed(() => locationStore.currentCoordinates)
    const trackingFrequency = ref('30') // default 30 seconds
    
    // Password change
    const showPasswordDialog = ref(false)
    const passwordForm = ref({
      current: '',
      new: '',
      confirm: ''
    })
    const passwordError = ref(null)
    
    // Computed properties
    const userInitials = computed(() => {
      if (!user.value || !user.value.name) return '?'
      return user.value.name
        .split(' ')
        .map(name => name.charAt(0).toUpperCase())
        .join('')
        .substring(0, 2)
    })
    
    const isAdmin = computed(() => {
      return user.value.role === 'admin'
    })
    
    // Methods
    const fetchUserData = async () => {
      try {
        loading.value = true
        error.value = null
        
        const response = await authStore.fetchUserDetails()
        
        if (response.success) {
          user.value = authStore.currentUser
        } else {
          error.value = 'Failed to load profile data. Please try again later.'
        }
      } catch (err) {
        error.value = 'An error occurred while loading your profile.'
        console.error('Profile data error:', err)
      } finally {
        loading.value = false
      }
    }
    
    const toggleTracking = () => {
      if (trackingActive.value) {
        locationStore.stopTracking()
      } else {
        locationStore.startTracking()
      }
    }
    
    const updateFrequency = () => {
      // This would be implemented to adjust the tracking frequency
      console.log(`Tracking frequency set to ${trackingFrequency.value} seconds`)
      // In a real implementation, you would update the tracking interval
    }
    
    const formatPosition = (pos) => {
      if (!pos) return 'Unknown'
      return `${pos.lat.toFixed(6)}, ${pos.lng.toFixed(6)}`
    }
    
    const changePassword = () => {
      showPasswordDialog.value = true
      passwordForm.value = { current: '', new: '', confirm: '' }
      passwordError.value = null
    }
    
    const closeDialog = () => {
      showPasswordDialog.value = false
    }
    
    const submitPasswordChange = async () => {
      try {
        passwordError.value = null
        
        // Validation
        if (!passwordForm.value.current || !passwordForm.value.new || !passwordForm.value.confirm) {
          passwordError.value = 'All fields are required'
          return
        }
        
        if (passwordForm.value.new !== passwordForm.value.confirm) {
          passwordError.value = 'New passwords do not match'
          return
        }
        
        if (passwordForm.value.new.length < 8) {
          passwordError.value = 'New password must be at least 8 characters long'
          return
        }
        
        // Submit password change
        const response = await api.post('/api/users/change-password', {
          currentPassword: passwordForm.value.current,
          newPassword: passwordForm.value.new
        }, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })
        
        // Close dialog and show success
        closeDialog()
        alert('Password changed successfully')
      } catch (err) {
        passwordError.value = err.response?.data?.message || 'Failed to change password'
        console.error('Password change error:', err)
      }
    }
    
    const goToAdminPanel = () => {
      router.push('/admin')
    }
    
    onMounted(() => {
      fetchUserData()
      
      // Initialize socket connection if authenticated
      if (authStore.token) {
        locationStore.initializeSocket(authStore.token)
      }
    })
    
    return {
      user,
      loading,
      error,
      userInitials,
      isAdmin,
      trackingActive,
      currentPosition,
      trackingFrequency,
      showPasswordDialog,
      passwordForm,
      passwordError,
      toggleTracking,
      updateFrequency,
      formatPosition,
      changePassword,
      closeDialog,
      submitPasswordChange,
      goToAdminPanel
    }
  }
}
</script>

<style>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.profile-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-top: 1.5rem;
}

.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  background-color: #4DBA87;
  color: white;
  font-size: 2rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-right: 1.5rem;
}

.profile-details h2 {
  margin: 0 0 0.25rem 0;
}

.profile-details p {
  margin: 0.25rem 0;
  color: #666;
}

.user-role {
  font-weight: bold;
  color: #4DBA87 !important;
}

.profile-actions, .profile-section, .admin-section {
  padding: 1.5rem 0;
  border-top: 1px solid #eee;
}

.setting-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1rem 0;
}

.tracking-info {
  background-color: #e8f5e9;
  border-radius: 4px;
  padding: 1rem;
  margin: 1rem 0;
}

.success-text {
  color: #4DBA87;
  font-weight: bold;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: #4DBA87;
}

input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.btn {
  padding: 0.5rem 1rem;
  background-color: #4DBA87;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn.secondary {
  background-color: #f0f0f0;
  color: #333;
}

.error-message {
  color: #e74c3c;
  margin: 1rem 0;
}

/* Dialog styles */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  width: 90%;
  max-width: 500px;
}

.dialog h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}
</style>
