import axios from 'axios';

// Determine base URL for API
let baseURL = '';
if (import.meta.env.VITE_BACKEND_URL) {
  baseURL = import.meta.env.VITE_BACKEND_URL;
  // Remove trailing slash if present
  if (baseURL.endsWith('/')) baseURL = baseURL.slice(0, -1);
} else {
  baseURL = window.location.origin;
}

// Create Axios instance with configuration
const api = axios.create({
  baseURL: baseURL, // Use env or origin for API calls
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
});

// Add a request interceptor to add the JWT token to all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    
    if (token) {
      // Make sure the token is a string
      const tokenString = typeof token === 'string' ? token : String(token);
      
      // Set the Authorization header with the Bearer token
      config.headers['Authorization'] = `Bearer ${tokenString}`;
    } 
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle common errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle unauthorized errors (401) - token expired or invalid
    if (error.response && error.response.status === 401) {
      // Clear local storage
      localStorage.removeItem('token');
      
      // Redirect to login page if not already there
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
