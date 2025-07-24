<template>
  <div class="home">
    <h1>Outdoor Tracker</h1>
    
    <div class="tracking-controls">
      <button 
        @click="toggleTracking" 
        :class="{ 'tracking-active': isTracking }"
      >
        {{ isTracking ? 'Stop Tracking' : 'Start Tracking' }}
      </button>
      
      <div v-if="isTracking" class="tracking-status">
        <div class="status-indicator active"></div>
        <span>Live tracking active</span>
      </div>
      <div v-else class="tracking-status">
        <div class="status-indicator inactive"></div>
        <span>Tracking inactive</span>
      </div>
    </div>
    
    <div v-if="currentCoordinates" class="coordinates-display">
      <h3>Your Current Position</h3>
      <p>Latitude: {{ currentCoordinates.lat.toFixed(6) }}</p>
      <p>Longitude: {{ currentCoordinates.lng.toFixed(6) }}</p>
      <p>Accuracy: {{ currentCoordinates.accuracy.toFixed(1) }} meters</p>
      <p>Last update: {{ formatTime(currentCoordinates.timestamp) }}</p>
    </div>
    
    <div v-if="trackingError" class="error-message">
      <p>Error: {{ trackingError }}</p>
    </div>
  </div>
</template>

<script>
import { useLocationStore } from '../stores/location'
import { useAuthStore } from '../stores/auth'
import { computed, onMounted, onUnmounted } from 'vue'

export default {
  name: 'HomeView',
  setup() {
    const locationStore = useLocationStore()
    const authStore = useAuthStore()
    
    // Initialize location tracking and WebSocket connection
    onMounted(() => {
      if (authStore.token) {
        locationStore.initializeSocket(authStore.token)
      }
    })
    
    onUnmounted(() => {
      locationStore.stopTracking()
    })
    
    // Computed properties
    const isTracking = computed(() => locationStore.isTracking)
    const currentCoordinates = computed(() => locationStore.currentCoordinates)
    const trackingError = computed(() => locationStore.trackingError)
    
    // Methods
    const toggleTracking = () => {
      if (isTracking.value) {
        locationStore.stopTracking()
      } else {
        locationStore.startTracking()
      }
    }
    
    const formatTime = (timestamp) => {
      if (!timestamp) return 'Unknown'
      return new Date(timestamp).toLocaleTimeString()
    }
    
    return {
      isTracking,
      currentCoordinates,
      trackingError,
      toggleTracking,
      formatTime
    }
  }
}
</script>

<style>
.tracking-controls {
  margin: 2rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

button {
  padding: 1rem 2rem;
  font-size: 1.2rem;
  border: none;
  border-radius: 4px;
  background-color: #4DBA87;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #3a8f67;
}

button.tracking-active {
  background-color: #e74c3c;
}

button.tracking-active:hover {
  background-color: #c0392b;
}

.tracking-status {
  display: flex;
  align-items: center;
  margin-top: 1rem;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 8px;
}

.status-indicator.active {
  background-color: #4DBA87;
  box-shadow: 0 0 8px #4DBA87;
  animation: pulse 2s infinite;
}

.status-indicator.inactive {
  background-color: #95a5a6;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(77, 186, 135, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(77, 186, 135, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(77, 186, 135, 0);
  }
}

.coordinates-display {
  margin-top: 2rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.error-message {
  margin-top: 1rem;
  color: #e74c3c;
  font-weight: bold;
}
</style>
