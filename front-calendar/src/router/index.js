import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'

// Definir rutas
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
]

// Crear el enrutador
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
