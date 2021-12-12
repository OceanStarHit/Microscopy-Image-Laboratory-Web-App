import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import protectedRoute from '../middlewares/protected'
import Home from '../views/test.vue'
import PageTwo from '../views/pageTwo.vue'
import AuthPage from '@/views/auth/auth.vue'
import MainComponent from '@/views/main.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Main',
    component: MainComponent,
  },
  {
    path: '/auth',
    name: 'Auth',
    component: AuthPage,
  },
  {
    path: '/test',
    name: 'Test',
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
