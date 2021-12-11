import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import protectedRoute from '../middlewares/protected'
import Home from '../views/Home.vue'
import PageTwo from '../views/pageTwo.vue'
import AuthPage from '@/views/auth/auth.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Auh',
    component: AuthPage,
  },

  {
    path: '/home',
    name: 'Home',
    component: Home,
  },

  {
    path: '/pagetwo',
    name: 'PageTwo',
    component: PageTwo,
    beforeEnter: protectedRoute,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
