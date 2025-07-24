import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'

// Service worker will be registered automatically by vite-plugin-pwa
// We don't need to register it manually here

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
