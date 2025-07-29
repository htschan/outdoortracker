import axios from 'axios';

// Global config object
let runtimeConfig = { backendUrl: '' }
let configPromise = null

function loadConfig() {
  if (!configPromise) {
    configPromise = fetch('/frontend_config.json')
      .then(res => res.ok ? res.json() : {})
      .then(cfg => {
        runtimeConfig = cfg
        console.log('Loaded runtime config:', runtimeConfig)
      })
      .catch(e => {
        console.error('Error loading frontend_config.json:', e)
      })
  }
  return configPromise
}

// Returns a ready-to-use Axios instance after config is loaded
export async function getApi() {
  await loadConfig()
  let baseURL = runtimeConfig.backendUrl || window.location.origin
  if (baseURL.endsWith('/')) baseURL = baseURL.slice(0, -1)
  const api = axios.create({
    baseURL: baseURL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    }
  })
  api.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token');
      if (token) {
        const tokenString = typeof token === 'string' ? token : String(token);
        config.headers['Authorization'] = `Bearer ${tokenString}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  )
  api.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response && error.response.status === 401) {
        localStorage.removeItem('token');
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }
      return Promise.reject(error);
    }
  )
  return api
}
