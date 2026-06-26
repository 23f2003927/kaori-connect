<template>
  <div id="kaori-app" :data-theme="theme">
    <!-- Toast notifications -->
    <div class="k-toast-container" v-if="toasts.length">
      <div v-for="toast in toasts" :key="toast.id" class="k-toast">
        {{ toast.message }}
      </div>
    </div>

    <!-- Navbar (only when authenticated & has partner) -->
    <NavBar v-if="isAuthenticated && hasPartner" @toggle-theme="toggleTheme" :theme="theme" />

    <!-- Main content -->
    <router-view v-slot="{ Component }">
      <transition name="k-fade" mode="out-in">
        <component :is="Component" :key="$route.path" />
      </transition>
    </router-view>

    <!-- Bottom nav for mobile -->
    <BottomNav v-if="isAuthenticated && hasPartner" />
  </div>
</template>

<script>
import { ref, onMounted, provide } from 'vue'
import { supabase } from '@/services/supabase.js'
import NavBar from '@/components/layout/NavBar.vue'
import BottomNav from '@/components/layout/BottomNav.vue'

export default {
  name: 'App',
  components: { NavBar, BottomNav },
  setup() {
    const isAuthenticated = ref(false)
    const hasPartner = ref(false)
    const user = ref(null)
    const profile = ref(null)
    const theme = ref(localStorage.getItem('kaori-theme') || 'light')
    const toasts = ref([])

    // Toast system
    function showToast(message, duration = 3000) {
      const id = Date.now()
      toasts.value.push({ id, message })
      setTimeout(() => {
        toasts.value = toasts.value.filter(t => t.id !== id)
      }, duration)
    }

    // Theme toggle
    function toggleTheme() {
      theme.value = theme.value === 'light' ? 'dark' : 'light'
      localStorage.setItem('kaori-theme', theme.value)
    }

    // Auth state listener
    onMounted(() => {
      supabase.auth.getSession().then(({ data: { session } }) => {
        if (session) {
          isAuthenticated.value = true
          user.value = session.user
          loadProfile(session.user.id)
        }
      })

      supabase.auth.onAuthStateChange((event, session) => {
        isAuthenticated.value = !!session
        user.value = session?.user || null
        if (session?.user) {
          loadProfile(session.user.id)
        } else {
          profile.value = null
          hasPartner.value = false
        }
      })
    })

    async function loadProfile(userId) {
      try {
        const { data, error } = await supabase
          .from('profiles')
          .select('id, display_name, email, partner_code, partner_id, avatar_url')
          .eq('id', userId)
          .single()
        
        if (data && !error) {
          profile.value = data
          hasPartner.value = !!data.partner_id
        } else {
          // Profile doesn't exist yet — will be created on registration
          hasPartner.value = false
        }
      } catch (e) {
        hasPartner.value = false
      }
    }

    // Provide global state
    provide('user', user)
    provide('profile', profile)
    provide('isAuthenticated', isAuthenticated)
    provide('hasPartner', hasPartner)
    provide('showToast', showToast)
    provide('theme', theme)

    return {
      isAuthenticated,
      hasPartner,
      theme,
      toasts,
      toggleTheme
    }
  }
}
</script>
