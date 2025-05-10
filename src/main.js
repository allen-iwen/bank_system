// import { createApp } from 'vue'
// import { createPinia } from 'pinia'
// import ElementPlus from 'element-plus'
// import 'element-plus/dist/index.css'
// import router from './router'
// import App from './App.vue'

// const app = createApp(App)
// const pinia = createPinia()

// app.use(pinia)
// app.use(router)
// app.use(ElementPlus)

// app.mount('#app')

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import App from './App.vue'

const app = createApp(App)
const pinia = createPinia()

try {
  app.use(router)
  app.use(pinia)
  app.use(ElementPlus)
  app.mount('#app')
} catch (error) {
  console.error('Failed to initialize application:', error)
}