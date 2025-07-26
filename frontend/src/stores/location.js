import { defineStore } from 'pinia'
import api from '../utils/axios'
import { io } from 'socket.io-client'

export const useLocationStore = defineStore('location', {
  state: () => ({
    currentPosition: null,
    trackingActive: false,
    watchId: null,
    socket: null,
    trackingInterval: null,
    userLocations: {}, // Other users' locations: { userId: { lat, lng, timestamp } }
    watchedUserId: null, // Currently watched user ID
    trackingError: null
  }),
  
  getters: {
    isTracking: (state) => state.trackingActive,
    currentCoordinates: (state) => state.currentPosition,
    otherUsersLocations: (state) => state.userLocations,
    watchedUserLocation: (state) => state.watchedUserId ? state.userLocations[state.watchedUserId] : null
  },
  
  actions: {
    initializeSocket(token) {
      if (this.socket) {
        this.socket.disconnect()
      }
      
      // Use VITE_BACKEND_URL as base for socket connection
      const wsBase = import.meta.env.VITE_BACKEND_URL || ''
      this.socket = io(wsBase + '/ws', {
        auth: { token },
        transports: ['websocket']
      })
      
      this.socket.on('connect', () => {
        console.log('Socket connected')
      })
      
      // Listen for location updates from other users
      this.socket.on('location_update', (data) => {
        const { userId, lat, lng, timestamp } = data
        this.userLocations[userId] = { lat, lng, timestamp }
      })
      
      this.socket.on('disconnect', () => {
        console.log('Socket disconnected')
      })
    },
    
    async startTracking() {
      if (this.trackingActive) return
      
      this.trackingError = null
      
      try {
        // Request geolocation permission
        if (!navigator.geolocation) {
          throw new Error('Geolocation is not supported by your browser')
        }
        
        // Start watching position
        this.watchId = navigator.geolocation.watchPosition(
          position => this.updatePosition(position),
          error => this.handlePositionError(error),
          { 
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0 
          }
        )
        
        // Set up tracking interval (backup for when watchPosition is unreliable)
        this.trackingInterval = setInterval(() => {
          navigator.geolocation.getCurrentPosition(
            position => this.updatePosition(position),
            error => this.handlePositionError(error),
            { enableHighAccuracy: true }
          )
        }, 30000) // Backup every 30 seconds
        
        this.trackingActive = true
      } catch (error) {
        this.trackingError = error.message
        console.error('Error starting tracking:', error)
      }
    },
    
    stopTracking() {
      if (this.watchId !== null) {
        navigator.geolocation.clearWatch(this.watchId)
        this.watchId = null
      }
      
      if (this.trackingInterval) {
        clearInterval(this.trackingInterval)
        this.trackingInterval = null
      }
      
      this.trackingActive = false
    },
    
    updatePosition(position) {
      const { latitude, longitude, accuracy, timestamp } = position.coords
      
      this.currentPosition = {
        lat: latitude,
        lng: longitude,
        accuracy,
        timestamp
      }
      
      // Send position to the server
      if (this.socket && this.socket.connected) {
        this.socket.emit('update_location', {
          lat: latitude,
          lng: longitude,
          accuracy,
          timestamp
        })
      } else {
        // Fallback to REST API if socket is not connected
        this.sendPositionViaApi()
      }
    },
    
    async sendPositionViaApi() {
      if (!this.currentPosition) return
      
      try {
        const { lat, lng, accuracy, timestamp } = this.currentPosition
        await api.post('/api/locations', {
          lat, 
          lng, 
          accuracy,
          timestamp
        })
      } catch (error) {
        console.error('Failed to send location via API:', error)
      }
    },
    
    handlePositionError(error) {
      this.trackingError = error.message
      console.error('Geolocation error:', error)
    },
    
    setWatchedUser(userId) {
      this.watchedUserId = userId
    },
    
    clearWatchedUser() {
      this.watchedUserId = null
    },
    
    disconnect() {
      this.stopTracking()
      
      if (this.socket) {
        this.socket.disconnect()
        this.socket = null
      }
      
      this.userLocations = {}
      this.currentPosition = null
    }
  }
})
