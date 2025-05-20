import { createRouter, createWebHistory } from 'vue-router';


import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import SpendingAnalysis from '@/views/SpendingAnalysis.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/spending-analysis',
    name: 'SpendingAnalysis',
    component: SpendingAnalysis
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;