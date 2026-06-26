import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '@/services/supabase.js'

// Lazy-loaded views
const Landing = () => import('@/views/LandingPage.vue')
const Login = () => import('@/views/LoginPage.vue')
const Register = () => import('@/views/RegisterPage.vue')
const Dashboard = () => import('@/views/DashboardPage.vue')
const Questions = () => import('@/views/QuestionsPage.vue')
const SelfieWall = () => import('@/views/SelfieWallPage.vue')
const Wardrobe = () => import('@/views/WardrobePage.vue')
const Health = () => import('@/views/HealthPage.vue')
const Notifications = () => import('@/views/NotificationsPage.vue')
const Profile = () => import('@/views/ProfilePage.vue')
const LinkPartner = () => import('@/views/LinkPartnerPage.vue')

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: Landing,
    meta: { guest: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { guest: true }
  },
  {
    path: '/link-partner',
    name: 'LinkPartner',
    component: LinkPartner,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true, requiresPartner: true }
  },
  {
    path: '/questions',
    name: 'Questions',
    component: Questions,
    meta: { requiresAuth: true, requiresPartner: true }
  },
  {
    path: '/selfie-wall',
    name: 'SelfieWall',
    component: SelfieWall,
    meta: { requiresAuth: true, requiresPartner: true }
  },
  {
    path: '/wardrobe',
    name: 'Wardrobe',
    component: Wardrobe,
    meta: { requiresAuth: true, requiresPartner: true }
  },
  {
    path: '/health',
    name: 'Health',
    component: Health,
    meta: { requiresAuth: true, requiresPartner: true }
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: Notifications,
    meta: { requiresAuth: true, requiresPartner: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

/**
 * Helper: Check if the logged-in user has a linked partner.
 * Looks up the profiles table for a non-null partner_id.
 */
async function checkHasPartner(userId) {
  try {
    const { data, error } = await supabase
      .from('profiles')
      .select('partner_id')
      .eq('id', userId)
      .single()

    if (error || !data) return false
    return !!data.partner_id
  } catch {
    return false
  }
}

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const { data: { session } } = await supabase.auth.getSession()

  // 1. Not logged in → redirect to login
  if (to.meta.requiresAuth && !session) {
    return next('/login')
  }

  // 2. Logged-in user visiting guest pages → decide where to send them
  if (to.meta.guest && session) {
    const paired = await checkHasPartner(session.user.id)
    return next(paired ? '/dashboard' : '/link-partner')
  }

  // 3. Route needs a partner → verify they have one
  if (to.meta.requiresPartner && session) {
    const paired = await checkHasPartner(session.user.id)
    if (!paired) {
      return next('/link-partner')
    }
  }

  next()
})

export default router
