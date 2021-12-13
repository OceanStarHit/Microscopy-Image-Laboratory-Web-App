import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';

import AuthPage from '@/views/auth/auth.vue';
import MainComponent from '@/views/main.vue';

import authGuard from './guards/auth.guard'
import authViewGuard from './guards/authView.guard'

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Main',
    component: MainComponent,
    beforeEnter: authGuard
  },
  {
    path: '/auth',
    name: 'Auth',
    component: AuthPage,
    beforeEnter: authViewGuard
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
