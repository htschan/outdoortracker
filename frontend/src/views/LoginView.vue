<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="email">Email</label>
        <input 
          type="email" 
          id="email" 
          v-model="email" 
          required 
          placeholder="Enter your email"
        >
      </div>
      
      <div class="form-group">
        <label for="password">Password</label>
        <input 
          type="password" 
          id="password" 
          v-model="password" 
          required 
          placeholder="Enter your password"
        >
      </div>
      
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Logging in...' : 'Login' }}
      </button>
      
      <div class="form-footer">
        <router-link to="/register">Don't have an account? Register</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const email = ref('')
    const password = ref('')
    const errorMessage = ref('')
    const isLoading = ref(false)
    
    const handleLogin = async () => {
      errorMessage.value = ''
      isLoading.value = true
      
      try {
        const result = await authStore.login(email.value, password.value)
        
        if (result.success) {
          router.push('/')
        } else {
          errorMessage.value = result.error
        }
      } catch (error) {
        errorMessage.value = 'An unexpected error occurred. Please try again.'
        console.error(error)
      } finally {
        isLoading.value = false
      }
    }
    
    return {
      email,
      password,
      errorMessage,
      isLoading,
      handleLogin
    }
  }
}
</script>

<style>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: bold;
}

input {
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  padding: 0.75rem;
  background-color: #4DBA87;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #3a8f67;
}

button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  font-size: 0.9rem;
}

.form-footer {
  text-align: center;
  margin-top: 1rem;
}

.form-footer a {
  color: #4DBA87;
  text-decoration: none;
}

.form-footer a:hover {
  text-decoration: underline;
}
</style>
