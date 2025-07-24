<template>
  <div class="map-container">
    <div id="map" ref="mapContainer"></div>
    
    <div class="map-controls">
      <div class="user-list">
        <h3>Active Users</h3>
        <ul v-if="activeUsers.length > 0">
          <li 
            v-for="user in activeUsers" 
            :key="user.id"
            :class="{ 'selected': watchedUserId === user.id }"
            @click="toggleWatchUser(user.id)"
          >
            {{ user.name }}
            <span class="last-seen">{{ getLastSeen(user.id) }}</span>
          </li>
        </ul>
        <p v-else>No active users</p>
      </div>
      
      <div class="tracking-control">
        <button 
          @click="toggleTracking" 
          :class="{ 'tracking-active': isTracking }"
        >
          {{ isTracking ? 'Stop Tracking' : 'Start Tracking' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useLocationStore } from '../stores/location'
import { useAuthStore } from '../stores/auth'
import api from '../utils/axios'
import 'leaflet/dist/leaflet.css'

// Need to import these separately due to how Leaflet works with bundlers
let L = null

export default {
  name: 'MapView',
  setup() {
    const mapContainer = ref(null)
    const map = ref(null)
    const markers = ref({})
    const activeUsers = ref([])
    const locationStore = useLocationStore()
    const authStore = useAuthStore()
    
    // Computed properties
    const isTracking = computed(() => locationStore.isTracking)
    const currentCoordinates = computed(() => locationStore.currentCoordinates)
    const otherUsersLocations = computed(() => locationStore.userLocations)
    const watchedUserId = computed(() => locationStore.watchedUserId)
    
    // Initialize map
    onMounted(async () => {
      // Import Leaflet dynamically to avoid SSR issues
      L = await import('leaflet')
      
      // Create map
      map.value = L.map(mapContainer.value).setView([51.505, -0.09], 13)
      
      // Add tile layer (OpenStreetMap)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
      }).addTo(map.value)
      
      // Initialize socket connection
      if (authStore.token) {
        locationStore.initializeSocket(authStore.token)
      }
      
      // Fetch active users
      fetchActiveUsers()
      
      // Set up watchers for location updates
      watchLocations()
    })
    
    onUnmounted(() => {
      if (map.value) {
        map.value.remove()
      }
    })
    
    // Methods
    const fetchActiveUsers = async () => {
      try {
        // Using our configured API instance that handles authentication
        const response = await api.get('/api/users/active')
        activeUsers.value = response.data
      } catch (error) {
        console.error('Failed to fetch active users:', error)
      }
    }
    
    const watchLocations = () => {
      // Update map when current user location changes
      if (currentCoordinates.value) {
        updateMarker('self', currentCoordinates.value, true)
      }
      
      // Update other users' markers
      for (const [userId, location] of Object.entries(otherUsersLocations.value)) {
        updateMarker(userId, location)
      }
      
      // If watching a specific user, center map on them
      if (watchedUserId.value && otherUsersLocations.value[watchedUserId.value]) {
        const location = otherUsersLocations.value[watchedUserId.value]
        map.value.setView([location.lat, location.lng])
      }
    }
    
    const updateMarker = (id, coords, isSelf = false) => {
      const { lat, lng } = coords
      
      if (!lat || !lng) return
      
      // Create or update marker
      if (!markers.value[id]) {
        // Create new marker with custom icon
        const icon = L.divIcon({
          className: isSelf ? 'user-marker self' : 'user-marker other',
          html: `<div class="marker-inner"></div>`,
          iconSize: [20, 20]
        })
        
        markers.value[id] = L.marker([lat, lng], { icon }).addTo(map.value)
      } else {
        // Update existing marker
        markers.value[id].setLatLng([lat, lng])
      }
      
      // If this is the current user and no specific user is being watched, center map
      if (isSelf && !watchedUserId.value) {
        map.value.setView([lat, lng])
      }
    }
    
    const toggleWatchUser = (userId) => {
      if (watchedUserId.value === userId) {
        // If already watching this user, stop watching
        locationStore.clearWatchedUser()
      } else {
        // Start watching this user
        locationStore.setWatchedUser(userId)
        
        // Center map on user if location is available
        if (otherUsersLocations.value[userId]) {
          const { lat, lng } = otherUsersLocations.value[userId]
          map.value.setView([lat, lng])
        }
      }
    }
    
    const getLastSeen = (userId) => {
      const location = otherUsersLocations.value[userId]
      if (!location || !location.timestamp) return 'N/A'
      
      const date = new Date(location.timestamp)
      return date.toLocaleTimeString()
    }
    
    const toggleTracking = () => {
      if (isTracking.value) {
        locationStore.stopTracking()
      } else {
        locationStore.startTracking()
      }
    }
    
    return {
      mapContainer,
      isTracking,
      activeUsers,
      watchedUserId,
      toggleWatchUser,
      getLastSeen,
      toggleTracking
    }
  }
}
</script>

<style>
.map-container {
  position: relative;
  width: 100%;
  height: calc(100vh - 120px);
}

#map {
  width: 100%;
  height: 100%;
  z-index: 1;
}

.map-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1000;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 15px;
  max-width: 250px;
  max-height: 80vh;
  overflow-y: auto;
}

.user-list {
  margin-bottom: 20px;
}

.user-list h3 {
  margin-top: 0;
  margin-bottom: 10px;
}

.user-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.user-list li {
  padding: 8px;
  cursor: pointer;
  border-radius: 4px;
  margin-bottom: 5px;
}

.user-list li:hover {
  background-color: #f0f0f0;
}

.user-list li.selected {
  background-color: #4DBA87;
  color: white;
}

.last-seen {
  font-size: 0.8em;
  color: #888;
  display: block;
}

.user-list li.selected .last-seen {
  color: #e0e0e0;
}

.tracking-control {
  display: flex;
  justify-content: center;
}

/* Custom marker styles */
.user-marker {
  display: flex;
  justify-content: center;
  align-items: center;
}

.marker-inner {
  width: 14px;
  height: 14px;
  background-color: #4DBA87;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 0 10px rgba(0,0,0,0.5);
}

.user-marker.self .marker-inner {
  background-color: #3498db;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(52, 152, 219, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(52, 152, 219, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(52, 152, 219, 0);
  }
}
</style>
