<template>
  <div class="app">
    <header class="header">
      <nav v-if="isAuthenticated">
        <router-link to="/">Home</router-link>
        <router-link to="/map">Map</router-link>
        <router-link to="/profile">Profile</router-link>
        <router-link v-if="isAdmin" to="/admin/users">Manage Users</router-link>
        <router-link to="/about">About</router-link>
        <a href="#" @click.prevent="logout">Logout</a>
      </nav>
    </header>

    <main class="main">
      <router-view />
    </main>

    <footer class="footer">
      <p>&copy; {{ currentYear }} Outdoor Tracker</p>
    </footer>
  </div>
</template>

<script>
import { useAuthStore } from './stores/auth'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const isAdmin = computed(() => authStore.isAdmin)
    const currentYear = new Date().getFullYear()
    
    const logout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    return {
      isAuthenticated,
      isAdmin,
      currentYear,
      logout
    }
  }
}
</script>

<style>
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  background-color: #4DBA87;
  color: white;
  padding: 1rem;
}

.header nav {
  display: flex;
  gap: 1rem;
}

.header a {
  color: white;
  text-decoration: none;
}

.main {
  flex: 1;
  padding: 1rem;
}

.footer {
  background-color: #f5f5f5;
  text-align: center;
  padding: 1rem;
}
</style>
