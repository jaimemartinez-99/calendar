import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import CalendarCreation from '../components/CalendarCreation.vue'

// Definir rutas
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/calendarCreation/:uuid',
    name: 'CalendarCreation',
    component: CalendarCreation,
    props: true // Permite pasar el parámetro uuid como prop al componente
  }
]

// Crear el enrutador
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router