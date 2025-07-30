<template>
  <div class="register-container">
    <h1>Register</h1>
    <form @submit.prevent="handleRegister" class="register-form">
      <div class="form-group">
        <label for="name">Name</label>
        <input type="text" id="name" v-model="name" required placeholder="Enter your name">
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required placeholder="Enter your email">
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required placeholder="Enter your password"
          minlength="8">
      </div>

      <div class="form-group">
        <label for="confirmPassword">Confirm Password</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required
          placeholder="Confirm your password">
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Registering...' : 'Register' }}
      </button>

      <div class="form-footer">
        <router-link to="/login">Already have an account? Login</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const name = ref('')
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const errorMessage = ref('')
    const successMessage = ref('')
    const isLoading = ref(false)

    const passwordsMatch = computed(() => {
      return password.value === confirmPassword.value
    })

    const handleRegister = async () => {
      console.log('Register: form submit', { name: name.value, email: email.value })
      // Reset messages
      errorMessage.value = ''
      successMessage.value = ''

      // Validate form
      if (!passwordsMatch.value) {
        errorMessage.value = 'Passwords do not match'
        console.log('Register: passwords do not match')
        return
      }

      isLoading.value = true
      console.log('Register: calling authStore.register')
      try {
        const result = await authStore.register(email.value, password.value, name.value)
        console.log('Register: result', result)

        if (result.success) {
          successMessage.value = result.message || 'Registration successful! Please check your email to verify your account.'
          console.log('Register: success', successMessage.value)

          // Reset form
          name.value = ''
          email.value = ''
          password.value = ''
          confirmPassword.value = ''

          // Redirect to login after a delay
          setTimeout(() => {
            router.push('/login')
          }, 3000)
        } else {
          errorMessage.value = result.error
          console.log('Register: error', errorMessage.value)
        }
      } catch (error) {
        errorMessage.value = 'An unexpected error occurred. Please try again.'
        console.error('Register: unexpected error', error)
      } finally {
        isLoading.value = false
        console.log('Register: done')
      }
    }

    return {
      name,
      email,
      password,
      confirmPassword,
      errorMessage,
      successMessage,
      isLoading,
      handleRegister
    }
  }
}
</script>

<style>
.register-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.success-message {
  color: #4DBA87;
  background-color: #e8f5e9;
  padding: 0.75rem;
  border-radius: 4px;
  text-align: center;
}
</style>
