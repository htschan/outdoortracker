import { defineStore } from 'pinia'
import api from '../utils/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user,
    isAdmin: (state) => state.user?.role === 'admin'
  },
  
  actions: {
    async login(email, password) {
      try {
        console.log('Attempting login with:', email);
        const response = await api.post('/api/auth/login', { email, password })
        console.log('Login response:', response.data);
        
        // Verify we have a valid token
        if (!response.data.token) {
          throw new Error('No token returned from server');
        }
        
        this.token = response.data.token
        localStorage.setItem('token', this.token)
        
        // Double-check that token was stored correctly
        const storedToken = localStorage.getItem('token');
        console.log('Token stored in localStorage:', storedToken);
        
        if (!storedToken) {
          console.error('Token was not stored in localStorage');
          throw new Error('Failed to store token');
        }
        
        // Small delay to ensure token is set before next request
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Fetch user details
        await this.fetchUserDetails()
        
        return { success: true }
      } catch (error) {
        console.error('Login error:', error)
        return { success: false, error: error.response?.data?.message || error.message || 'Login failed' }
      }
    },
    
    async register(email, password, name) {
      try {
        const response = await api.post('/api/auth/register', { email, password, name })
        return { success: true, message: response.data.message }
      } catch (error) {
        return { success: false, error: error.response?.data?.message || 'Registration failed' }
      }
    },
    
    async fetchUserDetails() {
      try {
        // Try a direct fetch with the token
        const token = localStorage.getItem('token');
        
        // Try with the API instance first
        try {
          const response = await api.get('/api/users/me', {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          this.user = response.data;
          return { success: true };
        } catch (apiError) {
          console.error('API instance fetch failed:', apiError);
          console.error('API Error response:', apiError.response?.data);
          
          // Use VITE_BACKEND_URL or fallback to window.location.origin
          let baseUrl = import.meta.env.VITE_BACKEND_URL || window.location.origin;
          // Ensure no trailing slash
          if (baseUrl.endsWith('/')) baseUrl = baseUrl.slice(0, -1);
          const directResponse = await fetch(`${baseUrl}/api/users/me`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          });
          
          if (!directResponse.ok) {
            throw new Error(`Direct fetch failed with status: ${directResponse.status}`);
          }
          
          const userData = await directResponse.json();
          this.user = userData;
          return { success: true };
        }
      } catch (error) {
        console.error('All fetch attempts failed:', error);
        if (error.response?.status !== 401) {
          this.logout();
        }
        return { success: false, error: 'Failed to fetch user details' };
      }
    },
    
    async verifyEmail(token) {
      try {
        const response = await api.post('/api/auth/verify-email', { token })
        return { success: true, message: response.data.message }
      } catch (error) {
        return { success: false, error: error.response?.data?.message || 'Email verification failed' }
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})
