import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";

// import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
// import protectedRoute from '../middlewares/protected'
// import Home from '../views/test.vue'
// import PageTwo from '../views/pageTwo.vue'
import AuthPage from "@/views/auth/auth.vue";
// import MainComponent from '@/views/main.vue'

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  // {
  //   path: '/',
  //   name: 'Main',
  //   component: MainComponent,
  // },
  {
    path: "/auth",
    name: "Auth",
    component: AuthPage
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
