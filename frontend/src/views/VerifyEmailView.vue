<template>
  <div class="verify-container">
    <div v-if="loading" class="loading">
      <p>Verifying your email...</p>
    </div>
    
    <div v-else-if="verified" class="success">
      <h1>Email Verified!</h1>
      <p>Your email has been successfully verified. Your account is now pending admin approval.</p>
      <p>You'll receive a notification once your account is approved.</p>
      <router-link to="/login" class="button">Go to Login</router-link>
    </div>
    
    <div v-else class="error">
      <h1>Verification Failed</h1>
      <p>{{ errorMessage || 'Unable to verify your email. The verification link may be invalid or expired.' }}</p>
      <router-link to="/login" class="button secondary">Back to Login</router-link>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'VerifyEmailView',
  setup() {
    const route = useRoute()
    const authStore = useAuthStore()
    
    const loading = ref(true)
    const verified = ref(false)
    const errorMessage = ref('')
    
    onMounted(async () => {
      // Get token from route params
      const token = route.params.token
      
      if (!token) {
        loading.value = false
        errorMessage.value = 'No verification token provided'
        return
      }
      
      try {
        // Call the verify email endpoint
        const result = await authStore.verifyEmail(token)
        
        loading.value = false
        
        if (result.success) {
          verified.value = true
        } else {
          errorMessage.value = result.error
        }
      } catch (error) {
        loading.value = false
        errorMessage.value = 'An unexpected error occurred'
        console.error('Verification error:', error)
      }
    })
    
    return {
      loading,
      verified,
      errorMessage
    }
  }
}
</script>

<style>
.verify-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  font-size: 1.2rem;
}

.success,
.error {
  padding: 2rem;
  border-radius: 8px;
  margin-top: 2rem;
}

.success {
  background-color: #e8f5e9;
  border: 1px solid #4DBA87;
}

.error {
  background-color: #ffebee;
  border: 1px solid #e74c3c;
}

.button {
  display: inline-block;
  margin-top: 1.5rem;
  padding: 0.75rem 2rem;
  background-color: #4DBA87;
  color: white;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
}

.button.secondary {
  background-color: #95a5a6;
}

.button:hover {
  opacity: 0.9;
  text-decoration: none;
}
</style>
