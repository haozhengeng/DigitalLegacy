import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { guest: true },
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue'),
      meta: { guest: true },
    },
    {
      path: '/',
      component: () => import('@/views/Layout.vue'),
      meta: { auth: true },
      children: [
        { path: '', name: 'Dashboard', component: () => import('@/views/Dashboard.vue') },
        { path: 'vault', name: 'Vault', component: () => import('@/views/VaultPage.vue') },
        { path: 'emotional', name: 'Emotional', component: () => import('@/views/EmotionalFiles.vue') },
        { path: 'beneficiaries', name: 'Beneficiaries', component: () => import('@/views/Beneficiaries.vue') },
        { path: 'trigger', name: 'Trigger', component: () => import('@/views/TriggerDashboard.vue') },
        { path: 'settings', name: 'Settings', component: () => import('@/views/Settings.vue') },
      ],
    },
  ],
})

router.beforeEach((to, _from) => {
  const auth = useAuthStore()
  if (to.meta.auth && !auth.isLoggedIn) return '/login'
  if (to.meta.guest && auth.isLoggedIn) return '/'
})

export default router
